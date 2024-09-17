from flask import Blueprint, request, jsonify
from firebase_admin import storage
from .models import Upload
from . import db

upload = Blueprint('upload', __name__)

@upload.route('/upload', methods=['POST'])
def upload_file():
    # Extract form data
    title = request.form.get('title')
    isbn = request.form.get('isbn')
    file = request.files['file']
    file_type = request.form.get('filetype')
    author = request.form.get('author')
    publisher = request.form.get('publisher')
    year = request.form.get('year')
    department = request.form.get('department')

    # Upload file to Firebase Storage
    bucket = storage.bucket()
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file)

    # Make the file public and get the URL
    blob.make_public()
    file_url = blob.public_url

    # Save file metadata to the database
    new_upload = Upload(
        title=title,
        isbn=isbn,
        file_url=file_url,
        file_type=file_type,
        author=author,
        publisher=publisher,
        year=year,
        department=department
    )
    db.session.add(new_upload)
    db.session.commit()

    return jsonify({'message': 'File successfully uploaded', 'url': file_url}), 201
