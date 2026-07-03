from services.tools import get_order


def main():
    order = get_order("ORD-1001")
    if order is None:
        print("Order not found.")
    else:
        print(order)


if __name__ == "__main__":
    main()
