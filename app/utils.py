def calculate_total_amount(items):
    return sum(item.price * item.quantity for item in items)

def validate_order_status(status):
    valid_statuses = ['PENDING', 'PROCESSING', 'COMPLETED', 'CANCELLED']
    if status not in valid_statuses:
        raise ValueError(f"Invalid order status. Must be one of {', '.join(valid_statuses)}")
