from flask import Blueprint, render_template, request, flash
from flask_mysqldb import MySQL
import os
from ssis import mysql


student = Blueprint('student', __name__)

@student.route('/student')
def studentRecord():
    myCursor = mysql.connection.cursor()
    myCursor.execute("""SELECT student.student_id, student.first_name, student.last_name, student.gender, course.course_name, student.year,course.course_code FROM course
                             INNER JOIN student ON student.course_code = course.course_code""")
    student_list = myCursor.fetchall()

    myCursor.execute("SELECT course.course_code FROM course")
    courses = myCursor.fetchall()
    myCursor = mysql.connection.cursor()
    myCursor.execute("SELECT college_code FROM college")
    colleges_code= myCursor.fetchall()
    
    return render_template("student.html", student_list=student_list, colleges_code=colleges_code, courses=courses)

@student.route('/add_student', methods=['GET', 'POST'])
def add_student():
    myCursor= mysql.connection.cursor()

    myCursor.execute("SELECT course_code FROM course")
    courses = myCursor.fetchall()
    mysql.connection.commit()

    myCursor = mysql.connection.cursor()
    myCursor.execute("SELECT college_code FROM college")
    colleges_code= myCursor.fetchall()

    if request.method == 'POST':

        fname = request.form.get('first_name')
        lname = request.form.get('last_name')
        idnum = request.form.get('student_id')
        course = request.form.get('course-code')
        yrlvl = request.form.get('year-level')
        gender = request.form.get('gender')

        
        if len(fname) == 0:
            flash('Please Complete the Name', category='error')
        elif len(lname) == 0:
            flash('Please Complete the Name', category='error')
        elif len(idnum) == 0:
            flash('Please Input an ID Number', category='error')
        elif course == None:
            flash('Please Select Course', category='error')
        elif yrlvl == None:
            flash('Please Select Year Level', category='error')
        elif gender == None:
            flash('Please Select Gender', category='error')
        else:
            myCursor.execute("INSERT INTO student(student_id, first_name, last_name, gender, course_code, year) "
                              "VALUES(%s, %s, %s, %s, %s, %s)", (idnum, fname, lname, gender, course, yrlvl))
            mysql.connection.commit()

            flash('Student Successfully Registered', category='success')

    return render_template("add_student.html", courses=courses, colleges_code=colleges_code)

@student.route('/updated_students', methods=['GET', 'POST'])
def updated_students():
    myCursor = mysql.connection.cursor()
    myCursor.execute("SELECT course_code FROM course")
    courses = myCursor.fetchall()
    mysql.connection.commit()

    myCursor = mysql.connection.cursor()
    myCursor.execute("SELECT college_code FROM college")
    colleges_code= myCursor.fetchall()

    if request.method == 'POST':
        fname = request.form.get('first_name')
        lname = request.form.get('last_name')
        idnum = request.form.get('student_id')
        course = request.form.get('course-code')
        yrlvl = request.form.get('year-level')
        gender = request.form.get('gender')


        if len(fname) == 0:
            flash('Please Complete the Name', category='error')
        elif len(lname) == 0:
            flash('Please Complete the Name', category='error')
        elif courses == None:
            flash('Please Select Course', category='error')
        elif yrlvl == None:
            flash('Please Select Year Level', category='error')
        elif gender == None:
            flash('Please Select Gender', category='error')
        else:
            myCursor.execute("UPDATE student SET student.first_name=%s, student.last_name=%s, student.gender=%s, student.course_code=%s, student.year=%s WHERE student.student_id=%s",
                (fname, lname, gender, course, yrlvl, idnum))
            mysql.connection.commit()

            flash("Student Successfully Updated", category='success')


    myCursor.execute("""SELECT student.student_id, student.first_name, student.last_name, student.gender, course.course_name, student.year, course.course_code FROM course
                                               INNER JOIN student ON student.course_code = course.course_code""")
    student_list = myCursor.fetchall()

    return render_template("student.html", student_list=student_list, courses=courses, colleges_code=colleges_code)

@student.route('/delete_students', methods=['GET', 'POST'])
def delete_students():
    myCursor = mysql.connection.cursor()
    myCursor.execute("SELECT course.course_code FROM course")
    courses= myCursor.fetchall()
    mysql.connection.commit()

    myCursor = mysql.connection.cursor()
    myCursor.execute("SELECT college_code FROM college")
    colleges_code= myCursor.fetchall()

    if request.method == 'POST':
        idn = request.form.get('idnum')

        print(idn)
        myCursor.execute("DELETE FROM student WHERE student.student_id=%s",
                          (request.form.get('idnum'),))
        mysql.connection.commit()
        flash("Student Successfully Remove", category='success')

    myCursor.execute("""SELECT student.student_id, student.first_name, student.last_name, student.gender, course.course_name, student.year, course.course_code FROM course
                                        INNER JOIN student ON student.course_code = course.course_code""")
    student_list = myCursor.fetchall()

    return render_template("student.html", student_list=student_list, courses=courses, colleges_code=colleges_code)

