# my_main.py
# Author: Yusra Batool

from fashion_bot import FashionHelper
from fashion_tool import FashionInventory

ITEMS = {
    "heels": "5 pairs available",
    "dresses": "12 available",
    "handbags": "3 available",
    "jackets": "out of stock",
}

fashion_inventory = FashionInventory(ITEMS)

helper = FashionHelper(
    "Stella",
    "You help customers of The Style Edit check fashion item availability.",
    fashion_inventory,
)

print("Type a message, or type quit to stop.")

user_message = input("You: ")

while user_message != "quit":
    print(f"{helper.name}: {helper.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(helper.history)}")
