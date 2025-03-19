import streamlit as st
import re
from generate_questions import generate_questions
from data_handler import save_data, save_report

# Streamlit UI
def main():
    st.title("TalentScout Hiring Assistant 🤖")
    st.write("🚀 Welcome to TalentScout! Let’s get you started with your job screening.")

    if "step" not in st.session_state:
        st.session_state.step = 0
        st.session_state.questions = []
        st.session_state.answers = []
        st.session_state.current_answer = ""  # Store temporary answer

    if st.session_state.step == 0:
        with st.form("candidate_form"):
            full_name = st.text_input("Full Name")
            email = st.text_input("Email Address")
            phone = st.text_input("Phone Number")
            experience = st.selectbox("Years of Experience", ["<1", "1-3", "3-5", "5+"])
            position = st.text_input("Desired Position")
            location = st.text_input("Current Location")
            tech_stack = st.text_area("Tech Stack (e.g., Python, React, SQL, AWS)")

            submitted = st.form_submit_button("Submit")

        if submitted:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                st.error("Please enter a valid email address.")
            elif not phone.isdigit():
                st.error("Phone number should contain only digits.")
            elif not re.match(r"^[a-zA-Z0-9, ]+$", tech_stack):
                st.error("Tech stack should contain only valid technologies separated by commas.")
            else:
                candidate_data = {
                    "full_name": full_name,
                    "email": email,
                    "phone": phone,
                    "experience": experience,
                    "position": position,
                    "location": location,
                    "tech_stack": tech_stack
                }
                save_data(candidate_data)  # Save to CSV

                st.session_state.questions = generate_questions(tech_stack, experience)
                st.session_state.answers = [""] * len(st.session_state.questions)  # Initialize answer list
                st.session_state.step = 1

    if 1 <= st.session_state.step <= len(st.session_state.questions):
        question_index = st.session_state.step - 1
        question = st.session_state.questions[question_index]

        st.write(f"### Question {st.session_state.step}")
        st.write(f"🤖 {question}")

        # Show text area with stored value, reset after submission
        answer = st.text_area("Your Answer", value=st.session_state.current_answer, key=f"answer_{st.session_state.step}")

        if st.button("Submit Answer"):
            cleaned_answer = answer.strip()  # ✅ Trim spaces to avoid validation issues
            if len(cleaned_answer) < 10:
                st.error("Answer must be at least 10 characters long.")
            else:
                st.session_state.answers[question_index] = cleaned_answer  # Store cleaned answer
                st.session_state.current_answer = ""  # Reset the text box
                st.session_state.step += 1  # Move to the next question
                st.rerun()  # ✅ Corrected from `st.experimental_rerun()`

    if st.session_state.step > len(st.session_state.questions):
        st.success("All your questions have been answered! We’ve saved your response, and one of our team members will contact you soon. 🚀")
        report = check_answers(st.session_state.questions, st.session_state.answers)
        save_report(report)
        st.write("### Report")
        st.write(report)

        # Reset for next session
        st.session_state.step = 0
        st.session_state.answers = []
        st.session_state.current_answer = ""

def check_answers(questions, answers):
    """Check the answers and generate a report."""
    report = []
    for q, a in zip(questions, answers):
        correct = "Yes" if len(a.strip()) >= 100 else "No"
        report.append({"question": q, "answer": a, "correct": correct})
    return report

if __name__ == "__main__":
    main()
 