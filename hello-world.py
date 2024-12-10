from flask import Flask, request, render_template
import os
from processors.xml_processor import extract_teachers  # Import processing logic

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part", 400

        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400

        if file and file.filename.endswith(".xml"):
            # Save the uploaded file
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(save_path)

            # Process the file to extract teachers
            teachers = extract_teachers(save_path)

            # Display teachers
            if teachers:
                return render_template("upload.html", teachers=teachers)
            else:
                return "No teachers found or invalid XML file.", 400
        else:
            return "Only XML files are allowed!", 400

    return render_template("upload.html", teachers=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
