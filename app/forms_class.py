# General
from app.funcs_class import Tokens, Database, Email, Action, FilesPath
from app.models import User, File, Token, Avatar
from flask import flash, url_for
from flask_login import login_user, current_user
# UserView
from datetime import datetime
# Login
from datetime import timedelta
from werkzeug.urls import url_parse
# Lost Password
from app import public_ip_list
# Upload
from config import Extensions
# Confirmation
from time import time
# Avatar
from os import path


class Register:
    def __init__(self, form=None):
        """
        Processes register form
        :param form: Register form
        """
        # User
        user = User(username=form.username.data.lower(), email=form.email.data.lower())
        user.set_password(form.password.data)
        db = Database()
        db.add(user)

        # Token
        token = Tokens()
        token = token.token
        token_db = Token(token=token, type="confirmation", user_id=user.id)

        # Avatar
        avatar = Avatar(user=user)

        # Commits to Database
        db.add(token_db, avatar)

        # Email
        ip_list = []
        for ip in range(len(public_ip_list)):
            ip_list.append('http://' + public_ip_list[ip] + ':5000' + url_for('confirmation', token=token))
        link = '\n'.join(ip_list)
        ip_list = []

        email = Email(user=user)
        email.confirmation(link=link)

        # Flash
        flash('A confirmation has been sent to your mail. Please verify!')


class Login:
    def __init__(self, form=None):
        """
        Processes login form
        :param form: Login form
        """
        self.form = form

    def login(self, next_page=None):
        """
        Logs in the user
        :param next_page: The page to redirect user after successful login
        :return: "next_page" if user is logged in else "login.html"
        """
        # Username & Password & Confirmation check
        user = User.query.filter_by(username=self.form.username.data.lower()).first() or \
                User.query.filter_by(email=self.form.username.data.lower()).first()
        if user is None or not user.check_password(self.form.password.data):
            flash('Invalid username or password!')
            return url_for('login')
        # Checks for confirmation(Comment out to disable)
        elif user.confirmed is False:
            flash('Please confirm your account before proceeding!')
            return url_for('login')

        # Handles login & Redirecting to the previous page
        login_user(user, remember=self.form.remember_me.data, duration=timedelta(minutes=5))
        # In case, the redirect is either to another domain or none
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return next_page


class UserView:
    def __init__(self, username=None, id=None):
        """
        Processes user profile
        :param username: Username of the user
        :param id: Id of the user
        """
        # Rendering the page
        self.username = username
        self.user = User.query.filter_by(username=self.username.lower()).first_or_404()
        self.file_view = File.query.filter_by(uploader=self.user).all()
        self.file = File.query.filter_by(id=id).first()
        self.timeuser = datetime.utcfromtimestamp(int(self.user.confirmed_on)).strftime('User since: %b %d, %Y')

    def action(self, action=None):
        """
        Processes action to be performed
        :param action: Which action to perform
        :return: Calls the specified action and returns results
        """
        act = Action(user=self.user, file=self.file)
        if action == "download":
            return act.download()
        elif action == "delete":
            return act.delete()
        else:
            return None


class LostPassword:
    def __init__(self, username=None):
        """
        Processes lost password form
        :param username: Username of the user
        """
        self.username = username
        self.user = User.query.filter_by(username=username.lower()).first() or User.\
            query.filter_by(email=username.lower()).first()
        if self.user is None:
            flash("No user or email found!")
        else:
            # Database updating
            token = Tokens()
            token = token.token
            token_db = Token(token=token, type="password", user_id=self.user.id)
            db = Database()
            db.add(token_db)

            # Email
            ip_list = []
            for ip in range(len(public_ip_list)):
                ip_list.append('http://' + public_ip_list[ip] + ':5000' + url_for('reset', token=token))
            link = '\n'.join(ip_list)
            ip_list = []

            email = Email(user=self.user)
            email.pass_reset(link=link)
            flash("Please follow the link in the recovery email!")


class Reset:
    def __init__(self, token=None):
        """
        Processes reset form
        :param token: Token of the reset form to be displayed
        """
        self.token = token
        self.token_db = Token.query.filter_by(token=self.token, type="password").first()
        self.tokens = Tokens(length=0)

    def verify(self):
        """
        Verifies the token
        :return: True of False
        """
        check = self.tokens.auth(token_db=self.token_db)
        if check != "auth":
            return False, url_for("error", error=check)
        else:
            user = self.token_db.auth
            return True, user

    def validate(self, user=None, password=None):
        """
        Validates new password
        :param user: User whose password is to be changed
        :param password: Password to be changed to
        :return: "login.html"
        """
        user.set_password(password)
        db = Database(commit=True)
        flash("Password successfully changed!")
        return url_for('login')


class Upload:
    def __init__(self, form=None):
        """
        Processes the upload form
        :param form: Upload form
        """
        self.form = form

    def validate(self):
        """
        Uploads the file
        :return: "upload.html"
        """
        file_path = FilesPath()

        # Set file model attributes
        file = self.form.file.data
        filename = self.form.filename.data or file.filename
        repo = self.form.repo.data
        ext = file_path.get_ext(filename=filename.lower())

        # Create dir
        if not file_path.isdir():
            file_path.newdir()

        user = User.query.filter_by(username=current_user.username).first()
        file_db = File(filename=filename, repo=repo, uploader=user)

        db = Database()
        db.add(file_db)

        type = None
        ext_list = [Extensions.document_list, Extensions.image_list, Extensions.audio_list, Extensions.video_list]
        if any(ext in ext_check for ext_check in ext_list):
            token = Tokens(length=7)
            filename_save = str(file_db.id) + ext
            if ext in ext_list[0]:
                type = "document"
            elif ext in ext_list[1]:
                type = "image"
            elif ext in ext_list[2]:
                type = "audio"
            elif ext in ext_list[3]:
                type = "video"

            file_db.type = type
            token_db = Token(token=token.token, type=type, auth=user, file=file_db)
            db.add(file_db, token_db)
        else:
            type = "misc"
            filename_save = str(file_db.id)

        if file_db.repo == "public":
            file_db.path = file_path.public(filename=filename_save, type=type)
            db.add(file_db)
            file.save(file_path.public(filename=filename_save, type=type))
        elif file_db.repo == "private":
            file_db.path = file_path.private(filename=filename_save, type=type)
            db.add(file_db)
            file.save(file_path.private(filename=filename_save, type=type))
        flash('File {} uploaded successfully!'.format(file.filename))
        return url_for('upload')


class Confirmation:
    def __init__(self, token):
        """
        Processes confirmation form
        :param token: Token of the form to be processed
        """
        self.token_db = Token.query.filter_by(token=token, type="confirmation").first()
        self.token = Tokens()
        self.auth = self.token.auth(token_db=self.token_db)

    def error(self):
        """
        Redirects to error page with specified error
        :return: "error.html"
        """
        return url_for("error", error=self.auth)

    def confirm(self):
        """
        Confirms the account
        :return: None
        """
        user = self.token_db.auth
        user.confirmed = True
        user.confirmed_on = int(time())
        db = Database()
        db.add(user)


class AvatarView:
    def __init__(self, form=None):
        """
        Processes the avatar form
        :param form: Avatar form
        """
        self.form = form
        self.file_path = FilesPath()

    def validate(self):
        """
        Uploads the avatar
        :return: "avatar.html"
        """
        avatar_db = Avatar.query.filter_by(user=current_user).first()
        avatar = self.form.avatar.data
        avatar_ext = self.file_path.get_ext(filename=avatar.filename)
        if avatar_db is not None:
            avatar_new_name = path.join(self.file_path.files_path_avatar, str(current_user.id) + '_' + str(avatar_db.counter + 1) + avatar_ext)
            avatar_db.avatar = '/static/avatars/' + str(current_user.id) + '_' + str(avatar_db.counter + 1) + avatar_ext
            avatar_db.counter += 1

        else:
            avatar_db = Avatar(avatar='/static/avatars/' + str(current_user.id) + '_1' + avatar_ext
                               , counter=1)
            avatar_new_name = path.join(self.file_path.files_path_avatar,
                                        str(current_user.id) + '_' + str(avatar_db.counter) + avatar_ext)
        #if self.file_path.isfile(repo=None, filename=avatar_new_name):
        #    self.file_path.delfile(repo=None, filename=avatar_new_name)
        avatar.save(avatar_new_name)
        db = Database()
        db.add(avatar_db)
        flash('Successfully uploaded avatar!')
        return url_for('avatar')


class Editor:
    def __init__(self, token=None):
        """
        Processes the document form
        :param token: token of the document to be processed
        """
        self.token = token
        self.token_db = Token.query.filter_by(token=self.token).first()
        self.file = File.query.filter_by(id=self.token_db.file_id).first()
        self.files_path = FilesPath(user=self.token_db.auth)
        self.file_name_ext = str(self.file.id) + self.files_path.get_ext(self.file.filename)
        if self.file.repo == "public":
            file_path = self.files_path.public(type=self.file.type, filename=self.file_name_ext)
            with open(file_path, 'r') as file_file:
                self.file_data = file_file.read()
        elif self.file.repo == "private":
            file_path = self.files_path.private(type=self.file.type, filename=self.file_name_ext)
            with open(file_path, 'r') as file_file:
                self.file_data = file_file.read()

    def validate(self, data=None):
        """
        Updates the document
        :param data: Data to update
        :return: Reloads the same page
        """
        data = data.replace('\n', '')
        if self.file.repo == "public":
            file_path = self.files_path.public(type=self.file.type, filename=self.file_name_ext)
        elif self.file.repo == "private":
            file_path = self.files_path.public(type=self.file.type, filename=self.file_name_ext)
        with open(file_path, 'w') as file_file:
            file_file.write(data)
        return url_for('document', token=self.token)
