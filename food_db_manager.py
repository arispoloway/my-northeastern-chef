from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey, Enum
from sqlalchemy import and_, or_
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from db_conn_settings import db_conn_settings as dbcs #settings for mysql server 
import requests, datetime, json

Base = declarative_base()

#Represents an object thats connected to the database with certain settings
class db_connection():
    def __init__(self, db_name):
        self.db_name = db_name
        self.engine = self.create_engine()
        self.sess = sessionmaker(bind=self.engine)()
        Base.metadata.create_all(self.engine)

    def create_engine(self):
        #eng_string='''sqlite:///my_neu_chef.db'''
        #code for mysql connection
        eng_string='''mysql+mysqlconnector://{0[userName]}:{0[password]}@
        {0[serverName]}:{0[portNumber]}/{1}'''.format(dbcs, self.db_name)
        eng=create_engine(eng_string)
        return eng

#Represents a database administrator who can add menus to the database
class db_admin(db_connection):
    def __init__(self, db_name="my_neu_chef"):
        super(db_admin, self).__init__(db_name)
        self.dining_halls_dict = {
        "Stetson West":"586d05e4ee596f6e6c04b528",
        "Stetson East":"586d05e4ee596f6e6c04b527",
        "IV":"586d17503191a27120e60dec",
        }
        self.site_id = "5751fd2b90975b60e048929a"
        self.base_url = "https://new.dineoncampus.com/v1/location/menu.json"

    #add menus from all dining hall locations for the given day
    def add_all_menus_for_day(self, date=datetime.date.today()):
        print('Getting all dining hall menus for', date)

        for d_hall in self.dining_halls_dict:
            if not self.sess.query(Meal).filter(
                and_ (Meal.date == date, Meal.d_hall == d_hall)).count() > 0:
                while True:
                    try:
                        d_hall_response = self.get_data_from_api(d_hall)
                        break
                    except json.decoder.JSONDecodeError:
                        print("Couldn't get", d_hall, "data for", date,
                         " Trying again now...")
                if d_hall_response['status'] == 'success':
                    self.add_menu_data(d_hall_response['menu'], d_hall, date)

        print('Done')

    #add menus from all dining hall locations for the next week, starting today
    def add_all_menus_for_next_week(self):
        td = datetime.timedelta(days=1)
        d = datetime.date.today()
        for _ in range(7):
            self.add_all_menus_for_day(d)
            d+=td

    #add menus from all dining hall locations for the next 30 days, starting today
    def add_all_menus_for_next_month(self):
        td = datetime.timedelta(days=1)
        d = datetime.date.today()
        for _ in range(30):
            self.add_all_menus_for_day(d)
            d+=td

    #add the given menu data/given dining hall/given day to the db
    def add_menu_data(self, m_data, d_hall_name, m_date):
        for period in m_data['periods']:
            #for each meal create a unique meal id and meal object
            m_id = period['id']+str(m_date)
            m = Meal(id=m_id, date=m_date,
                d_hall=d_hall_name, name=period['name'])
            for station in period['categories']:
                for food in station['items']:
                    #this conditional avoids a bug in the menu api
                    if len(food['nutrients'])>0:
                        #for each food item, create an item object
                        i = Food_Item(id=food['id'], name=food['name'], 
                            calories=food['nutrients'][0]['value'])
                        for filt in food['filters']:
                            #for each filter on the food create a filtr object
                            f = Filter(id=filt['id'], name=filt['name'])
                            i.Filters.append(f)
                        m.Food_Items.append(i)
            self.sess.merge(m)
        self.sess.commit()

    #retrieve data from the online menu api for the given dining hall/date
    def get_data_from_api(self, d_hall, date=datetime.date.today()):
        #create request arguments
        #date=date.strftime("%Y-%m-%d")
        params = {
            "date":date,
            "location_id":self.dining_halls_dict[d_hall],
            "platform":0,
            "site_id":self.site_id
        }
        headers = {
            "Content-Type":"application/json"
        }

        data = json.loads(requests.get(self.base_url, headers=headers, params=params).text)

        return data

#Represents a database user who can query the database 
class db_user(db_connection):
    def __init__(self, db_name="my_neu_chef"):
        super(db_user, self).__init__(db_name)

    #TODO: check the date and time as part of the query
    #get the next occurances of the given food in the given dining halls
    def get_next_occurances(self, food, d_halls=['IV', 'Stetson West', 
        'Stetson East'], max_occurances=5):
        #create a query of meal and item colums
        q = self.sess.query(Meal, Food_Item).join(Food_Item.Meals)
        #filter for items like the one the user wants
        f_string = '%' + food + '%'
        q = q.filter(Food_Item.name.like(f_string))
        #filter for dining halls the user wants
        q = q.filter(Meal.d_hall.in_(d_halls))
        #return only meals from today on
        q = q.filter(Meal.date >= datetime.date.today())
        #order the results by date, then by meal
        q = q.order_by(Meal.date).order_by(Meal.name)

        return q.all()[:max_occurances]

    def get_current_status(self, somethingelse):
        #not too sure what this should be yet
        print("Get current status unimplemented")
        return []

#Represents a meal with a date, location, name and items
class Meal(Base):
    __tablename__ = 'Meal'

    id = Column(String(50), primary_key=True)
    date = Column(Date)
    d_hall = Column(String(50))
    name = Column(Enum('Breakfast', 'Lunch', 'Dinner'))

    #table for linking meals and their food items in a many-many relationship
    assoc_t = Table('Meal_Food_Item_assoc', Base.metadata,
            Column('Meal_id', String(50), ForeignKey('Meal.id')),
            Column('Food_Item_id', String(50), ForeignKey('Food_Item.id')))
    Food_Items = relationship('Food_Item',
        secondary=assoc_t,
        backref='Meals')

    def __repr__(self):
        return "<Meal(date='%s', d_hall='%s', name='%s')>"%(
            self.date, self.d_hall, self.name)

#Represents a food item with a name, calorie count, and filters
class Food_Item(Base):
    __tablename__ = 'Food_Item'

    id = Column(String(50), primary_key=True)
    name = Column(String(150))
    calories = Column(Integer)

    #table for linking food items and filters in a many-many relationship
    assoc_t = Table('Food_Item_Filter_assoc', Base.metadata,
            Column('Food_Item_id', String(50), ForeignKey('Food_Item.id')),
            Column('Filter_id', String(50), ForeignKey('Filter.id')))
    Filters = relationship('Filter',
        secondary=assoc_t,
        backref='Food_Items')

    def __repr__(self):
        return "<Food_Item(name='%s', calories='%s')>"%(
            self.name, self.calories)

#represents an item filter with a name
class Filter(Base):
    __tablename__ = 'Filter'

    id = Column(String(50), primary_key=True)
    name = Column(String(150))

    def __repr__(self):
        return "<Filter(name='%s')>"%(self.name)
