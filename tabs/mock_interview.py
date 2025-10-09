# tabs/mock_interview.py
import streamlit as st
from ai_logic import get_groq_response, speech_to_text, text_to_speech

def render_mock_interview(inputs):
    st.subheader("🤖 Mock Interview")

    job_role = inputs["job_role"]
    conversation_history = []

    if st.button("Start Interview"):
        if job_role:
            while True:
                ai_question = get_groq_response(job_role, "", "Act as an interviewer. Ask questions one by one and provide feedback.")
                st.write("🗣️ Interviewer:", ai_question)
                text_to_speech(ai_question)

                user_response = speech_to_text()
                st.write("🎙️ You said:", user_response)

                if user_response.lower() in ["exit", "quit", "stop"]:
                    st.write("🛑 Interview Ended.")
                    break

                conversation_history.append({"role": "user", "content": user_response})

                ai_feedback = get_groq_response(job_role, user_response, "Evaluate response, provide feedback and a score.")
                st.write("💡 Feedback:", ai_feedback)
                text_to_speech(ai_feedback)

                conversation_history.append({"role": "system", "content": ai_feedback})
        else:
            st.warning("⚠ Please enter the Job Role.")