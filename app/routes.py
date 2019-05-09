from app import synco
from flask import render_template, redirect, url_for, request, send_file
from app.forms import LoginForm, RegistrationForm, FileUploadForm, LostPasswordForm, ResetPasswordForm, AvatarUploadForm, DocumentForm
from flask_login import current_user, logout_user, login_required
from app.models import User, Token
from app.forms_class import Register, Login, UserView, LostPassword, Reset, Upload, Confirmation, AvatarView, Editor
from app.funcs_class import FilesPath
# Users/User
from datetime import datetime


@synco.route('/')
def home():
    """
    Home page
    :return: "home.html"
    """
    return render_template('home.html', title="Synco")


@synco.route('/register', methods=['GET', 'POST'])
def register():
    """
    Registeration page
    :return: "register.html"
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        register = Register(form=form)
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)


@synco.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login page
    :return: "login.html"
    """
    if current_user.is_authenticated:
        return redirect(url_for('user', username=current_user.username))
    form = LoginForm()
    if form.validate_on_submit():
        login = Login(form=form)
        return redirect(login.login(next_page=request.args.get('next')))
    return render_template('login.html', title="Login - Synco", form=form)


@synco.route('/logout')
def logout():
    """
    Logouts the user
    :return: "home.html"
    """
    logout_user()
    return redirect(url_for('home'))


@synco.route('/users/<username>')
@login_required
def user(username):
    """
    User profile page
    :param username: Username of the user.
    :return: Profile page of the user with given username.
    """
    user = UserView(username=username, id=request.args.get('id'))
    action_arg = request.args.get('action')
    action = user.action(action=action_arg)
    token_db = Token()
    if action:
        if action_arg == "download":
            return send_file(action, as_attachment=True, attachment_filename=user.file.filename)
        elif action_arg == "delete":
            return redirect(action)
    return render_template('user.html', time=datetime, int=int, timeuser=user.timeuser, user=user.user, files=user.file_view, title='Profile - Synco', token=token_db)


@synco.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """
    Upload files page
    :return: "upload.html"
    """
    form = FileUploadForm()
    if form.validate_on_submit():
        upload = Upload(form=form)
        return redirect(upload.validate())
    return render_template('upload.html', title='Upload - Synco', form=form)


@synco.route('/user')
@login_required
def users():
    """
    Lists of users page
    :return: "users.html"
    """
    time = datetime
    return render_template('users.html', time=datetime, int=int, title="Members - Synco", users=User.query.all())


@synco.route('/about')
def about():
    """
    About page
    :return: "about.html"
    """
    return render_template('about.html', title="About - Synco")


@synco.route('/lost-password', methods=['GET', 'POST'])
def lost_password():
    """
    Lost password page
    :return: "lost-password.html"
    """
    if current_user.is_authenticated:
        redirect(url_for('user', username=current_user))
    else:
        form = LostPasswordForm()
        if form.validate_on_submit():
            LostPassword(username=form.username.data)
        return render_template("lost-password.html", title="Synco - Reset Password", form=form)


@synco.route('/reset/<token>', methods=['GET', 'POST'])
def reset(token):
    """
    Reset password page.
    :param token: Token mailed at the user's email.
    :return: Error if invalid token else password reset form.
    """
    if current_user.is_authenticated:
        redirect(url_for('user', username=current_user))
    else:
        reset = Reset(token=token)
        reset_check, reset_return = reset.verify()
        if reset_check:
            form = ResetPasswordForm(user=reset_return)
            if form.validate_on_submit():
                redirect(reset.validate(user=reset_return, password=form.password.data))
            return render_template('reset.html', title="Synco - Reset Password", form=form)
        else:
            return redirect(reset_return)


@synco.route('/error/<error>')
def error(error):
    """
    Error display page
    :param error: Type of error.
    :return: "error.html"
    """
    return render_template("error.html", title="Synco - Error!", error=error)


@synco.route('/confirmation/<token>')
def confirmation(token):
    """
    Confirmation account page
    :param token: Token mailed to the registered user's email.
    :return: "confirmation.html" if success else error.
    """
    if current_user.is_authenticated:
        redirect(url_for('user', username=current_user))
    else:
        confirmation = Confirmation(token=token)
        if confirmation.auth != "auth":
            return redirect(confirmation.error())
        else:
            confirmation.confirm()
            return render_template("confirmation.html", title="Synco - Confirmation!")


@synco.route('/avatar', methods=['GET', 'POST'])
@login_required
def avatar():
    """
    Avatar upload page
    :return: "avatar.html"
    """
    form = AvatarUploadForm()
    if form.validate_on_submit():
        avatar = AvatarView(form=form)
        redirect(avatar.validate())
    return render_template('avatar.html', title='Synco - Avatar', form=form)


@synco.route('/document/<token>', methods=['GET', 'POST'])
@login_required
def document(token):
    """
    Document page
    :param token: Token of a specific document
    :return: "document.html"
    """
    form = DocumentForm()
    editor = Editor(token=token)
    if form.validate_on_submit():
        return redirect(editor.validate(data=form.file_data.data))
    form.file_data.data = editor.file_data
    return render_template('document.html', form=form, title='Synco - Document View')


@synco.route('/audio/<token>')
@login_required
def audio(token):
    """
    Audio page
    :param token: Token of a specific audio
    :return: "audio.html"
    """
    files_path = FilesPath()
    file = Token.query.filter_by(token=token).first().file
    user = Token.query.filter_by(token=token).first().auth
    file_name_ext = str(file.id) + files_path.get_ext(file.filename)
    if file.repo == "public":
        file_path = "/static/files/" + str(user.id) + "/public/audio/" + file_name_ext
    elif file.repo == "private":
        file_path = "/static/files/" + str(user.id) + "/private/audio/" + file_name_ext
    return render_template('audio.html', title='Synco - Audio View', src=file_path, file=file)


@synco.route('/video/<token>')
@login_required
def video(token):
    """
    Video page
    :param token: Token of a specific video
    :return: "video.html"
    """
    files_path = FilesPath()
    file = Token.query.filter_by(token=token).first().file
    user = Token.query.filter_by(token=token).first().auth
    file_name_ext = str(file.id) + files_path.get_ext(file.filename)
    if file.repo == "public":
        file_path = "/static/files/" + str(user.id) + "/public/video/" + file_name_ext
    elif file.repo == "private":
        file_path = "/static/files/" + str(user.id) + "/private/video/" + file_name_ext
    return render_template('video.html', title='Synco - Video View', src=file_path, file=file)


@synco.route('/image/<token>')
@login_required
def image(token):
    """
    Image page
    :param token: Token of a specific image
    :return: "image.html"
    """
    files_path = FilesPath()
    file = Token.query.filter_by(token=token).first().file
    user = Token.query.filter_by(token=token).first().auth
    file_name_ext = str(file.id) + files_path.get_ext(file.filename)
    if file.repo == "public":
        file_path = "/static/files/" + str(user.id) + "/public/image/" + file_name_ext
    elif file.repo == "private":
        file_path = "/static/files/" + str(user.id) + "/private/image/" + file_name_ext
    return render_template('image.html', title='Synco - Image View', src=file_path, file=file)
