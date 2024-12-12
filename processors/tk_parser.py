def parse_tk_teachers(file_path):
    """
    Parse teachers from TK timetable export.
    Expects <teacher> tags with 'uuid', 'firstName', and 'lastName' attributes.
    """
    teachers = []
    tree = ET.parse(file_path)
    root = tree.getroot()

    for teacher in root.findall(".//teacher"):
        ref_id = teacher.get("uuid", "None")  # Use 'uuid' attribute as reference ID
        firstname = teacher.get("firstName", "").strip()
        lastname = teacher.get("lastName", "").strip()
        name = f"{firstname} {lastname}".strip()  # Combine first and last names

        if name:  # Ensure name is not empty
            teachers.append({"name": name, "ref_id": ref_id})
    return teachers
