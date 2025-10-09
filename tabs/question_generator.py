# tabs/question_generator.py
import streamlit as st
from learn import get_company_description, generate_interview_questions, generate_solutions

def render_question_generator(inputs):
    st.subheader("📌 Interview Question Generator")

    company = inputs["company_name"]
    role = inputs["job_role"]
    category = st.selectbox("Select Category", ["DSA", "SQL", "System Design", "Behavioral", "AI/ML", "Other"])

    if company:
        with st.spinner(f"Fetching description for {company}..."):
            company_description = get_company_description(company)

        st.subheader(f"About {company}")
        st.write(company_description)

    if st.button("Generate Questions"):
        if company and role and category:
            with st.spinner("Generating interview questions..."):
                questions = generate_interview_questions(company, role, category)

            if questions:
                st.success(f"Successfully generated {len(questions)} {category} questions!")

                with st.spinner("Generating solutions..."):
                    solutions = generate_solutions(category, questions)

                st.subheader(f"{category} Interview Questions & Answers")
                for solution in solutions:
                    st.markdown(solution)
            else:
                st.error("No questions generated. Try different inputs!")
        else:
            st.warning("Please fill in all fields.")