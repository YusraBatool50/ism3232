# my_main.py
# Author: Yusra Batool

from fashion_bot import FashionHelper
from fashion_tool import FashionInventory
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
The store is open Monday through Saturday, 10 AM to 8 PM.
Customers can try on clothing in the fitting rooms.
Only state facts provided in these instructions.
If you do not know an answer, say you do not know
and suggest speaking to a store associate.
"""

inventory = FashionInventory(ITEMS)
model = OllamaModel("granite4.1:3b")

helper = FashionHelper("Stella", INSTRUCTIONS, inventory, model)

print("Type a message, or type quit to stop.")

user_message = input("You: ")

while user_message.lower() != "quit":
    print(f"{helper.name}: {helper.respond(user_message)}")
    user_message = input("You: ")

print(f"Messages in this conversation: {len(helper.history)}")
