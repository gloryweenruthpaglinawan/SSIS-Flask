from flask import Blueprint, render_template, request, flash
from flask_mysqldb import MySQL
import os
from ssis import mysql


course = Blueprint('course', __name__)

@course.route('/course')
def courseRecord():
    return render_template("course.html")