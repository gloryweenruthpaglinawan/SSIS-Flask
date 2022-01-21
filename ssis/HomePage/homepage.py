from flask import Blueprint, render_template, request, flash
from flask_mysqldb import MySQL
import os
from ssis import mysql


homepage= Blueprint('homepage', __name__)

@homepage.route('/')
def home(): 
    myCursor = mysql.connection.cursor()
    myCursor.execute("SELECT college_code FROM college")
    colleges_code= myCursor.fetchall()

    myCursor.execute("SELECT course_code FROM course")
    courses = myCursor.fetchall()
    mysql.connection.commit()
    
    return render_template("homepage.html", colleges_code=colleges_code, courses=courses)