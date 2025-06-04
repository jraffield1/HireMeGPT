# HireMeGPT

**HireMeGPT** is an AI-powered resume and cover letter tailoring tool. It helps you generate personalized job application materials based on a job posting URL or a pasted job description. Built with Streamlit, OpenAI, WeasyPrint, and Playwright.

---

## 🚀 Features

- ✨ Automatically tailor your resume and cover letter to any job posting
- 🧠 Uses OpenAI to analyze job descriptions and suggest edits
- 📄 Live PDF previews and download options
- 📝 Interactive editing of resume content
- 🌐 URL scraping with Playwright
- 🐳 One-command startup via Docker Compose

---

## 📦 Requirements

- Docker and Docker Compose (recommended)
- OR Python 3.12+ (for local non-Docker use)
- OpenAI API Key

---

## 🐳 Quick Start (Docker Compose)

1. Clone the repository:

```bash
git clone https://github.com/jraffield1/HireMeGPT.git
cd HireMeGPT
```

2. Create a `.env` file in the project root:

```
OPENAI_API_KEY=sk-...yourkey...
```

3. Start the app with Docker Compose:

```bash
docker-compose up --build
```

4. Open your browser and go to: [http://localhost:8501](http://localhost:8501)

---

## 🔧 Manual Setup (Without Docker)

1. Set up a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
playwright install --with-deps
```

3. Create a `.env` file with your OpenAI key:

```
OPENAI_API_KEY=sk-...yourkey...
```

4. Run the app:

```bash
streamlit run streamlit_app.py
```

## Personalizing

In app/templates/resumes.py there is a preloaded dummy resume called OriginalResume which should be updated to reflect your own unedited resume.
In app/templates there are also html templates for the resume and coverletter formatting that you want to export with.

---

## 📁 Project Structure

```
.
├── app/
│   ├── models/                 # Pydantic models for resume structure
│   ├── services/               # Business logic: scraping, generation, rendering
│   └── templates/              # Jinja2 templates for HTML/PDF rendering
├── streamlit_app.py           # Main Streamlit interface
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Docker config
├── docker-compose.yml         # Compose for easy local dev
├── .env                       # Your OpenAI API key goes here
└── README.md
```

---

## 📄 License

MIT License  
© 2025 Jesse Raffield

This project is not affiliated with OpenAI or any job board. Use responsibly and ethically.

---

## 💡 Future Improvements (Ideas)

- Google Drive PDF export
- Resume importing
- Multi-template support (choose resume layouts)
- LinkedIn job parsing

---

## 🤝 Contributing

PRs welcome! If you want to extend this tool, feel free to fork and improve it.
