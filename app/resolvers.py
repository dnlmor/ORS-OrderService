from .services import OrderService

def resolve_create_order(info, user_id, items):
    return OrderService.create_order(user_id, items)

def resolve_update_order_status(info, id, status):
    return OrderService.update_order_status(id, status)

def resolve_get_order(info, id):
    return OrderService.get_order_by_id(id)

def resolve_list_orders(info):
    return OrderService.list_orders()

def resolve_get_user_orders(info, user_id):
    return OrderService.get_user_orders(user_id)
