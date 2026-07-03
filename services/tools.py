import json
import os

_ORDERS_PATH = os.path.join("data", "orders.json")


def _load_orders() -> list[dict]:
    """Load all orders from the JSON file.

    Returns:
        A list of order dictionaries.

    Raises:
        FileNotFoundError: If the orders file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
    """
    if not os.path.exists(_ORDERS_PATH):
        raise FileNotFoundError(f"Orders file not found at {_ORDERS_PATH}")

    with open(_ORDERS_PATH, encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Orders file must contain a JSON array")

    return data


def get_order(order_id: str) -> dict | None:
    """Search for an order by its ID.

    Args:
        order_id: The unique identifier of the order.

    Returns:
        The matching order dictionary, or None if not found.
    """
    try:
        orders = _load_orders()
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return None

    for order in orders:
        if isinstance(order, dict) and order.get("order_id") == order_id:
            return order

    return None