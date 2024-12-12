from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
import xml.etree.ElementTree as ET
from gender_guesser.detector import Detector

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/teachers_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
detector = Detector()

# Teacher Model
class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    ref_id = db.Column(db.String(50), nullable=True)

# Parsing Functions
def parse_asc_teachers(file_path):
    teachers = []
    tree = ET.parse(file_path)
    root = tree.getroot()
    for teacher in root.findall(".//teacher"):
        ref_id = teacher.get("id")
        first_name = teacher.get("firstname", "").strip()
        last_name = teacher.get("lastname", "").strip()
        name = f"{first_name} {last_name}".strip()
        teachers.append({"name": name, "ref_id": ref_id})
    return teachers

def parse_tk_teachers(file_path):
    teachers = []
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Namespace handling
    namespace = {'ns': 'https://www.tks.eu/iphis/xsd/export'}
    
    for teacher in root.findall(".//ns:teacher", namespace):
        ref_id = teacher.get("uuid")
        first_name = teacher.get("firstName", "").strip()
        last_name = teacher.get("lastName", "").strip()
        name = f"{first_name} {last_name}".strip()
        
        # Debugging: Print the first name before guessing
        print(f"Processing Name: {first_name}")
        
        # Guess gender using gender_guesser
        print(first_name)       # Expected: male
        print(detector.get_gender("Alice"))     # Expected: female
        print(detector.get_gender("Babette"))   # Check if it works for names in your list
        print(detector.get_gender("Gerhard"))   
        gender_guess = detector.get_gender(first_name) if first_name else "unknown"
        
        # Debugging: Print the gender guess result
        print(f"First Name: {first_name}, Gender Guess: {gender_guess}")
        
        # Map gender_guess to Male/Female/Unknown
        if gender_guess in ["male", "mostly_male"]:
            gender = "Male"
        elif gender_guess in ["female", "mostly_female"]:
            gender = "Female"
        else:
            gender = "Unknown"

        # Debugging: Print the final mapped gender
        print(f"Final Gender for '{first_name}': {gender}")
        
        # Append to teachers list
        teachers.append({"name": name, "ref_id": ref_id, "gender": gender})
    
    return teachers


def parse_untis_teachers(file_path):
    teachers = []
    tree = ET.parse(file_path)
    root = tree.getroot()
    namespace = {'ns': 'https://untis.at/untis/XmlInterface'}
    for teacher in root.findall(".//ns:teacher", namespace):
        ref_id = teacher.get("id")
        name = teacher.get("name", "").strip()
        teachers.append({"name": name, "ref_id": ref_id})
    return teachers

@app.route("/", methods=["GET", "POST"])
def upload_file():
    teachers = []
    if request.method == "POST":
        file = request.files.get("file")
        timetable_format = request.form.get("format")

        if not file or not timetable_format:
            return "Please select a file and format.", 400

        # Save the file
        save_path = os.path.join("uploads", file.filename)
        os.makedirs("uploads", exist_ok=True)
        file.save(save_path)

        # Parse teachers
        if timetable_format == "asc":
            teachers = parse_asc_teachers(save_path)
        elif timetable_format == "tk":
            teachers = parse_tk_teachers(save_path)
        elif timetable_format == "untis":
            teachers = parse_untis_teachers(save_path)
        else:
            return "Invalid format selected.", 400

        # Save teachers to the database
        for teacher in teachers:
            name = teacher.get("name", "Unknown")
            ref_id = teacher.get("ref_id", "None")
            gender = teacher.get("gender", "Unknown")

            # Add to the database
            db_teacher = Teacher(name=name, gender=gender, ref_id=ref_id)
            db.session.add(db_teacher)

        db.session.commit()

    # Retrieve teachers from the database
    teachers = Teacher.query.all()
    return render_template("upload.html", teachers=teachers)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
