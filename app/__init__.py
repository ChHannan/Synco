from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from subprocess import check_output

synco = Flask(__name__)
synco.config.from_object(Config)

# Get all public IPs
public_ip = check_output('ipconfig')
print(" * Listening to following public IPs:")
public_ip_list = []
for counter in public_ip.decode().split("IPv4 Address"):
    if '.' is counter[0]:
        ip = counter[counter.find(':')+2:counter.find('\r')]
        public_ip_list.append(ip)
        print('\t', ip)

db = SQLAlchemy(synco)

migrate = Migrate(synco, db)

login = LoginManager(synco)
login.login_view = 'login'

from app import routes, models
