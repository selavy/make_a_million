#!/usr/bin/env python


import mmillion.rules as rules


def test_rank_as_str():
    assert rules.rank_as_str(40) == "$40,000"
    assert rules.rank_as_str(30) == "$30,000"    
    assert rules.rank_as_str(10) == "$10,000"
    assert rules.rank_as_str(5)  == "$5,000"
    assert rules.rank_as_str(1)  == "1"
    assert rules.rank_as_str(3)  == "3"


def test_make_deck():
    deck = rules.make_deck()
    for card in deck:
        assert card.rank in rules.RANKS

    for suit in (
            rules.Suit.RED,
            rules.Suit.YELLOW,
            rules.Suit.BLACK,
            rules.Suit.GREEN
    ):
        suit_cards = [c for c in deck if c.suit == suit]
        assert len(suit_cards) == 13, "13 cards in each suit"
        assert len(suit_cards) == len(set(suit_cards)), \
            "No duplicate cards in set"

    for animal in (
            rules.Suit.BEAR,
            rules.Suit.BULL,
            rules.Suit.TIGER,
    ):
        cards = [c for c in deck if c.suit == animal]
        assert len(cards) == 1, "1 of each animal"

    assert len(deck) == len(set(deck)), "No duplicate cards"
    assert len(deck) == 13*4 + 3
