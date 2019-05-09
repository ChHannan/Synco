from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    """Login form at /login"""
    username = StringField(label='User:', validators=[DataRequired()], id="username")
    password = PasswordField('Password:', validators=[DataRequired()], id="password")
    remember_me = BooleanField('Remember Me?')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """Registeration form at /register"""
    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email()])
    password = PasswordField('Password:', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        """
        Validates username.
        :param username: Username of the user.
        :return: ValidationError if condition matches.
        """
        user = User.query.filter_by(username=username.data.lower()).first()
        if user is not None:
            raise ValidationError('Please enter a different username.')

    def validate_email(self, email):
        """
        Validates email.
        :param email: Email of the user.
        :return: ValidationError if condition matches.
        """
        email = User.query.filter_by(email=email.data.lower()).first()
        if email is not None:
            raise ValidationError('Please enter a different email address.')


class FileUploadForm(FlaskForm):
    """File Upload Form at /upload"""
    filename = StringField('Filename:')
    file = FileField('Choose file to upload:', validators=[FileRequired()])
    repo = RadioField('Choose your repository :', validators=[DataRequired()], choices=[('public', 'Public'),
                                                                                        ('private', 'Private')])
    submit = SubmitField('Upload')


class LostPasswordForm(FlaskForm):
    """Lost Password Form at /lost-password"""
    username = StringField('Enter username or email:', validators=[DataRequired()])
    submit = SubmitField('Send mail')


class ResetPasswordForm(FlaskForm):
    """Reset Password Form at /reset"""
    password = PasswordField('Enter new password', validators=[DataRequired()])
    password2 = PasswordField('Confirm your password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset password')


class AvatarUploadForm(FlaskForm):
    """Avatar Upload Form at /avatar"""
    avatar = FileField('', validators=[FileRequired(), FileAllowed(['jpeg', 'jpg', 'png', 'gif'], 'Invalid file type!')]
                       )
    submit = SubmitField('Upload')


class DocumentForm(FlaskForm):
    """Document Form at /document/<token>"""
    file_data = TextAreaField('Editor')
    submit = SubmitField('Update')
