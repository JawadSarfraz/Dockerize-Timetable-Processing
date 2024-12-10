import xml.etree.ElementTree as ET

def parse_tk_teachers(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    teachers = []
    for teacher in root.findall(".//teacher", namespaces={"": "https://www.tks.eu/iphis/xsd/export"}):
        firstname = teacher.get("firstName", "").strip()
        lastname = teacher.get("lastName", "").strip()
        if firstname and lastname:
            teachers.append(f"{firstname} {lastname}")
    return teachers
