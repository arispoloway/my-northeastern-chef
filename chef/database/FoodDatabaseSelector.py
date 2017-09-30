from chef.database import NeuFoodDatabase

slang = {
    "northeastern": "neu"
}

databases = {
    "neu": NeuFoodDatabase.db_user()
}


def get_school_database(school: str):
    school = school.lower()
    if school in slang:
        school = slang[school]
    if school in databases:
        return databases[school]
    return None
