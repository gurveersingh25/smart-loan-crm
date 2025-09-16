from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import bcrypt



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.String(20), default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    predictions = db.relationship('Prediction', backref='user', lazy=True, cascade="all, delete-orphan")
    loans = db.relationship('Loan', backref='officer', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)


class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    result = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Float)
    input_data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    officer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Fields from your form
    business = db.Column(db.String(100))
    jobs_reatained = db.Column(db.Integer)
    jobs_created = db.Column(db.Integer)
    guaranteed_approved__loan = db.Column(db.Float)
    low_documentation_loan = db.Column(db.String(20))
    demography = db.Column(db.String(50))
    state_of_bank = db.Column(db.String(50))
    chargedoff_amount = db.Column(db.Float)
    borrower_city = db.Column(db.String(50))
    borrower_state = db.Column(db.String(50))
    gross_amount_balance = db.Column(db.Float)
    count_employees = db.Column(db.Integer)
    classification_code = db.Column(db.String(50))
    loan_approved_gross = db.Column(db.Float)
    gross_amount_disbursed = db.Column(db.Float)
    loan_term = db.Column(db.Integer)
    code_franchise = db.Column(db.String(50))
    name_of_bank = db.Column(db.String(50))
    revolving_credit_line = db.Column(db.String(50))

    # Prediction result
    prediction = db.Column(db.String(20))

    def __repr__(self):
        return f"<Loan {self.id} - Officer {self.officer_id}>"


# -------------------------
# Loan seeding function
# -------------------------
def seed_loans():
    """Ensure at least one sample loan exists in the database."""
    if Loan.query.count() == 0:
        # make sure there’s at least one officer to assign loan to
        officer = User.query.filter_by(role="admin").first()
        if not officer:
            officer = User(
                username="admin",
                email="admin@example.com",
                role="admin"
            )
            officer.set_password("admin123")
            db.session.add(officer)
            db.session.commit()

        sample_loan = Loan(
            officer_id=officer.id,
            business="Retail",
            jobs_reatained=5,
            jobs_created=2,
            guaranteed_approved__loan=250000.0,
            low_documentation_loan="Yes",
            demography="Urban",
            state_of_bank="Delhi",
            chargedoff_amount=0.0,
            borrower_city="New Delhi",
            borrower_state="Delhi",
            gross_amount_balance=100000.0,
            count_employees=10,
            classification_code="451120",
            loan_approved_gross=250000.0,
            gross_amount_disbursed=250000.0,
            loan_term=36,
            code_franchise="N/A",
            name_of_bank="State Bank of India",
            revolving_credit_line="No",
            prediction="Pending"
        )
        db.session.add(sample_loan)
        db.session.commit()
        print("✅ Sample loan and admin seeded.")

