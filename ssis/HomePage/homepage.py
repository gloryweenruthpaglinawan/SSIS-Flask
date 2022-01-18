from flask import Blueprint, render_template, request, flash
from flask_mysqldb import MySQL
import os
from ssis import mysql


homepage= Blueprint('homepage', __name__)

@homepage.route('/')
def home(): 
    return render_template("homepage.html")