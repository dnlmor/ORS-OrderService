import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.models import Order, OrderItem
from app import db

class OrderType(SQLAlchemyObjectType):
    class Meta:
        model = Order

class OrderItemType(SQLAlchemyObjectType):
    class Meta:
        model = OrderItem

class CreateOrder(graphene.Mutation):
    order = graphene.Field(OrderType)

    class Arguments:
        user_id = graphene.Int(required=True)
        items = graphene.List(graphene.JSONString, required=True)

    def mutate(self, info, user_id, items):
        total_price = sum(item['price'] * item['quantity'] for item in items)
        order = Order(user_id=user_id, total_price=total_price)
        db.session.add(order)
        db.session.commit()

        for item in items:
            order_item = OrderItem(
                order_id=order.id,
                item_id=item['id'],
                name=item['name'],
                price=item['price'],
                quantity=item['quantity']
            )
            db.session.add(order_item)
        db.session.commit()

        return CreateOrder(order=order)

class UpdateOrderStatus(graphene.Mutation):
    order = graphene.Field(OrderType)

    class Arguments:
        order_id = graphene.Int(required=True)
        status = graphene.String(required=True)

    def mutate(self, info, order_id, status):
        order = Order.query.get(order_id)
        if not order:
            raise ValueError("Order not found")

        order.status = status
        db.session.commit()

        return UpdateOrderStatus(order=order)

class Query(graphene.ObjectType):
    order = graphene.Field(OrderType, id=graphene.Int())
    orders = graphene.List(OrderType, user_id=graphene.Int())

    def resolve_order(self, info, id):
        return Order.query.get(id)

    def resolve_orders(self, info, user_id):
        return Order.query.filter_by(user_id=user_id).all()

class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
    update_order_status = UpdateOrderStatus.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
