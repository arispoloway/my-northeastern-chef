import requests
import datetime
import json
import sqlite3

dining_halls = {
    "Stetson West":"586d05e4ee596f6e6c04b528",
    "Stetson East":"586d05e4ee596f6e6c04b527",
    "IV":"586d17503191a27120e60dec",
        }

site_id = "5751fd2b90975b60e048929a"

base_url = "https://new.dineoncampus.com/v1/location/menu.json"

db_name = 'my_ne_chef.db'
menu_table_name = 'full_menu'

#takes a dining hall string and date object to create a menu object
def get_menu_from_api(d_hall, date=datetime.date.today()):

    #create request arguments
    date=date.strftime("%Y-%m-%d")
    params = {
        "date":date,
        "location_id":dining_halls[d_hall],
        "platform":0,
        "site_id":site_id
    }
    headers = {
        "Content-Type":"application/json"
    }

    ret = json.loads(requests.get(base_url, headers=headers, params=params).text)
    for key in ret:
        print(key)

    print(ret['status'])
    print(ret['msg'])

    return ret["menu"]

#uses the given db connection, table name, and date object to add to a table
def add_menu_for_day(date):

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    #make sure the table is created
    create_table()

    #if we already loaded this day, dont load it again
    select_statement = "SELECT * FROM "+menu_table_name+" WHERE date=?"
    if len(cursor.execute(select_statement, (date,)).fetchall())>0:
        print(date, "MENU ALREADY ADDED")
        return 

    #loop trough the menu structure for each d_hall while collecting info
    for d_hall in dining_halls:
        menu = get_menu_from_api(d_hall, date)
        print("Got the", d_hall, "menu for", date)
        for meal in menu["periods"]:
            meal_name = meal["name"]
            for station in meal["categories"]:
                station_name = station["name"]
                for item in station["items"]:
                    item_name = item["name"]
                    item_calories = item["nutrients"][0]["value"]
                    item_filters = []
                    for filt in item["filters"]:
                        item_filters.append(filt["name"])
                    is_vege = "Vegetarian" in item_filters
                    cont_gluten = "Gluten" in item_filters

                    #insert the info if it is not a duplicate item
                    # (same day, hall, station, item)
                    insert_statement = '''INSERT OR IGNORE INTO '''+menu_table_name+''' 
                    (date, d_hall, meal_name, station_name, item_name, 
                    calories_value, is_vegetarian, contains_gluten) 
                    VALUES (?,?,?,?,?,?,?,?)'''
                    cursor.execute(insert_statement, 
                        (date.strftime("%Y-%m-%d"), d_hall, meal_name, station_name, 
                            item_name, item_calories, is_vege, cont_gluten))


    
    #commit changes to the given connection
    conn.commit()
    print("ADDED ", date, "MENU")
    conn.close()

def add_menu_for_next_week():
    date = datetime.date.today()
    td = datetime.timedelta(days=1)

    for _ in range(7):
        add_menu_for_day(date)
        date += td

def delete_table():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    drop_statement = 'DROP TABLE '+menu_table_name
    cursor.execute(drop_statement)
    conn.commit()
    conn.close()

def create_table():
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor() 

    create_statement = '''CREATE TABLE IF NOT EXISTS '''+menu_table_name+''' 
    (date text, d_hall text, meal_name text, station_name text, item_name text,
    calories_value text, is_vegetarian bool, contains_gluten bool)'''
    cursor.execute(create_statement)   
    conn.close()

def get_whatever(d=datetime.date.today(),d_h='IV',m_name='Breakfast'
    ,s_name='Everyday',i_name='Banana'):
    print("unimplemented get whatever")
    return []