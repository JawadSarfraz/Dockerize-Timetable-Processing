def parse_asc_teachers(file_path):
    """
    Parse teachers from ASC timetable export.
    Expects <teacher> tags with 'id', 'firstname', and 'lastname' attributes.
    """
    teachers = []
    tree = ET.parse(file_path)
    root = tree.getroot()

    for teacher in root.findall(".//teacher"):
        ref_id = teacher.get("id", "None")  # Use 'id' attribute as reference ID
        firstname = teacher.get("firstname", "").strip()
        lastname = teacher.get("lastname", "").strip()
        name = f"{firstname} {lastname}".strip()  # Combine first and last names

        if name:  # Ensure name is not empty
            teachers.append({"name": name, "ref_id": ref_id})
    return teachers