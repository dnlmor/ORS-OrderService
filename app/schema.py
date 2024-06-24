import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from .models import Order as OrderModel, OrderItem as OrderItemModel
from .resolvers import (
    resolve_create_order, resolve_update_order_status, resolve_get_order,
    resolve_list_orders, resolve_get_user_orders
)

class OrderItem(SQLAlchemyObjectType):
    class Meta:
        model = OrderItemModel

class Order(SQLAlchemyObjectType):
    class Meta:
        model = OrderModel

class Query(graphene.ObjectType):
    get_order = graphene.Field(Order, id=graphene.Int(required=True))
    list_orders = graphene.List(Order)
    get_user_orders = graphene.List(Order, user_id=graphene.Int(required=True))

    def resolve_get_order(self, info, id):
        return resolve_get_order(info, id)

    def resolve_list_orders(self, info):
        return resolve_list_orders(info)

    def resolve_get_user_orders(self, info, user_id):
        return resolve_get_user_orders(info, user_id)

class OrderItemInput(graphene.InputObjectType):
    dish_id = graphene.Int(required=True)
    quantity = graphene.Int(required=True)
    price = graphene.Float(required=True)

class CreateOrder(graphene.Mutation):
    class Arguments:
        user_id = graphene.Int(required=True)
        items = graphene.List(OrderItemInput, required=True)

    order = graphene.Field(lambda: Order)

    def mutate(self, info, user_id, items):
        return resolve_create_order(info, user_id, items)

class UpdateOrderStatus(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        status = graphene.String(required=True)

    order = graphene.Field(lambda: Order)

    def mutate(self, info, id, status):
        return resolve_update_order_status(info, id, status)

class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
    update_order_status = UpdateOrderStatus.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
