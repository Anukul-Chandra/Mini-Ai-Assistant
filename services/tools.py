import json
import os
import re


_ORDERS_PATH = os.path.join("data", "orders.json")
_PRODUCTS_PATH = os.path.join("data", "products.json")

_ORDER_KEYWORDS = ["order", "shipping", "delivery", "track", "where is"]
_PRODUCT_KEYWORDS = ["product", "have", "got", "looking for", "price of", "do you"]


def _load_json(file_path: str) -> list[dict]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found at {file_path}")

    with open(file_path, encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("File must contain a JSON array")

    return data


def _normalize_id(raw: str) -> str:
    return re.sub(r"[-_\s]", "", raw)


def _lookup_by_id(file_path: str, id_field: str, target_id: str) -> dict | None:
    try:
        items = _load_json(file_path)
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return None

    for item in items:
        if isinstance(item, dict) and item.get(id_field) == target_id:
            return item

    return None


def get_order(order_id: str) -> dict | None:
    return _lookup_by_id(_ORDERS_PATH, "order_id", order_id)


def get_product(product_id: str) -> dict | None:
    return _lookup_by_id(_PRODUCTS_PATH, "product_id", product_id)


def search_product_by_name(query: str) -> list[dict]:
    try:
        products = _load_json(_PRODUCTS_PATH)
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return []

    query_lower = query.lower()
    results = []
    for product in products:
        name = product.get("name", "")
        if name.lower() in query_lower:
            results.append(product)
    return results


def detect_intent(question: str) -> tuple[str | None, dict | list[dict] | None]:
    order_id_match = re.search(r"(?:ORD)[-_\s]?\d+", question, re.IGNORECASE)
    if order_id_match:
        raw = order_id_match.group()
        normalized = _normalize_id(raw)
        result = get_order(normalized)
        if result:
            return ("order", result)

    has_order_keyword = any(kw in question.lower() for kw in _ORDER_KEYWORDS)
    order_id_any = re.search(r"[A-Z]*\d{3,}", question)
    if has_order_keyword and order_id_any:
        result = get_order(order_id_any.group())
        if result:
            return ("order", result)

    product_id_match = re.search(r"(?:PRD)[-_\s]?\d+", question, re.IGNORECASE)
    if product_id_match:
        raw = product_id_match.group()
        normalized = _normalize_id(raw)
        result = get_product(normalized)
        if result:
            return ("product", result)

    has_product_keyword = any(kw in question.lower() for kw in _PRODUCT_KEYWORDS)
    if has_product_keyword:
        results = search_product_by_name(question)
        if results:
            return ("product", results)

    results = search_product_by_name(question)
    if results:
        return ("product", results)

    return (None, None)


def route_tool(question: str) -> dict | list[dict] | None:
    _, result = detect_intent(question)
    return result
