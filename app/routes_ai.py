from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from . import db
from .models import Loan  # Correct table
from .utils_ai import get_ai_answer

bp = Blueprint('ai', __name__, url_prefix='/api/ai')


@bp.route('/chat', methods=['POST'])
def ai_chat():
    """
    Endpoint for AI chat widget.
    Expects JSON:
    {
        "message": "User message",
        "loan_id": 123  # optional, can be null if generic question
    }
    """
    data = request.get_json()
    message = data.get("message", "").strip()
    loan_id = data.get("loan_id")

    officer = current_user if current_user.is_authenticated else None

    loan = None
    if loan_id:
        loan = Loan.query.get(loan_id)
        if not loan:
            return jsonify({"answer": "Loan not found."})

    answer = get_ai_answer(message, loan, officer)
    return jsonify({"answer": answer})

