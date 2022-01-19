from flask import Blueprint, render_template, request, flash
from flask_mysqldb import MySQL
import os
from ssis import mysql


college = Blueprint('college', __name__)

@college.route('/college')
def collegeRecord():
    myCursor = mysql.connection.cursor()
    myCursor.execute("SELECT college_code, college_name FROM college")
    college= myCursor.fetchall()
    mysql.connection.commit()
    return render_template("colleges.html", college=college)

@college.route('/create_college', methods=['GET', 'POST'])
def create_college():
    myCursor = mysql.connection.cursor()
    if request.method == 'POST':
        college_code= request.form.get('college_code')
        college_name= request.form.get('college_name')

        if len(college_code) == 0:
            flash("Kindly Input College Code", category="error")
        elif len(college_name) == 0:
            flash("Kindly Input College Name", category="error")
        else:
            myCursor.execute("INSERT INTO college(college_code, college_name) VALUES(%s, %s)",(college_code, college_name))
            mysql.connection.commit()

            flash('College Successfully Registered!', category='success')

    return render_template("create_college.html")

@college.route('/update-college', methods=['GET', 'POST'])
def update_college():
    myCursor = mysql.connection.cursor()

    if request.method == 'POST':
        college_name = request.form.get('college-name')
        college_code= request.form.get('college-code')
        
        if len(college_name ) == 0:
            flash("Kindly Input College Name", category='error')

        elif len(college_code) == 0:
            flash("Kindly Input College Name", category='error')

        else:
            myCursor.execute("UPDATE college SET college_code=%s, college_name=%s WHERE college_code=%s", (college_code, college_name, college_code))
            mysql.connection.commit()
            flash("College Name Successfully Updated", category='success')
            myCursor.execute("SELECT college_code, college_name  FROM college")
            college= myCursor .fetchall()
            return render_template("colleges.html", college=college)

@college.route('/delete-college', methods=['GET', 'POST'])
def delete_college():
    myCursor = mysql.connection.cursor()
    
    if request.method == 'POST':
        myCursor.execute("DELETE FROM college WHERE college.college_code=%s", (request.form.get('college-code'),))
        mysql.connection.commit()

        flash("College Successfully Removed!", category='success')
        myCursor.execute("SELECT college_code, college_name FROM college")
        college= myCursor.fetchall()
        return render_template("colleges.html", college=college)
