from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField,SelectField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange,InputRequired



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                   validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


#class PredictionForm(FlaskForm):
#    income = FloatField('Annual Income', validators=[DataRequired(), NumberRange(min=0)])
#    loan_amount = FloatField('Loan Amount', validators=[DataRequired(), NumberRange(min=0)])
#    credit_score = IntegerField('Credit Score', validators=[DataRequired(), NumberRange(min=300, max=850)])
#    employment_years = IntegerField('Years of Employment', validators=[DataRequired(), NumberRange(min=0)])
#    debt_to_income = FloatField('Debt to Income Ratio', validators=[DataRequired(), NumberRange(min=0, max=1)])
#    submit = SubmitField('Predict Loan Eligibility')



class PredictionForm(FlaskForm):
    business = SelectField('Business Type', choices=[], validators=[DataRequired()])
    jobs_reatained = FloatField('Jobs Retained', validators=[InputRequired()])
    jobs_created = FloatField('Jobs Created', validators=[InputRequired()])
    guaranteed_approved__loan = FloatField('Guaranteed Loan', validators=[DataRequired()])
    low_documentation_loan = SelectField('Low Documentation', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])
    demography = SelectField('Demography', choices=[], validators=[DataRequired()])
    state_of_bank = SelectField('Bank State', choices=[], validators=[DataRequired()])
    chargedoff_amount = FloatField('Charged-Off Amount', validators=[InputRequired()])
    borrower_city = SelectField('Borrower City', choices=[], validators=[DataRequired()])
    borrower_state = SelectField('Borrower State', choices=[], validators=[DataRequired()])
    gross_amount_balance = FloatField('Gross Amount Balance', validators=[InputRequired()])
    count_employees = IntegerField('Number of Employees', validators=[InputRequired()])
    classification_code = StringField('Classification Code', validators=[DataRequired()])
    loan_approved_gross = FloatField('Loan Approved Gross', validators=[DataRequired()])
    gross_amount_disbursed = FloatField('Gross Amount Disbursed', validators=[DataRequired()])
    loan_term = IntegerField('Term (Months)', validators=[InputRequired(), NumberRange(min=1, max=360)])
    code_franchise = IntegerField('Franchise Code', validators=[InputRequired()])
    name_of_bank = SelectField('Bank Name', choices=[], validators=[DataRequired()])
    revolving_credit_line = SelectField('Revolving Credit Line', choices=[('Yes', 'Yes'), ('No', 'No')], validators=[DataRequired()])

    submit = SubmitField('Predict Loan Eligibility')

