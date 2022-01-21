from flask import Blueprint, render_template, request, flash
from flask_mysqldb import MySQL
import os
from ssis import mysql


course = Blueprint('course', __name__)

@course.route('/course')
def courseRecord():
    myCursor = mysql.connection.cursor()
    myCursor.execute("""SELECT course.course_code, course.course_name, college.college_name, college.college_code FROM college INNER JOIN course ON course.college_code = college.college_code""")
    course_list = myCursor.fetchall()

    myCursor.execute("SELECT college_code FROM college")
    colleges_code= myCursor.fetchall()

    myCursor.execute("SELECT course_code FROM course")
    courses = myCursor.fetchall()
    mysql.connection.commit()
    return render_template("course.html", course_list=course_list, colleges_code=colleges_code, courses=courses ) 

@course.route('/create_course', methods=['GET', 'POST'])
def create_course():
    myCursor = mysql.connection.cursor()
    myCursor.execute("SELECT college_code FROM college")
    colleges_code= myCursor.fetchall()

    myCursor.execute("SELECT course_code FROM course")
    courses = myCursor.fetchall()
    mysql.connection.commit()

    if request.method == 'POST':

        course_code = request.form.get('course_code')
        course_name = request.form.get('course_name')
        college_code = request.form.get('college-code')

        if len(course_code) < 1:
            flash('Please Input Course Code', category='error')
        elif len(course_name) < 1:
            flash('Please Input Course Name', category='error')
        elif college_code == "Select College":
            flash('Please Select College', category='error')
        else:
            myCursor.execute("INSERT INTO course(course_code, course_name, college_code) VALUES(%s, %s, %s)", (course_code, course_name, college_code))
            mysql.connection.commit()
            flash('Course Successfully Register', category='success')

    return render_template("create_course.html", colleges_code=colleges_code, courses=courses)

@course.route('/updated_course', methods=['GET', 'POST'])
def updated_course():
    myCursor = mysql.connection.cursor()
    
    myCursor.execute("SELECT college_code FROM college")
    college = myCursor.fetchall()
    mysql.connection.commit()

    myCursor.execute("SELECT course_code FROM course")
    courses = myCursor.fetchall()
    mysql.connection.commit()

    if request.method =='POST':
        course_code=request.form.get('course-code')
        course_name=request.form.get('course-name')
        college_code=request.form.get('college-code')

        if len(course_name) == 0:
            flash("Please Input Course Name", category='error')
        elif college_code == None:
            flash("Please Select College", category='error')
        else:
            myCursor.execute("UPDATE course SET course.course_code=%s, course.course_name=%s, course.college_code=%s WHERE course.course_code=%s", (course_code, course_name, college_code, course_code))
            flash("Course Successfully Updated",category='success')
            mysql.connection.commit()

        myCursor.execute("""SELECT course.course_code, course.course_name, college.college_name, college.college_code FROM college INNER JOIN course ON course.college_code = college.college_code""")
        course_list = myCursor.fetchall()

        return render_template('course.html', college=college, course_list=course_list, courses=courses)

@course.route('/delete_course', methods=['GET', 'POST'])
def delete_course():
    myCursor = mysql.connection.cursor()
    myCursor.execute("SELECT college_code FROM college")
    college = myCursor.fetchall()

    myCursor.execute("SELECT course_code FROM course")
    courses = myCursor.fetchall()
    mysql.connection.commit()

    if request.method == 'POST':
       myCursor.execute("DELETE FROM course WHERE course.course_code=%s", (request.form.get('course-code'),))

       flash("Course Successfully Remove", category='success')
       mysql.connection.commit()

    myCursor.execute("""SELECT course.course_code, course.course_name, college.college_name, college.college_code FROM college INNER JOIN course ON course.college_code = college.college_code""")
    course_list = myCursor.fetchall()
    mysql.connection.commit()

    return render_template("course.html", college=college, course_list=course_list, courses=courses)
    