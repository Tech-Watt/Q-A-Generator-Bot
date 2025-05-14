import streamlit as st
import os
import json
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import csv
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
# --- Load API Key ---
load_dotenv()
# openai_api_key = os.getenv("openai_model")
openai_api_key = st.secrets["openai_model"]
if not openai_api_key:
    raise EnvironmentError("OPENAI_API_KEY not found. Please set it in your .env file.")

# --- Prompt Template ---
quiz_prompt = PromptTemplate(
    input_variables=["class_level", "topics", "question_types", "difficulty", "num_questions"],
    template="""
You are a professional teacher creating a quiz for {class_level} students.

Topics: {topics}
Question Types: {question_types}
Difficulty: {difficulty}
Number of Questions: {num_questions}

Please return a quiz in the following JSON format:

{{
  "questions": [
    {{
      "type": "MCQ" | "Fill-in-the-blank" | "Open-ended",
      "topic": "The topic of the question",
      "question": "The question here",
      "options": ["A", "B", "C", "D"],  # Only for MCQ
      "answer": "Correct answer"
    }}],
  "answer_key": [
    {{
      "question": "The question here",
      "answer": "Correct answer"
    }}
  ]
}}

Return correct answers even though answers may vary for some questions.
Make sure the questions are well-distributed across the topics. Ensure valid JSON output.

"""
)

# --- LangChain Chain ---
def get_quiz_chain():
    parser = StrOutputParser()
    llm = ChatOpenAI(temperature=0.7, model="gpt-4", openai_api_key=openai_api_key)
    return quiz_prompt | llm | parser

# --- Helpers ---
def generate_pdf(quiz_data):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    textobject = c.beginText(1 * inch, height - 1 * inch)
    textobject.setFont("Helvetica", 12)

    textobject.textLine("Quiz Questions")
    textobject.textLine("")

    for idx, q in enumerate(quiz_data["questions"], 1):
        textobject.textLine(f"{idx}. ({q['type']}) [{q['topic']}] {q['question']}")
        if q["type"] == "MCQ":
            for opt in q["options"]:
                textobject.textLine(f"  - {opt}")
        textobject.textLine("")

    c.drawText(textobject)
    c.showPage()

    # Add Answer Key
    textobject = c.beginText(1 * inch, height - 1 * inch)
    textobject.setFont("Helvetica", 12)
    textobject.textLine("Answer Key")
    textobject.textLine("")

    for idx, a in enumerate(quiz_data["answer_key"], 1):
        textobject.textLine(f"{idx}. {a['question']}")
        textobject.textLine(f"Answer: {a['answer']}")
        textobject.textLine("")

    c.drawText(textobject)
    c.save()
    buffer.seek(0)
    return buffer


def generate_csv(quiz_data):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Question", "Type", "Topic", "Options", "Answer"])

    for q in quiz_data["questions"]:
        options = ", ".join(q.get("options", [])) if q["type"] == "MCQ" else ""
        writer.writerow([q["question"], q["type"], q["topic"], options, q["answer"]])
    
    return output.getvalue()

# --- Streamlit UI Setup ---
st.set_page_config(page_title="Jesi AI Quiz Generator", page_icon="🧠")
st.title("🧠 Jesi AI Quiz Generator")

# --- Session State Init ---
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = None

if "show_answers" not in st.session_state:
    st.session_state.show_answers = False

# --- Quiz Form ---
with st.form("quiz_form"):
    class_level = st.multiselect(
        "Class Levels",
        ["Class one","Class two","Class three","Class four","Class five",
         "Class six","JHS one","JHS two","JHS three","SHS one","SHS two","SHS three"],
        default=["JHS one"]
    )
    topics = st.text_input("Topics (comma-separated)", value="Photosynthesis, Respiration")
    question_types = st.multiselect("Question Types", ["MCQ", "Fill-in-the-blank", "Open-ended"], default=["MCQ"])
    difficulty = st.selectbox("Difficulty Level", ["Easy", "Medium", "Hard", "Mixed"], index=3)
    num_questions = st.slider("Number of Questions", min_value=2, max_value=50, value=5)

    submitted = st.form_submit_button("Generate Quiz")

# --- Generate Quiz Logic ---
if submitted:
    with st.spinner("Generating quiz..."):
        try:
            chain = get_quiz_chain()
            response = chain.invoke({
                "class_level": ", ".join(class_level),
                "topics": topics,
                "question_types": ", ".join(question_types),
                "difficulty": difficulty,
                "num_questions": num_questions
            })

            quiz_data = json.loads(response)
            st.session_state.quiz_data = quiz_data
            st.session_state.show_answers = False  # Reset state
            st.success("✅ Quiz generated successfully!")

        except Exception as e:
            st.error(f"❌ Failed to generate quiz: {str(e)}")

# --- Display Quiz ---
if st.session_state.quiz_data:
    quiz_data = st.session_state.quiz_data

    st.subheader("📘 Questions")
    for idx, q in enumerate(quiz_data["questions"], 1):
        st.markdown(f"**{idx}. ({q['type']}) [{q['topic']}]**")
        st.markdown(q["question"])
        if q["type"] == "MCQ":
            for opt in q["options"]:
                st.markdown(f"- {opt}")
        st.markdown("---")

    if st.button("👁 Show Answers"):
        st.session_state.show_answers = True

    if st.session_state.show_answers:
        st.subheader("✅ Answer Key")
        for idx, a in enumerate(quiz_data["answer_key"], 1):
            st.markdown(f"**{idx}.** {a['question']}")
            st.markdown(f"**Answer:** {a['answer']}")
            st.markdown("---")

    # --- Downloads ---
    st.subheader("⬇️ Download Quiz")
    
    pdf_file = generate_pdf(quiz_data)
    st.download_button("📄 Download PDF", data=pdf_file, file_name="quiz.pdf", mime="application/pdf")


    csv_content = generate_csv(quiz_data)
    st.download_button("📊 Download CSV", data=csv_content, file_name="quiz.csv", mime="text/csv")

    st.download_button("📥 Download JSON", data=json.dumps(quiz_data, indent=2),
                       file_name="quiz.json", mime="application/json")

