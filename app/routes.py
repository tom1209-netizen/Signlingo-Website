# Import from library
from flask import render_template, request, redirect, url_for, jsonify, session, flash, g
from flask_mail import Message
import random
import string
from datetime import datetime, timedelta
from keras.models import load_model
import tempfile
import os
import cv2

# Import from package
# Import database, mail
from app.database_models import User
from app import app, db, mail

# Import video data
from app.video_data import video_data_en, video_data_vn, get_video_data

# Import model, classifying function, custom layer
from app.classification_model import classify_video, classes

# Model
# Load the model
model_filename = "LSTM_preprocess.h5"
model_path = os.path.join(app.root_path, "static", "saved model", model_filename)

lstm_model = load_model(model_path)


@app.context_processor
def inject_user_status():
    user_is_logged_in = session.get('user_is_logged_in', False)
    return dict(user_is_logged_in=user_is_logged_in)


@app.route('/', methods=['GET'])
@app.route('/home', methods=['GET'])
def home_page():
    return render_template('home.html')


@app.route('/course_en')
def course_page_en():
    return render_template("course_en.html")


@app.route('/course_vn')
def course_page_vn():
    return render_template("course_vn.html")


@app.route('/library')
def library_page():
    return render_template("library.html")


@app.route('/faq')
def faq_page():
    return render_template("faq.html")


@app.route('/contribution')
def contribution_page():
    return render_template("contribution.html")


@app.route('/about')
def about_page():
    return render_template("aboutus.html")


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        # Get the submitted login form data
        email = request.form['email']
        password = request.form['password']

        # Query the database to check if the email exists
        user = User.query.filter_by(email=email).first()

        if user and user.password == password:
            # Successful login, you can redirect the user to a dashboard or home page
            session['user_id'] = user.id

            session['user_is_logged_in'] = True

            return redirect(url_for('home_page'))
        else:
            # Invalid credentials, show an error message on the login page
            return render_template('login.html', error="Invalid email or password")

    # For GET requests, simply render the login page
    return render_template('login.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'POST':
        try:
            # Retrieve form data from the request
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            full_name = request.form['full_name']
            phone_number = request.form['phone_number']

            if User.check_email_exists(email):
                # Email already exists, handle the situation (e.g., show an error message)
                return render_template("signup.html", error="Email already exists. Please use a different email")

            # Check if the username already exists in the database
            if User.check_username_exists(username):
                # Username already exists
                if User.check_email_exists(email):  # Check if the email also exists
                    # Both email and username exist, handle the situation
                    return render_template("signup.html", error="Email and username already exist. Please login.")
                else:
                    # Only the username exists, handle the situation
                    return render_template("signup.html", error="Username already exists. Please choose a different "
                                                                "username.")

            # Create a new User object
            new_user = User(
                username=username,
                email=email,
                password=password,
                full_name=full_name,
                phone_number=phone_number
            )

            # Save the User object to the database
            db.session.add(new_user)
            db.session.commit()

            # Send a welcome email to the new user
            welcome_message = f"Hello {full_name},\n\nThank you for registering an account with us!"
            msg = Message("Welcome to Our Website", recipients=[email])
            msg.body = welcome_message
            mail.send(msg)

            # Redirect the user to the login page after successful signup
            return render_template("signup.html", success="Account registered, please go to login page to login")
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return render_template("signup.html")


@app.route('/logout')
def logout_page():
    session.clear()
    return redirect(url_for('login_page'))


# Reset password

# Generate a random token for password reset
def generate_reset_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))


@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            token = generate_reset_token()
            user.reset_token = token
            user.reset_token_expiration = datetime.utcnow() + timedelta(hours=1)
            db.session.commit()

            # Send reset email
            msg = Message('Password Reset Request', recipients=[user.email])
            msg.body = f"Click the following link to reset your password: {url_for('reset_password', token=token, _external=True)}"
            mail.send(msg)

            return redirect(url_for('login_page'))

    return render_template('forgot_password.html')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    user = User.query.filter_by(reset_token=token).first()
    if user and user.reset_token_expiration > datetime.utcnow():
        if request.method == 'POST':
            new_password = request.form['new_password']
            user.password = new_password
            user.reset_token = None
            user.reset_token_expiration = None
            db.session.commit()

            flash('Your password has been reset successfully. You can now log in with your new password.', 'success')
            return redirect(url_for('login_page'))

        return render_template('reset_password.html', token=token)

    flash('Invalid or expired reset token.', 'danger')
    return redirect(url_for('forgot_password'))


# Camera logic
@app.route('/camera')
def camera_page():
    return render_template("cam.html")


@app.route('/get_result')
def get_result():
    result = session.get('result', 'none')
    return jsonify({'result': result})


@app.route('/process_video', methods=['POST'])
def process_video():
    if 'video' not in request.files:
        return jsonify({'error': 'No video found'}), 400

    video_file = request.files['video']

    # Save the video file temporarily to a temporary directory
    temp_dir = tempfile.mkdtemp()
    temp_video_path = os.path.join(temp_dir, 'temp_video.mp4')
    video_file.save(temp_video_path)

    # Open the video file using OpenCV's VideoCapture
    cap = cv2.VideoCapture(temp_video_path)

    # Read video frames and store them in a list
    video_frames = []
    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            print("Error: Failed to capture frame.")
            break

        video_frames.append(frame)

    cap.release()

    # Perform video classification
    index = classify_video(video_frames, lstm_model)
    result = classes[index]

    print(result)

    # Delete the temporary video file and directory
    os.remove(temp_video_path)
    os.rmdir(temp_dir)

    session['result'] = result

    return jsonify(result)


@app.route('/Leaderboard')
def ranking_page():
    return render_template("bxh.html")


@app.route('/chart')
def chart_page():
    return render_template("charts.html")


@app.route('/users')
def user_page():
    if 'user_id' in session:  # Check if user_id exists in the session
        user_id = session['user_id']
        user = User.query.get(user_id)  # Retrieve the user from the database using the user_id
        if user:
            return render_template('users-profile.html', user=user)
    return redirect(url_for('login_page'))


# Course video
@app.route('/video_by_topic/<string:language>/<string:topic>')
def video_by_topic(language, topic):
    global video_data, video_language
    video_language = language
    video_data = get_video_data(language)

    if topic in video_data:
        topic_videos = video_data[topic]
        first_video_id = topic_videos[0]['id']
        return redirect(url_for('video', video_id=first_video_id))
    print(topic)
    return "Topic not found"


@app.route('/video/<int:video_id>')
def video(video_id):
    for topic, topic_videos in video_data.items():
        for index, video in enumerate(topic_videos):
            if video['id'] == video_id:
                current_index = index + 1
                total_videos = len(topic_videos)
                prev_video_id = topic_videos[index - 1]['id'] if index > 0 else None
                next_video_id = topic_videos[index + 1]['id'] if index < len(topic_videos) - 1 else None
                topic_name = topic
                return render_template('video.html',
                                       video=video,
                                       prev_video_id=prev_video_id,
                                       next_video_id=next_video_id,
                                       current_index=current_index,
                                       total_videos=total_videos,
                                       topic_name=topic_name,
                                       language=video_language)

    return "Video not found"


@app.route('/communities')
def communities_page():
    return render_template("communities.html")


@app.route('/social-culture')
def social_culture_page():
    return render_template("social-culture.html")


@app.route('/document')
def document_page():
    return render_template("document.html")


@app.route('/upgrade')
def upgrade_page():
    return render_template("upgrade.html")


@app.route('/quiz_home')
def quiz_home():
    return render_template("quiz_home.html")

@app.route('/quiz')
def quiz_page():
    return render_template("quiz.html")






