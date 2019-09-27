<img src="https://github.com/michal0929/ICoS/users/static_in_users/static_files/static/img/icon.png" >
# Installation
Assuming you use virtualenv, follow these steps to download and run the
ICoS application in this directory:

    $ git clone https://github.com/michal0929/ICoS
    $ cd eLearning
    $ virtualenv venv
    $ source ./venv/bin/activate
    $ pip install -r requirements
    $ python manage.py migrate
    $ python manage.py runserver

# Compatibility
	* Python 2.7
	* Django 1.9
	* SQLite, PostgreSQL, MySQL