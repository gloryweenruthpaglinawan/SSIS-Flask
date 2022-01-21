from flask import Flask
from flask_mysqldb import MySQL
from flask_mysql_connector import MySQL
from config import host, user, database, password, secret_key
mysql = MySQL()

print(database)

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=secret_key,
        MYSQL_HOST=host,
        MYSQL_DATABASE=database,
        MYSQL_USER=user,
        MYSQL_PASSWORD=password,
    )


    mysql.init_app(app)

    from .College.college import college as college
    from .Student.student import student as student
    from .Course.course import course as course
    from .HomePage.homepage import homepage as homepage
    from .HomePage.search import search as search

    app.register_blueprint(college, url_prefix='/')
    app.register_blueprint(student, url_prefix='/')
    app.register_blueprint(course, url_prefix='/')
    app.register_blueprint(homepage, url_prefix='/')
    app.register_blueprint(search, url_prefix='/')
    return app 