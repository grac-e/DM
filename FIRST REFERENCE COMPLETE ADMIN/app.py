import os
from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify, send_file
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

# # Configure server-side session
# app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SESSION_FILE_DIR'] = os.path.join(app.root_path, 'flask_session')
# app.config['SESSION_PERMANENT'] = False
# app.config['SESSION_USE_SIGNER'] = True
# app.config['SESSION_FILE_THRESHOLD'] = 500

# # Initialize the session extension
# session(app)



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
            Activities TEXT,
            Skills TEXT,
            Technology TEXT
        )
    ''')
    connection.commit()
    connection.close()
    
    
def create_business_process_table():
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS BusinessProcess (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            BusinessSector TEXT,
            BusinessFunction TEXT,
            BusinessProcess TEXT,
            Activities TEXT,
            BusinessResource TEXT
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

def create_trimmed_business_process_table():
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ArrangingBusinessProcessIntoProperOrder (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            BusinessSector TEXT,
            BusinessFunction TEXT,
            BusinessProcess TEXT,
            Activities INTEGER,
            BusinessResource TEXT
        )
    ''')
    connection.commit()
    connection.close()
    
    
def create_temporal_table():
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS TemporalTable (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            BusinessSector TEXT,
            BusinessFunction TEXT,
            MeasuringElt TEXT,
            SUbCategory TEXT,
            AsIsQuestions TEXT,
            ToBeQuestions TEXT
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
            BusinessSector TEXT,
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
            BusinessSector TEXT,
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
create_temporal_table()
create_business_process_table()
create_trimmed_business_process_table()


# Utility functions
def get_unique_business_sectors():
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    
    # Fetch distinct business sectors from the correct table (CombinedTable in this example)
    cursor.execute('SELECT DISTINCT BusinessSector FROM CombinedTable')  # Ensure this is the correct table
    business_sectors = cursor.fetchall()
    
    connection.close()
    
    # Debugging print to check if any sectors were fetched
    if not business_sectors:
        print("No business sectors found in the database.")
    
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



# Administrator create a new user
@app.route('/Adminregister', methods=['GET', 'POST'])
def Adminregister():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    
    # Get business sectors for dropdown
    business_sectors = get_unique_business_sectors()
    print("These are the unique business sectors in the admin: ", business_sectors)

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        account_type = request.form['users']
        user_photo = request.files['User_photo']
        business_sector = request.form['business_sector']

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('administrator.html', business_sectors=business_sectors, user_name=user_name)

        # Check if the user already exists
        connection = sqlite3.connect('DigitalMaturityDatabase.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM User WHERE email=?', (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            connection.close()
            flash('User with this email already exists', 'error')
            return render_template('administrator.html', business_sectors=business_sectors, user_name=user_name)

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # Read the photo data and convert it to binary
        user_photo_data = user_photo.read()

        # Insert the new user into the database
        cursor.execute(
            'INSERT INTO User (name, email, password, account_type, BusinessSector, userPhoto) VALUES (?, ?, ?, ?, ?, ?)',
            (name, email, hashed_password, account_type, business_sector, user_photo_data))
        connection.commit()
        connection.close()

        # Flash success message and redirect
        flash('User successfully registered!', 'success')
        return redirect('/Adminregister')

    # Pass business sectors to the template
    return render_template('administrator.html', business_sectors=business_sectors, user_name=user_name)



# Login app route
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Fetch business sectors for dropdown
    business_sectors = get_unique_business_sectors()
    

    if request.method == 'POST':
        email = request.form.get('email', None)
        password = request.form.get('password', None)
        account_type = request.form.get('users', None)
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
            session['email'] = user[2]
            session['name'] = user[1]
            session['logged_in'] = True
            session['account_type'] = account_type

            # Check the account type and business sector
            if account_type in ["Business Manager", "Business Analyst"]:
                if business_sector != user[5]:
                    error_message = "You have selected the wrong business sector for this account."
                    return render_template('login.html', error=error_message, business_sectors=business_sectors)
                session['selected_business_sector'] = business_sector  # Store the business sector in the session

            elif account_type == "Administrator":
                session['selected_business_sector'] = user[5]  # Store admin's business sector

            # Redirect based on account type
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
    user_name = session.get('name', 'User')  # Retrieve the user's name from sess
    selected_business_sector = session.get('selected_business_sector', None)  # Correctly fetch the sector
    business_functions = []
    business_functions_for_business_process=[]
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
        
        # Fetching from the business process
        # Fetch distinct business functions for the stored sector
        cursor.execute('''
            SELECT DISTINCT BusinessFunction
            FROM ArrangingBusinessProcessIntoProperOrder
            WHERE BusinessSector=?
        ''', (selected_business_sector,))

        business_functions_for_business_process = [row[0] for row in cursor.fetchall()]        
        connection.close()

        # print("The selected business sector is:", selected_business_sector)
        # print("These are the distinct business functions:", business_functions)

        business_sector_rating = get_the_different_answer_rating_for_sector(selected_business_sector)
        session['business_sector_rating'] = business_sector_rating

    return render_template('BusinessAnalyst.html', business_functions=business_functions, business_sector_rating=business_sector_rating, user_name=user_name, unique_business_pricess_function=business_functions_for_business_process)



# Business analysts question and answer section
@app.route('/select_business_function_in_business_function_html_page', methods=['GET', 'POST'])
def select_business_function():
    user_name = session.get('name', 'User')  # Retrieve the user's name from sess
    business_function_selected_data = []
    business_sector_rating = []
    user_photo_base64 = None
    business_functions_for_business_process=[]
    
    user = None
    SectorError = ""

    if request.method == 'POST':
        selected_business_function = request.form.get('business_function_user', None)
        selected_business_sector = session.get('selected_business_sector', None)  # Fetch the business sector from session

        if selected_business_function:
            connection = sqlite3.connect('DigitalMaturityDatabase.db')
            cursor = connection.cursor()
            cursor.execute('''
                SELECT DISTINCT MeasuringElt, Rating, SUbCategory
                FROM ArrangingTheDataInProperOrder
                WHERE BusinessFunction=?
            ''', (selected_business_function,))
            business_function_selected_data = cursor.fetchall()

            # Initialize session storage for MeasuringElt and SUbCategory
            measuring_elt_subcategory_dict = {}
            as_is_to_be_questions_dict = {}
            business_process_dic = {}
            
            

            # Loop through the selected data, generate questions, and check for existing entries before inserting
            for data in business_function_selected_data:
                measuring_elt = data[0]  # MeasuringElt
                sub_category = data[2]   # SUbCategory
                measuring_elt_subcategory_dict[measuring_elt] = sub_category

                # Generate AS-IS and TO-BE questions for the measuring element
                as_is_question = f"For the lists of activities in the {measuring_elt} process how will you best describe your application of digital maturity ?"
                to_be_question = f"For the lists of activities in the  {measuring_elt} process, Where would you want these activities be placed in the future ?"

                # Generate AS-IS and TO-BE questions for the sub-category
  

                as_is_to_be_questions_dict[measuring_elt] = {
                    "as_is_question": as_is_question,
                    "to_be_question": to_be_question
                }

 
                # Check if the exact data already exists in the TemporalTable
                cursor.execute('''
                    SELECT COUNT(*)
                    FROM TemporalTable
                    WHERE BusinessSector = ? AND BusinessFunction = ? AND MeasuringElt = ? AND SUbCategory = ? AND AsIsQuestions = ? AND ToBeQuestions = ?
                ''', (selected_business_sector, selected_business_function, measuring_elt, sub_category, as_is_question, to_be_question))
                
                count = cursor.fetchone()[0]

                # Insert data only if it doesn't exist
                if count == 0:
                    cursor.execute('''
                        INSERT INTO TemporalTable (BusinessSector, BusinessFunction, MeasuringElt, SUbCategory, AsIsQuestions, ToBeQuestions)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (selected_business_sector, selected_business_function, measuring_elt, sub_category, as_is_question, to_be_question))

            cursor.execute('''
            SELECT DISTINCT BusinessFunction
            FROM ArrangingBusinessProcessIntoProperOrder
            WHERE BusinessSector=?
        ''', (selected_business_sector,))

            business_functions_for_business_process = [row[0] for row in cursor.fetchall()] 
            
            
            
            
            
            
            # Commit changes to the database
            connection.commit()
            connection.close()

            # Store the generated dictionaries in session
            session['measuring_elt_subcategory'] = measuring_elt_subcategory_dict
            session['as_is_to_be_questions'] = as_is_to_be_questions_dict
         

            business_sector_rating = session.get('business_sector_rating', [])
            # Store selected business function in session
            session['selected_business_function'] = selected_business_function
            
            return render_template('AsIsandToBeQuestionandAnswer.html', user=user, user_photo_base64=user_photo_base64,
                                   business_function_selected_data=business_function_selected_data,
                                   SectorError=SectorError, business_sector_rating=business_sector_rating, user_name=user_name, unique_business_pricess_function=business_functions_for_business_process)
       
    return render_template('BusinessAnalyst.html', user=user, user_photo_base64=user_photo_base64,
                           SectorError=SectorError, business_function_selected_data=business_function_selected_data,
                           business_sector_rating=business_sector_rating, user_name=user_name, unique_business_pricess_function=business_functions_for_business_process)



# Function to store into temporal table
def function_to_insert_into_temporal_table(selected_business_function):
    selected_business_sector = session.get('selected_business_sector')
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    
    # Check if data is already in the TemporalTable
    cursor.execute('''
        SELECT COUNT(*)
        FROM TemporalTable
        WHERE BusinessFunction=?
    ''', (selected_business_function,))
    
    count = cursor.fetchone()[0]

    # If not, fetch the data from ArrangingTheDataInProperOrder
    if count == 0:
        cursor.execute('''
            SELECT DISTINCT MeasuringElt, SUbCategory
            FROM ArrangingTheDataInProperOrder
            WHERE BusinessSector = ? AND BusinessFunction=?
        ''', (selected_business_sector, selected_business_function))
        
        selected_subcategories = cursor.fetchall()
        
        # Insert the selected SUbCategory along with placeholders for AsIsQuestions and ToBeQuestions
        for sub_category in selected_subcategories:
            as_is_question = f"As is question for the {sub_category[0]}"
            to_be_question = f"To be question for the {sub_category[0]}"
            
            cursor.execute('''
                INSERT INTO TemporalTable (BusinessSector, BusinessFunction, SUbCategory, AsIsQuestions, ToBeQuestions)
                VALUES (?, ?, ?, ?, ?)
            ''', (selected_business_sector, selected_business_function, sub_category[0], as_is_question, to_be_question))
        
        connection.commit()

    # Fetch the inserted SUbCategory data from TemporalTable
    cursor.execute('''
        SELECT SUbCategory
        FROM TemporalTable
        WHERE BusinessFunction=?
    ''', (selected_business_function,))
    
    business_function_selected_data = cursor.fetchall()
    
    connection.close()
    return business_function_selected_data



# Submitting the as-is and to-be answers into the database
@app.route('/userSubmissionDataIntoTable', methods=['GET', 'POST'])
@login_required
def CombinedTiersForUser():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    error_display_asistobe = None

    if request.method == 'POST':
        selected_business_sector = session.get('selected_business_sector')
        if not selected_business_sector:
            raise ValueError("Business sector is not selected in the session.")

        selected_business_function = session.get('selected_business_function')
        measuring_elements = request.form.getlist('Measuring_element_user[]')
        unique_code = request.form.get('Unique_code_from_User')

        user_answers_as_is = request.form.getlist('UserAnswerRatingAsIs[]')
        user_answers_to_be = request.form.getlist('UserAnswerRatingToBe[]')

        connection = sqlite3.connect('DigitalMaturityDatabase.db')
        cursor = connection.cursor()

        cursor.execute('SELECT MAX(AnswerRatingValue) FROM AnswerRatings')
        max_rating = cursor.fetchone()[0]

        # Loop through the measuring elements and subcategories
        for index, measuring_element in enumerate(measuring_elements):
            sub_categories = request.form.getlist(f'sub_category_for_user_{measuring_element}[]')

            for sub_category in sub_categories:
                # Fetch AsIsQuestions and ToBeQuestions from TemporalTable
                cursor.execute('''
                    SELECT AsIsQuestions, ToBeQuestions
                    FROM TemporalTable
                    WHERE BusinessSector = ? AND BusinessFunction = ? AND MeasuringElt = ? AND SUbCategory = ?
                ''', (selected_business_sector, selected_business_function, measuring_element, sub_category))
                
                question_data = cursor.fetchone()

                if question_data:
                    as_is_question, to_be_question = question_data
                else:
                    raise ValueError(f"Questions not found for {measuring_element} and {sub_category}")

                cursor.execute('''
                    SELECT Rating
                    FROM ArrangingTheDataInProperOrder
                    WHERE BusinessFunction = ? AND MeasuringElt = ?
                ''', (selected_business_function, measuring_element))
                rating_row = cursor.fetchone()

                if rating_row:
                    rating = rating_row[0]

                    selected_as_is_answer = user_answers_as_is[index]
                    selected_to_be_answer = user_answers_to_be[index]

                    expected_cum_sum = rating * max_rating
                    user_cum_sum_as_is = int(selected_as_is_answer) * rating
                    user_cum_sum_to_be = int(selected_to_be_answer) * rating

                    # Check if this exact record already exists
                    cursor.execute('''
                        SELECT COUNT(*)
                        FROM UserSubmissionRecord
                        WHERE BusinessSector = ? AND UniqueCodeUser = ? AND BusinessFunction = ? AND MeasuringEltUser = ? AND SUbCategoryUser = ? AND AsIsQuestionsUser = ? AND ToBeQuestionsUser = ?
                    ''', (selected_business_sector, unique_code, selected_business_function, measuring_element, sub_category, as_is_question, to_be_question))

                    existing_record_count = cursor.fetchone()[0]

                    if existing_record_count == 0:
                        # Insert the new record only if it doesn't already exist
                        cursor.execute('''
                            INSERT INTO UserSubmissionRecord (BusinessSector, UniqueCodeUser, BusinessFunction, MeasuringEltUser, SUbCategoryUser, AsIsQuestionsUser, ToBeQuestionsUser, RatingUser, MaxRatingUser, AnswersUserAsIs, AnswersUserToBe, ExpectedCumSum, UserCumSumAsIs, UserCumSumToBe)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (selected_business_sector, unique_code, selected_business_function, measuring_element, sub_category, as_is_question, to_be_question, rating, max_rating, selected_as_is_answer, selected_to_be_answer, expected_cum_sum, user_cum_sum_as_is, user_cum_sum_to_be))
                    else:
                        # Optionally handle the case where the record exists (e.g., update it or skip)
                        flash(f'Record for {measuring_element} and {sub_category} already exists.', 'info')



        # Feedback function and close connection
        feedback_function(cursor)
        connection.commit()
        connection.close()

        # Flash success message
        flash('Successfully submitted the answers for this business function into the database.', 'success')

        return redirect(url_for('dashboardBusinessAnalysts'))

    return render_template('BusinessAnalyst.html', error_display_asistobe=error_display_asistobe, user_name=user_name)




# Function to process user submitted data into the feedback table for processing
def feedback_function(cursor):
    try:
        # Select distinct UniqueCodeUser and BusinessFunction from UserSubmissionRecord
        cursor.execute('''
            SELECT DISTINCT UniqueCodeUser, BusinessFunction
            FROM UserSubmissionRecord
        ''')
        user_records = cursor.fetchall()

        for user_record in user_records:
            unique_code, selected_business_function = user_record

            cursor.execute('''
                SELECT BusinessSector, MeasuringEltUser, RatingUser, MaxRatingUser, SUbCategoryUser, AnswersUserAsIs, AnswersUserToBe, ExpectedCumSum, UserCumSumAsIs, UserCumSumToBe
                FROM UserSubmissionRecord
                WHERE UniqueCodeUser = ? AND BusinessFunction = ?
            ''', (unique_code, selected_business_function))

            submissions = cursor.fetchall()

            if not submissions:
                continue  # Skip if there are no submissions

            for submission in submissions:
                BusinessSector, MeasuringEltUser, RatingUser, MaxRatingUser, SUbCategoryUser, AnswersUserAsIs, AnswersUserToBe, ExpectedCumSum, UserCumSumAsIs, UserCumSumToBe = submission

                # Calculate percentages
                percentage_as_is = round((UserCumSumAsIs / ExpectedCumSum) * 100, 2) if ExpectedCumSum != 0 else 0
                percentage_to_be = round((UserCumSumToBe / ExpectedCumSum) * 100, 2) if ExpectedCumSum != 0 else 0

                # Growth rate calculation
                growth_rate = round(((percentage_to_be - percentage_as_is) / percentage_as_is) * 100, 2) if percentage_as_is != 0 else 0

                # Calculate the duration in years
                duration = round(math.log(UserCumSumToBe / UserCumSumAsIs) / math.log(1 + growth_rate / 100), 4) if growth_rate != 0 else 0

                # Generate feedback based on percentages
                feedback_as_is = generate_feedback(percentage_as_is)
                feedback_to_be = generate_feedback(percentage_to_be)

                # Check if the record already exists in the UserSubmittedFeedback table
                cursor.execute('''
                    SELECT COUNT(*)
                    FROM UserSubmittedFeedback
                    WHERE UniqueCodeUser = ? AND BusinessFunction = ? AND MeasuringEltUser = ? AND SUbCategoryUser = ?
                ''', (unique_code, selected_business_function, MeasuringEltUser, SUbCategoryUser))

                record_exists = cursor.fetchone()[0]

                if record_exists == 0:
                    # Insert the new feedback if the record doesn't exist
                    cursor.execute('''
                        INSERT INTO UserSubmittedFeedback (
                            BusinessSector, UniqueCodeUser, BusinessFunction, MeasuringEltUser, RatingUser, SUbCategoryUser,
                            AnswersUserAsIs, AnswersUserToBe, MaxRatingUser, ExpectedCumSum,
                            UserCumSumAsIs, UserCumSumToBe, PercentageAsIs, PercentageToBe,
                            FeedbackAsIs, FeedbackToBe, GrowthRate, Duration)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        BusinessSector, unique_code, selected_business_function, MeasuringEltUser, RatingUser, SUbCategoryUser,
                        AnswersUserAsIs, AnswersUserToBe, MaxRatingUser, ExpectedCumSum,
                        UserCumSumAsIs, UserCumSumToBe, percentage_as_is, percentage_to_be,
                        feedback_as_is, feedback_to_be, growth_rate, duration
                    ))
                else:
                    # Update the existing record instead of inserting a new one
                    cursor.execute('''
                        UPDATE UserSubmittedFeedback
                        SET BusinessSector = ?, RatingUser = ?, AnswersUserAsIs = ?, AnswersUserToBe = ?, MaxRatingUser = ?, ExpectedCumSum = ?,
                            UserCumSumAsIs = ?, UserCumSumToBe = ?, PercentageAsIs = ?, PercentageToBe = ?,
                            FeedbackAsIs = ?, FeedbackToBe = ?, GrowthRate = ?, Duration = ?
                        WHERE UniqueCodeUser = ? AND BusinessFunction = ? AND MeasuringEltUser = ? AND SUbCategoryUser = ?
                    ''', (
                        BusinessSector, RatingUser, AnswersUserAsIs, AnswersUserToBe, MaxRatingUser, ExpectedCumSum,
                        UserCumSumAsIs, UserCumSumToBe, percentage_as_is, percentage_to_be,
                        feedback_as_is, feedback_to_be, growth_rate, duration,
                        unique_code, selected_business_function, MeasuringEltUser, SUbCategoryUser
                    ))

        # Handle TypeOfDigitalMaturity table logic similarly
        cursor.execute('''
            SELECT UniqueCodeUser, BusinessFunction, AVG(PercentageAsIs), AVG(PercentageToBe)
            FROM UserSubmittedFeedback
            GROUP BY UniqueCodeUser, BusinessFunction
        ''')
        average_percentages = cursor.fetchall()

        business_sector = session.get('selected_business_sector', None)

        for avg_record in average_percentages:
            UniqueCodeUser, BusinessFunction, avg_percentage_as_is, avg_percentage_to_be = avg_record

            cursor.execute('''
                SELECT COUNT(*)
                FROM TypeOfDigitalMaturity
                WHERE UniqueCodeUser = ? AND BusinessFunction = ?
            ''', (UniqueCodeUser, BusinessFunction))
            entry_exists = cursor.fetchone()[0]

            if entry_exists == 0:
                predicted_maturity_type = ClassifyingDigitalMaturity(business_sector, BusinessFunction)
                cursor.execute('''
                    INSERT INTO TypeOfDigitalMaturity (
                        BusinessSector, UniqueCodeUser, DigitalMaturityType, BusinessFunction, MaturityAsIs, MaturityToBe)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (business_sector, UniqueCodeUser, predicted_maturity_type, BusinessFunction, avg_percentage_as_is, avg_percentage_to_be))
            else:
                cursor.execute('''
                    UPDATE TypeOfDigitalMaturity
                    SET MaturityAsIs = ?, MaturityToBe = ?
                    WHERE UniqueCodeUser = ? AND BusinessFunction = ?
                ''', (avg_percentage_as_is, avg_percentage_to_be, UniqueCodeUser, BusinessFunction))

    except Exception as e:
        print(f"Error in feedback_function: {str(e)}")




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
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    business_sectors = get_unique_business_sectors()
    if session.get('email'):
        connection = sqlite3.connect('DigitalMaturityDatabase.db')
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM User WHERE email=?', (session['email'],))
        user = cursor.fetchone()  # Fetch the entire row

        if user:  # Check if user is found
            user_name = user[1]  # Access the user's name
        else:
            flash('No user found for the current email.')  # Handle no user case

        connection.close()

    return render_template('administrator.html', user_name=user_name, business_sectors=business_sectors)



@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    business_sectors = get_unique_business_sectors()

    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['newpassword']
        confirm_new_password = request.form['confnewpassword']

        if new_password != confirm_new_password:
            flash('Passwords do not match', 'error')
            return redirect('/change_password')  # Redirect to avoid resubmission

        connection = sqlite3.connect('DigitalMaturityDatabase.db')
        cursor = connection.cursor()

        # Check if the email exists in the database
        cursor.execute('SELECT * FROM User WHERE email=?', (email,))
        user = cursor.fetchone()

        if user:
            # Hash the new password
            hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute('UPDATE User SET password=? WHERE email=?', (hashed_password, email))
            connection.commit()
            flash('Password updated successfully.', 'success')
        else:
            flash('Email does not exist.', 'error')

        connection.close()

        # Redirect to avoid resubmission issues and clear form data
        return redirect('/change_password')

    return render_template('administrator.html', user_name=user_name, business_sectors=business_sectors)



@app.route('/requestPasswordChange', methods=['GET', 'POST'])
def PasswordChange():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
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
    return render_template('ForgotPassword.html', requestMessage=requestMessage, user_name=user_name)


# BusinessManager
@app.route('/BusinessManager')
@login_required
def dashboardBusinessManager():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
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

        return render_template('manager.html', user=user, business_data=business_functions_data, business_functions=business_functions, user_name=user_name)

    return redirect('/login')


# Displaying the elements in the database on the admin side of the panel
@app.route('/view_combined_data', methods=['GET', 'POST'])
@login_required
def view_combined_data():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    business_sectors = get_unique_business_sectors()
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
                           unique_business_functions=unique_business_functions, user_name=user_name, business_sectors=business_sectors)


# View combined business process data
@app.route('/view_combined_business_process_data', methods=['GET', 'POST'])
@login_required
def view_combined_business_process_data():
    
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    business_sectors = get_unique_business_sectors()
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id, BusinessSector, BusinessFunction, BusinessProcess, Activities, BusinessResource 
        FROM BusinessProcess
    ''')
    combined_business_process_data = cursor.fetchall()
    connection.close()

    return render_template('administratorViewBusinessProcess.html', combined_business_process_data=combined_business_process_data, user_name=user_name, business_sectors=business_sectors)


#Delete business process
@app.route('/delete_business_process_data', methods=['POST'])
@login_required
def delete_business_process_data():
    if request.method == 'POST':
        # Get the ID of the record to delete from the form
        delete_record_id = request.form['record_id']
        try:
            # Delete the record from the database
            connection = sqlite3.connect('DigitalMaturityDatabase.db')
            cursor = connection.cursor()
            cursor.execute('''
                DELETE FROM BusinessProcess
                WHERE id = ?
            ''', (delete_record_id,))
            connection.commit()
            connection.close()

            # Flash success message
            flash('Business Process deleted successfully.', 'success')

            # Redirect back to the page displaying combined data
            return redirect('/view_combined_business_process_data')
        except Exception as e:
            # Flash error message if something goes wrong
            flash('Error occurred during deletion: ' + str(e), 'danger')
            return redirect('/view_combined_business_process_data')
    else:
        return "Method Not Allowed"



# View value chain data
@app.route('/view_combined_value_chain_data', methods=['GET', 'POST'])
@login_required
def view_combined_value_chain_data():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    business_sectors = get_unique_business_sectors()
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id, BusinessSector, BusinessFunction, BusinessProcess, Activities, Skills, Technology  
        FROM ValueChain
    ''')
    combined_value_chain_data = cursor.fetchall()
    connection.close()

    return render_template('administratorViewValueChain.html', 
                           combined_value_chain_data=combined_value_chain_data, 
                           user_name=user_name, 
                           business_sectors=business_sectors)
    

#Delete value chain
@app.route('/delete_value_chain_data', methods=['POST'])
@login_required
def delete_value_chain_data():
    if request.method == 'POST':
        # Get the ID of the record to delete from the form
        delete_record_id = request.form['record_id']
        try:
            # Delete the record from the database
            connection = sqlite3.connect('DigitalMaturityDatabase.db')
            cursor = connection.cursor()
            cursor.execute('''
                DELETE FROM ValueChain
                WHERE id = ?
            ''', (delete_record_id,))
            connection.commit()
            connection.close()

            # Flash success message
            flash('Value chain record deleted successfully.', 'success')

            # Redirect back to the page displaying combined data
            return redirect('/view_combined_value_chain_data')
        except Exception as e:
            # Flash error message if something goes wrong
            flash('Error occurred during deletion: ' + str(e), 'danger')
            return redirect('/view_combined_value_chain_data')
    else:
        return "Method Not Allowed"


# View combined answer ratings
@app.route('/view_combined_answer_rating_data', methods=['GET', 'POST'])
@login_required
def view_combined_answer_rating_data():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    business_sectors = get_unique_business_sectors()
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id, BusinessFunction, RatingName, RatingDescription, AnswerRatingValue 
        FROM AnswerRatings
    ''')
    combined_answer_rating_data = cursor.fetchall()
    connection.close()

    return render_template('administratorViewAllAnswerRating.html', 
                           combined_answer_rating_data=combined_answer_rating_data, 
                           user_name=user_name, 
                           business_sectors=business_sectors)

# View all user accounts
@app.route('/view_combined_user_accounts', methods=['GET', 'POST'])
@login_required
def view_combined_user_accounts():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    business_sectors = get_unique_business_sectors()
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute('''
        SELECT id, name, email, account_type, BusinessSector 
        FROM User
    ''')
    combined_user_account_data = cursor.fetchall()
    connection.close()

    return render_template('administratorUserAccounts.html', 
                           combined_user_account_data=combined_user_account_data, 
                           user_name=user_name, 
                           business_sectors=business_sectors)

#Delete user account
@app.route('/delete_user_account_data', methods=['POST'])
@login_required
def delete_user_data():
    if request.method == 'POST':
        # Get the ID of the record to delete from the form
        delete_record_id = request.form['record_id']
        try:
            # Delete the record from the database
            connection = sqlite3.connect('DigitalMaturityDatabase.db')
            cursor = connection.cursor()
            cursor.execute('''
                DELETE FROM User
                WHERE id = ?
            ''', (delete_record_id,))
            connection.commit()
            connection.close()

            # Flash success message
            flash('User account deleted successfully.', 'success')

            # Redirect back to the page displaying combined data
            return redirect('/view_combined_user_accounts')
        except Exception as e:
            # Flash error message if something goes wrong
            flash('Error occurred during deletion: ' + str(e), 'danger')
            return redirect('/view_combined_user_accounts')
    else:
        return "Method Not Allowed"






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




# normalizing the business process table
def normalize_business_process_table():
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()

    # Clear existing data in ArrangingBusinessProcessIntoProperOrder table to prevent duplication
    cursor.execute('DELETE FROM ArrangingBusinessProcessIntoProperOrder')

    cursor.execute('''
        WITH RECURSIVE split(id, BusinessSector, BusinessFunction, BusinessProcess, Activities, BusinessResource, function_value, process_value, function_rest, process_rest) AS (
            SELECT
                id,
                BusinessSector,
                TRIM(SUBSTR(BusinessFunction || ',', 1, INSTR(BusinessFunction || ',', ',') - 1)),
                TRIM(SUBSTR(BusinessProcess || ',', 1, INSTR(BusinessProcess || ',', ',') - 1)),
                Activities,
                BusinessResource,
                TRIM(SUBSTR(BusinessFunction || ',', 1, INSTR(BusinessFunction || ',', ',') - 1)),
                TRIM(SUBSTR(BusinessProcess || ',', 1, INSTR(BusinessProcess || ',', ',') - 1)),
                TRIM(SUBSTR(BusinessFunction || ',', INSTR(BusinessFunction || ',', ',') + 1)),
                TRIM(SUBSTR(BusinessProcess || ',', INSTR(BusinessProcess || ',', ',') + 1))
            FROM BusinessProcess
            UNION ALL
            SELECT
                id,
                BusinessSector,
                TRIM(SUBSTR(function_rest, 1, INSTR(function_rest, ',') - 1)),
                TRIM(SUBSTR(process_rest, 1, INSTR(process_rest, ',') - 1)),
                Activities,
                BusinessResource,
                TRIM(SUBSTR(function_rest, 1, INSTR(function_rest, ',') - 1)),
                TRIM(SUBSTR(process_rest, 1, INSTR(process_rest, ',') - 1)),
                TRIM(SUBSTR(function_rest, INSTR(function_rest, ',') + 1)),
                TRIM(SUBSTR(process_rest, INSTR(process_rest, ',') + 1))
            FROM split
            WHERE function_rest != '' OR process_rest != ''
        )
        INSERT INTO ArrangingBusinessProcessIntoProperOrder (
            BusinessSector, BusinessFunction, BusinessProcess, Activities, BusinessResource
        )
        SELECT
            BusinessSector, function_value, process_value, Activities, BusinessResource
        FROM split
        WHERE function_value IS NOT NULL AND function_value != '' AND process_value IS NOT NULL AND process_value != ''
    ''')

    connection.commit()
    connection.close()





# Root to upload csv file for the diffeent business sectors, functions, process into the digital maturity table 
@app.route('/upload_csv', methods=['GET', 'POST'])
def upload_file():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    business_sectors = get_unique_business_sectors()
    unique_business_functions = []
    
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            try:
                # Process CSV file and insert into the database
                process_csv(file)

                # Normalize the BusinessFunction column
                normalize_business_function()

                # Fetch unique business functions
                connection = sqlite3.connect('DigitalMaturityDatabase.db')
                cursor = connection.cursor()
                cursor.execute(
                    'SELECT DISTINCT BusinessFunction FROM ArrangingTheDataInProperOrder')
                unique_business_functions = cursor.fetchall()
                flash('Records added successfully into the digital maturity database table', 'success')
                connection.close()

                # Redirect to view data
                return redirect(url_for('view_combined_data'))

            except ValueError as ve:
                flash(str(ve), 'error')  # Flash error message for incorrect file format
            except Exception as e:
                flash('An unexpected error occurred during file processing.', 'error')  # Flash general error message
        else:
            flash('Please upload a valid CSV file.', 'error')

    # Fetch unique business functions for GET request
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()
    cursor.execute(
        'SELECT DISTINCT BusinessFunction FROM ArrangingTheDataInProperOrder')
    unique_business_functions = cursor.fetchall()
    connection.close()

    return render_template('administrator.html', unique_business_functions=unique_business_functions, user_name=user_name, business_sectors=business_sectors)



# Function to process the digital maturity csv file
def process_csv(csv_file):
    try:
        connection = sqlite3.connect('DigitalMaturityDatabase.db')
        cursor = connection.cursor()

        # Convert file object to text mode
        csv_text = csv_file.stream.read().decode("utf-8")
        csv_data = csv.reader(csv_text.splitlines())

        next(csv_data)  # Skip header row if present
        for row in csv_data:
            if len(row) != 8:
                raise ValueError("The uploaded file has incorrect format. Please ensure to download the file format for this strcuture.")

            business_sector, business_function, measuring_elt, rating, sub_category, AsIsQuestions, ToBeQuestions, max_rating = row

            # Dynamically generate the as_is_question and to_be_question
            as_is_question = f"How will you best describe your {sub_category} procedure?"
            to_be_question = f"Where would you want to find {sub_category} procedure in the future?"

            cursor.execute('''
                INSERT INTO CombinedTable (BusinessSector, BusinessFunction, MeasuringElt, Rating, SubCategory, AsIsQuestions, ToBeQuestions, MaxRating)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (business_sector, business_function, measuring_elt, rating, sub_category, as_is_question,
                  to_be_question, max_rating))

        connection.commit()
    except ValueError as ve:
        raise ve  # Re-raise error to be handled in the route function
    except Exception as e:
        raise e  # Handle other exceptions
    finally:
        connection.close()

    
    


# Uploading csv into value chain table
@app.route('/business_process_upload_csv', methods=['GET', 'POST'])
def upload_file_To_Business_Process():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    business_sectors = get_unique_business_sectors()
    
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            try:
                # Process CSV file and insert into database
                process_business_process_csv(file)

                # Flash success message
                flash('Records added successfully into the business process database table', 'success')

                # Redirect to view data
                return redirect(url_for('view_combined_data'))

            except ValueError as ve:
                flash(str(ve), 'error')  # Flash specific error message if CSV format is incorrect
            except Exception as e:
                flash('An unexpected error occurred during file processing.', 'error')  # Flash for any other errors
        else:
            flash('Please upload a valid CSV file.', 'error')

    return render_template('administrator.html', user_name=user_name, business_sectors=business_sectors)




# Function to process the digital maturity csv file
def process_business_process_csv(csv_file):
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()

    # Convert file object to text mode
    csv_text = csv_file.stream.read().decode("utf-8")
    csv_data = csv.reader(csv_text.splitlines())

    next(csv_data)  # Skip header row if present
    for row in csv_data:
        if len(row) != 5:
            raise ValueError("CSV file must have exactly 5 columns")

        business_sector, business_function, business_process, business_activity, business_resource = row

        cursor.execute('''
            INSERT INTO BusinessProcess (BusinessSector, BusinessFunction, BusinessProcess, Activities, BusinessResource)
            VALUES (?, ?, ?, ?, ?)
        ''', (business_sector, business_function, business_process, business_activity, business_resource))

    connection.commit()
    connection.close()



# Download digital maturity file 
@app.route('/digital_download_excel')
def Digital_download_excel():
    
    # Replace 'your_excel_file.xlsx' with the path to your actual Excel file
    path_to_excel = 'Files/DOWNLOADED FORMAT/DIGITAL MATURITY/Digital Maturity format.csv'
    return send_file(path_to_excel, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',)


# Download answer rating file 
@app.route('/answer_download_excel')
def Naswer_download_excel():
    
    # Replace 'your_excel_file.xlsx' with the path to your actual Excel file
    path_to_excel = 'Files/DOWNLOADED FORMAT/ANSWER RATING/ANSWER RATING FORMAT.csv'
    return send_file(path_to_excel, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# Download value chain file
@app.route('/value_chain_download_excel')
def Value_download_excel():
    
    # Replace 'your_excel_file.xlsx' with the path to your actual Excel file
    path_to_excel = 'Files/DOWNLOADED FORMAT/VALUE CHAIN/Value chain excel file format.csv'
    return send_file(path_to_excel, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

# doanload business process file
 
@app.route('/business_process_download_excel')
def BP_download_excel():
    
    # Replace 'your_excel_file.xlsx' with the path to your actual Excel file
    path_to_excel = 'Files/DOWNLOADED FORMAT/BUSINESS PROCESS/BUSINESS PROCESS FILE FORMAT.csv'
    return send_file(path_to_excel, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')


# Uploading csv into value chain table
@app.route('/value_chain_upload_csv', methods=['GET', 'POST'])
def upload_file_To_Value_Chain():
    business_sectors = get_unique_business_sectors()
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            try:
                # Process CSV file and insert into database
                value_chain_process_csv(file)

                # Flash success message
                flash('Records added successfully into the value chain database table', 'success')

                # Redirect to view data
                return redirect(url_for('view_combined_data'))

            except ValueError as ve:
                flash(str(ve), 'error')  # Flash specific error message if CSV format is incorrect
            except Exception as e:
                flash('An unexpected error occurred during file processing.', 'error')  # Flash for other errors
        else:
            flash('Please upload a valid CSV file.', 'error')

    return render_template('administrator.html', user_name=user_name, business_sectors=business_sectors)



# Function to process the value chain csv file
def value_chain_process_csv(csv_file):
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()

    # Convert file object to text mode
    csv_text = csv_file.stream.read().decode("utf-8")
    csv_data = csv.reader(csv_text.splitlines())

    next(csv_data)  # Skip header row if present
    for row in csv_data:
        if len(row) != 6:
            raise ValueError("CSV file must have exactly 6 columns")

        business_sector, business_function, business_process, business_activities, business_skills, business_technologies = row

        cursor.execute('''
            INSERT INTO ValueChain (BusinessSector, BusinessFunction, BusinessProcess, Activities, Skills, Technology)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (business_sector, business_function, business_process, business_activities, business_skills, business_technologies))

    connection.commit()
    connection.close()

    
    
# Root to upload csv file into the answer rating table
@app.route('/answer_rating_upload_csv', methods=['GET', 'POST'])
def upload_file_To_answer_rating():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    business_sectors = get_unique_business_sectors()

    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.endswith('.csv'):
            try:
                # Process CSV file and insert into database
                answer_rating_csv_file(file)

                # Flash success message
                flash('Records added successfully into the answer rating database table', 'success')

                # Redirect to view data
                return redirect(url_for('view_combined_data'))

            except ValueError as ve:
                flash(str(ve), 'error')  # Flash specific error message if CSV format is incorrect
            except Exception as e:
                flash('An unexpected error occurred during file processing.', 'error')  # Flash for any other errors
        else:
            flash('Please upload a valid CSV file.', 'error')

    return render_template('administrator.html', user_name=user_name, business_sectors=business_sectors)




# Function to process the answer rating CSV file
def answer_rating_csv_file(csv_file):
    connection = sqlite3.connect('DigitalMaturityDatabase.db')
    cursor = connection.cursor()

    # Convert file object to text mode
    csv_text = csv_file.stream.read().decode("utf-8")
    csv_data = csv.reader(csv_text.splitlines())

    next(csv_data)  # Skip header row if present
    for row in csv_data:
        if len(row) != 4:
            raise ValueError("CSV file must have exactly 4 columns")

        business_sector, rating_name, rating_description, answer_rating_value = row

        cursor.execute('''
            INSERT INTO AnswerRatings (BusinessFunction, RatingName, RatingDescription, AnswerRatingValue)
            VALUES (?, ?, ?, ?)
        ''', (business_sector, rating_name, rating_description, answer_rating_value))

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

            # Flash success message
            flash('Business sector deleted successfully.', 'success')

            # Redirect back to the page displaying combined data
            return redirect('/view_combined_data')
        except Exception as e:
            # Flash error message if something goes wrong
            flash('Error occurred during deletion: ' + str(e), 'danger')
            return redirect('/view_combined_data')
    else:
        return "Method Not Allowed"


# Adding individual data into database
@app.route('/CombinedTiersForAll', methods=['GET', 'POST'])
@login_required
def CombinedTiers():
    business_sectors = get_unique_business_sectors()
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    if request.method == 'POST':
        business_sector_name = request.form['business_sector_name']
        business_function_name = request.form['business_function']
        measuring_element_name = request.form['Measuring_Element']
        rating = request.form['Rating']
        subCategory_name = request.form['subCategory_name']

        # Dynamically generate the as_is_question and to_be_question
        as_is_question = f"How will you best describe your {subCategory_name} procedure?"
        to_be_question = f"Where would you want to find {subCategory_name} procedure in the future?"

        MaxRating = request.form['MaxRating']

        connection = sqlite3.connect('DigitalMaturityDatabase.db')
        cursor = connection.cursor()

        # Check if the record already exists
        cursor.execute('''
            SELECT * FROM CombinedTable
            WHERE BusinessSector = ? AND BusinessFunction = ? AND MeasuringElt = ? AND SUbCategory = ? AND Rating = ? AND MaxRating = ?
        ''', (business_sector_name, business_function_name, measuring_element_name, subCategory_name, rating, MaxRating))

        existing_record = cursor.fetchone()

        if existing_record:
            # Flash message if record already exists
            flash(f"Record already exists for business sector: {business_sector_name}, function: {business_function_name}", "warning")
        else:
            # Insert the new record
            cursor.execute('''
                INSERT INTO CombinedTable (BusinessSector, BusinessFunction, MeasuringElt, Rating, SUbCategory, AsIsQuestions, ToBeQuestions, MaxRating)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (business_sector_name, business_function_name, measuring_element_name, rating, subCategory_name,
                  as_is_question, to_be_question, MaxRating))
            connection.commit()

            # Flash success message
            flash(f"Record successfully created for business sector: {business_sector_name}", "success")

        connection.close()

        return redirect('/Adminregister')

    return render_template('administrator.html', user_name=user_name, business_sectors=business_sectors)



# Updating the combined tiers
@app.route('/UpdateCombinedTiersForAll', methods=['GET', 'POST'])
@login_required
def UpdateCombinedTiers():
    business_sectors = get_unique_business_sectors()
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
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

        # Check if the old record exists
        cursor.execute('''
            SELECT * FROM CombinedTable
            WHERE BusinessSector=? AND BusinessFunction=? AND MeasuringElt=? AND Rating=? AND SUbCategory=? AND MaxRating=?
        ''', (oldbusiness_sector_name, oldbusiness_function, oldmeasuring_element_name, oldrating, oldsubCategory_name, oldMaxRating))

        old_record = cursor.fetchone()

        # If the old record does not exist, prepare a flash message
        if not old_record:
            # Check each field individually to identify which ones do not exist
            cursor.execute('SELECT * FROM CombinedTable WHERE BusinessSector=?', (oldbusiness_sector_name,))
            sector_exists = cursor.fetchone()

            cursor.execute('SELECT * FROM CombinedTable WHERE BusinessFunction=?', (oldbusiness_function,))
            function_exists = cursor.fetchone()

            cursor.execute('SELECT * FROM CombinedTable WHERE MeasuringElt=?', (oldmeasuring_element_name,))
            element_exists = cursor.fetchone()

            cursor.execute('SELECT * FROM CombinedTable WHERE Rating=?', (oldrating,))
            rating_exists = cursor.fetchone()

            cursor.execute('SELECT * FROM CombinedTable WHERE SUbCategory=?', (oldsubCategory_name,))
            subCategory_exists = cursor.fetchone()

            cursor.execute('SELECT * FROM CombinedTable WHERE MaxRating=?', (oldMaxRating,))
            max_rating_exists = cursor.fetchone()

            # Build the flash message based on which fields do not exist
            error_messages = []
            if not sector_exists:
                error_messages.append(f"Business Sector '{oldbusiness_sector_name}' does not exist.")
            if not function_exists:
                error_messages.append(f"Business Function '{oldbusiness_function}' does not exist.")
            if not element_exists:
                error_messages.append(f"Measuring Element '{oldmeasuring_element_name}' does not exist.")
            if not rating_exists:
                error_messages.append(f"Rating '{oldrating}' does not exist.")
            if not subCategory_exists:
                error_messages.append(f"Sub Category '{oldsubCategory_name}' does not exist.")
            if not max_rating_exists:
                error_messages.append(f"Max Rating '{oldMaxRating}' does not exist.")

            # Flash all error messages
            for message in error_messages:
                flash(message, "error")

        else:
            # If the record exists, perform the update
            cursor.execute('''
                UPDATE CombinedTable
                SET BusinessSector=?, BusinessFunction=?, MeasuringElt=?, Rating=?, SUbCategory=?, MaxRating=?
                WHERE BusinessSector=? AND BusinessFunction=? AND MeasuringElt=? AND Rating=? AND SUbCategory=? AND MaxRating=?
            ''', (newbusiness_sector_name, newbusiness_function, newmeasuring_element_name, newrating, newsubCategory_name,
                  newMaxRating,
                  oldbusiness_sector_name, oldbusiness_function, oldmeasuring_element_name, oldrating, oldsubCategory_name,
                  oldMaxRating))

            connection.commit()

            # Flash success message
            flash(f"Record successfully updated for business sector: {newbusiness_sector_name}", "success")

        # Close the connection
        connection.close()

        # Redirect back to administrator page
        return redirect('/administrator')

    return render_template('administrator.html', user_name=user_name, business_sectors=business_sectors)



@app.route('/ratingAnswersBusinessFunctions', methods=['GET', 'POST'])
@login_required
def answerratingforbusinesssector():
    business_sectors = get_unique_business_sectors()
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
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
        flash('Record updated successfully', 'success')

        return redirect('/CombinedTiersForAll')

    return render_template('administrator.html', user_name=user_name, business_sectors=business_sectors)


# Updating the combined tiers
@app.route('/updateratingAnswersBusinessFunctions', methods=['GET', 'POST'])
@login_required
def Updateanswerrating():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    business_sectors = get_unique_business_sectors()
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
        
        flash('Record added successfully', 'success')

        # Commit changes and close connection
        connection.commit()
        connection.close()

        # Redirect back to administrator page
        return redirect('/administrator')

    return render_template('administrator.html', user_name=user_name, business_sectors=business_sectors)


# View all answer rating
@app.route('/view_all_answer_rating', methods=['GET', 'POST'])
@login_required
def viewAllAnswerRatings():
    business_sectors = get_unique_business_sectors()
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
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
                           unique_business_functions=unique_business_functions, user_name=user_name, business_sectors=business_sectors)


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

            # Flash success message
            flash('Answer rating deleted successfully.', 'success')

            # Redirect back to the page displaying combined data
            return redirect('/view_all_answer_rating')
        except Exception as e:
            # Flash error message if something goes wrong
            flash('Error occurred during deletion: ' + str(e), 'danger')
            return redirect('/view_all_answer_rating')
    else:
        return "Method Not Allowed"
    
    

# Value chain backend 
@app.route('/addinnewvaluechainrecord', methods=['GET', 'POST'])
@login_required
def addingManualValueChain():
    business_sectors = get_unique_business_sectors()
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    if request.method == 'POST':
        vc_business_sector = request.form['value_chain_business_sector_name']
        vc_business_function = request.form['value_chain_business_function']
        dvc_business_process = request.form['value_chain_business_process_name']
        vc_activities = request.form['value_chain_business_activities']
        vc_skills = request.form['value_chain_skills']
        vc_technology = request.form['value_chain_technology']

        connection = sqlite3.connect('DigitalMaturityDatabase.db')
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO ValueChain (BusinessSector, BusinessFunction, BusinessProcess, Activities, Skills, Technology)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (vc_business_sector, vc_business_function, dvc_business_process,
              vc_activities, vc_skills, vc_technology))
        connection.commit()
        connection.close()

        # Normalize the BusinessFunction column
        normalize_business_function()
        flash('Record added successfully into the value chain database', 'success')

        return redirect('/CombinedTiersForAll')

    return render_template('administrator.html', user_name=user_name, business_sectors=business_sectors)



# Update value chain records 
@app.route('/updateValueChainSkillsandTechnology', methods=['GET', 'POST'])
@login_required
def UpdateValueChainData():
    business_sectors = get_unique_business_sectors()
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    if request.method == 'POST':
        # Extract values from the form
        vc_bs = request.form['value_chain_business_sector_name']
        vc_bf = request.form['value_chain_business_function']
        vc_bp = request.form['value_chain_business_process_name']
        vc_ba = request.form['value_chain_business_activities']
        vc_ns = request.form['value_chain_new_skills']
        vc_nt = request.form['value_chain_new_technology']

        # Connect to the database
        connection = sqlite3.connect('DigitalMaturityDatabase.db')
        cursor = connection.cursor()

        # Check if the record exists
        cursor.execute('''
            SELECT * FROM ValueChain
            WHERE BusinessSector=? AND BusinessFunction=? AND BusinessProcess=? AND Activities=?
        ''', (vc_bs, vc_bf, vc_bp, vc_ba))
        record = cursor.fetchone()

        if record:
            # If the record exists, update it
            cursor.execute('''
                UPDATE ValueChain
                SET Skills=?, Technology=?
                WHERE BusinessSector=? AND BusinessFunction=? AND BusinessProcess=? AND Activities=?
            ''', (vc_ns, vc_nt, vc_bs, vc_bf, vc_bp, vc_ba))

            flash('Value chain record updated successfully', 'success')
            # Commit the changes
            connection.commit()

        else:
            # If the record does not exist, send a flash error message
            missing_record = f"Record with Business Sector '{vc_bs}', Function '{vc_bf}', Process '{vc_bp}', and Activities '{vc_ba}' does not exist."
            flash(missing_record, 'error')

        # Close the connection
        connection.close()

        # Redirect back to administrator page
        return redirect('/administrator')

    return render_template('administrator.html', user_name=user_name, business_sectors=business_sectors)

# Business process 
# Adding a business process 
@app.route('/addinnewbusinessprocessrecord', methods=['GET', 'POST'])
@login_required
def addingManualBusinessProcess():
    business_sectors = get_unique_business_sectors()
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    if request.method == 'POST':
        bp_business_sector = request.form['bp_business_sector_name']
        bp_business_function = request.form['bp_business_function']
        bp_business_process = request.form['bp_business_process_name']
        bp_activities = request.form['bp_business_activities']
        bp_resources = request.form['bp_resources']
        

        connection = sqlite3.connect('DigitalMaturityDatabase.db')
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO BusinessProcess (BusinessSector, BusinessFunction, BusinessProcess, Activities, BusinessResource)
            VALUES (?, ?, ?, ?, ?)
        ''', (bp_business_sector, bp_business_function, bp_business_process,
              bp_activities, bp_resources))
        connection.commit()
        connection.close()

        # Normalize the BusinessFunction column
        normalize_business_function()
        flash('Record added successfully into the business process database', 'success')

        return redirect('/CombinedTiersForAll')

    return render_template('administrator.html', user_name=user_name, business_sectors=business_sectors)

# Update business process 
@app.route('/updateBusinessProcessResource', methods=['GET', 'POST'])
@login_required
def UpdateBusinessProcessActivityResource():
    business_sectors = get_unique_business_sectors()
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    if request.method == 'POST':
        # Extract values from the form
        bp_bs = request.form['bp_business_sector_name']
        bp_bf = request.form['bp_business_function']
        bp_bp = request.form['bp_business_process_name']
        bp_oa = request.form['bp_old_business_activities']
        bp_or = request.form['bp_old_business_resources']
        bp_na = request.form['bp_old_business_resources']
        bp_nr = request.form['bp_new_business_resources']
        

        # Connect to the database
        connection = sqlite3.connect('DigitalMaturityDatabase.db')
        cursor = connection.cursor()

        # Check if the record exists
        cursor.execute('''
            SELECT * FROM BusinessProcess
            WHERE BusinessSector=? AND BusinessFunction=? AND BusinessProcess=? AND Activities=? AND BusinessResource=?  
        ''', (bp_bs, bp_bf, bp_bp, bp_oa, bp_or))
        record = cursor.fetchone()

        if record:
            # If the record exists, update it
            cursor.execute('''
                UPDATE BusinessProcess
                SET Activities=?, BusinessResource=?
                WHERE BusinessSector=? AND BusinessFunction=? AND BusinessProcess=? AND Activities=?
            ''', (bp_na, bp_nr, bp_bs, bp_bf, bp_bp, bp_oa))

            flash('Business Process record updated successfully', 'success')
            # Commit the changes
            connection.commit()

        else:
            # If the record does not exist, send a flash error message
            missing_record = f"Record with Business Sector '{bp_bs}', Function '{bp_bf}', Process '{bp_bp}', and Activities '{bp_oa}' does not exist in business process database."
            flash(missing_record, 'error')

        # Close the connection
        connection.close()

        # Redirect back to administrator page
        return redirect('/administrator')

    return render_template('administrator.html', user_name=user_name, business_sectors=business_sectors)




# Business_Manager_account
@app.route('/add_random_characters', methods=['GET', 'POST'])
@login_required
def add_random_characters_route():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    business_functions_data = {}  # Ensure this is a dictionary
    modified_word = None
    if request.method == 'POST':
        word = request.form['word']
        modified_word = add_random_characters(word)
    return render_template('manager.html', modified_word=modified_word, business_data=business_functions_data, user_name=user_name)




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




@app.route('/submit_unique_code', methods=['GET', 'POST'])
@login_required
def submitting_unique_code():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    error_message = None
    business_functions_data = {}  # Ensure this is a dictionary
    plot_images = []
    bar_plot_images = []
    growth_rate_images = []
    maturity_data = []
    pie_chart_as_is = None
    pie_chart_to_be = None
    feedback_data = []  # New list to hold feedback for MaturityAsIs and MaturityToBe

    if request.method == 'POST':
        unique_code = request.form['unique_code_user']

        # Retrieve the business sector from session
        business_sector = session.get('selected_business_sector')  # Ensure this matches your session key

        if unique_code:
            connection = sqlite3.connect('DigitalMaturityDatabase.db')
            cursor = connection.cursor()

            # Check if the unique code is associated with the business sector
            cursor.execute('''
                SELECT DISTINCT BusinessSector
                FROM UserSubmissionRecord
                WHERE UniqueCodeUser = ?
            ''', (unique_code,))
            code_sector = cursor.fetchone()

            if code_sector is None or code_sector[0] != business_sector:
                error_message = "This unique code is not for this sector."
                connection.close()
                return render_template('manager.html', error_message=error_message, business_data=business_functions_data)

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

            # Generate feedback for MaturityAsIs and MaturityToBe
            for record in maturity_data:
                maturity_type, business_function, maturity_as_is, maturity_to_be = record

                feedback_as_is = generate_feedback(maturity_as_is)
                feedback_to_be = generate_feedback(maturity_to_be)

                feedback_data.append({
                    'business_function': business_function,
                    'maturity_as_is': maturity_as_is,
                    'feedback_as_is': feedback_as_is,
                    'maturity_to_be': maturity_to_be,
                    'feedback_to_be': feedback_to_be,
                })

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
                        plt.plot(x_values, y_values, label=f'{labels[idx]} Growth Curve')

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
            business_functions = [record[1] for record in maturity_data]
            maturity_as_is_values = [record[2] for record in maturity_data]
            maturity_to_be_values = [record[3] for record in maturity_data]

            # Combine maturity_type and business_functions with a space
            labels = [f"{maturity} /n {function}" for maturity, function in zip(maturity_type, business_functions)]


            # Create pie chart for Maturity As-Is
            if maturity_as_is_values:
                plt.figure(figsize=(7, 7))
                plt.pie(maturity_as_is_values, labels=labels,
                        autopct=lambda p: '{:.0f}%'.format(p) if p > 0 else '')
                plt.title('Current State')

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                pie_chart_as_is = base64.b64encode(
                    buf.getvalue()).decode('utf-8')
                plt.close()

            # Create pie chart for Maturity To-Be
            if maturity_to_be_values:
                plt.figure(figsize=(12, 12))
                plt.pie(maturity_to_be_values, labels=labels,
                        autopct=lambda p: '{:.0f}%'.format(p) if p > 0 else '')
                plt.title('Future State')

                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                pie_chart_to_be = base64.b64encode(
                    buf.getvalue()).decode('utf-8')
                plt.close()

    return render_template('manager.html', error_message=error_message,
                           plot_images=plot_images, business_data=business_functions_data,
                           bar_plot_images=bar_plot_images, growth_rate_images=growth_rate_images,
                           maturity_data=maturity_data, pie_chart_as_is=pie_chart_as_is,
                           pie_chart_to_be=pie_chart_to_be, feedback_data=feedback_data, user_name=user_name)


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

def ClassifyingDigitalMaturity(business_sector, business_function_selected):
    prediction_label = None

    if business_sector and business_function_selected:
        try:
            # Encode using LabelEncoder
            Business_Sector_encoded = label_encoder_sector.transform([business_sector])[0]
            Business_Function_encoded = label_encoder_function.transform([business_function_selected])[0]

            # print("Encoded Business Sector:", Business_Sector_encoded)
            # print("Encoded Business Function:", Business_Function_encoded)

            # Prepare features and make a prediction
            features = np.array([[Business_Sector_encoded, Business_Function_encoded]])
            # print("Features passed to model:", features)

            prediction_encoded = Extra_Tree_model.predict(features)[0]
            # print("Encoded prediction from model:", prediction_encoded)

            # Inverse transform the prediction to get the categorical label
            prediction_label = label_encoder_prediction.inverse_transform([prediction_encoded])[0] + " Maturity"

        except ValueError as e:
            # print(f"ValueError encountered: {e}")
            # Handle unseen labels appropriately
            prediction_label = "Process Maturity"
        except Exception as e:
            # print(f"An unexpected error occurred: {e}")
            prediction_label = "Process Maturity"

    return prediction_label




# Value chain recommendation with improved plotting
@app.route('/recommendations_from_value_chain', methods=['POST'])
@login_required
def ValueChainRecommendation():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    business_functions_data = {}
    recommendations = []
    plot_image = None  # To store the plot image
    if request.method == 'POST':
        # Extract values from the form
        business_sector_name = session.get('business_sector')
        business_function = request.form['business_function_recomm']

        # Connect to the database
        connection = sqlite3.connect('DigitalMaturityDatabase.db')
        cursor = connection.cursor()

        # Fetch Skills and Technology from the ValueChain table based on Business Sector and Business Function
        cursor.execute('''
            SELECT BusinessProcess, Activities, Skills, Technology
            FROM ValueChain
            WHERE BusinessSector = ? AND BusinessFunction = ?
        ''', (business_sector_name, business_function))
        
        value_chain_data = cursor.fetchall()
        connection.close()

        if value_chain_data:
            business_processes = {}
            for process, activity, skills, technology in value_chain_data:
                if process not in business_processes:
                    business_processes[process] = {"activities": [], "skills": [], "technology": []}
                business_processes[process]["activities"].append(activity)
                business_processes[process]["skills"].append(skills)
                business_processes[process]["technology"].append(technology)

            # Create the hierarchical plot
            plt.figure(figsize=(20, 14))  # Increase the plot size for better clarity

            # Calculate positions for each node
            y_start = 0
            x_start = 0
            for process, elements in business_processes.items():
                activities = elements["activities"]
                skills = elements["skills"]
                technology = elements["technology"]
                
                # Plot Business Function
                plt.text(x_start + 0.5, y_start + 3, f'Business Function: {business_function}', ha='center', va='center', 
                         bbox=dict(facecolor='white', edgecolor='black'), wrap=True)

                # Plot Business Process
                plt.text(x_start + 1.5, y_start + 2.5, f'Business Process: {process}', ha='center', va='center', 
                         bbox=dict(facecolor='white', edgecolor='black'), wrap=True)

                for i, activity in enumerate(activities):
                    # Plot Business Activity
                    plt.text(x_start + 2.5, y_start + 2 - i*1.5, f'Business Activity: {activity}', ha='center', va='center', 
                             bbox=dict(facecolor='white', edgecolor='black'), wrap=True)
                    
                    # Plot Skills
                    plt.text(x_start + 3.5, y_start + 1.5 - i*1.5, f'Skills: {skills[i]}', ha='center', va='center', 
                             bbox=dict(facecolor='white', edgecolor='black'), wrap=True)
                    
                    # Plot Technology
                    plt.text(x_start + 4.5, y_start + 1.5 - i*1.5, f'Technology: {technology[i]}', ha='center', va='center', 
                             bbox=dict(facecolor='white', edgecolor='black'), wrap=True)

                    # Draw connections
                    plt.plot([x_start + 1.5, x_start + 2.5], [y_start + 2.5, y_start + 2 - i*1.5], 'k-', lw=1.5)
                    plt.plot([x_start + 2.5, x_start + 3.5], [y_start + 2 - i*1.5, y_start + 1.5 - i*1.5], 'k-', lw=1.5)
                    plt.plot([x_start + 3.5, x_start + 4.5], [y_start + 1.5 - i*1.5, y_start + 1.5 - i*1.5], 'k-', lw=1.5)

                y_start -= len(activities)  # Adjust y_start for the next process

            plt.axis('off')  # Turn off the axis

            # Save the plot to a bytes buffer and encode it as base64
            buf = io.BytesIO()
            plt.savefig(buf, format='png', bbox_inches='tight')  # Use 'bbox_inches' to avoid cutting off the plot
            buf.seek(0)
            plot_image = base64.b64encode(buf.getvalue()).decode('utf-8')
            plt.close()

    return render_template('managerRecommendations.html', recommendations=value_chain_data, plot_image=plot_image, business_data=business_functions_data, user_name=user_name)







# Mapping business processes
@app.route('/mapping_the_business_processes', methods=['GET', 'POST'])
def business_process_mapping():
    user_name = session.get('name', 'User')  # Retrieve the user's name from session
    Seclected_business_processes_for_mapping = []
    
    if request.method == 'POST':
        selected_business_sector = session.get('selected_business_sector', None)  # Fetch the business sector from session
        business_name_business_sector = request.form['business_function_user']

        # Ensure that both fields are not None before proceeding
        if selected_business_sector and business_name_business_sector:
            connection = sqlite3.connect('DigitalMaturityDatabase.db')
            cursor = connection.cursor()

            try:
                # Adjust the SQL query, ensure there are no syntax errors and columns are correct
                cursor.execute('''
                    SELECT BusinessProcess, Activities, BusinessResource
                    FROM ArrangingBusinessProcessIntoProperOrder
                    WHERE BusinessSector = ? AND BusinessFunction = ?
                ''', (selected_business_sector, business_name_business_sector))

                Seclected_business_processes_for_mapping = cursor.fetchall()
                connection.commit()

                print("These are the extracted business processes:", Seclected_business_processes_for_mapping)
            except sqlite3.OperationalError as e:
                print(f"SQL error occurred: {e}")
                flash(f"An error occurred while fetching data: {e}", 'danger')
            finally:
                connection.close()


        return redirect('/mapping_the_business_processes')

    # Render the template with the business process data if available
    return render_template('BusinessProcessMapping.html', user_name=user_name, business_process_map=Seclected_business_processes_for_mapping)

    





if __name__ == '__main__':
    app.run(debug=True) 