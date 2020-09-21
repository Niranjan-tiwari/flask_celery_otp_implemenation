**Installation**
* Clone repo :
> git clone https://gitlab.com/monkEsh/flask-celery-otp.git

* Install requirements.txt : 
> pip install -r requirements.txt 

* Start celery worker: 
> celery worker -A otp_auth.celery --loglevel=info 

* Start Application: 
> python otp_auth.py

**Reference**
1. http://flask.pocoo.org/docs/0.12/patterns/celery/
2. https://blog.miguelgrinberg.com/post/using-celery-with-flask
