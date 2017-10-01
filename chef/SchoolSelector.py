slang = {
    "neu":"northeastern"
}

schools = ["northeastern"]

def get_school(school: str):
    school = school.lower()
    if school in slang:
        school = slang[school]
    if school not in schools:
        return None
    return school