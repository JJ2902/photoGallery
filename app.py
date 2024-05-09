from flask import Flask, render_template,request, redirect,send_from_directory # Importing the Flask class from the flask module
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)  # Creating an instance of the Flask class
import os
# Set the URI for the database that SQLAlchemy will connect to.
# Here, it's using SQLite with the database file named 'database.db'.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

# Disable SQLAlchemy's modification tracking, which can improve performance.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set the path where uploaded files will be stored.
# Specify a folder named 'uploads' where uploaded files will be saved.
# This is often used in web applications to specify where files uploaded by users should be stored on the server.
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')  # Associating the index() function with the root URL ('/')
def index():  # The index function that will be executed when the user visits the root URL
    files = File.query.all()
    return render_template('index.html',files=files) 

@app.route('/uploads', methods=['POST'])
def uploads():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_file = File(filename = filename)
            db.session.add(new_file)
            db.session.commit()
            return redirect('/')
    return 'something wrong. Please try again'

@app.route('/uploaded_file/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/download/<int:file_id>')
def download(file_id):
    file= File.query.get_or_404(file_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'], file.filename, as_attachment=True)

@app.route('/delete/<int:file_id>')
def delete(file_id):
    file= File.query.get_or_404(file_id)
    filename = file.filename

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    os.remove(file_path)

    db.session.delete(file)
    db.session.commit()
    return redirect('/')


    return send_from_directory(app.config['UPLOAD_FOLDER'], file.filename, as_attachment=True)

if __name__ == "__main__":  # Checking if the script is being run directly
    # app.run(debug=True)  # Starting the Flask development server in debug mode
    app.run(host='0.0.0.0', debug=False)