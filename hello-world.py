# # from flask import Flask, request, render_template
# # import os
# # from processors.asc_parser import parse_asc_teachers  # Parser for ASC timetable

# # app = Flask(__name__)

# # # Configure upload folder
# # UPLOAD_FOLDER = 'uploads'
# # if not os.path.exists(UPLOAD_FOLDER):
# #     os.makedirs(UPLOAD_FOLDER)
# # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # @app.route("/", methods=["GET", "POST"])
# # def upload_file():
# #     """
# #     Handles file uploads and displays teachers' names with gender.
# #     """
# #     if request.method == "POST":
# #         # Get form data
# #         timetable_format = request.form.get("format")
# #         file = request.files.get("file")

# #         # Validate inputs
# #         if not file or not timetable_format:
# #             return "Please select a file and format.", 400
# #         if not file.filename.endswith(".xml"):
# #             return "Only XML files are allowed.", 400

# #         # Save uploaded file
# #         save_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
# #         file.save(save_path)

# #         # Process teachers for ASC format only (other formats can be added)
# #         if timetable_format == "asc":
# #             teachers = parse_asc_teachers(save_path)
# #         else:
# #             return "Invalid format selected.", 400

# #         # Render results in HTML
# #         return render_template("upload.html", teachers=teachers)

# #     return render_template("upload.html", teachers=None)


# # if __name__ == "__main__":
# #     app.run(host="0.0.0.0", port=5000, debug=True)


# from flask import Flask, request, render_template
# import os
# from processors.asc_parser import parse_asc_teachers
# from processors.tk_parser import parse_tk_teachers
# from processors.untis_parser import parse_untis_teachers
# from gender_guesser.detector import Detector

# app = Flask(__name__)
# UPLOAD_FOLDER = "uploads"
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# gender_detector = Detector()

# @app.route("/", methods=["GET", "POST"])
# def upload_file():
#     teachers = None
#     if request.method == "POST":
#         file = request.files.get("file")
#         timetable_format = request.form.get("format")

#         if not file or not timetable_format:
#             return "Please select a file and format.", 400
#         if not file.filename.endswith(".xml"):
#             return "Only XML files are allowed.", 400

#         save_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
#         file.save(save_path)

#         if timetable_format == "asc":
#             teachers = parse_asc_teachers(save_path)
#         elif timetable_format == "tk":
#             teachers = parse_tk_teachers(save_path)
#         elif timetable_format == "untis":
#             teachers = parse_untis_teachers(save_path)
#         else:
#             return "Invalid timetable format selected.", 400

#         # Guess gender
#         teacher_with_gender = [
#             {"name": teacher, "gender": gender_detector.get_gender(teacher.split()[0])}
#             for teacher in teachers
#         ]

#         return render_template("upload.html", teachers=teacher_with_gender)

#     return render_template("upload.html", teachers=None)

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5000)
