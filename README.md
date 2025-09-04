# 🚀 Smart Loan + CRM

**Smart Loan + CRM** – An **intelligent loan management and decision-support system** that combines **Machine Learning**, **secure web interfaces**, and **database integration** to optimize loan officer operations and minimize financial risk.  

---

## 🎯 Project Overview

> **Objective:** Enable loan officers to make **data-driven decisions** efficiently by predicting **loan default risk** in real time.  

This platform allows:  

- Officers to **input customer and loan details**  
- Instant evaluation of whether a loan is **“Likely to Default”** or **“Not Likely to Default”**  
- Admins to **manage officers** and oversee all application evaluations  
- Tracking of all applications with **secure database logging**  

**Key Features:**  

- ✅ **Machine Learning Predictions**: Trained models predict default probability  
- ✅ **Explainable & Debug-Friendly**: Processing and prediction steps are logged for clarity  
- ✅ **Full-Stack Interface**: Admin and User dashboards built with **Tailwind + FastAPI**  
- ✅ **Role-Based Access Control**: Admin (main officer) vs User (loan evaluators)  
- ✅ **Database Integration**: Stores full loan application history  
- ✅ **Secure & Production-Ready**: Authentication, session management, and sensitive data handling  
- ✅ **Student-Prototyped, Production-Ready**: Debugging outputs visible for transparency and learning  

> 💡 **Innovative Edge:** By combining ML predictions with CRM workflows, this system transforms traditional loan offices into **smart, data-driven decision-making hubs**, reducing default risk and improving operational efficiency.  

---

## 🛠️ Technology Stack

- **Backend:** FastAPI  
- **Frontend:** HTML + TailwindCSS  
- **Database:** SQLite (`instance/site.db`)  
- **ML / AI:** Scikit-learn, joblib (RandomForestClassifier)  
- **Security:** Role-based authentication (Admin/User)  
- **Deployment:** Railway / any cloud host  
- **Data Files:** Model & encoders hosted externally for easier deployment  

> ⚠️ **Note:** The ML model (`mudra_model.pkl`) downloads automatically on first run. You don’t need to manually place it. Errors are logged clearly in the terminal for transparency.

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
---
- **Admin:** Full control over loan officers  
- **User:** Evaluate incoming loan applications
---


##📊 Prediction Flow

1. **Input loan & borrower details**
2. **ML model predicts default probability**
3.**Officers can review decoded input values (debug info visible)**

---

## 📂 Data Handling
---
- All sensitive customer data is stored in `instance/site.db`  
- ML artifacts (`mudra_model.pkl`) is downloaded externally to keep the repository light  
- Label encoders ensure consistent categorical mapping  

---

## 🔧 Notes for Developers
---
- The system is **fully functional**, but still under **active improvements**  
- Debug prints and warnings are intentionally left for **learning and transparency**  
- Compatible with **scikit-learn 1.6.1**, ensuring pre-saved encoders load correctly  
- Database and model files can be replaced if needed; system **auto-updates missing artifacts**  

---

## 📈 Future Improvements
---
- Enhanced **UI/UX dashboards**  
- Integration with **real-time banking APIs**  
- Support for **multiple ML models** with auto-selection  
- Comprehensive **audit logs** for compliance    

---

## 🎉 Conclusion
---
**Smart Loan + CRM** provides a **production-like experience** for loan officers, combining **ML predictions**, **secure role-based access**, and **transparent debugging logs**.  

> Ideal for educational, prototype, and demonstration purposes, while being deployable on platforms like **Railway** without major issues.  

⚡ **Pro Tip:** Run locally, observe all debug outputs, and explore the full workflow. The system is designed to be **self-explanatory** and fully transparent.  

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
---
**Name:** Gurveer Singh  
**Role:** Data Scientist & Full Stack Developer  
**GitHub:** [https://github.com/gurveersingh25](https://github.com/gurveersingh25)  
**LinkedIn:** [https://www.linkedin.com/in/gurveersingh25/](https://www.linkedin.com/in/gurveersingh25/)  
**Email:** indian.army25ff@gmail.com  

**About the Author:**  
Gurveer Singh is a passionate developer specializing in **Data Science, Machine Learning, and Full Stack Development**. This project, Smart Loan + CRM, demonstrates his ability to create **data-driven, deployable solutions** with secure role-based access, interactive web interfaces, and AI-powered predictions.  

**Connect:** Reach out for collaboration, feedback, or any queries regarding this project.



