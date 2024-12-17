import os
from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
import sqlite3
import bcrypt
import random
import string
import io
import base64
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from functools import wraps
import math
import csv
import pickle
from sklearn.preprocessing import LabelEncoder

matplotlib.use('Agg')  # Use a non-GUI backend

app = Flask(__name__)
app.secret_key = 'secret_key'


# Database setup functions
def create_user_table():
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            account_type TEXT,
            password TEXT NOT NULL,
            BusinessSector TEXT,
            userPhoto BLOB
        )
    ''')
    connection.commit()
    connection.close()


def create_combined_table():
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS CombinedTable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            BusinessSector TEXT,
            BusinessFunction TEXT,
            MeasuringElt TEXT,
            Rating INTEGER,
            SUbCategory TEXT,
            AsIsQuestions TEXT,
            ToBeQuestions TEXT,
            MaxRating INTEGER
        )
    ''')
    connection.commit()
    connection.close()


def create_value_chain_table():
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ValueChain (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            BusinessSector TEXT,
            BusinessFunction TEXT,
            BusinessProcess TEXT,
            BusinessActivities,
            Technology TEXT,
            Skills TEXT
        )
    ''')
    connection.commit()
    connection.close()


def create_forgot_password_table():
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ForgotPassword (
            email TEXT UNIQUE NOT NULL
        )
    ''')
    connection.commit()
    connection.close()


def create_trimmed_table():
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ArrangingTheDataInProperOrder (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            BusinessSector TEXT,
            BusinessFunction TEXT,
            MeasuringElt TEXT,
            Rating INTEGER,
            SUbCategory TEXT,
            AsIsQuestions TEXT,
            ToBeQuestions TEXT,
            MaxRating INTEGER,
            AnswerRating TEXT,
            AnswerRatingValue INTEGER
        )
    ''')
    connection.commit()
    connection.close()


def create_answer_rating_table():
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS AnswerRatings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            BusinessFunction TEXT,
            RatingName TEXT,
            RatingDescription TEXT,
            AnswerRatingValue INTEGER
        )
    ''')
    connection.commit()
    connection.close()


def create_user_submission_record_table():
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UserSubmissionRecord (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            UniqueCodeUser TEXT,
            BusinessFunction TEXT,
            MeasuringEltUser TEXT,
            RatingUser INTEGER,
            SUbCategoryUser TEXT,
            AsIsQuestionsUser TEXT,
            AnswersUserAsIs TEXT,
            ToBeQuestionsUser TEXT,
            AnswersUserToBe TEXT,
            MaxRatingUser INTEGER DEFAULT 5,
            ExpectedCumSum INTEGER,
            UserCumSumAsIs INTEGER,
            UserCumSumToBe INTEGER
        )
    ''')
    connection.commit()
    connection.close()


def create_type_of_maturity_table():
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TypeOfDigitalMaturity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            BusinessSector TEXT,
            UniqueCodeUser TEXT,
            DigitalMaturityType TEXT,
            BusinessFunction TEXT,
            MaturityAsIs INTEGER,
            MaturityToBe INTEGER
        )
    ''')
    connection.commit()
    connection.close()


def create_final_feedback_data():
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS UserSubmittedFeedback (
            UniqueCodeUser TEXT,
            BusinessFunction TEXT,  
            MeasuringEltUser TEXT,
            RatingUser INTEGER,
            SUbCategoryUser TEXT,
            AnswersUserAsIs TEXT,
            AnswersUserToBe TEXT,   
            MaxRatingUser INTEGER DEFAULT 5,
            ExpectedCumSum INTEGER,
            UserCumSumAsIs INTEGER,
            UserCumSumToBe INTEGER,
            PercentageAsIs INTEGER,
            PercentageToBe INTEGER,
            FeedbackAsIs TEXT,
            FeedbackToBe TEXT,
            GrowthRate INTEGER,
            Duration INTEGER
        )
    ''')
    connection.commit()
    connection.close()


# Create tables
create_user_table()
create_combined_table()
create_trimmed_table()
create_answer_rating_table()
create_user_submission_record_table()
create_final_feedback_data()
create_forgot_password_table()
create_value_chain_table()
create_type_of_maturity_table()


# Utility functions
def get_unique_business_sectors():
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute(
        'SELECT DISTINCT BusinessSector FROM ArrangingTheDataInProperOrder')
    business_sectors = cursor.fetchall()
    connection.close()
    return business_sectors


def get_the_different_answer_rating_for_sector(selected_sector):
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute('SELECT RatingName, RatingDescription, AnswerRatingValue FROM AnswerRatings WHERE BusinessFunction=?',
                   (selected_sector,))
    business_sectors_rating = cursor.fetchall()
    connection.close()
    return business_sectors_rating


def get_answer_rating_column_names():
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute('PRAGMA table_info(AnswerRatings)')
    columns = cursor.fetchall()
    connection.close()
    return [col[1] for col in columns]


def add_random_characters(word, num_chars=12):
    def generate_random_string(length):
        letters = string.ascii_letters
        return ''.join(random.choice(letters) for _ in range(length))

    return word + generate_random_string(num_chars)


# Decorator for login-required routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('You need to login first.')
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    session.pop('email', None)
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    # Get business sectors for dropdown
    business_sectors = get_unique_business_sectors()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        account_type = request.form['users']
        user_photo = request.files['User_photo']
        # Retrieve BusinessSector
        business_sector = request.form['business_sector']

        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match', business_sectors=business_sectors)

        connection = sqlite3.connect('DigitalMaturityDatabase.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM User WHERE email=?', (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            connection.close()
            return render_template('register.html', error='User with this email already exists',
                                   business_sectors=business_sectors)

        hashed_password = bcrypt.hashpw(password.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Read the photo data and convert it to binary
        user_photo_data = user_photo.read()

        cursor.execute(
            'INSERT INTO User (name, email, password, account_type, BusinessSector, userPhoto) VALUES (?, ?, ?, ?, ?, ?)',
            (name, email, hashed_password, account_type, business_sector,
             user_photo_data))  # Insert BusinessSector
        connection.commit()
        connection.close()

        return redirect('/login')

    return render_template('register.html', business_sectors=business_sectors)


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Fetch business sectors for dropdown
    business_sectors = get_unique_business_sectors()

    if request.method == 'POST':
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        account_type = request.form.get('users', None)
        # Retrieve selected business sector
        business_sector = request.form.get('business_sector', None)

        if not email or not password or not account_type or (account_type != "Administrator" and not business_sector):
            error_message = "Please fill in all the required fields."
            return render_template('login.html', error=error_message, business_sectors=business_sectors)

        connection = sqlite3.connect('DigitalMaturityDatabase.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM User WHERE email=?', (email,))
        user = cursor.fetchone()
        connection.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[4].encode('utf-8')) and user[3] == account_type:
            # Check if the account type is either Business Manager or Business Analyst
            if account_type in ["Business Manager", "Business Analyst"]:
                # Verify that the selected business sector matches the one in the database
                # Assuming user[5] is the BusinessSector column
                if business_sector != user[5]:
                    error_message = "You have selected the wrong business sector for this account."
                    return render_template('login.html', error=error_message, business_sectors=business_sectors)

            session['email'] = user[2]
            session['logged_in'] = True
            session['account_type'] = account_type  # Store the account type
            # Store the business sector in the session
            session['business_sector'] = business_sector
            if account_type == "Administrator":
                return redirect('/administrator')
            elif account_type == "Business Manager":
                return redirect('/BusinessManager')
            elif account_type == "Business Analyst":
                return redirect('/BusinessAnalysts')
        else:
            error_message = "Invalid credentials. Please make sure to enter the correct email, password, and account type."
            return render_template('login.html', error=error_message, business_sectors=business_sectors)

    return render_template('login.html', business_sectors=business_sectors)


# BusinessAnalyst
@app.route('/BusinessAnalysts')
@login_required
def dashboardBusinessAnalysts():
    # Get the business sector from the session
    selected_business_sector = session.get('business_sector', None)
    business_functions = []
    business_sector_rating = []

    if session.get('email') and selected_business_sector:
        connection = sqlite3.connect('DigitalMaturityDatabase.db')
        cursor = connection.cursor()

        # Fetch distinct business functions for the stored sector
        cursor.execute('''
            SELECT DISTINCT BusinessFunction 
            FROM ArrangingTheDataInProperOrder 
            WHERE BusinessSector=?
        ''', (selected_business_sector,))

        business_functions = [row[0] for row in cursor.fetchall()]
        connection.close()

        business_sector_rating = get_the_different_answer_rating_for_sector(
            selected_business_sector)
        # Store in session
        session['business_sector_rating'] = business_sector_rating

    return render_template('BusinessAnalyst.html', business_functions=business_functions, business_sector_rating=business_sector_rating)


@app.route('/select_business_function_in_business_function_html_page', methods=['GET', 'POST'])
def select_business_function():
    business_function_selected_data = []
    business_sector_rating = []
    answer_rating_columns = []
    user_photo_base64 = None
    user = None
    SectorError = ""

    if request.method == 'POST':
        selected_business_function = request.form.get(
            'business_function_user', None)

        if selected_business_function:
            connection = sqlite3.connect('DigitalMaturityDatabase.db')
            cursor = connection.cursor()
            cursor.execute('''
                SELECT DISTINCT MeasuringElt, Rating, SUbCategory, AsIsQuestions, ToBeQuestions, MaxRating
                FROM ArrangingTheDataInProperOrder
                WHERE BusinessFunction=?
            ''', (selected_business_function,))
            business_function_selected_data = cursor.fetchall()
            connection.close()

            answer_rating_columns = get_answer_rating_column_names()
            business_sector_rating = session.get('business_sector_rating', [])
            # Store selected business function in session
            session['selected_business_function'] = selected_business_function

            return render_template('AsIsandToBeQuestionandAnswer.html', user=user, user_photo_base64=user_photo_base64,
                                   business_function_selected_data=business_function_selected_data,
                                   SectorError=SectorError, business_sector_rating=business_sector_rating,
                                   answer_rating_columns=answer_rating_columns)
        else:
            SectorError = "You did not select a business function. Now you have to start all over again"

    return render_template('BusinessAnalyst.html', user=user, user_photo_base64=user_photo_base64,
                           SectorError=SectorError, business_function_selected_data=business_function_selected_data,
                           business_sector_rating=business_sector_rating, answer_rating_columns=answer_rating_columns)


# Utility functions
def get_unique_business_functions_for_administrator(business_sector):
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT DISTINCT BusinessFunction 
        FROM ArrangingTheDataInProperOrder 
        WHERE BusinessSector=?
    ''', (business_sector,))
    business_functions = cursor.fetchall()
    connection.close()
    return business_functions


# Administrator
@app.route('/administrator')
@login_required
def dashboardAdministrator():
    if session.get('email'):
        connection = sqlite3.connect('DigitalMaturityDatabase.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM User WHERE email=?', (session['email'],))
        user = cursor.fetchone()
        connection.close()

        return render_template('administrator.html', user=user)

    return redirect('/login')


@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    Password_error = None  # Initialize Password_error

    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['newpassword']
        confirm_new_password = request.form['confnewpassword']

        if new_password != confirm_new_password:
            Password_error = 'Passwords do not match'
            return render_template('administrator.html', Password_error=Password_error)

        connection = sqlite3.connect('DigitalMaturityDatabase.db')
        cursor = connection.cursor()

        # Check if the email exists in the database
        cursor.execute('SELECT * FROM User WHERE email=?', (email,))
        user = cursor.fetchone()

        if user:
            hashed_password = bcrypt.hashpw(new_password.encode(
                'utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute(
                'UPDATE User SET password=? WHERE email=?', (hashed_password, email))
            connection.commit()
            connection.close()
            Password_error = "Password updated successfully"
            time.sleep(5)
        else:
            Password_error = "Email does not exist"
            time.sleep(5)
            connection.close()

    return render_template('administrator.html', Password_error=Password_error)


@app.route('/requestPasswordChange', methods=['GET', 'POST'])
def PasswordChange():
    if request.method == 'POST':
        emailReset = request.form['password_reset']

        connection = sqlite3.connect('DigitalMaturityDatabase.db')
        cursor = connection.cursor()

        # Check if the email exists in the database
        cursor.execute('SELECT * FROM User WHERE email=?', (emailReset,))
        user = cursor.fetchone()

        if user:
            cursor.execute('''
                INSERT INTO ForgotPassword (email)
                VALUES (?)
            ''', (emailReset,))
            connection.commit()
            connection.close()
            requestMessage = "Your request has been received. Wait for an administrator to email your new password credentials."
        else:
            requestMessage = "Email does not exist"
            connection.close()

        # Adding a delay
        import time
        time.sleep(5)

        return redirect(url_for('PasswordChange', requestMessage=requestMessage))

    requestMessage = request.args.get('requestMessage')
    return render_template('ForgotPassword.html', requestMessage=requestMessage)


# BusinessManager
@app.route('/BusinessManager')
@login_required
def dashboardBusinessManager():
    business_functions_data = {}
    business_functions = []
    if session.get('email'):
        connection = sqlite3.connect('DigitalMaturityDatabase.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM User WHERE email=?', (session['email'],))
        user = cursor.fetchone()
        connection.close()

        # Get the business sector from the session
        selected_business_sector = session.get('business_sector', None)

        # Get business functions for the logged-in user's business sector
        if selected_business_sector:
            business_functions = get_unique_business_functions_for_administrator(
                selected_business_sector)

        return render_template('manager.html', user=user, business_data=business_functions_data, business_functions=business_functions)

    return redirect('/login')


# Displaying the elements in the database on the admin side of the panel
@app.route('/view_combined_data', methods=['GET', 'POST'])
@login_required
def view_combined_data():
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id, BusinessSector, BusinessFunction, MeasuringElt, Rating, SUbCategory, AsIsQuestions, ToBeQuestions, MaxRating
        FROM CombinedTable
    ''')
    combined_data = cursor.fetchall()

    # Normalize the BusinessFunction column
    normalize_business_function()

    cursor.execute(
        'SELECT DISTINCT BusinessFunction FROM ArrangingTheDataInProperOrder')
    unique_business_functions = cursor.fetchall()

    connection.close()

    return render_template('administrator.html', combined_data=combined_data,
                           unique_business_functions=unique_business_functions)


# Uploading CSV file to database
def normalize_business_function():
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()

    # Clear existing data in ArrangingTheDataInProperOrder table to prevent duplication
    cursor.execute('DELETE FROM ArrangingTheDataInProperOrder')

    cursor.execute('''
        WITH RECURSIVE split(id, BusinessSector, BusinessFunction, MeasuringElt, Rating, SUbCategory, AsIsQuestions, ToBeQuestions, MaxRating, value, rest) AS (
            SELECT
                id,
                BusinessSector,
                BusinessFunction,
                MeasuringElt,
                Rating,
                SUbCategory,
                AsIsQuestions,
                ToBeQuestions,
                MaxRating,
                TRIM(SUBSTR(BusinessFunction || ',', 1, INSTR(BusinessFunction || ',', ',') - 1)),
                TRIM(SUBSTR(BusinessFunction || ',', INSTR(BusinessFunction || ',', ',') + 1))
            FROM CombinedTable
            UNION ALL
            SELECT
                id,
                BusinessSector,
                BusinessFunction,
                MeasuringElt,
                Rating,
                SUbCategory,
                AsIsQuestions,
                ToBeQuestions,
                MaxRating,
                TRIM(SUBSTR(rest, 1, INSTR(rest, ',') - 1)),
                TRIM(SUBSTR(rest, INSTR(rest, ',') + 1))
            FROM split
            WHERE rest != ''
        )
        INSERT INTO ArrangingTheDataInProperOrder (
            BusinessSector, BusinessFunction, MeasuringElt, Rating, SUbCategory, 
            AsIsQuestions, ToBeQuestions, MaxRating
        )
        SELECT
            BusinessSector, value, MeasuringElt, Rating, SUbCategory, 
            AsIsQuestions, ToBeQuestions, MaxRating
        FROM split
        WHERE value IS NOT NULL AND value != ''
    ''')

    connection.commit()
    connection.close()


@app.route('/upload_csv', methods=['GET', 'POST'])
def upload_file():
    unique_business_functions = []
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            # Process CSV file and insert into database
            process_csv(file)

            # Normalize the BusinessFunction column
            normalize_business_function()

            # Fetch unique business functions
            connection = sqlite3.connect('DigitalMaturityDatabase.db')
            cursor = connection.cursor()
            cursor.execute(
                'SELECT DISTINCT BusinessFunction FROM ArrangingTheDataInProperOrder')
            unique_business_functions = cursor.fetchall()
            connection.close()

            # Redirect to view data
            return redirect(url_for('view_combined_data'))

    # Fetch unique business functions for GET request
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute(
        'SELECT DISTINCT BusinessFunction FROM ArrangingTheDataInProperOrder')
    unique_business_functions = cursor.fetchall()
    connection.close()

    return render_template('administrator.html', unique_business_functions=unique_business_functions)


def process_csv(csv_file):
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()

    # Convert file object to text mode
    csv_text = csv_file.stream.read().decode("utf-8")
    csv_data = csv.reader(csv_text.splitlines())

    next(csv_data)  # Skip header row if present
    for row in csv_data:
        if len(row) != 9:
            raise ValueError("CSV file must have exactly 9 columns")

        id, business_sector, business_function, measuring_elt, rating, sub_category, AsIsQuestions, ToBeQuestions, max_rating = row

        # Dynamically generate the as_is_question and to_be_question
        as_is_question = f"How will you best describe your {
            sub_category} procedure?"
        to_be_question = f"Where would you want to find {
            sub_category} procedure in the future?"

        cursor.execute('''
            INSERT INTO CombinedTable (id, BusinessSector, BusinessFunction, MeasuringElt, Rating, SUbCategory, AsIsQuestions, ToBeQuestions, MaxRating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (id, business_sector, business_function, measuring_elt, rating, sub_category, as_is_question,
              to_be_question, max_rating))

    connection.commit()
    connection.close()


@app.route('/delete_combined_data', methods=['POST'])
@login_required
def delete_combined_data():
    if request.method == 'POST':
        # Get the ID of the record to delete from the form
        delete_record_id = request.form['record_id']
        try:
            # Delete the record from the database
            connection = sqlite3.connect('DigitalMaturityDatabase.db')
            cursor = connection.cursor()
            cursor.execute('''
                DELETE FROM CombinedTable
                WHERE id = ?
            ''', (delete_record_id,))
            connection.commit()
            connection.close()

            # Redirect back to the page displaying combined data
            return redirect('/view_combined_data')
        except Exception as e:
            return "Error occurred during deletion: " + str(e)
    else:
        return "Method Not Allowed"


# Adding individual data into database
@app.route('/CombinedTiersForAll', methods=['GET', 'POST'])
@login_required
def CombinedTiers():
    if request.method == 'POST':
        business_sector_name = request.form['business_sector_name']
        business_function_name = request.form['business_function']
        measuring_element_name = request.form['Measuring_Element']
        rating = request.form['Rating']
        subCategory_name = request.form['subCategory_name']

        # Dynamically generate the as_is_question and to_be_question
        as_is_question = f"How will you best describe your {
            subCategory_name} procedure?"
        to_be_question = f"Where would you want to find {
            subCategory_name} procedure in the future?"

        MaxRating = request.form['MaxRating']

        connection = sqlite3.connect('DigitalMaturityDatabase.db')
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO CombinedTable (BusinessSector, BusinessFunction, MeasuringElt, Rating, SUbCategory, AsIsQuestions, ToBeQuestions, MaxRating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (business_sector_name, business_function_name, measuring_element_name, rating, subCategory_name,
              as_is_question, to_be_question, MaxRating))
        connection.commit()
        connection.close()

        # Normalize the BusinessFunction column
        normalize_business_function()

        return redirect('/CombinedTiersForAll')

    return render_template('administrator.html')


# Updating the combined tiers
@app.route('/UpdateCombinedTiersForAll', methods=['GET', 'POST'])
@login_required
def UpdateCombinedTiers():
    if request.method == 'POST':
        # Extract old values from the form
        oldbusiness_sector_name = request.form['oldbusiness_sector_name']
        oldbusiness_function = request.form['oldbusiness_function']
        oldmeasuring_element_name = request.form['oldMeasuring_Element']
        oldrating = request.form['oldRating']
        oldsubCategory_name = request.form['oldsubCategory_name']
        oldMaxRating = request.form['oldMaxRating']

        # Extract new values from the form
        newbusiness_sector_name = request.form['newbusiness_sector_name']
        newbusiness_function = request.form['newbusiness_function']
        newmeasuring_element_name = request.form['newMeasuring_Element']
        newrating = request.form['newRating']
        newsubCategory_name = request.form['newsubCategory_name']
        newMaxRating = request.form['newMaxRating']

        # Connect to the database
        connection = sqlite3.connect('DigitalMaturityDatabase.db')
        cursor = connection.cursor()

        # Execute the SQL update query
        cursor.execute('''
            UPDATE CombinedTable 
            SET BusinessSector=?, BusinessFunction=?, MeasuringElt=?, Rating=?, SUbCategory=?, MaxRating=?
            WHERE BusinessSector=? AND BusinessFunction=? AND MeasuringElt=? AND Rating=? AND SUbCategory=? AND MaxRating=?
        ''', (newbusiness_sector_name, newbusiness_function, newmeasuring_element_name, newrating, newsubCategory_name,
              newMaxRating,
              oldbusiness_sector_name, oldbusiness_function, oldmeasuring_element_name, oldrating, oldsubCategory_name,
              oldMaxRating))

        # Commit changes and close connection
        connection.commit()
        connection.close()

        # Redirect back to administrator page
        return redirect('/administrator')

    return render_template('administrator.html')


@app.route('/ratingAnswersBusinessFunctions', methods=['GET', 'POST'])
@login_required
def answerratingforbusinesssector():
    if request.method == 'POST':
        business_sector_name = request.form['rating_business_sector_name']
        business_name_business_sector = request.form['rating_name_business_sector']
        description_name_business_sector = request.form['rating_description_business_sector']
        rating_value_business_sector = request.form['rating_value_business_sector']

        connection = sqlite3.connect('DigitalMaturityDatabase.db')
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO AnswerRatings (BusinessFunction, RatingName, RatingDescription, AnswerRatingValue)
            VALUES (?, ?, ?, ?)
        ''', (business_sector_name, business_name_business_sector, description_name_business_sector,
              rating_value_business_sector))
        connection.commit()
        connection.close()

        # Normalize the BusinessFunction column
        normalize_business_function()

        return redirect('/CombinedTiersForAll')

    return render_template('administrator.html')


# Updating the combined tiers
@app.route('/updateratingAnswersBusinessFunctions', methods=['GET', 'POST'])
@login_required
def Updateanswerrating():
    if request.method == 'POST':
        # Extract values from the form
        business_sector_name = request.form['rating_business_sector_name']
        business_name_business_sector = request.form['rating_name_business_sector']
        description_name_business_sector = request.form['newrating_description_business_sector']
        rating_value_business_sector = request.form['newrating_value_business_sector']

        # Connect to the database
        connection = sqlite3.connect('DigitalMaturityDatabase.db')
        cursor = connection.cursor()

        # Execute the SQL update query
        cursor.execute('''
            UPDATE AnswerRatings 
            SET RatingDescription=?, AnswerRatingValue=?
            WHERE BusinessFunction=? AND RatingName=?
        ''', (description_name_business_sector, rating_value_business_sector, business_sector_name,
              business_name_business_sector))

        # Commit changes and close connection
        connection.commit()
        connection.close()

        # Redirect back to administrator page
        return redirect('/administrator')

    return render_template('administrator.html')


# View all answer rating
@app.route('/view_all_answer_rating', methods=['GET', 'POST'])
@login_required
def viewAllAnswerRatings():
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id, BusinessFunction, RatingName, RatingDescription, AnswerRatingValue
        FROM AnswerRatings
    ''')
    combined_ratings = cursor.fetchall()

    # Normalize the BusinessFunction column
    normalize_business_function()

    cursor.execute(
        'SELECT DISTINCT BusinessFunction FROM ArrangingTheDataInProperOrder')
    unique_business_functions = cursor.fetchall()

    connection.close()

    return render_template('administratorViewAllAnswerRating.html', combined_ratings=combined_ratings,
                           unique_business_functions=unique_business_functions)


# Delete answer ratings
@app.route('/delete_answer_rating', methods=['POST'])
@login_required
def deleteAnAnswerRating():
    if request.method == 'POST':
        # Get the ID of the record to delete from the form
        delete_record_id = request.form['record_id']
        try:
            # Delete the record from the database
            connection = sqlite3.connect('DigitalMaturityDatabase.db')
            cursor = connection.cursor()
            cursor.execute('''
                DELETE FROM AnswerRatings
                WHERE id = ?
            ''', (delete_record_id,))
            connection.commit()
            connection.close()

            # Redirect back to the page displaying combined data
            return redirect('/view_all_answer_rating')
        except Exception as e:
            return "Error occurred during deletion: " + str(e)
    else:
        return "Method Not Allowed"


# Business_Manager_account


@app.route('/add_random_characters', methods=['GET', 'POST'])
@login_required
def add_random_characters_route():
    business_functions_data = {}  # Ensure this is a dictionary
    modified_word = None
    if request.method == 'POST':
        word = request.form['word']
        modified_word = add_random_characters(word)
    return render_template('manager.html', modified_word=modified_word, business_data=business_functions_data)


@app.route('/userSubmissionDataIntoTable', methods=['GET', 'POST'])
@login_required
def CombinedTiersForUser():
    error_display_asistobe = None  # Initialize error_display_asistobe

    if request.method == 'POST':
        UserSubmittedUniqueCode = request.form['Unique_code_from_User']
        measuring_element_name_user = request.form.getlist(
            'Measuring_element_user[]')
        rating_user = request.form.getlist('Rting_User[]')
        sub_category_name_user = request.form.getlist(
            'sub_category_for_user[]')
        as_is_questions_user = request.form.getlist('as_is_questions_user[]')
        answers_user_as_is = request.form.getlist('UserAnswerRatingAsIs[]')
        to_be_questions_user = request.form.getlist('to_be_questions_user[]')
        answers_user_to_be = request.form.getlist('UserAnswerRatingToBe[]')

        # Get selected business function from session
        selected_business_function = session.get(
            'selected_business_function', None)

        if not answers_user_as_is or not answers_user_to_be:
            error_display_asistobe = "An error occurred. Please make sure to select an answer for every question before submitting your answers."
            print("Error message:", error_display_asistobe)
        else:
            connection = sqlite3.connect('DigitalMaturityDatabase.db')
            cursor = connection.cursor()

            # Get max rating value from AnswerRatings table
            cursor.execute('SELECT MAX(AnswerRatingValue) FROM AnswerRatings')
            max_rating_user = cursor.fetchone()[0]

            for i in range(len(measuring_element_name_user)):
                rating_user_val = float(rating_user[i])
                user_answer_rating_as_is = float(answers_user_as_is[i])
                user_answer_rating_to_be = float(answers_user_to_be[i])

                expected_cum_sum = rating_user_val * max_rating_user
                user_cum_sum_as_is = rating_user_val * user_answer_rating_as_is
                user_cum_sum_to_be = rating_user_val * user_answer_rating_to_be

                cursor.execute('''
                    INSERT INTO UserSubmissionRecord (
                        UniqueCodeUser, BusinessFunction, MeasuringEltUser, RatingUser, SUbCategoryUser, 
                        AsIsQuestionsUser, AnswersUserAsIs, ToBeQuestionsUser, AnswersUserToBe, 
                        MaxRatingUser, ExpectedCumSum, UserCumSumAsIs, UserCumSumToBe)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (UserSubmittedUniqueCode, selected_business_function, measuring_element_name_user[i], rating_user_val,
                      sub_category_name_user[i], as_is_questions_user[i], user_answer_rating_as_is,
                      to_be_questions_user[i], user_answer_rating_to_be, max_rating_user,
                      expected_cum_sum, user_cum_sum_as_is, user_cum_sum_to_be))

            connection.commit()
            connection.close()

            feedback_function()

            # Redirect to the user account page
            return redirect('/BusinessAnalysts')

    return render_template('BusinessFunction.html', error_display_asistobe=error_display_asistobe)


def feedback_function():
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()

    # Select distinct UniqueCodeUser and BusinessFunction from UserSubmissionRecordTrimmed
    cursor.execute('''
        SELECT DISTINCT UniqueCodeUser, BusinessFunction, MeasuringEltUser, RatingUser, SUbCategoryUser, 
                        AnswersUserAsIs, AnswersUserToBe, MaxRatingUser, ExpectedCumSum, 
                        UserCumSumAsIs, UserCumSumToBe
        FROM UserSubmissionRecord
    ''')
    trimmed_records = cursor.fetchall()

    for record in trimmed_records:
        (UniqueCodeUser, BusinessFunction, MeasuringEltUser, RatingUser, SUbCategoryUser,
         AnswersUserAsIs, AnswersUserToBe, MaxRatingUser, ExpectedCumSum,
         UserCumSumAsIs, UserCumSumToBe) = record

        # Calculate percentages
        percentage_as_is = round(
            (UserCumSumAsIs / ExpectedCumSum) * 100, 2) if ExpectedCumSum != 0 else 0
        percentage_to_be = round(
            (UserCumSumToBe / ExpectedCumSum) * 100, 2) if ExpectedCumSum != 0 else 0

        # Growth rate calculation
        growth_rate = round(((percentage_to_be - percentage_as_is) /
                             percentage_as_is) * 100, 2) if percentage_as_is != 0 else 0

        # Calculate the duration in years
        duration = round(math.log(UserCumSumToBe / UserCumSumAsIs) /
                         math.log(1 + growth_rate / 100), 4) if growth_rate != 0 else 0

        # Generate feedback based on percentages
        feedback_as_is = generate_feedback(percentage_as_is)
        feedback_to_be = generate_feedback(percentage_to_be)

        # Insert feedback into UserSubmittedFeedback
        cursor.execute('''
            INSERT INTO UserSubmittedFeedback (
                UniqueCodeUser, BusinessFunction, MeasuringEltUser, RatingUser, SUbCategoryUser, 
                AnswersUserAsIs, AnswersUserToBe, MaxRatingUser, ExpectedCumSum, 
                UserCumSumAsIs, UserCumSumToBe, PercentageAsIs, PercentageToBe, 
                FeedbackAsIs, FeedbackToBe, GrowthRate, Duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            UniqueCodeUser, BusinessFunction, MeasuringEltUser, RatingUser, SUbCategoryUser,
            AnswersUserAsIs, AnswersUserToBe, MaxRatingUser, ExpectedCumSum,
            UserCumSumAsIs, UserCumSumToBe, percentage_as_is, percentage_to_be,
            feedback_as_is, feedback_to_be, growth_rate, duration
        ))

    # Calculate average percentages and insert into TypeOfDigitalMaturity table
    cursor.execute('''
        SELECT UniqueCodeUser, BusinessFunction, AVG(PercentageAsIs), AVG(PercentageToBe)
        FROM UserSubmittedFeedback
        GROUP BY UniqueCodeUser, BusinessFunction
    ''')
    average_percentages = cursor.fetchall()

    # Get business sector from session
    business_sector = session.get('business_sector', None)

    for avg_record in average_percentages:
        UniqueCodeUser, BusinessFunction, avg_percentage_as_is, avg_percentage_to_be = avg_record

        # Check if an entry already exists
        cursor.execute('''
            SELECT COUNT(*) FROM TypeOfDigitalMaturity
            WHERE UniqueCodeUser = ? AND BusinessFunction = ?
        ''', (UniqueCodeUser, BusinessFunction))
        entry_exists = cursor.fetchone()[0]

        if entry_exists == 0:
            # Get the predicted maturity type
            predicted_maturity_type = ClassifyingDigitalMaturity(
                business_sector, BusinessFunction)

            cursor.execute('''
                INSERT INTO TypeOfDigitalMaturity (
                    BusinessSector, UniqueCodeUser, DigitalMaturityType, BusinessFunction, MaturityAsIs, MaturityToBe)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (business_sector, UniqueCodeUser, predicted_maturity_type, BusinessFunction, avg_percentage_as_is, avg_percentage_to_be))

    # Commit changes to the database and close the connection
    connection.commit()
    connection.close()



def generate_feedback(percentage):
    if 0 <= percentage <= 15.5:
        return "Stage 0:, Level: Incomplete"
    elif 16 <= percentage <= 34.5:
        return "Stage 1, Level Performed"
    elif 35 <= percentage <= 50.5:
        return "Stage 2, level Managed"
    elif 51 <= percentage <= 67.5:
        return "Stage 3: Level: Established"
    elif 68 <= percentage <= 84.5:
        return "Stage 4: Level: Predictable"
    elif 85 <= percentage <= 100:
        return "Stage 5: Level: Optimizing"


def ClassifyingDigitalMaturity(business_sector, business_function_selected):
    prediction_label = None

    if business_sector and business_function_selected:
        try:
            # Encode using LabelEncoder
            Business_Sector_encoded = label_encoder_sector.transform([business_sector])[0]
            Business_Function_encoded = label_encoder_function.transform([business_function_selected])[0]

            print("The encoded sector", Business_Sector_encoded)
            print("The encoded function", Business_Function_encoded)

            # Prepare features and make a prediction
            features = np.array([[Business_Sector_encoded, Business_Function_encoded]])
            prediction_encoded = Extra_Tree_model.predict(features)[0]

            # Inverse transform the prediction to get the categorical label
            prediction_label = label_encoder_prediction.inverse_transform([prediction_encoded])[0] + " " + "Maturity"

        except ValueError as e:
            print(f"ValueError encountered: {e}")
            # Handle unseen labels appropriately
            # You can log the error, or map the unseen label to a default value if necessary
            prediction_label = "Unknown Maturity"

    return prediction_label



@app.route('/submit_unique_code', methods=['GET', 'POST'])
@login_required
def submitting_unique_code():
    error_message = None
    business_functions_data = {}
    plot_images = []
    bar_plot_images = []
    growth_rate_images = []
    maturity_data = []
    pie_chart_as_is = None
    pie_chart_to_be = None

    if request.method == 'POST':
        unique_code = request.form['unique_code_user']

        if unique_code:
            connection = sqlite3.connect('DigitalMaturityDatabase.db')
            cursor = connection.cursor()

            cursor.execute('''
                SELECT BusinessFunction, MeasuringEltUser, ExpectedCumSum, UserCumSumAsIs, UserCumSumToBe, PercentageAsIs, PercentageToBe, FeedbackAsIs, FeedbackToBe, GrowthRate, Duration
                FROM UserSubmittedFeedback
                WHERE UniqueCodeUser = ? AND PercentageAsIs IS NOT NULL AND PercentageToBe IS NOT NULL AND FeedbackAsIs IS NOT NULL AND FeedbackToBe IS NOT NULL AND GrowthRate IS NOT NULL AND Duration IS NOT NULL  
                GROUP BY BusinessFunction, MeasuringEltUser
                ORDER BY BusinessFunction, MeasuringEltUser;
            ''', (unique_code,))
            rows = cursor.fetchall()

            cursor.execute('''
                SELECT DigitalMaturityType, BusinessFunction, MaturityAsIs, MaturityToBe
                FROM TypeOfDigitalMaturity
                WHERE UniqueCodeUser = ?
            ''', (unique_code,))
            maturity_data = cursor.fetchall()

            connection.close()

            if not rows and not maturity_data:
                error_message = "No records found for the provided unique code."
                return render_template('manager.html', error_message=error_message,
                                       business_data=business_functions_data, maturity_data=maturity_data)

            for row in rows:
                business_function, measuring_elt_user, exped_sum, as_is_sum, to_be_sum, percent_maturity_as_is, percent_maturity_to_be, feedback_as_is, feedback_to_be, growth_rate, time_to_grow = row
                if business_function not in business_functions_data:
                    business_functions_data[business_function] = []
                business_functions_data[business_function].append(
                    (measuring_elt_user, exped_sum, as_is_sum, to_be_sum, percent_maturity_as_is,
                     percent_maturity_to_be, feedback_as_is, feedback_to_be, growth_rate, time_to_grow)
                )

            for business_function, data in business_functions_data.items():
                if not data:
                    continue
                labels = [item[0] for item in data]
                exped_sums = [item[1] for item in data]
                as_is_sums = [item[2] for item in data]
                to_be_sums = [item[3] for item in data]
                growth_rates = [item[8] for item in data]
                durations = [item[9] for item in data]

                if not labels or not exped_sums or not as_is_sums or not to_be_sums:
                    continue

                angles = np.linspace(
                    0, 2 * np.pi, len(labels), endpoint=False).tolist()
                angles += angles[:1]

                # Increase the size of the polar plots
                plt.figure(figsize=(10, 10))
                ax = plt.subplot(111, polar=True)
                ax.plot(angles, as_is_sums + [as_is_sums[0]],
                        'o-', linewidth=2, label='AS IS', color='red')
                ax.fill(angles, as_is_sums +
                        [as_is_sums[0]], alpha=0.4, color='red')
                ax.plot(angles, to_be_sums + [to_be_sums[0]],
                        'o-', linewidth=2, label='TO BE', color='blue')
                ax.fill(angles, to_be_sums +
                        [to_be_sums[0]], alpha=0.4, color='blue')
                ax.set_xticks(angles[:-1])
                ax.set_xticklabels(labels, color='grey', size=8)

                ax.set_title(business_function, size=10,
                             color='black', weight='bold')
                ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                plot_image = base64.b64encode(buf.getvalue()).decode('utf-8')
                plot_images.append(plot_image)
                plt.close()

                # Create bar plot for each business function
                plt.figure(figsize=(10, 6))
                bar_width = 0.25
                index = np.arange(len(labels))

                plt.bar(index, exped_sums, bar_width,
                        label='Position of 10 best performing organization')
                plt.bar(index + bar_width, as_is_sums, bar_width,
                        label='Current position of your organization')
                plt.bar(index + 2 * bar_width, to_be_sums, bar_width,
                        label='Expected position of your organization')

                plt.xlabel('Measuring Element')
                plt.ylabel('Values')
                plt.title(f'{business_function}')
                plt.xticks(index + bar_width, labels, rotation=45)
                plt.legend()

                for i in range(len(labels)):
                    plt.text(i, exped_sums[i], exped_sums[i], ha='center')
                    plt.text(i + bar_width,
                             as_is_sums[i], as_is_sums[i], ha='center')
                    plt.text(i + 2 * bar_width,
                             to_be_sums[i], to_be_sums[i], ha='center')

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                bar_plot_image = base64.b64encode(
                    buf.getvalue()).decode('utf-8')
                bar_plot_images.append(bar_plot_image)
                plt.close()

                # Create growth rate curve for each business function
                for idx in range(len(labels)):
                    if durations[idx] > 0:  # Ensure duration is not zero or negative
                        x_values = np.linspace(0, durations[idx], 100)
                        growth_rate = growth_rates[idx]
                        y_values = to_be_sums[idx] * \
                            np.exp(growth_rate * x_values)
                        plt.plot(x_values, y_values, label=f'{
                                 labels[idx]} Growth Curve')

                plt.xlabel('Time (Years)')
                plt.ylabel('Value')
                plt.title(f'Exponential growth curve for :{business_function}')
                plt.legend()
                plt.tight_layout()  # Adjust layout for better spacing

                # Convert plot to base64
                img_buffer = io.BytesIO()
                plt.savefig(img_buffer, format='png')
                img_buffer.seek(0)
                img_str = base64.b64encode(img_buffer.getvalue()).decode()
                growth_rate_images.append(img_str)
                plt.close()

            # Store data for pie charts from TypeOfDigitalMaturity
            maturity_type = [record[0] for record in maturity_data]
            # business_functions = [record[1] for record in maturity_data]
            maturity_as_is_values = [record[2] for record in maturity_data]
            maturity_to_be_values = [record[3] for record in maturity_data]

            # Create pie chart for Maturity As-Is
            if maturity_as_is_values:
                plt.figure(figsize=(8, 8))
                plt.pie(maturity_as_is_values, labels=maturity_type, autopct=lambda p: '{:.0f}%'.format(p) if p > 0 else '')
                plt.title('Current State')

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                pie_chart_as_is = base64.b64encode(buf.getvalue()).decode('utf-8')
                plt.close()

            # Create pie chart for Maturity To-Be
            if maturity_to_be_values:
                plt.figure(figsize=(8, 8))
                plt.pie(maturity_to_be_values, labels=maturity_type, autopct=lambda p: '{:.0f}%'.format(p) if p > 0 else '')
                plt.title('Future State')

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                pie_chart_to_be = base64.b64encode(buf.getvalue()).decode('utf-8')
                plt.close()

    return render_template('manager.html', error_message=error_message,
                           plot_images=plot_images, business_data=business_functions_data,
                           bar_plot_images=bar_plot_images, growth_rate_images=growth_rate_images,
                           maturity_data=maturity_data, pie_chart_as_is=pie_chart_as_is,
                           pie_chart_to_be=pie_chart_to_be)








# Machine learning model

# Load your model
model_path = 'Model/ET_DM (1).pkl'
with open(model_path, 'rb') as f:
    Extra_Tree_model = pickle.load(f)

# Assume these are your labels
business_sector_labels = ["MINING", "Energy", "Sector3"]
business_function_labels = [
    "Exploration and Geology", "Mining Operations", "Function3", "Supply Chain and Logistics",
    "Legal and Compliance", "Human Resources (HR)", "Health Safety and Environment (HSE)",
    "Finance and Accounting", "Marketing and sales", "Corporate Development and Strategy",
    "Community and Stakeholder Relations", "Operations", "IT", "Customer Service",
    "Safety and Compliance", "Safety", "Finance", "Processing and Metallurgy",
    "Research and Development", "Power Generation", "Health", "Logistics", "HR",
    "Environment and Quality(SHEQ)"
]

# Prediction labels
predicted_labels = ["Process", "Hardware", "Culture", "Software", "Strategy"]

# Initialize label encoders
label_encoder_sector = LabelEncoder()
label_encoder_function = LabelEncoder()
label_encoder_prediction = LabelEncoder()

# Fit encoders with all possible labels
label_encoder_sector.fit(business_sector_labels)
label_encoder_function.fit(business_function_labels)
label_encoder_prediction.fit(predicted_labels)




if __name__ == '__main__':
    app.run(debug=True)
