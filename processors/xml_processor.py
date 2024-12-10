import xml.etree.ElementTree as ET

def extract_teachers(file_path):
    """
    Parse XML file and extract all teachers' first and last names.
    :param file_path: Path to the uploaded XML file.
    :return: List of teacher names.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        teachers = []
        for teacher in root.findall(".//teacher"):
            firstname = teacher.get("firstname", "").strip()
            lastname = teacher.get("lastname", "").strip()
            fullname = f"{firstname} {lastname}".strip()
            if fullname:  # Ignore empty names
                teachers.append(fullname)

        return teachers
    except ET.ParseError as e:
        print(f"Error parsing XML file: {e}")
        return []
