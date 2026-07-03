import json
import os
import re

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


def _lookup_by_id(file_path: str, id_field: str, target_id: str) -> dict | None:
    """Load a JSON array and find an item matching the given ID field.

    Args:
        file_path: Path to the JSON file.
        id_field: The dictionary key to match against.
        target_id: The value to search for.

    Returns:
        The matching dictionary, or None if not found.
    """
    try:
        items = _load_json(file_path)
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return None

    for item in items:
        if isinstance(item, dict) and item.get(id_field) == target_id:
            return item

    return None


def get_order(order_id: str) -> dict | None:
    """Search for an order by its ID.

    Args:
        order_id: The unique identifier of the order.

    Returns:
        The matching order dictionary, or None if not found.
    """
    return _lookup_by_id(_ORDERS_PATH, "order_id", order_id)


def get_product(product_id: str) -> dict | None:
    """Search for a product by its ID.

    Args:
        product_id: The unique identifier of the product.

    Returns:
        The matching product dictionary, or None if not found.
    """
    return _lookup_by_id(_PRODUCTS_PATH, "product_id", product_id)


def route_tool(question: str) -> dict | None:
    """Detect entity IDs in a question and route to the appropriate lookup tool.

    Args:
        question: The user's question string.

    Returns:
        The matched order or product dictionary, or None if no ID is found.
    """
    order_match = re.search(r"ORD-\d+", question)
    if order_match:
        return get_order(order_match.group())

    product_match = re.search(r"PRD-\d+", question)
    if product_match:
        return get_product(product_match.group())

    return None