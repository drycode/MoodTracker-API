from app import app, db
from app.models import User, MoodEntry


@app.shell_context_processor
def make_shell_context():
    """
    Establishes necessary context to test server in the python shell.
    Execute by typing `flask shell`
    """
    return {"db": db, "User": User, "MoodEntry": MoodEntry}
