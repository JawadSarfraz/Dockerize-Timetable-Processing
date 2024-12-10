import xml.etree.ElementTree as ET

def parse_untis_teachers(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    teachers = []
    for teacher in root.findall(".//teacher", namespaces={"": "https://untis.at/untis/XmlInterface"}):
        name = teacher.get("name", "").strip()
        if name:
            teachers.append(name)
    return teachers
