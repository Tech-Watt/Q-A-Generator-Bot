
# 🧠 TechWatt AI Quiz Generator

TechWatt AI Quiz Generator is a Streamlit-based web app that uses OpenAI’s GPT model to generate high-quality quizzes for students based on specified class levels, topics, question types, and difficulty. The app allows downloading the quiz in **JSON**, **PDF**, and **CSV** formats.

---

## 🚀 Features

- Generate quizzes for multiple class levels (e.g., JHS, SHS)
- Supports question types:
  - Multiple Choice (MCQ)
  - Fill-in-the-blank
  - Open-ended
- Choose difficulty level: Easy, Medium, Hard, Mixed
- Export quiz as:
  - 🗂️ JSON (structured)
  - 📄 PDF (print-ready)
  - 📊 CSV (spreadsheet-friendly)
- View answer key in the app
- Easy-to-use Streamlit UI

---

## 🧰 Tech Stack

- Python
- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [OpenAI GPT-4](https://platform.openai.com/)
- [reportlab](https://www.reportlab.com/) (for PDF generation)
- [dotenv](https://pypi.org/project/python-dotenv/) (for API key management)

---

## 📦 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/jesi-ai-quiz-generator.git
cd jesi-ai-quiz-generator
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt` Example:**
```text
streamlit
openai
langchain
langchain-openai
fpdf
reportlab
python-dotenv
```

### 4. Set Up `.env`

Create a `.env` file and add your OpenAI API key:

```env
openai_model=your-openai-api-key
```

---

## ▶️ Run the App

```bash
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`

---

## 📂 File Structure

```
├── main.py            # Main Streamlit app
├── .env               # Environment file for API key
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

---

## 💡 Example Use Case

A science teacher for JHS 1 can generate a 10-question quiz on "Photosynthesis" and "Respiration", download the quiz as a PDF for printing and a CSV for digital grading.

---

## 🛡️ License

MIT License. See [LICENSE](LICENSE) for details.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request for any feature requests or bug fixes.

---

## 🙋‍♂️ Author

**Felix Sam Nanor**  
📧 [info@techwatt.ai](mailto:info@techwatt.ai)  
🌐 [TechWatt.ai](https://www.techwatt.ai)
