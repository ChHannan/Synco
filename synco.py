from app import synco, db
from app.models import User, File, Token, Avatar


@synco.shell_context_processor
def make_shell_context():
    """Sets Database models for flask shell"""
    return {'db': db, 'User': User, 'File': File, 'Token': Token, 'Avatar': Avatar}
