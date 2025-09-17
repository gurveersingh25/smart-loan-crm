# 🌟 Smart Loan + CRM

**Smart Loan + CRM** – An **AI-powered loan intelligence system** that combines **Machine Learning predictions**, **CRM features**, **AI assistance**, and **database integration** to help loan officers make faster, smarter, and more reliable credit decisions.  

---

## **🚀 LIVE DEMO:** [Click here to see the project in action!](https://smart-loan-crm-9c860c8ee5b7.herokuapp.com/)

⚡ **Note:** This project is a **live prototype** built for **training, demonstration, and recruiter showcase purposes**.  
- Debugging information and internal workflows are **intentionally visible** for learners and reviewers.  
- Not a production deployment — instead, a **working educational system** demonstrating **real AI + CRM integration**.  

---

## 🎯 Project Overview

> **Objective:** Provide loan officers with a **data-driven, AI-assisted tool** that evaluates loans, flags high-risk cases, tracks activity, and visualizes live performance data.  

This platform delivers:  

- Instant **loan default risk prediction** (Likely to Default = Flagged Loan)  
- **AI Loan Assistant** for officer queries and insights  
- **CRM dashboards** with live charts  
- **Flagged Loan filters + downloadable reports**  
- **History module** for tracking all past evaluations  

---

## 🗂️ Core Modules

1. **Prediction**  
   - Officers input loan & borrower details  
   - ML model predicts default probability  
   - AI Assistant explains “why default / why not”  

2. **CRM**  
   - Live **Pie Chart + Bar Chart** showing system-wide prediction stats  
   - Charts update in **real time** with actual prediction data  

3. **Flagged Loans**  
   - Displays **loans likely to default**  
   - Filter by **today, this week, overall**  
   - Export results as **downloadable report**  

4. **History**  
   - Complete log of all past predictions  
   - Filter by timeframe  
   - Export as **downloadable file**  

---

## 🤖 AI Loan Assistant

The integrated **AI Loan Assistant** enhances officer workflows:  

- Answers operational questions like:  
  - *“Who am I?”*  
  - *“What loans did I approve today?”*  
  - *“Why did this loan default?”*  
  - *“Show me total predictions this week.”*  
  - *“List my last predictions.”*
  - *"And many more"*
- Current version: **rule-based + dataset-powered Q&A**  
- Roadmap: Expanding to **NLP-driven assistant** with natural conversation capability  

---

## 🛠️ Technology Stack

- **Backend:** Flask  
- **Frontend:** HTML + TailwindCSS  
- **Database:** Supabase (PostgreSQL, free tier)  
- **ML / AI:** Scikit-learn (RandomForestClassifier), joblib  
- **AI Assistant:** Rule-based Q&A → (planned NLP integration)  
- **Security:** Flask-Login, bcrypt; Role-based authentication (Admin/User)  
- **Deployment:** Heroku (App) + Supabase (DB)  

---

## ⚡ Usage Instructions

1. **Install Dependencies:**  
   ```bash
   pip install -r requirements.txt
2. **Start the Application:**
   ```bash
   python run.py
3. Open in Browser:
   ```bash
   Visit http://127.0.0.1:8000
---

## 👤 Admin / User Login  

### Admin  
- Full control over officers, system stats, and flagged loans  

### User (Officer)  
- Enter loans, run predictions, access AI Assistant, view dashboards  

---

## 📊 Prediction Flow  

1. Officer inputs loan & borrower details  
2. ML model predicts default probability  
3. AI Assistant provides reasoning & totals  
4. If risky → Loan marked as Flagged  
5. Prediction stored in Supabase DB  
6. Results reflected in CRM charts + History logs  

---

## 📂 Data Handling  

- All data stored in **Supabase (PostgreSQL)**  
- ML model + encoders (`mudra_model.pkl`) included in repo  
- Label encoders ensure consistent categorical mappings  
- Export option available in **Flagged Loans** + **History** modules  

---

## 🔧 Notes for Developers  

- Deployed on **Heroku + Supabase**  
- Active development: system is evolving (AI, UI, features)  
- Debugging info left intentionally visible for learners/recruiters  
- Compatible with **scikit-learn 1.6.1**  
- Swappable database & ML artifacts  

---

## 📈 Future Improvements  

- Full NLP-based **AI Loan Assistant** (conversational)  
- Advanced analytics dashboards with trends & KPIs  
- Support for multiple ML models with auto-selection  
- Real-time financial API integration  
- Compliance-ready audit logs  

---

## 🎉 Conclusion  

**Smart Loan + CRM** is a working, deployed AI prototype that combines:  
- Loan predictions (ML)  
- AI assistance (Q&A + insights)  
- CRM workflows (live charts, flagged loans, history)  
- Deployment-ready stack (**Heroku + Supabase**)  

⚡ Designed to showcase real-world AI integration in financial workflows while remaining transparent and beginner-friendly for learning.  

---

## 📌 Emojis / Stickers Legend
---
- ✅ : Implemented feature  
- ⚡ : Important note / tip  
- 💡 : Innovative idea / edge  
- 🏗️ : File structure / build  
- 📈 : Future improvements  
- 🎯 : Objective / goal  
- 🎉 : Success / conclusion

---

## 👤 Author / Developer  

- **Name:** Gurveer Singh  
- **Role:** Data Scientist & Full Stack Developer  
- **GitHub:** [https://github.com/gurveersingh25](https://github.com/gurveersingh25)  
- **LinkedIn:** [https://www.linkedin.com/in/gurveersingh25/](https://www.linkedin.com/in/gurveersingh25/)  
- **Email:** indian.army25ff@gmail.com  

### About the Author  
Gurveer Singh specializes in **Data Science, ML, and Full Stack Development**. This project demonstrates how AI, ML, and secure web platforms can transform loan management into a smart, data-driven system.   

**Connect:** Reach out for collaboration, feedback, or any queries regarding this project.



