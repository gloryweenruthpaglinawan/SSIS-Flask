from flask import Blueprint, render_template, request, flash
from flask_mysqldb import MySQL
import os
from ssis import mysql


search = Blueprint('search', __name__)

@search.route('/studentRecord', methods=['GET', 'POST'])
def studentRecord():
    global idnm, fnm, lnm, gndr, crs, clg, yrl
    
    

    myCursor = mysql.connection.cursor()
    if request.method == 'POST':
        idnm = str(request.form.get('search-student_id'))
        fnm = str(request.form.get('search-first_name'))
        lnm = str(request.form.get('search-last_name'))
        gndr = str(request.form.get('search-gender'))
        crs = str(request.form.get('search-course-code'))
        clg = str(request.form.get('search-college-code'))
        yrl = str(request.form.get('search-year-level'))
        
        if len(idnm) == 0 and len(fnm) == 0 and len(lnm) ==0 and gndr == '' and crs == '' and clg == '' and yrl == '':
            flash("Please enter something to search...", category='error')

        else:       

            myCursor.execute("""SELECT  student_id, first_name, last_name, gender, course_name, year, student.course_code FROM ssis_flask.student
                                        INNER JOIN ssis_flask.course ON course.course_code = student.course_code
                                        INNER JOIN ssis_flask.college ON college.college_code = course.college_code
                                        WHERE student_id LIKE %s AND first_name LIKE %s AND last_name LIKE %s 
                                        AND gender LIKE %s AND student.course_code LIKE %s AND course.college_code LIKE %s AND year LIKE %s;""",
                                        ("%"+str(request.form.get('search-student_id')+"%"),("%"+(request.form.get('search-first_name'))+"%"),("%"+lnm+"%"),("%"+gndr+"%"),("%"+crs+"%"),("%"+clg+"%"),("%"+yrl+"%")))
            student_list = myCursor.fetchall()
            #print(student_list)
            mysql.connection.commit()

            if not student_list:
                flash("No Existing Student Recorded According to your Search Fields (Search Again)", category='error')
        
            myCursor.execute("SELECT course.course_code FROM course")
            courses = myCursor.fetchall()
            myCursor.execute("SELECT college_code FROM college")
            colleges_code= myCursor.fetchall()
            return render_template("search.html", student_list=student_list, colleges_code=colleges_code, courses=courses)


@search.route('/updated_student', methods=['GET', 'POST'])
def updated_student():
    
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

        
        myCursor.execute("""SELECT  student_id, first_name, last_name, gender, course_name, year, student.course_code FROM ssis_flask.student
                                        INNER JOIN ssis_flask.course ON course.course_code = student.course_code
                                        INNER JOIN ssis_flask.college ON college.college_code = course.college_code
                                        WHERE student_id LIKE %s AND first_name LIKE %s AND last_name LIKE %s 
                                        AND gender LIKE %s AND student.course_code LIKE %s AND course.college_code LIKE %s AND year LIKE %s;""",
                                        (("%"+idnm+"%"),("%"+fnm+"%"),("%"+lnm+"%"),("%"+gndr+"%"),("%"+crs+"%"),("%"+clg+"%"),("%"+yrl+"%")))
        student_list = myCursor.fetchall()
        print(student_list)

    return render_template("search.html", student_list=student_list, courses=courses, colleges_code=colleges_code)

@search.route('/delete_student', methods=['GET', 'POST'])
def delete_student():
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
        print("delete -------------------")
        myCursor.execute("DELETE FROM student WHERE student.student_id=%s",
                          (request.form.get('idnum'),))
        mysql.connection.commit()
        flash("Student Successfully Remove", category='success')

        myCursor.execute("""SELECT  student_id, first_name, last_name, gender, course_name, year, student.course_code FROM ssis_flask.student
                                            INNER JOIN ssis_flask.course ON course.course_code = student.course_code
                                            INNER JOIN ssis_flask.college ON college.college_code = course.college_code
                                            WHERE student_id LIKE %s AND first_name LIKE %s AND last_name LIKE %s 
                                            AND gender LIKE %s AND student.course_code LIKE %s AND course.college_code LIKE %s AND year LIKE %s;""",
                                            (("%"+idnm+"%"),("%"+fnm+"%"),("%"+lnm+"%"),("%"+gndr+"%"),("%"+crs+"%"),("%"+clg+"%"),("%"+yrl+"%")))
        student_list = myCursor.fetchall()

        return render_template("search.html", student_list=student_list, courses=courses, colleges_code=colleges_code)

