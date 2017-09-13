from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey 
from sqlalchemy import and_
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from db_conn_settings import db_conn_settings as dbcs
import requests
import datetime
import json

Base = declarative_base()

class db_manager():
    def __init__(self):
        self.dining_halls_dict = {
        "Stetson West":"586d05e4ee596f6e6c04b528",
        "Stetson East":"586d05e4ee596f6e6c04b527",
        "IV":"586d17503191a27120e60dec",
        }
        self.site_id = "5751fd2b90975b60e048929a"
        self.base_url = "https://new.dineoncampus.com/v1/location/menu.json"

        self.engine = self.create_engine()
        self.sess = sessionmaker(bind=self.engine)()
        Base.metadata.create_all(self.engine)

    def create_engine(self):
        eng_string='''mysql+mysqlconnector://{0[userName]}:{0[password]}@
        {0[serverName]}:{0[portNumber]}/{0[dbName]}'''.format(dbcs)
        eng=create_engine(eng_string)
        return eng

    def add_all_menus_for_day(self, date=datetime.date.today()):
        print('Getting menus all dining halls for', date)

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

    def add_all_menus_for_next_week(self):
        td = datetime.timedelta(days=1)
        d = datetime.date.today()
        for _ in range(7):
            self.add_all_menus_for_day(d)
            d+=td

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
                        i = Item(id=food['id'], name=food['name'], 
                            calories=food['nutrients'][0]['value'])
                        for filt in food['filters']:
                            #for each filter on the food create a filtr object
                            f = Filter(id=filt['id'], name=filt['name'])
                            i.Filters.append(f)
                        i.Meals.append(m)
                        self.sess.merge(f)
        self.sess.commit()

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

    def get_all_pizza_meals(self):
        for m, i in self.sess.query(Meal, Item).join(Item.Meals, Item.Filters).filter(Filter.name=='Vegetarian').all():
            print(m.name, ", ", m.d_hall, ", ", m.date, ", ", i.name)

class Meal(Base):
    __tablename__ = 'Meal'

    id = Column(String(50), primary_key=True)
    date = Column(Date)
    d_hall = Column(String(50))
    name = Column(String(50))

    assoc_t = Table('Meal_Item_assoc', Base.metadata,
            Column('Meal_id', String(50), ForeignKey('Meal.id')),
            Column('Item_id', String(50), ForeignKey('Item.id')))

    Items = relationship('Item',
        secondary=assoc_t,
        backref='Meals')

    def __repr__(self):
        return "<Meal(date='%s', d_hall='%s', name='%s')>"%(
            self.date, self.d_hall, self.name)

class Item(Base):
    __tablename__ = 'Item'

    id = Column(String(50), primary_key=True)
    name = Column(String(50))
    calories = Column(Integer)

    assoc_t = Table('Item_Filter_assoc', Base.metadata,
            Column('Item_id', String(50), ForeignKey('Item.id')),
            Column('Filter_id', String(50), ForeignKey('Filter.id')))

    Filters = relationship('Filter',
        secondary=assoc_t,
        backref='Items')

    def __repr__(self):
        return "<Item(name='%s', calories='%s')>"%(
            self.name, self.calories)

class Filter(Base):
    __tablename__ = 'Filter'

    id = Column(String(50), primary_key=True)
    name = Column(String(50))

    def __repr__(self):
        return "<Filter(name='%s')>"%(self.name)
