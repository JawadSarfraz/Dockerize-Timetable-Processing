from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from processors.asc_parser import parse_asc_teachers
from processors.tk_parser import parse_tk_teachers
from processors.untis_parser import parse_untis_teachers
from gender_guesser.detector import Detector

app = Flask(__name__)

# Configure SQLAlchemy with MySQL database
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
        file.save(save_path)

        # Parse teachers
        if timetable_format == "asc":
            teachers = parse_asc_teachers(save_path)
        elif timetable_format == "tk":
            teachers = parse_tk_teachers(save_path)
        elif timetable_format == "untis":
            teachers = parse_untis_teachers(save_path)

        # Save to database
        for teacher in teachers:
            gender = detector.get_gender(teacher.split()[0])
            gender = "Male" if gender in ["male", "mostly_male"] else "Female" if gender in ["female", "mostly_female"] else "Unknown"
            db_teacher = Teacher(name=teacher, gender=gender)
            db.session.add(db_teacher)

        db.session.commit()

    # Retrieve teachers from database
    teachers = Teacher.query.all()
    return render_template("upload.html", teachers=teachers)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
