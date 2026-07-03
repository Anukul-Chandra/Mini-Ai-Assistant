import json
import os

_ORDERS_PATH = os.path.join("data", "orders.json")
_PRODUCTS_PATH = os.path.join("data", "products.json")


def _load_json(file_path: str) -> list[dict]:
    """Load and validate a JSON file containing an array of objects.

    Args:
        file_path: Path to the JSON file.

    Returns:
        A list of dictionaries parsed from the file.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file contains invalid JSON.
        ValueError: If the root value is not a JSON array.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at {file_path}")

    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError(f"File must contain a JSON array")

    return data


def get_order(order_id: str) -> dict | None:
    """Search for an order by its ID.

    Args:
        order_id: The unique identifier of the order.

    Returns:
        The matching order dictionary, or None if not found.
    """
    try:
        orders = _load_json(_ORDERS_PATH)
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return None

    for order in orders:
        if isinstance(order, dict) and order.get("order_id") == order_id:
            return order

    return None


def get_product(product_id: str) -> dict | None:
    """Search for a product by its ID.

    Args:
        product_id: The unique identifier of the product.

    Returns:
        The matching product dictionary, or None if not found.
    """
    try:
        products = _load_json(_PRODUCTS_PATH)
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return None

    for product in products:
        if isinstance(product, dict) and product.get("product_id") == product_id:
            return product

    return None