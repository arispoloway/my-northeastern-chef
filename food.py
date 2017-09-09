import requests
import datetime
import json

locations = {
    "Stetson West":"586d05e4ee596f6e6c04b528",
    "Stetson East":"586d05e4ee596f6e6c04b527",
    "IV":"586d17503191a27120e60dec",
        }

site_id = "5751fd2b90975b60e048929a"

base_url = "https://new.dineoncampus.com/v1/location/menu.json"


def get_menu(location, date=datetime.date.today()):
    if location not in locations:
        raise Exception("Invalid Location")


    date_formatted = date.strftime("%Y-%m-%d")

    params = {
        "date":date_formatted,
        "location_id":locations[location],
        "platform":0,
        "site_id":site_id
    }

    headers = {
        "Content-Type":"application/json"
    }
    return json.loads(requests.get(base_url, headers=headers, params=params).text)["menu"]


def flatten_menu(menu):

    food_listing = {}
    for period in menu["periods"]:
    	food_listing[period["name"]] = []
    	for category in period["categories"]:
            food_listing[period["name"]] += [item["name"] for item in category["items"]]

    return food_listing





print(flatten_menu(get_menu("IV")))
