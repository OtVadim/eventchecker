from app import app, db
from app.models import User, Comments, Events, Place, EventImage


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Comments': Comments, 'Events': Events, 
    'Place': Place, 'EventImage': EventImage }