from chef.database import NeuFoodModels

slang = {
    "northeastern": "neu"
}

databases = {
    "neu": NeuFoodModels.db_user()
}


def get_school_database(school: str):
    school = school.lower()
    if school in slang:
        school = slang[school]
    if school in databases:
        return databases[school]
    return None
