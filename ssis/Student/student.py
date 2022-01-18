from flask import Blueprint, render_template, request, flash
from flask_mysqldb import MySQL
import os
from ssis import mysql


student = Blueprint('student', __name__)

@student.route('/student')
def studentRecord():
    return render_template("student.html")