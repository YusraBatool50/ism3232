# my_main.py
# Author: Yusra Batool

from fashion_bot import FashionHelper
from fashion_queue import FashionQueue
from fashion_tool import FashionInventory
from fashion_toolbox import FashionToolbox
from ollama_model import OllamaModel

ITEMS = {
    "heels": "5 pairs available",
    "jackets": "out of stock",
    "dresses": "8 available",
    "handbags": "3 available",
}

INSTRUCTIONS = """
You are Stella, a helpful fashion store assistant.
Answer in one short sentence.
If the customer only says hello, greet them and ask how you can help.
The store is open Monday through Saturday, 10 AM to 8 PM.
Customers can try on clothing in the fitting rooms.
Use the stock tool when a customer asks about item availability.
To request a reservation, you need the item and customer's full name.
If a customer asks to reserve an item, use the reservation tool.
Never say an item is reserved until a store associate approves it.
Only state facts provided in these instructions or tool results.
If you do not know an answer, suggest speaking to a store associate.
"""

inventory = FashionInventory(ITEMS)
queue = FashionQueue(inventory)
tools = FashionToolbox(inventory, queue)
model = OllamaModel("granite4.1:3b")

helper = FashionHelper("Stella", INSTRUCTIONS, tools, model)

print("Type a message, or type quit to stop.")

user_message = input("You: ")

while user_message.lower() != "quit":
    print(f"{helper.name}: {helper.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(helper.history)}")

print("Store associate review")

for request in queue.waiting():
    number = request["number"]

    print(f"Request {number}: {request['customer']}, {request['item']}")

    answer = input("Approve? yes or no: ")

    if answer.lower() == "yes":
        print(queue.approve(number))
    else:
        print(queue.reject(number))

print(f"Reservations: {len(inventory.reservations)}")
