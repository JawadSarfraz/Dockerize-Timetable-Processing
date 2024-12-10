import xml.etree.ElementTree as ET

def parse_asc_teachers(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    teachers = []
    for teacher in root.findall(".//teacher"):
        name = teacher.get("name")
        if name:
            teachers.append(name.strip())
    return teachers
