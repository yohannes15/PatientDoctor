from app import app, db
from app.models import User, Patient

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Therapist': Therapist, 'Patient': Patient}
