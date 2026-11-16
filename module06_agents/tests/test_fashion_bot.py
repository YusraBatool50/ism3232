# test_fashion_bot.py

from fake_model import FakeModel
from fashion_bot import FashionHelper
from fashion_queue import FashionQueue
from fashion_tool import FashionInventory
from fashion_toolbox import FashionToolbox


def make_helper(model):
    """Build a fresh fashion helper."""
    inventory = FashionInventory(
        {"heels": "5 pairs available", "jackets": "out of stock"}
    )
    queue = FashionQueue(inventory)
    tools = FashionToolbox(inventory, queue)

    return FashionHelper("Stella", "Be clear.", tools, model)


def reservation(item, customer):
    """Build a reservation tool decision."""
    return {
        "tool": "request_reservation",
        "arguments": {"item": item, "customer": customer},
    }


def test_model_can_check_stock():
    model = FakeModel(
        [
            {"tool": "check_stock", "arguments": {"item": "heels"}},
            {"text": "There are 5 pairs of heels available."},
        ]
    )

    helper = make_helper(model)
    helper.respond("Are heels available?")

    assert helper.history[1]["content"] == "Stock for heels: 5 pairs available."


def test_reservation_waits_for_approval():
    model = FakeModel(
        [
            reservation("heels", "Dana Cruz"),
            {"text": "Your request was sent."},
        ]
    )

    helper = make_helper(model)
    helper.respond("Please reserve heels for Dana Cruz")

    assert len(helper.tools.fashion_queue.waiting()) == 1
    assert helper.tools.fashion_inventory.reservations == []


def test_made_up_name_is_refused():
    model = FakeModel(
        [
            reservation("heels", "Jane Doe"),
            {"text": "What is your name?"},
        ]
    )

    helper = make_helper(model)
    helper.respond("Please reserve heels")

    assert "has not given that name" in helper.history[1]["content"]
    assert helper.tools.fashion_queue.waiting() == []


def test_approval_only_happens_once():
    inventory = FashionInventory({"heels": "5 pairs available"})
    queue = FashionQueue(inventory)

    queue.request_reservation("heels", "Dana Cruz")
    queue.approve(1)
    queue.approve(1)

    assert len(inventory.reservations) == 1


def test_purchase_goes_to_a_human():
    helper = make_helper(FakeModel([]))

    reply = helper.respond("Can I buy the heels?")

    assert "store associate" in reply


def test_unknown_tool_is_refused():
    helper = make_helper(FakeModel([]))

    result = helper.tools.run("delete_inventory", {}, helper.history)

    assert "There is no tool named" in result


def test_missing_item_is_refused():
    helper = make_helper(FakeModel([]))

    result = helper.tools.run("check_stock", {"item": ""}, helper.history)

    assert "item is missing" in result


def test_model_can_greet():
    model = FakeModel([{"text": "Hello! How can I help you today?"}])

    helper = make_helper(model)

    assert helper.respond("hello") == "Hello! How can I help you today?"


def test_model_without_answer_gets_safe_reply():
    helper = make_helper(FakeModel([None]))

    assert "try again" in helper.respond("What is your favorite color?")
