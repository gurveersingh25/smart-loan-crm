from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort, jsonify, Flask
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app import db
from .models import User, Prediction, Loan 
from .forms import LoginForm, RegisterForm, PredictionForm
import random
from app.ml_model.predict import model_encoders, feature_order
from app.ml_model.predict import predict_loan_default
from app.ml_model.utils import decode_value
import json
from collections import defaultdict
from datetime import datetime
from datetime import datetime, timedelta
from app.utils_ai import get_ai_answer

def get_encoder_choices(column_name):
    if column_name not in model_encoders:
        return []
    encoder = model_encoders[column_name]
    if hasattr(encoder, 'classes_'):
        return [(cls, cls) for cls in encoder.classes_]
    return []


bp = Blueprint('routes', __name__)


@bp.route('/')
def home():
    return render_template('home.html', loan=None)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('routes.user_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('routes.user_dashboard'))
        flash('Invalid email or password', 'danger')
    return render_template('login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('routes.user_dashboard'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if username exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already taken. Please choose another.', 'danger')
            return render_template('register.html', form=form)
        
        # Check if email exists
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered', 'danger')
            return render_template('register.html', form=form)
        
        # Create new user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!', 'success')
        return redirect(url_for('routes.login'))
    
    return render_template('register.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('routes.home'))


@bp.route('/dashboard')
@login_required
def user_dashboard():
    if current_user.role == 'admin':
        return redirect(url_for('routes.admin_dashboard'))
    
    user_predictions = Prediction.query.filter_by(user_id=current_user.id).all()

    total_predictions = len(user_predictions)
    likely_default = sum(1 for p in user_predictions if p.result.lower() == 'likely to default')
    not_likely_default = sum(1 for p in user_predictions if p.result.lower() == 'not likely to default')

    # ⚡ Fetch the latest loan for AI chat
    loan = Loan.query.filter_by(officer_id=current_user.id).order_by(Loan.id.desc()).first()

    return render_template(
        'user_dashboard.html',
        total_predictions=total_predictions,
        not_likely_default=not_likely_default,
        likely_default=likely_default,
        loan=loan  # <<< pass loan object for AI chat
    )


@bp.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        abort(403)
    users = User.query.all()
    return render_template('admin_dashboard.html', users=users)


@bp.route('/predict', methods=['GET', 'POST'])
@login_required
def predict_loan():
    form = PredictionForm()

    # Set dynamic choices
    form.business.choices = get_encoder_choices("business")
    form.demography.choices = get_encoder_choices("demography")
    form.borrower_state.choices = get_encoder_choices("borrower_state")
    form.borrower_city.choices = get_encoder_choices("borrower_city")
    form.name_of_bank.choices = get_encoder_choices("name_of_bank")
    form.state_of_bank.choices = get_encoder_choices("state_of_bank")
    form.low_documentation_loan.choices = [(0, 'No'), (1, 'Yes')]
    form.revolving_credit_line.choices = [(0, 'No'), (1, 'Yes')]

    prediction = None
    decoded_inputs = None
    last_loan = None  # <<< variable to hold last loan

    if request.method == "POST":
        print("✅ POST Request Received")

        if form.validate_on_submit():
            print("✅ Form validated successfully")

            input_data = {
                field.name: field.data
                for field in form if field.name in feature_order and field.data is not None
            }

            result, score, decoded_inputs, X_input_decoded = predict_loan_default(input_data)

            pred = Prediction(
                user_id=current_user.id,
                result=result,
                score=score,
                input_data=json.dumps(decoded_inputs)
            )
            db.session.add(pred)
            db.session.commit()

            # ✅ Create Loan entry tied to prediction
            loan = Loan(
                officer_id=current_user.id,
                business=decoded_inputs.get('business'),
                jobs_reatained=decoded_inputs.get('jobs_reatained'),
                jobs_created=decoded_inputs.get('jobs_created'),
                guaranteed_approved__loan=decoded_inputs.get('guaranteed_approved__loan'),
                low_documentation_loan=decoded_inputs.get('low_documentation_loan'),
                demography=decoded_inputs.get('demography'),
                state_of_bank=decoded_inputs.get('state_of_bank'),
                chargedoff_amount=decoded_inputs.get('chargedoff_amount'),
                borrower_city=decoded_inputs.get('borrower_city'),
                borrower_state=decoded_inputs.get('borrower_state'),
                gross_amount_balance=decoded_inputs.get('gross_amount_balance'),
                count_employees=decoded_inputs.get('count_employees'),
                classification_code=decoded_inputs.get('classification_code'),
                loan_approved_gross=decoded_inputs.get('loan_approved_gross'),
                gross_amount_disbursed=decoded_inputs.get('gross_amount_disbursed'),
                loan_term=decoded_inputs.get('loan_term'),
                code_franchise=decoded_inputs.get('code_franchise'),
                name_of_bank=decoded_inputs.get('name_of_bank'),
                revolving_credit_line=decoded_inputs.get('revolving_credit_line'),
                prediction=result
            )
            db.session.add(loan)
            db.session.commit()
            last_loan = loan

            prediction = f"{result} (Score: {score:.2f})"
            flash(f'Prediction completed: {prediction}', 'info')

        else:
            print("❌ Form validation failed:", form.errors)

    # On GET, set last_loan to last prediction's loan if exists
    if last_loan is None:
        last_loan = Loan.query.order_by(Loan.id.desc()).filter_by(officer_id=current_user.id).first()

    return render_template(
        'predict.html',
        form=form,
        prediction=prediction,
        decoded_inputs=decoded_inputs,
        loan=last_loan  # pass loan to template for AI chat
    )


@bp.route('/history')
@login_required
def prediction_history():
    predictions = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.created_at.desc()).all()
    last_loan = Loan.query.filter_by(officer_id=current_user.id)\
                      .order_by(Loan.id.desc()).first()
    return render_template('prediction_history.html', predictions=predictions,loan=last_loan)


@bp.route('/flagged-loans')
@login_required
def flagged_loans_view():
    last_loan = Loan.query.filter_by(officer_id=current_user.id)\
                      .order_by(Loan.id.desc()).first()
    today = datetime.today()
    week_ago = today - timedelta(days=7)

    # Flagged = result "Likely to Default"
    #flagged_loans = Prediction.query.filter_by(result="Likely to Default").all()
    flagged_loans = Prediction.query.filter_by(
        result="Likely to Default",
        user_id=current_user.id  # <-- filter by officer
    ).all()

    for loan in flagged_loans:
        # Parse input data safely
        try:
            loan.parsed_data = json.loads(loan.input_data)
        except Exception:
            loan.parsed_data = {}

        # Ensure created_at is always valid for JS filters
        if not loan.created_at:
            loan.created_at = datetime.utcnow()

    # Stats
    flagged_count = len(flagged_loans)
    flagged_today = (
        Prediction.query.filter_by(result="Likely to Default")
        .filter(Prediction.created_at >= datetime(today.year, today.month, today.day))
        .count()
    )
    flagged_week = (
        Prediction.query.filter_by(result="Likely to Default")
        .filter(Prediction.created_at >= week_ago)
        .count()
    )

    return render_template(
        'flagged_loans.html',
        flagged_loans=flagged_loans,
        flagged_count=flagged_count,
        flagged_today=flagged_today,
        flagged_week=flagged_week,
        loan=last_loan
    )









@bp.route('/crm')
@login_required
def crm_view():
    last_loan = Loan.query.filter_by(officer_id=current_user.id)\
                      .order_by(Loan.id.desc()).first()
    user_predictions = Prediction.query.filter_by(user_id=current_user.id).all()

    total_predictions = len(user_predictions)
    likely_default = sum(1 for p in user_predictions if p.result.lower() == 'likely to default')
    not_likely_default = sum(1 for p in user_predictions if p.result.lower() == 'not likely to default')

    # Pie chart data
    chart_labels = ['Likely to Default', 'Not Likely to Default']
    chart_values = [likely_default, not_likely_default]

    # --- Line chart / trend data ---
    # Group predictions by month
    trend_counts = defaultdict(lambda: {'likely': 0, 'not_likely': 0})
    for p in user_predictions:
        month_label = p.created_at.strftime('%b %Y')  # e.g., 'Sep 2025'
        if p.result.lower() == 'likely to default':
            trend_counts[month_label]['likely'] += 1
        else:
            trend_counts[month_label]['not_likely'] += 1

    # Sort months chronologically
    sorted_months = sorted(trend_counts.keys(), key=lambda x: datetime.strptime(x, '%b %Y'))
    trend_dates = sorted_months
    trend_defaults = [trend_counts[m]['likely'] for m in sorted_months]
    trend_nondefaults = [trend_counts[m]['not_likely'] for m in sorted_months]

    return render_template(
        'crm.html',
        user=current_user,
        predictions=user_predictions,
        total_predictions=total_predictions,
        chart_labels=chart_labels,
        chart_values=chart_values,
        trend_dates=trend_dates,
        trend_defaults=trend_defaults,
        trend_nondefaults=trend_nondefaults,
        loan=last_loan
    )


@bp.route('/promote-user/<int:user_id>')
@login_required
def promote_user(user_id):
    if current_user.role != 'admin':
        abort(403)
    user = User.query.get_or_404(user_id)
    user.role = 'admin'
    db.session.commit()
    flash(f'User {user.username} promoted to admin', 'success')
    return redirect(url_for('routes.admin_dashboard'))


@bp.route('/delete-user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        abort(403)

    user = User.query.get_or_404(user_id)

    if user.id == current_user.id:
        flash('Cannot delete your own account', 'danger')
        return redirect(url_for('routes.admin_dashboard'))

    prediction_count = len(user.predictions)

    # Log or warn if predictions exist
    if prediction_count > 0:
        flash(f'⚠ User {user.username} has {prediction_count} prediction records — deleting will remove all history.', 'warning')

    db.session.delete(user)
    db.session.commit()
    flash(f'✅ User {user.username} deleted successfully', 'success')
    return redirect(url_for('routes.admin_dashboard'))



@bp.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'answer':'No message sent'}), 400

        user_message = data['message']
        loan_id = data.get('loan_id')

        # Officer is current_user if logged in, otherwise None
        officer = current_user if current_user.is_authenticated else None

        # Loan only makes sense if logged in
        loan = None
        if officer and loan_id:
            loan = Loan.query.get(loan_id)
        elif officer:
            loan = Loan.query.filter_by(officer_id=officer.id).order_by(Loan.id.desc()).first()

        answer = get_ai_answer(user_message=user_message, loan=loan, officer=officer)
        return jsonify({'answer': answer})

    except Exception as e:
        return jsonify({'answer': f'Error processing request: {str(e)}'}), 500





@bp.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403
