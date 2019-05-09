# Synco - Share your files the Synco way!
Synco is an intranet file sharing server based on Python's web framework - Flask. It addresses the problem 
of file sharing over LAN by removing the need of any third-party app or configuration once the server has 
been installed and set running. Synco is multi-platform, some files such as audio, video can be played
right in the browser, documents can be edited on the go and more!
	
# Core features of Synco
* Ease of sharing
	* No configuration on user end
	* No third-party apps
* Multi-platform
	* Built for mobile first using bootstrap
* Realtime access to data
	* Play audio/video right in the browser
	* Edit documents on the go
	* View images
	
# Setting up Synco
Synco is built using on the following version of python:

	$ python
	Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 27 2018, 04:06:47) [MSC v.1914 32 bit (Intel)] on win32
	Type "help", "copyright", "credits" or "license" for more information.

Following version of flask is installed:

	$ pip install flask
	$ flask --version
	Flask 1.0.2

Following extensions are required and can be installed by pip:
	
	$ pip install flask-wtf
	$ pip install flask-sqlalchemy
	$ pip install flask-migrate
	$ pip install flask-login
	
That's it!
Now head over to cmd, change the directory to Synco and run the following command:

	$ flask run --host=0.0.0.0

# Contact us!
Join our group to become part of a small but growing programmer's community!
https://www.facebook.com/groups/509008306285106/

# License
Synco is open-source. Anyone can modify it and use it but a link to this git repository must be added in any thing Synco is used.
