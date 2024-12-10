from gender_guesser.detector import Detector

# Initialize the gender detector
detector = Detector(case_sensitive=False)

def detect_gender(name):
    """
    Detects gender based on the first name using the gender-guesser library.
    :param name: First name to determine gender
    :return: 'Male', 'Female', or 'Unknown'
    """
    if not name:
        return "Unknown"

    result = detector.get_gender(name)

    # Map the result to standard gender labels
    if result in ["male", "mostly_male"]:
        return "Male"
    elif result in ["female", "mostly_female"]:
        return "Female"
    else:
        return "Unknown"
