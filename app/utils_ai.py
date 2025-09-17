import json
import numpy as np
import pandas as pd
import shap
from datetime import datetime, timedelta
from .ml_model.predict import model, preprocess_input, feature_order, encoders
from .models import Prediction, Loan
from flask_login import current_user
from app import db
import re

def get_ai_answer(user_message, loan, officer):
    """
    Hybrid rule-based + ML Q&A for Loan Officer
    user_message: string typed by officer
    loan: Loan object (can be None)
    officer: current_user object (can be None)
    """

    msg = re.sub(r'[^\w\s]', '', user_message.lower().strip())

    # --- Not signed in / officer object is None ---
    if officer is None:
        return ("👋 Hey there! I’m your AI Loan Assistant. "
                "Sign in to interact with me, loans, borrowers, and predictions.")


    if hasattr(officer, "role") and officer.role == "admin":
    return (f"Hello {officer.username}, I see you are logged in as an Admin. "
            "This AI assistant is currently tailored for Loan Officers to manage borrower and loan insights. "
            "For administrative access to this service, please contact the developer, Gurveer Singh.")
    
    # --- Friendly / conversational responses ---
    if re.search(r'\b(hello|hi|hey)\b', msg):
        return f"Hello {officer.username}! How can I assist you today?"

    if any(word in msg for word in ["thank", "thanks", "thx"]):
        return "I'm happy to help! Your satisfaction keeps me motivated 😊"

    if "good job" in msg or "well done" in msg:
        return "Thank you! Glad I could assist you effectively."

    if "how are you" in msg:
        return "I'm functioning at full capacity, ready to help you with your loans!"

    if "who made you" in msg or "who created you" in msg:
        return "I was created by Gurveer Singh to assist Loan Officers in making informed decisions."

    if "bye" in msg or "see you" in msg:
        return "Goodbye! Wishing you a productive day."

    # --- Officer identity & role ---
    if "who am i" in msg or msg == "me":
        if loan is None:
            return ("You are logged in, but I cannot find any predictions or loans associated with you yet. "
                    "Please make your first prediction so I can get to know you better.")
        return f"You are {officer.username}, logged in as a Loan Officer."

    if "officer" in msg:
        return f"You are {officer.username}, your role is Loan Officer."
    
    # --- Loan info ---
    if "loan id" in msg:
        if loan:
            return f"This is loan #{loan.id} for {loan.borrower_city}, {loan.borrower_state}."
        return ("I don't see any loans associated with you yet. Please make your first prediction "
                "so I can provide loan-related information.")

    if "borrower" in msg or "business" in msg:
        if loan:
            return (f"Borrower info:\nBank Name: {loan.name_of_bank}\nCity: {loan.borrower_city}\n"
                    f"State: {loan.borrower_state}\nBusiness Type: {loan.business}")
        return ("No borrower info available. It seems you haven't made any predictions yet. "
                "Create your first prediction to access borrower details.")

    if "help" in msg or "what can i do" in msg:
        return ("You can ask about default risk, borrower info, loan ID, your predictions "
                "(today, this week, all-time), or your last prediction. You can also greet me or ask who created me!")

    # --- Officer prediction stats ---
    today = datetime.now().date()
    if any(keyword in msg for keyword in ["total prediction today", "prediction today", "made today"]):
        count = Prediction.query.filter(
            Prediction.user_id == officer.id,
            db.func.date(Prediction.created_at) == today
        ).count()
        return f"You have made {count} prediction(s) today."

    if any(keyword in msg for keyword in ["total prediction this week", "prediction this week"]):
        start_week = datetime.combine(today - timedelta(days=today.weekday()), datetime.min.time())
        end_week = datetime.combine(today, datetime.max.time())
        count = Prediction.query.filter(
            Prediction.user_id == officer.id,
            Prediction.created_at.between(start_week, end_week)
        ).count()
        return f"You have made {count} prediction(s) this week."

    if any(keyword in msg for keyword in ["total prediction all time", "all prediction", "total prediction"]):
        count = Prediction.query.filter_by(user_id=officer.id).count()
        return f"You have made {count} prediction(s) in total."

    if any(keyword in msg for keyword in ["last prediction", "recent prediction", "latest prediction"]):
        last_pred = Prediction.query.filter_by(user_id=officer.id).order_by(Prediction.created_at.desc()).first()
        if last_pred:
            return f"Your last prediction: {last_pred.result} (Score: {last_pred.score:.2f}) made on {last_pred.created_at.strftime('%Y-%m-%d %H:%M')}."
        return "You have no predictions yet. Make your first prediction so I can track it!"

    # --- Default risk / loan prediction questions ---
    if any(word in msg for word in ["default", "risk", "probability", "why", "chance"]):
        if not loan:
            return "I cannot provide risk information because no loan is selected or available."

        try:
            # --- ML prediction ---
            loan_features = {col: getattr(loan, col) for col in feature_order}
            X_input = pd.DataFrame([preprocess_input(loan_features, encoders, feature_order)], columns=feature_order)
            pred_label_num = model.predict(X_input)[0]
            pred_prob = model.predict_proba(X_input)[0][1]
            pred_label_text = "High risk of default" if pred_label_num == 1 else "Low risk of default"

            explanation = ""

            # --- Categorical features ---
            def decode_binary(value):
                try:
                    val = int(value)  # ensure integer
                    return "Yes" if val == 1 else "No"
                except:
                    return "No"

            cat_features = [f for f in encoders.keys() if f in feature_order]
            binary_cols = ["low_documentation_loan", "revolving_credit_line"]

            cat_desc = []
            for f in cat_features:
                if f in binary_cols:
                    decoded = decode_binary(getattr(loan, f))
                else:
                    val = X_input[f].iloc[0]
                    decoded = encoders[f].inverse_transform([val])[0]
                cat_desc.append(f"{f}={decoded}")

            explanation += "Categorical features:\n" + ", ".join(cat_desc) + "\n"

            # --- Numeric SHAP contributors ---
            try:
                explainer = shap.TreeExplainer(model)
                shap_values = explainer.shap_values(X_input)
                shap_vals = shap_values[1] if isinstance(shap_values, list) else shap_values

                numeric_features = [f for f in feature_order if f not in cat_features]
                indices = [feature_order.index(f) for f in numeric_features]
                top_idx = np.argsort(np.abs(shap_vals[0][indices]))[::-1][:3]

                numeric_desc = []
                for idx in top_idx:
                    feat = feature_order[idx]
                    val = X_input[feat].iloc[0]
                    contrib = shap_vals[0][idx]
                    direction = "increases" if contrib > 0 else "decreases"
                    numeric_desc.append(f"{feat}={val} ({direction} risk)")
                explanation += "Top numeric contributors:\n" + ", ".join(numeric_desc)
            except Exception:
                numeric_features = [f for f in feature_order if f not in cat_features]
                explanation += "\nFeature-based reasoning (approx):\n" + ", ".join(
                    [f"{f}={X_input[f].iloc[0]}" for f in numeric_features[:3]]
                )

            # --- Dynamic safe thresholds ---
            safe_msgs = []
            if hasattr(loan, "jobs_created"):
                safe_msgs.append("jobs_created is high, reducing risk" if loan.jobs_created > 50 else "jobs_created is low, increasing risk")
            if hasattr(loan, "jobs_retained"):
                safe_msgs.append("jobs_retained is sufficient" if loan.jobs_reatained > 2 else "jobs_retained is low, increasing risk")
            if hasattr(loan, "guaranteed_approved__loan"):
                safe_msgs.append("guaranteed_approved_loan is moderate, reducing risk" if loan.guaranteed_approved__loan < 2_000_000 else "guaranteed_approved_loan is high, increasing risk")
            explanation += "\n\n" + "; ".join(safe_msgs)

            # --- Loan performance trends / stats ---
            similar_loans = Loan.query.filter(
                Loan.borrower_state == loan.borrower_state,
                Loan.business == loan.business
            ).all()
            if similar_loans:
                avg_loan_amt = np.mean([l.guaranteed_approved__loan for l in similar_loans])
                avg_jobs_created = np.mean([l.jobs_created for l in similar_loans])
                avg_jobs_retained = np.mean([l.jobs_reatained for l in similar_loans])
                explanation += (
                    f"\n\nLoan Trends in {loan.borrower_state} for {loan.business}:\n"
                    f"- Average loan amount: {avg_loan_amt:.0f}\n"
                    f"- Average jobs created: {avg_jobs_created:.1f}\n"
                    f"- Average jobs retained: {avg_jobs_retained:.1f}"
                )

            # --- Alerts / warnings ---
            alerts = []
            if pred_prob > 0.7:
                alerts.append("\n⚠️ This loan has high default probability!")
            if decode_binary(getattr(loan, "low_documentation_loan")) == "Yes":
                alerts.append("\n⚠️ This loan has low documentation, needs attention!")
            if alerts:
                explanation += "\n\nAlerts:\n" + "\n".join(alerts)

            # --- Historical officer stats ---
            officer_preds = Prediction.query.filter_by(user_id=officer.id).all()
            if officer_preds:
                total_preds = len(officer_preds)
                correct_preds = sum(1 for p in officer_preds if getattr(p, 'result_num', -1) == getattr(p, 'actual_default', -1))
                avg_score = np.mean([p.score for p in officer_preds])
                explanation += f"\n\nYour Historical Stats:\n- Accuracy: {correct_preds/total_preds*100:.1f}%\n- Avg Risk Score: {avg_score:.2f}"

            # --- Loan recommendations ---
            recommendation = []
            if decode_binary(getattr(loan, "low_documentation_loan")) == "Yes":
                recommendation.append("Increase documentation for the loan to reduce risk.")

            if hasattr(loan, "jobs_created") and similar_loans:
                if loan.jobs_created < avg_jobs_created:
                    recommendation.append("Encourage borrower to expand jobs created.")

            if recommendation:
                explanation += "\n\nRecommendations:\n- " + "\n- ".join(recommendation)

            return f"Prediction: {pred_label_text} ({pred_prob*100:.2f}% probability).\n{explanation}"

        except Exception as e:
            return f"Error generating prediction: {str(e)}"

    # --- Interactive / fallback queries ---
    if any(keyword in msg for keyword in ["last 5 predicts", "recent 5 predicts"]):
        try:
            last5 = Prediction.query.filter_by(user_id=officer.id).order_by(Prediction.created_at.desc()).limit(5).all()
            if last5:
                return "\n".join([f"Loan #{p.id}: {p.result} ({p.score:.2f})" for p in last5])
            return "No recent predictions found."
        except Exception as e:
            return f"Error fetching last 5 loans: {str(e)}"

    if "rank my loans by risk" in msg:
        loans = Prediction.query.filter_by(user_id=officer.id).all()
        if loans:
            sorted_loans = sorted(loans, key=lambda x: getattr(x, 'score', 0), reverse=True)
            return "\n".join([f"Loan #{l.loan_id}: {l.score:.2f}" for l in sorted_loans])
        return "No loans found to rank."

    if loan is None:
        return ("I notice you haven't made any predictions yet. Try creating your first loan prediction, "
                "and I can provide insights, stats, and risk assessments for you.")

    return ("I'm here to answer questions about loans, borrower info, default risk, "
            "your prediction stats, and recommendations. Can you clarify or ask something specific?")

