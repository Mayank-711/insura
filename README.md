# 🛡️ Insurance Advisor Chatbot

An intelligent insurance advisor chatbot built with **Django**, **Gemini AI**, and a custom **chat UI**. It helps users find personalized insurance recommendations, explains BFSI (Banking, Financial Services, and Insurance) terms, and compares plans — all in real-time.

---

## 🚀 Features

- 🔍 **BFSI Term Explanation** – Explains insurance/banking terms using simple analogies, definitions, and layman-friendly examples.
- 👤 **User Profiling** – Extracts user age, income, occupation, goals, and risk level from conversation context.
- 📊 **Insurance Recommendation Engine** – Suggests best plans based on user's needs.
- 📈 **Plan Comparison Table** – Shows structured plan comparison (coverage, premium, tax benefit).
- 🧾 **Summary with Next Steps** – Provides a clear actionable summary.
- 💬 **Chat UI** – Animated, responsive chatbot built with vanilla JS and CSS.

---

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML5, CSS3, JavaScript
- **Other:** Prompt engineering, JSON profile extraction, structured HTML rendering

---

## 📂 Project Structure

```

insura/
│
├── advisor/
│   ├── templates/
│   │   └── home.html, chat.html
│   ├── static/
│   │   └── chatbot.css, chatbot.js
│   ├── views.py
│   ├── utils.py
│   └── urls.py
├── manage.py
└── requirements.txt

````

---

## 🧪 Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/Mayank-711/insura.git
cd insura

# 2. Create virtual environment
python -m venv env
source env/bin/activate  # or env\Scripts\activate on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Django server
python manage.py runserver
````

---

## 🧠 How It Works

1. **User Message** → captured and appended to conversation context
2. **Django View** → sends chat history to Gemini
3. **Gemini Prompt** → extracts profile / recommends plans / compares them
4. **Response Rendered** → structured `<h3>`, `<table>`, `<ul>` in chat UI

---

## 📌 Note

This project is for educational/demo purposes only. It does not replace professional financial advice.

---

## 📄 License

MIT License © 2025 Mayank-711 (https://github.com/Mayank-711)



