# 💼 Haired AI: Resume & Interview Analyzer

Haired AI is an AI-powered web application designed to help job seekers analyze their resumes, simulate mock interviews, generate tailored interview questions, and evaluate GitHub projects using LLMs (Large Language Models).

Built with **Streamlit**, this tool offers an all-in-one experience for interview preparation and technical self-assessment.

---

## 🚀 Features

- 📄 **Resume Analysis**  
  Analyze your resume and get AI-generated insights and suggestions for improvement.

- 🤖 **Mock Interview**  
  Experience real-time mock interviews with voice interaction and get instant AI feedback.

- 📌 **Question Generator**  
  Generate company and role-specific interview questions along with AI-generated solutions.

- 📝 **LLM Project Analyzer**  
  Evaluate your GitHub projects using LLMs, extract insights from README files, and get interview-style questions based on your work.

- 🧠 **GitHub Parser**  
  Automatically scans your GitHub profile, identifies relevant repositories, analyzes project quality, and suggests improvements. It also generates interview questions based on your code and documentation.

---

## 🛠 Tech Stack

- **Frontend:** Streamlit  
- **Backend:** Python  
- **AI/LLM:** GROQ API  
- **Voice Support:** SpeechRecognition, gTTS, pydub  
- **PDF Parsing:** PyPDF2  
- **Data Processing:** Pandas, NumPy

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/haired-ai.git
cd haired-ai
pip install -r requirements.txt
```

---

## 🔐 API Setup

1. Register for a **GROQ API key**:
    - Visit [GROQ API registration](https://console.groq.com/docs/quickstart) to get your API key.

2. Create a `.env` file in the root directory and add the key:
    ```env
    GROQ_API_KEY=your_api_key_here
    ```

---

## ▶️ Running the Application

1. Make sure you're in the project directory and have activated your virtual environment.

2. Start the Streamlit app:
    ```bash
    streamlit run main.py
    ```

3. Open your browser and visit:  
    [http://localhost:8501](http://localhost:8501)

---

## 📁 Project Structure

```
├── main.py
├── utils/
│   └── common_inputs.py
├── tabs/
│   ├── resume_analysis.py
│   ├── mock_interview.py
│   ├── question_generator.py
│   └── llm_project_analyzer.py
├── github_parser/
├── llm/
├── parser_scorer/
└── other/
```

---

## 📄 Requirements

All required packages are listed in `requirements.txt`.

> **Note:** If you encounter any missing libraries, you can install them individually using:
> ```bash
> pip install <library-name>
> ```

---

## 🙋‍♂️ Author

Made with ❤️ by [Your Name]

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
