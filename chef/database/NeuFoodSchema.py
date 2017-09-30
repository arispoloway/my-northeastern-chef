import graphene
from graphene import relay
from graphene_sqlalchemy import *
from NeuFoodModels import db_session, Meal as MealModel, Food_Item as FoodItemModel, Filter as FilterModel
import datetime

class Meal(SQLAlchemyObjectType):
    class Meta:
        model = MealModel
        interfaces = (relay.Node, )


class Food_Item(SQLAlchemyObjectType):
    class Meta:
        model = FoodItemModel
        interfaces = (relay.Node, )

class Filter(SQLAlchemyObjectType):
    class Meta:
        model = FilterModel
        interfaces = (relay.Node,)


class Query(graphene.ObjectType):
    node = relay.Node.Field()
    nextMeals = SQLAlchemyConnectionField(Meal, times=graphene.List(graphene.String), dHalls=graphene.List(graphene.String),
                                          max=graphene.Int())
    nextOccurance = SQLAlchemyConnectionField(Meal, food=graphene.String(), max=graphene.Int())


    def resolve_nextMeals(self, info, times=['Breakfast', 'Lunch', 'Dinner'], max=5, dHalls=['IV', 'Stetson West',
        'Stetson East']):
        query = Meal.get_query(info)

        query = query.filter(MealModel.d_hall.in_(dHalls))
        query = query.filter(MealModel.name.in_(times))

        query = query.order_by(MealModel.date).order_by(MealModel.name)
        d = datetime.datetime.today() - datetime.timedelta(days=1)
        query = query.filter(MealModel.date >= d)

        query = query.limit(max)
        return query

    def resolve_nextOccurance(self, info, food='pulled pork', max=5):
        query  = Meal.get_query(info)

        query = query.join(FoodItemModel.Meals)
        query = query.filter(FoodItemModel.name.like('%'+food+'%'))

        query  = query.order_by(MealModel.date).order_by(MealModel.name)

        d = datetime.datetime.today() - datetime.timedelta(days=1)
        query = query.filter(MealModel.date > d)

        query = query.limit(max)
        return query




schema = graphene.Schema(query=Query)


