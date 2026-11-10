from fashion_bot import FashionHelper
from fashion_tool import FashionInventory


def make_helper():
    """Build a fresh helper with its own tool for each test."""
    inventory = FashionInventory(
        {"heels": "5 pairs available", "jackets": "out of stock"}
    )
    return FashionHelper("Stella", "Be clear.", inventory)


def test_stock_question_uses_the_tool():
    helper = make_helper()
    reply = helper.respond("Are heels available?")
    assert reply == "Stock for heels: 5 pairs available."


def test_question_without_a_known_item_asks_for_one():
    helper = make_helper()
    assert "Which item?" in helper.respond("Are sneakers available?")


def test_purchase_request_goes_to_a_human():
    helper = make_helper()
    assert "store associate" in helper.respond("Can I buy the heels?")


def test_unknown_request_gets_a_safe_reply():
    helper = make_helper()
    assert "not sure" in helper.respond("What is your favorite color?")


def test_history_grows_by_two_each_turn():
    helper = make_helper()
    helper.respond("hello")
    helper.respond("Are jackets in stock?")
    assert len(helper.history) == 4
