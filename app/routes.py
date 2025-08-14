from flask import Blueprint, render_template, request, redirect, url_for, flash, session, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from app import db
from .models import User, Prediction
from .forms import LoginForm, RegisterForm, PredictionForm
import random
from app.ml_model.predict import model_encoders,feature_order
from app.ml_model.predict import predict_loan_default
from app.ml_model.utils import decode_value
import json


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
    return render_template('home.html')


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
    return render_template(
        'user_dashboard.html',
        total_predictions=total_predictions,
        not_likely_default=not_likely_default,
        likely_default=likely_default
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

    if request.method == "POST":
        print("✅ POST Request Received")

        if form.validate_on_submit():
            print("✅ Form validated successfully")

            input_data = {
                field.name: field.data
                for field in form if field.name in feature_order and field.data is not None
            }

            result, score, decoded_inputs = predict_loan_default(input_data)

            pred = Prediction(
                user_id=current_user.id,
                result=result,
                score=score,
                input_data=json.dumps(decoded_inputs)
            )
            db.session.add(pred)
            db.session.commit()

            prediction = f"{result} (Score: {score:.2f})"
            flash(f'Prediction completed: {prediction}', 'info')
        else:
            print("❌ Form validation failed:", form.errors)

    return render_template(
        'predict.html',
        form=form,
        prediction=prediction,
        decoded_inputs=decoded_inputs
    )











@bp.route('/history')
@login_required
def prediction_history():
    predictions = Prediction.query.filter_by(user_id=current_user.id).order_by(Prediction.created_at.desc()).all()
    return render_template('prediction_history.html', predictions=predictions)


@bp.route('/apply-loan')
@login_required
def apply_loan():
    return render_template('apply_loan.html')



@bp.route('/crm')
@login_required
def crm_view():
    user_predictions = Prediction.query.filter_by(user_id=current_user.id).all()

    total_predictions = len(user_predictions)
    likely_default = sum(1 for p in user_predictions if p.result.lower() == 'likely to default')
    not_likely_default = sum(1 for p in user_predictions if p.result.lower() == 'not likely to default')

    # Add these two lines for Chart.js
    chart_labels = ['Likely to Default', 'Not Likely to Default']
    chart_values = [likely_default, not_likely_default]

    return render_template(
        'crm.html',
        user=current_user,
        predictions=user_predictions,
        total_predictions=total_predictions,
        chart_labels=chart_labels,
        chart_values=chart_values
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




@bp.errorhandler(403)
def forbidden(e):
    return render_template('403.html'), 403
