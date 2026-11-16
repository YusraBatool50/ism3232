# fashion_queue.py
# Author: Yusra Batool


class FashionQueue:
    """Reservation requests waiting for store approval."""

    def __init__(self, fashion_inventory):
        self.fashion_inventory = fashion_inventory
        self.requests = []

    def request_reservation(self, item, customer):
        """Request a fashion item reservation.

        Args:
            item: The item the customer wants to reserve.
            customer: The customer's full name.
        """
        found = self.fashion_inventory.find_item(item)

        if found is None:
            return "That item was not found."

        if self.fashion_inventory.stock_for(found) == "out of stock":
            return "That item is out of stock."

        number = len(self.requests) + 1

        request = {
            "number": number,
            "item": found,
            "customer": customer,
            "status": "waiting",
        }

        self.requests.append(request)
        return f"Request {number} sent to the store associate. Nothing is reserved yet."

    def waiting(self):
        """Return requests still waiting for approval."""
        result = []
        for request in self.requests:
            if request["status"] == "waiting":
                result.append(request)
        return result

    def find(self, number):
        """Find a request by number."""
        for request in self.requests:
            if request["number"] == number:
                return request
        return None

    def approve(self, number):
        """Approve a request and record the reservation."""
        request = self.find(number)

        if request is None:
            return f"There is no request {number}."

        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."

        request["status"] = "approved"

        self.fashion_inventory.add_reservation(request["item"], request["customer"])

        return f"Request {number} approved."

    def reject(self, number):
        """Reject a reservation request."""
        request = self.find(number)

        if request is None:
            return f"There is no request {number}."

        if request["status"] != "waiting":
            return f"Request {number} is already {request['status']}."

        request["status"] = "rejected"
        return f"Request {number} rejected."
