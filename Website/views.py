from flask import Flask,Blueprint,render_template,url_for,request,redirect,flash
from flask_login import login_required as lr
from .models import User,Upload
from flask_login import current_user
from werkzeug.security import generate_password_hash
from . import db
import os 
import json 

views = Blueprint('views', __name__)

@views.route('/')
@lr
def home():
    user = current_user
    
    # Fetch all documents from the database
    document_db = Upload.query.all()
    
    # Path to the JSON file
    json_file_path = os.path.join( 'document.json')
    
    # Load and parse JSON file
    with open(json_file_path, 'r') as json_file:
        document_json = json.load(json_file)
    
    # Combine the JSON data with the database documents
    # Assuming that the structure of both is similar, e.g., a list of dictionaries or objects
    all_documents = document_db + document_json
    print(all_documents)
    
    return render_template('/Home/index.html', user=user, documents=all_documents)

@views.route('/profile',methods=['GET','POST'])
@lr
def profile_page():
    user = User.query.get(current_user.id)
    return render_template('Profile/index.html', user=user)

@views.route('/change_password', methods=['GET','POST'])
@lr
def change_password():
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    

    if new_password != confirm_password:
        flash('Passwords do not match!', 'danger')
        return redirect(url_for('profile.profile_page'))

    current_user.password_hash = generate_password_hash(new_password)
    current_user.password_changed = True
    db.session.commit()
    
    flash('Password changed successfully!', 'success')
    return redirect(url_for('views.profile_page'))

@views.route('/borrowed_book')
@lr
def borrowed_book():
    return render_template('Borrow/index.html')
