def parse_untis_teachers(file_path):
    """
    Parse teachers from UNTIS timetable export.
    Expects <Teacher> tags with 'id' and 'name' attributes.
    """
    teachers = []
    tree = ET.parse(file_path)
    root = tree.getroot()

    for teacher in root.findall(".//Teacher"):
        ref_id = teacher.get("id", "None")  # Use 'id' attribute as reference ID
        name = teacher.get("name", "").strip()  # Use 'name' attribute for teacher name

        if name:  # Ensure name is not empty
            teachers.append({"name": name, "ref_id": ref_id})
    return teachers