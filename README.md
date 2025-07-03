# MySpending

MySpending is a personal expense tracker web application that helps users monitor their daily spending, set budgets, and analyze expenses through interactive visualizations. Built with Flask, SQLite, and Chart.js, it's designed to be simple, intuitive, and mobile-friendly.

# 🚀 Features

- 🔐 User Registration & Login
- 📝 Add, edit, and delete expenses
- 📊 View spending breakdown by category
- 💰 Set personal monthly budget
- 📈 Visual charts for better expense insights
- 📦 Export expenses as CSV
- 📱 Responsive & mobile-ready UI

# 🛠️ Tech Stack

- Backend: Python (Flask), SQLAlchemy, Flask-Login
- Frontend: HTML, CSS, Jinja2, Chart.js
- Database: SQLite
- Hosting: Render

# 📷 Screenshots
![Screenshot (20)](https://github.com/user-attachments/assets/b4c4324d-9967-4021-a94a-56e085161ba5)

# 📁 Project Structure

```
myspending/
│
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models.py
│   ├── templates/
│   │   ├── layout.html
│   │   ├── index.html
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard.html
│   │   └── ...
│   └── static/
│       └── style.css
│
├── run.py
├── requirements.txt
└── README.md
```

# 🔐 Authentication

- Passwords are securely hashed using `werkzeug.security`.
- User sessions are managed with Flask-Login.
- Access to dashboard and budget features requires login.

# 📤 Deployment

- Deployed to Render
- Link to deployed app:

# 📌 Future Improvements

- ✅ Forgot password recovery
- ✅ Profile management
- ✅ Monthly summary emails
- 🌍 Multi-currency support
- 📱 PWA/mobile offline mode
- ✅ Link banking app to track expenses and automate expense summarry

# 👩🏽‍💻 Author

Thandeka Siphiwokuhle Mavundla

Senior Research Assistant in Bioinformatics

💻 ALX Software Engineering Student

📫 [LinkedIn](www.linkedin.com/in/thandeka-mavundla-01b232188)

# 📄 License
This project is licensed under the MIT License.
