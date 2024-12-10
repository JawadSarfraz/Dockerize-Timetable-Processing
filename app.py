from flask import Flask, request, render_template
import os
from processors.asc_parser import parse_asc_teachers
from processors.tk_parser import parse_tk_teachers
from processors.untis_parser import parse_untis_teachers
from gender_guesser.gender_guesser import detect_gender

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        timetable_format = request.form.get("format")
        file = request.files.get("file")

        if not file or not timetable_format:
            return "Please select a file and format.", 400

        if not file.filename.endswith(".xml"):
            return "Only XML files are allowed.", 400

        # Save the file
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(save_path)

        # Parse teachers based on format
        if timetable_format == "asc":
            teachers = parse_asc_teachers(save_path)
        elif timetable_format == "tk":
            teachers = parse_tk_teachers(save_path)
        elif timetable_format == "untis":
            teachers = parse_untis_teachers(save_path)
        else:
            return "Invalid format selected.", 400

        # Detect gender for each teacher
        teacher_with_gender = [
            {"name": teacher, "gender": detect_gender(teacher.split()[0])}
            for teacher in teachers
        ]

        return render_template("upload.html", teachers=teacher_with_gender)

    return render_template("upload.html", teachers=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
