import os
import fitz  # PyMuPDF for PDF text extraction
from dotenv import load_dotenv
from groq import Groq
from gtts import gTTS
import speech_recognition as sr
from pydub import AudioSegment
from playsound import playsound
import re
import io

try:
    import streamlit as st  # type: ignore
except ImportError:  # pragma: no cover
    st = None

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("Missing GROQ_API_KEY environment variable.")

# Initialize Groq client using the provided API key
client = Groq(api_key=groq_api_key)


def get_groq_response(input_text, resume_text, prompt):
    model = "llama-3.3-70b-versatile"
    full_prompt = f"{prompt}\n\nJob Description:\n{input_text}\n\nResume Content:\n{resume_text}"
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": full_prompt}],
        temperature=0.7,
        max_tokens=1024,
    )

    return response.choices[0].message.content.strip()

def extract_text_from_pdf(uploaded_file):
    """Extract text from a PDF file."""
    if uploaded_file is not None:
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = "\n".join([page.get_text("text") for page in pdf_document])
        return text if text.strip() else "Error: No readable text found in PDF."
    else:
        raise FileNotFoundError("No file uploaded")

def interview_chatbot(job_type, conversation_history, prompt_type="next_question"):
    """Generate questions and feedback for mock interviews."""
    prompts = {
        "start": f"""
        Act as an interviewer for a {job_type} interview. Start by introducing yourself and asking the first question.
        Format your response with a brief introduction followed by "Question 1:" and then your first question.
        Ask only one question at a time and wait for the response.
        """,
        "feedback": f"""
        Act as an interviewer for a {job_type} interview. You've just received an answer to your question.
        Provide feedback on the answer, including strengths, areas for improvement, and a score out of 10.
        """,
        "next_question": f"""
        Act as an interviewer for a {job_type} interview. You've already asked previous questions and provided feedback.
        Now ask the next logical question in the interview sequence.
        """
    }
    
    messages = [{"role": "system", "content": prompts[prompt_type]}] + conversation_history

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=1,
        max_tokens=1024,
        top_p=1,
    )
    
    return response.choices[0].message.content.strip()

def extract_next_question(response_text):
    """Extract the next question from a response that might contain feedback."""
    match = re.search(r"(?:Question \d+:|Next question:)(.*?)(?=$)", response_text, re.DOTALL)
    return match.group(1).strip() if match else response_text

def text_to_speech(text, speed=200):
    """Convert text to speech and play it with increased speed."""
    tts = gTTS(text=text, lang='en', slow=False)
    tts.save("response.mp3")
    
    audio = AudioSegment.from_file("response.mp3")
    faster_audio = audio.speedup(playback_speed=1.5)  # Adjust speed
    faster_audio.export("faster_response.mp3", format="mp3")
    playsound("faster_response.mp3")

def speech_to_text():
    """Capture microphone input and transcribe using Groq Whisper with Google fallback."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        recognizer.energy_threshold = 300
        recognizer.pause_threshold = 5
        audio = recognizer.listen(source, timeout=None, phrase_time_limit=90)

    audio_wav = audio.get_wav_data(convert_rate=16000, convert_width=2)
    audio_buffer = io.BytesIO(audio_wav)
    audio_buffer.name = "speech.wav"

    try:
        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3-turbo",
            file=(audio_buffer.name, audio_buffer.getvalue()),
            response_format="text",
        )
        if hasattr(transcription, "text"):
            return transcription.text.strip()
        if isinstance(transcription, dict) and "text" in transcription:
            return transcription["text"].strip()
        return str(transcription)
    except Exception as exc:
        message = f"Groq transcription failed, falling back to Google Speech Recognition. Error: {exc}"
        print(message)
        if st is not None:
            st.warning(message)
        try:
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Could not understand audio. Please try again."
        except sr.RequestError:
            return "Speech recognition service unavailable."
        except Exception as google_exc:
            return f"Fallback transcription failed: {google_exc}"