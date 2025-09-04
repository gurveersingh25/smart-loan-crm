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

## 🏗️ File Structure




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




## 📂 **Project Structure**

