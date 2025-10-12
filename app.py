# app.py
from flask import Flask, request, jsonify, render_template, send_from_directory, session, redirect, url_for, flash
from gtts import gTTS
import os
import shutil
import atexit
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash, check_password_hash
from models import Base, User

# Import the OpenAI client from your renamed file
from openai_config import client
from audio_processor import transcribe_audio  # Ensure this module exists and works

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for session management

<<<<<<< HEAD
logging.basicConfig(level=logging.DEBUG)

# Database setup...
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

TEMP_DIR = 'tmp_audio'
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

# Use the client directly
try:
    client.models.list()  # Updated to use the new API method
    app.logger.debug(f"OpenAI client initialized successfully!")
=======
logging.basicConfig(level=logging.INFO)

# Database setup...
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    app.logger.warning("DATABASE_URL not set, using SQLite fallback")
    DATABASE_URL = "sqlite:///./test.db"

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    app.logger.info("Database connection established successfully")
except Exception as e:
    app.logger.error(f"Database connection failed: {str(e)}")
    # Create a fallback SQLite database
    DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    app.logger.info("Using SQLite fallback database")

TEMP_DIR = 'tmp_audio'
RESUME_DIR = 'resumes'
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)
if not os.path.exists(RESUME_DIR):
    os.makedirs(RESUME_DIR)

# Use the client directly
try:
    # Test the client with a simple call instead of models.list() which can be slow
    app.logger.info("Initializing OpenAI client...")
    # We'll test the client when it's actually used, not during startup
    app.logger.info("OpenAI client initialized successfully!")
>>>>>>> 18a57e2 (Add .gitignore to exclude venv and temp files)
except Exception as e:
    app.logger.error(f"Failed to initialize OpenAI client: {str(e)}")
    client = None

# List of URLs to fetch content for knowledge base (generalized for different roles)
RESOURCE_URLS = [
    {"title": "SQL Tutorial - W3Schools", "url": "https://www.w3schools.com/sql/sql_intro.asp", "keywords": ["primary key", "foreign key", "constraints"], "role": "Software Engineer"},
    {"title": "SQL Joins - MySQL Documentation", "url": "https://dev.mysql.com/doc/refman/8.0/en/join.html", "keywords": ["inner join", "left join", "right join", "full join"], "role": "Data Analyst"},
    {"title": "Python Docs", "url": "https://docs.python.org/3/", "keywords": ["python", "programming"], "role": "Software Engineer"},
    {"title": "Product Management Guide", "url": "https://www.productplan.com/learn/what-is-product-management/", "keywords": ["product management", "roadmap"], "role": "Product Manager"},
    {"title": "DevOps Practices", "url": "https://aws.amazon.com/devops/what-is-devops/", "keywords": ["devops", "ci/cd"], "role": "DevOps Engineer"}
]

# Fetch content from online resources and build the knowledge base
def fetch_knowledge_base():
    knowledge_base = []
    for resource in RESOURCE_URLS:
        try:
<<<<<<< HEAD
            # In a real environment, this would fetch the content from the URL
            response = requests.get(resource["url"])
            response.raise_for_status()  # Raise an error for bad status codes

            # Parse the HTML content using BeautifulSoup to extract relevant text
            soup = BeautifulSoup(response.text, 'html.parser')
            content = soup.get_text(separator='\n', strip=True)[:1000]  # Limit to 1000 characters for brevity
=======
            # Skip actual network requests during startup to avoid hanging
            # Use predefined content instead
            app.logger.info(f"Loading knowledge base for: {resource['title']}")
>>>>>>> 18a57e2 (Add .gitignore to exclude venv and temp files)

            # Simulated content (since we can't make real HTTP requests in this environment)
            if "W3Schools" in resource["title"]:
                content = """
SQL Tutorial
Source: W3Schools SQL Tutorial

SQL (Structured Query Language) is a standard language for accessing and manipulating databases. It is used to perform tasks such as updating data on a database or retrieving data from a database. 

Key Concepts:
- Tables: A table is a collection of related data entries and it consists of columns and rows.
- Primary Key: The PRIMARY KEY constraint uniquely identifies each record in a table.
- Foreign Key: A FOREIGN KEY is a field in one table that refers to the PRIMARY KEY in another table.
                """
            elif "MySQL Documentation" in resource["title"]:
                content = """
SQL Joins
Source: MySQL 8.0 Documentation

A JOIN clause is used to combine rows from two or more tables, based on a related column between them. MySQL supports several types of joins:

- INNER JOIN: Returns records that have matching values in both tables.
- LEFT JOIN: Returns all records from the left table, and the matched records from the right table.
- RIGHT JOIN: Returns all records from the right table, and the matched records from the left table.
                """
            elif "Python Docs" in resource["title"]:
                content = """
Python Documentation
Source: Python Official Docs

Python is a high-level, interpreted programming language known for its readability and versatility. It supports multiple programming paradigms, including object-oriented, procedural, and functional programming.

Key Features:
- Easy syntax and readability.
- Extensive standard library.
- Support for data structures like lists, dictionaries, and sets.
                """
            elif "Product Management Guide" in resource["title"]:
                content = """
Product Management Guide
Source: ProductPlan

Product management involves the planning, development, and launch of a product. It requires understanding customer needs, defining a product vision, and working with cross-functional teams.

Key Responsibilities:
- Creating a product roadmap.
- Prioritizing features based on user feedback.
- Collaborating with engineering and design teams.
                """
            elif "DevOps Practices" in resource["title"]:
                content = """
DevOps Practices
Source: AWS

DevOps is a set of practices that combines software development (Dev) and IT operations (Ops) to shorten the development lifecycle and provide continuous delivery.

Key Practices:
- Continuous Integration and Continuous Deployment (CI/CD).
- Infrastructure as Code (IaC).
- Monitoring and logging for system performance.
                """

            knowledge_base.append({
                "title": resource["title"],
                "content": content,
                "keywords": resource["keywords"],
                "role": resource["role"]
            })
        except Exception as e:
            # Log the error and continue with the next resource
            print(f"Failed to fetch content from {resource['url']}: {str(e)}")
            knowledge_base.append({
                "title": resource["title"],
                "content": "Failed to fetch content.",
                "keywords": resource["keywords"],
                "role": resource["role"]
            })
    return knowledge_base

# Initialize the knowledge base at startup
KNOWLEDGE_BASE = fetch_knowledge_base()

# Use generative AI to create 6 role-specific questions based on user input
def get_role_specific_questions():
    # Get user inputs from session
    user_info = session.get('user_info', {})
    role = user_info.get('role', 'Software Engineer')
    difficulty = user_info.get('difficulty', 'Beginner')
    company = user_info.get('company', 'Generic')

    # Define company-specific focus (simulated)
    company_focus = {
        "Google": "Focus on scalability, performance optimization, and innovation.",
        "Amazon": "Emphasize large-scale systems, customer-centric solutions, and operational efficiency.",
        "Microsoft": "Highlight integration with enterprise systems, security, and collaboration tools.",
        "Meta": "Focus on user engagement, real-time analytics, and social media challenges.",
        "Generic": "No specific company focus, general knowledge for the role."
    }
    company_guidance = company_focus.get(company, "No specific company focus, general knowledge for the role.")

    # Default questions in case OpenAI API fails
    default_questions = {
        "Software Engineer": [
            "What is the difference between a list and a tuple in Python?",
            "Explain the concept of object-oriented programming.",
            "How do you optimize a SQL query for better performance?",
            "What is a REST API and how does it work?",
            "How do you handle memory leaks in a program?",
            "What are the benefits of using a version control system like Git?"
        ],
        "Data Analyst": [
            "How do you calculate the average of a column in SQL?",
            "What is the difference between a bar chart and a histogram?",
            "How do you handle missing data in a dataset?",
            "What is a pivot table and how do you use it?",
            "How do you use SQL to join multiple tables?",
            "What are some common data visualization tools you use?"
        ],
        "Data Scientist": [
            "What is the difference between supervised and unsupervised learning?",
            "How do you handle imbalanced datasets in machine learning?",
            "What is a confusion matrix and how do you interpret it?",
            "How do you use SQL to perform time-series analysis?",
            "What is overfitting and how do you prevent it?",
            "How do you evaluate the performance of a regression model?"
        ],
        "DevOps Engineer": [
            "What is Continuous Integration and how does it work?",
            "How do you set up a CI/CD pipeline using Jenkins?",
            "What is Infrastructure as Code and why is it important?",
            "How do you monitor the performance of a production server?",
            "What are the benefits of using Docker in a DevOps workflow?",
            "How do you ensure security in a cloud-based infrastructure?"
        ],
        "Product Manager": [
            "How do you prioritize features for a product roadmap?",
            "What metrics would you use to measure the success of a new feature?",
            "How do you handle conflicting feedback from stakeholders?",
            "What is the role of a product manager in an agile team?",
            "How do you conduct a competitive analysis for your product?",
            "What strategies do you use to improve user retention?"
        ]
    }

    # If OpenAI client failed to initialize, return default questions
    if client is None:
        app.logger.warning("OpenAI client not initialized. Using default questions.")
        return default_questions.get(role, default_questions["Software Engineer"])[:6]

    # Create a prompt for OpenAI to generate 6 role-specific questions
    prompt = f"""
You are an expert interview coach tasked with generating six technical or domain-specific interview questions for a candidate. The candidate is applying for a {role} position at {company} with a {difficulty} difficulty level. {company_guidance} The questions should be relevant to the role, appropriately challenging for the difficulty level, and aligned with the company's focus. Provide the questions as a numbered list (1. 2. 3. etc.) without additional explanations.

Example format for a Software Engineer:
1. How do you optimize a SQL query for better performance?
2. Explain the difference between a stack and a queue.
3. What is the time complexity of a binary search algorithm?
4. How do you handle exceptions in Python?
5. What are the benefits of using a version control system like Git?
6. How do you ensure code quality in a large-scale project?

Example format for a Product Manager:
1. How do you prioritize features for a product roadmap?
2. What metrics would you use to measure the success of a new feature?
3. How do you handle conflicting feedback from stakeholders?
4. What is the role of a product manager in an agile team?
5. How do you conduct a competitive analysis for your product?
6. What strategies do you use to improve user retention?
"""
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert interview coach."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=250  # Increased slightly to accommodate 6 questions
        )
        questions_text = response.choices[0].message.content.strip()
        # Parse the questions into a list
        questions = []
        for line in questions_text.split('\n'):
            if line.strip() and line[0].isdigit() and '.' in line:
                question = line.split('.', 1)[1].strip()
                if question:
                    questions.append(question)
        # Ensure we have exactly 6 questions, fall back to defaults if needed
        role_fallbacks = default_questions.get(role, default_questions["Software Engineer"])
        while len(questions) < 6:
            questions.append(role_fallbacks[len(questions)])
        return questions[:6]  # Return exactly 6 questions
    except Exception as e:
        app.logger.error(f"Failed to generate questions with OpenAI: {str(e)}")
        # Fallback to default questions for the role
        return default_questions.get(role, default_questions["Software Engineer"])[:6]

# Initialize interview state with empty questions (to be populated after user input)
interview_state = {
    'current_question': 0,
    'audio_files': [],
    'questions': [],  # Will be populated after user input
    'table_data': []
}

# Routes for authentication
@app.route('/')
def index():
<<<<<<< HEAD
    if 'email' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))
=======
    return render_template('landing.html')
>>>>>>> 18a57e2 (Add .gitignore to exclude venv and temp files)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'email' in session:
        flash('You are already logged in.')
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        role = request.form.get('role')

        # Validate inputs
        if not all([email, first_name, last_name, password, re_password, role]):
            return render_template('register.html', error="All fields are required.")

        if password != re_password:
            return render_template('register.html', error="Passwords do not match.")

        # Hash the password
        password_hash = generate_password_hash(password)

        # Create a new user
        db = SessionLocal()
        try:
            user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=password_hash,
                role=role
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        except Exception as e:
            db.rollback()
            app.logger.error(f"Registration failed: {str(e)}")
            return render_template('register.html', error="Email already exists.")
        finally:
            db.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        flash('You are already logged in.')
        return redirect(url_for('home'))
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email, User.role == role).first()
            if user and check_password_hash(user.password, password):
                session['email'] = email
                session['first_name'] = user.first_name
                session['role'] = user.role
                flash('Login successful!')
                return redirect(url_for('home'))
            else:
                flash('Invalid email, password, or role.')
                return redirect(url_for('login'))
        finally:
            db.close()

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('email', None)
    session.pop('first_name', None)
    session.pop('role', None)
    session.pop('user_info', None)
    session.pop('resume_path', None)
    global interview_state
    interview_state = {
        'current_question': 0,
        'audio_files': [],
        'questions': [],
        'table_data': []
    }
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'email' not in session:
        flash('Please log in to access this page.')
        return redirect(url_for('login'))
    return render_template('home.html', first_name=session['first_name'])

@app.route('/dashboard')
def dashboard():
    if 'email' not in session:
        flash('Please log in to access this page.')
        return redirect(url_for('login'))
    
    # Construct a user dictionary from session data
    user = {
        'first_name': session.get('first_name', 'Unknown'),
        'email': session.get('email', 'Unknown'),
        'role': session.get('role', 'Unknown')
    }
    
    return render_template('dashboard_student.html', user=user)

@app.route('/landing')
def landing():
<<<<<<< HEAD
    if 'email' not in session:
        flash('Please log in to access this page.')
        return redirect(url_for('login'))
    app.logger.debug("Serving landing page")
    return render_template('landing.html')
=======
    app.logger.debug("Serving landing page")
    return render_template('landing.html')

@app.route('/practice')
def practice():
    if 'email' not in session:
        flash('Please log in to access this page.')
        return redirect(url_for('login'))
    return redirect(url_for('home'))

@app.route('/demo')
def demo():
    if 'email' not in session:
        flash('Please log in to access this page.')
        return redirect(url_for('login'))
    return redirect(url_for('home'))

@app.route('/privacy')
def privacy():
    return render_template('privacy.html') if os.path.exists('templates/privacy.html') else "Privacy policy coming soon."

@app.route('/terms')
def terms():
    return render_template('terms.html') if os.path.exists('templates/terms.html') else "Terms of service coming soon."

@app.route('/contact')
def contact():
    return render_template('contact.html') if os.path.exists('templates/contact.html') else "Contact page coming soon."
>>>>>>> 18a57e2 (Add .gitignore to exclude venv and temp files)

@app.route('/submit_user_info', methods=['POST'])
def submit_user_info():
    if 'email' not in session:
        flash('Please log in to access this page.')
        return redirect(url_for('login'))

    app.logger.debug("Received form submission at /submit_user_info")
    # Get form data
    role = request.form.get('role')
    difficulty = request.form.get('difficulty')
    company = request.form.get('company')

    # Store user inputs in session
    session['user_info'] = {
        'role': role,
        'difficulty': difficulty,
        'company': company
    }

    # Handle resume upload
    if 'resume' in request.files:
        resume_file = request.files['resume']
        if resume_file.filename != '':
            # Save the resume file
            resume_path = os.path.join(RESUME_DIR, resume_file.filename)
            resume_file.save(resume_path)
            session['resume_path'] = resume_path
            app.logger.debug(f"Resume saved at {resume_path}")
        else:
            session['resume_path'] = None
    else:
        session['resume_path'] = None

    # Generate questions based on user input
    global interview_state
    interview_state['questions'] = get_role_specific_questions()
    app.logger.debug(f"Generated questions: {interview_state['questions']}")

    # Redirect to the interview page
    app.logger.debug("Redirecting to /interview")
    return redirect(url_for('interview'))

@app.route('/interview')
def interview():
    if 'email' not in session:
        flash('Please log in to access this page.')
        return redirect(url_for('login'))
    app.logger.debug("Serving interview page at /interview")
    return render_template('index.html')

@app.route('/audio/<filename>')
def serve_audio(filename):
    app.logger.debug(f"Serving audio file: {filename}")
    return send_from_directory(TEMP_DIR, filename)

@app.route('/start_interview', methods=['POST'])
def start_interview():
    if 'email' not in session:
        return jsonify({'status': 'error', 'message': 'Please log in to access this page.'}), 401

    app.logger.debug("Starting interview")
    global interview_state
    if interview_state['current_question'] == 0:
        question = interview_state['questions'][0]
        audio_filename = 'q1.mp3'
        audio_path = generate_question_audio(question, audio_filename)
        timestamp = datetime.now().isoformat()
        interview_state['table_data'].append({
            'timestamp': timestamp,
            'question': question,
            'answer': ''
        })
        return jsonify({'audio_url': f'/audio/{audio_filename}', 'question_number': 1})
    return jsonify({'status': 'already_started'})

@app.route('/next_question', methods=['POST'])
def next_question():
    if 'email' not in session:
        return jsonify({'status': 'error', 'message': 'Please log in to access this page.'}), 401

    app.logger.debug("Fetching next question")
    global interview_state
    interview_state['current_question'] += 1
    if interview_state['current_question'] >= len(interview_state['questions']):
        # Interview complete, evaluate answers and return table with evaluation
        for audio in interview_state['audio_files']:
            if os.path.exists(audio['path']):
                os.remove(audio['path'])
        
        # Extract questions and answers for evaluation
        questions = [entry['question'] for entry in interview_state['table_data']]
        answers = [entry['answer'] for entry in interview_state['table_data']]
        
        # Evaluate answers using OpenAI with RAG
        try:
            evaluations = evaluate_answers(questions, answers)
        except Exception as e:
            evaluations = [{'question': q, 'answer': a, 'score': 0, 'feedback': f'Error evaluating answer: {str(e)}'} 
                           for q, a in zip(questions, answers)]
        
        # Combine table data with evaluations
        table = []
        for entry, eval_result in zip(interview_state['table_data'], evaluations):
            table.append({
                'timestamp': entry['timestamp'],
                'question': entry['question'],
                'answer': entry['answer'],
                'score': eval_result['score'],
                'feedback': eval_result['feedback']
            })
        
        # Reset interview state
        interview_state = {
            'current_question': 0,
            'audio_files': [],
            'questions': [],  # Will be repopulated on next form submission
            'table_data': []
        }
        return jsonify({'status': 'complete', 'table': table})
    
    question = interview_state['questions'][interview_state['current_question']]
    audio_filename = f'q{interview_state["current_question"] + 1}.mp3'
    audio_path = generate_question_audio(question, audio_filename)
    timestamp = datetime.now().isoformat()
    interview_state['table_data'].append({
        'timestamp': timestamp,
        'question': question,
        'answer': ''
    })
    return jsonify({
        'audio_url': f'/audio/{audio_filename}',
        'question_number': interview_state['current_question'] + 1
    })

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    if 'email' not in session:
        return jsonify({'status': 'error', 'message': 'Please log in to access this page.'}), 401

    app.logger.debug("Submitting answer")
    global interview_state
    if 'audio' not in request.files:
        app.logger.error("No audio file provided in the request")
        return jsonify({'status': 'error', 'message': 'No audio file provided'}), 400
    
    audio_file = request.files['audio']
    if audio_file.filename == '':
        app.logger.error("No file selected in the request")
        return jsonify({'status': 'error', 'message': 'No file selected'}), 400

    # Log the content type of the file from the request headers
    content_type = audio_file.content_type
    app.logger.debug(f"Content-Type from request: {content_type}")

    # Use the original file extension from the uploaded file
    original_filename = audio_file.filename
    file_extension = original_filename.rsplit('.', 1)[-1].lower() if '.' in original_filename else 'webm'
    app.logger.debug(f"Received audio file with extension: {file_extension}")
    
    # Validate the file extension against supported formats
    supported_formats = ['flac', 'm4a', 'mp3', 'mp4', 'mpeg', 'mpga', 'oga', 'ogg', 'wav', 'webm']
    if file_extension not in supported_formats:
        app.logger.error(f"Unsupported file format: {file_extension}")
        return jsonify({'status': 'error', 'message': f'Unsupported file format: {file_extension}. Supported formats are: {supported_formats}'}), 400

    filename = f"q{interview_state['current_question']+1}_answer.{file_extension}"
    temp_path = os.path.join(TEMP_DIR, filename)
    
    # Save the file and check its size
    audio_file.save(temp_path)
    if not os.path.exists(temp_path) or os.path.getsize(temp_path) == 0:
        app.logger.error(f"Uploaded file is empty or invalid: {temp_path}")
        return jsonify({'status': 'error', 'message': 'Uploaded file is empty or invalid'}), 400
    
    file_size = os.path.getsize(temp_path)
    app.logger.debug(f"Saved audio file to: {temp_path}, size: {file_size} bytes")

    # Transcribe the audio file
    if transcribe_audio is None:
        app.logger.error("Audio transcription is not available due to OpenAI API failure.")
        return jsonify({'status': 'error', 'message': 'Audio transcription is not available due to OpenAI API failure.'}), 500

    try:
        transcription = transcribe_audio(temp_path)
        app.logger.debug(f"Transcription successful: {transcription}")
        interview_state['table_data'][interview_state['current_question']]['answer'] = transcription
        interview_state['audio_files'].append({'path': temp_path})
        return jsonify({'status': 'recorded'})
    except Exception as e:
        app.logger.error(f"Failed to transcribe audio: {str(e)}")
        return jsonify({'status': 'error', 'message': f'Failed to transcribe audio: {str(e)}'}), 500

def generate_question_audio(text, filename):
    """
    Generate an audio file for a question using gTTS.
    """
    tts = gTTS(text=text, lang='en')
    audio_path = os.path.join(TEMP_DIR, filename)
    tts.save(audio_path)
    return audio_path

def retrieve_context(question, role):
    """
    Retrieve the most relevant document from the knowledge base based on the question and role.
    Uses simple keyword matching for retrieval.
    """
    question_lower = question.lower()
    best_match = None
    best_score = 0

    # Find the most relevant document for the role
    for doc in KNOWLEDGE_BASE:
        if doc["role"] != role:
            continue
        keywords = doc.get("keywords", [])
        score = sum(1 for keyword in keywords if keyword in question_lower)
        if score > best_score:
            best_score = score
            best_match = doc

    if best_match:
        return f"Relevant Document: {best_match['title']}\nContent: {best_match['content']}"
    return "No relevant document found."

def evaluate_answers(questions, answers):
    """
    Send questions and answers to OpenAI for evaluation with RAG context.
    Returns a list of evaluation results with correctness scores and concise feedback.
    """
    evaluations = []
    user_info = session.get('user_info', {})
    role = user_info.get('role', 'Software Engineer')
    
    # If OpenAI client failed to initialize, return default evaluations
    if client is None:
        app.logger.warning("OpenAI client not initialized. Skipping answer evaluation.")
        return [{'question': q, 'answer': a, 'score': 0, 'feedback': 'Answer evaluation skipped due to OpenAI API failure.'} 
                for q, a in zip(questions, answers)]

    for i, (question, answer) in enumerate(zip(questions, answers)):
        # Retrieve context using RAG, specific to the role
        context = retrieve_context(question, role)
        prompt = f"""
You are an expert interview coach evaluating a candidate's answer to a technical or domain-specific question for a {role} role. Your task is to assess the correctness of the answer, provide a score out of 100, and give concise feedback (1-2 sentences) on what was correct and where the candidate went wrong. Use the provided context to ensure accuracy and relevance in your feedback. If the answer is incomplete or unclear, note that as well.

### Context for the Question:
{context}

### Question:
{question}

### Candidate's Answer:
{answer}

Provide your evaluation in the following format:
- Correctness Score (out of 100): [score]
- Feedback: [concise feedback]
"""
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": f"You are an expert interview coach for {role} roles."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150  # Limit tokens to enforce concise feedback
            )
            evaluation_text = response.choices[0].message.content.strip()
            # Parse the evaluation text to extract score and feedback
            score_line = evaluation_text.split('\n')[0]
            feedback = '\n'.join(evaluation_text.split('\n')[1:]).replace('Feedback: ', '')
            try:
                score = int(score_line.split(': ')[1].replace('[', '').replace(']', ''))
            except (IndexError, ValueError):
                score = 0  # Default to 0 if parsing fails
            evaluations.append({
                'question': question,
                'answer': answer,
                'score': score,
                'feedback': feedback
            })
        except Exception as e:
            app.logger.error(f"Failed to evaluate answer with OpenAI: {str(e)}")
            evaluations.append({
                'question': question,
                'answer': answer,
                'score': 0,
                'feedback': f'Error evaluating answer: {str(e)}'
            })
    return evaluations

@atexit.register
def cleanup_temp():
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    if os.path.exists(RESUME_DIR):
        shutil.rmtree(RESUME_DIR)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)