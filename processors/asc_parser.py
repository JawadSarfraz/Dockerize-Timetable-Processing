import xml.etree.ElementTree as ET
from gender_guesser.detector import Detector

# Initialize gender detector
detector = Detector(case_sensitive=False)

def parse_asc_teachers(file_path):
    """
    Parses teachers from ASC timetable XML file and guesses their gender.

    Args:
        file_path (str): Path to the uploaded ASC XML file.

    Returns:
        list: List of dictionaries with "name" and "gender".
    """
    teachers = []

    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract all teacher elements and attributes
    for teacher in root.findall(".//teachers/teacher"):
        firstname = teacher.get("firstname", "").strip()
        lastname = teacher.get("lastname", "").strip()

        # Combine first and last name
        if firstname or lastname:
            full_name = f"{firstname} {lastname}".strip()

            # Guess gender using the first name
            gender = detector.get_gender(firstname)
            if gender in ["male", "mostly_male"]:
                gender = "Male"
            elif gender in ["female", "mostly_female"]:
                gender = "Female"
            else:
                gender = "Unknown"

            # Add the teacher name and gender to the list
            teachers.append({"name": full_name, "gender": gender})

    return teachers
