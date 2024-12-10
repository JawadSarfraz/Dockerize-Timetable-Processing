from flask import Flask, request, render_template
import os
from processors.asc_parser import parse_asc_teachers  # Parser for ASC timetable

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def upload_file():
    """
    Handles file uploads and displays teachers' names with gender.
    """
    if request.method == "POST":
        # Get form data
        timetable_format = request.form.get("format")
        file = request.files.get("file")

        # Validate inputs
        if not file or not timetable_format:
            return "Please select a file and format.", 400
        if not file.filename.endswith(".xml"):
            return "Only XML files are allowed.", 400

        # Save uploaded file
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(save_path)

        # Process teachers for ASC format only (other formats can be added)
        if timetable_format == "asc":
            teachers = parse_asc_teachers(save_path)
        else:
            return "Invalid format selected.", 400

        # Render results in HTML
        return render_template("upload.html", teachers=teachers)

    return render_template("upload.html", teachers=None)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
