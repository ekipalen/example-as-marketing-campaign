"""
An example Action to assist with marketing campaigns.

Check out the base guidance on AI Actions in our main repository readme:
https://github.com/robocorp/robocorp/blob/master/README.md
"""

from robocorp.actions import action
import sqlite3


@action(is_consequential=False)
def identify_customers(category: str, months_since_last_purchase: int) -> str:
    """
    Helps to find customers for new marketing campaign. Identifies customers based on their last purchase in a specific category and the time since their last purchase.

    Args:
        category (str): Category of the product. Possible categories include "high-end kitchen", "electronics", "furniture".
        months_since_last_purchase (int): The number of months since the last purchase.

    Returns:
        str: A string representation of the list of customers matching the criteria.
    """

    database_path = "marketing_campaign_demo.db"
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    query = """
    SELECT c.customer_id, c.name, c.email
    FROM customers c
    JOIN purchases p ON c.customer_id = p.customer_id
    WHERE p.category = ?
    AND p.purchase_date <= date('now', ?)
    GROUP BY c.customer_id
    HAVING MAX(p.purchase_date) <= date('now', ?);
    """
    months_param = f"-{months_since_last_purchase} months"
    cursor.execute(query, (category, months_param, months_param))

    customers = cursor.fetchall()

    conn.close()

    if customers:
        result = (
            "Identified customers below. Ask if user wants to filter customers by engagemnent stats. \n"
            + "\n".join(
                [
                    f"ID: {customer[0]}, Name: {customer[1]}, Email: {customer[2]}"
                    for customer in customers
                ]
            )
        )
    else:
        result = "No customers matched the criteria."
    print(result)
    return result


@action(is_consequential=False)
def filter_customers_by_engagement(
    customer_ids: str, min_email_open_rate: float
) -> str:
    """
    Before this action you need to identified the suitable customers. Filters customers from a provided list of customer IDs based on email engagement.

    Args:
        customer_ids (str): A comma-separated list of customer IDs to filter.
        min_email_open_rate (float): Minimum email open rate as a decimal (e.g., 0.75).

    Returns:
        str: List of customers matching the criteria.
    """

    database_path = "marketing_campaign_demo.db"
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    customer_ids_list = list(map(int, customer_ids.split(",")))

    query = """
    SELECT DISTINCT c.customer_id, c.name, c.email
    FROM customers c
    JOIN engagement e ON c.customer_id = e.customer_id
    WHERE c.customer_id IN ({seq})
      AND e.email_open_rate > ?
    ORDER BY c.customer_id;
    """.format(seq=",".join(["?"] * len(customer_ids_list)))

    cursor.execute(query, customer_ids_list + [min_email_open_rate])
    customers = cursor.fetchall()

    conn.close()

    if customers:
        result = (
            "Filtered customers by engagement below. Ask user if you should find suitable products for exclusive offer:\n"
            + "\n".join(
                [
                    f"ID: {customer[0]}, Name: {customer[1]}, Email: {customer[2]}"
                    for customer in customers
                ]
            )
        )
    else:
        result = "No customers matched the criteria."

    print(result)
    return result


@action(is_consequential=False)
def query_exclusive_offers_by_category(category: str) -> str:
    """
    Queries exclusive products by category.

    Args:
        category (str): The category to filter exclusive offers by. Possible values include "high-end kitchen", "furniture", "electronics".

    Returns:
        str: A formatted string listing the exclusive offers in the specified category.
    """

    database_path = "marketing_campaign_demo.db"

    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    query = """
    SELECT offer_id, product_name, discount_rate, description
    FROM exclusive_offers
    WHERE category = ?
    ORDER BY offer_id;
    """

    cursor.execute(query, (category,))
    offers = cursor.fetchall()
    conn.close()

    if offers:
        result_lines = [
            "Exclusive Offers below. Ask if user wants to send offers for some products."
        ]
        for offer in offers:
            result_lines.append(
                f"Product: {offer[1]}, Discount: {offer[2]*100}%, Description: {offer[3]}"
            )
        result = "\n".join(result_lines)
    else:
        result = "No exclusive offers found in the specified category."

    print(result)
    return result


@action(is_consequential=False)
def send_emails() -> str:
    """
    Simulates the action of sending marketing emails.

    This function represents the process of sending out emails in a demo context,
    but it does not perform any actual email sending operations.

    Returns:
        str: Confirmation message indicating the emails were "sent" successfully.
    """

    print("Simulating email sending process...")

    return "Email(s) sent successfully."
