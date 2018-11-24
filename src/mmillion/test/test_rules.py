#!/usr/bin/env python

import mmillion.rules as rules
from mmillion.rules import Card
from mmillion.rules import Suit
from mmillion.rules import TIGER_CARD
from mmillion.rules import BULL_CARD
from mmillion.rules import BEAR_CARD


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


def test_find_lead_suit():
    cards = (
        Card.make(Suit.YELLOW, 1),
        Card.make(Suit.BLACK,  2),
        Card.make(Suit.YELLOW, 3),
        Card.make(Suit.GREEN,  4),
    )
    assert rules.find_lead_suit(cards) == Suit.YELLOW

    cards = (
        BEAR_CARD,
        Card.make(Suit.BLACK,  2),
        Card.make(Suit.YELLOW, 3),
        Card.make(Suit.GREEN,  4),
    )
    assert rules.find_lead_suit(cards) == Suit.BLACK, \
        "Skip bear if first card"

    cards = (
        BULL_CARD,
        Card.make(Suit.BLACK,  2),
        Card.make(Suit.YELLOW, 3),
        Card.make(Suit.GREEN,  4),
    )
    assert rules.find_lead_suit(cards) == Suit.BLACK, \
        "Skip bull if first card"

    cards = (
        TIGER_CARD,
        Card.make(Suit.BLACK,  2),
        Card.make(Suit.YELLOW, 3),
        Card.make(Suit.GREEN,  4),
    )
    assert rules.find_lead_suit(cards) == Suit.TIGER, \
        "Tiger first means trump is lead"

    assert rules.find_lead_suit([]) is None, \
        "Handle no cards in trick"


def test_winner():
    cards = (
        Card.make(Suit.BLACK, 40),
        Card.make(Suit.BLACK, 30),
        Card.make(Suit.BLACK, 10),
        TIGER_CARD,
    )
    assert rules.winner(Suit.BLACK, cards) == 3, "Tiger always wins"

    cards = (
        Card.make(Suit.BLACK, 10),
        Card.make(Suit.BLACK, 30),
        Card.make(Suit.BLACK, 40),
        Card.make(Suit.BLACK, 1),
    )
    assert rules.winner(Suit.YELLOW, cards) == 2, "High card of lead suit"
    
    cards = (
        Card.make(Suit.BLACK, 10),
        Card.make(Suit.BLACK, 30),
        Card.make(Suit.BLACK, 40),
        Card.make(Suit.YELLOW, 1),
    )
    assert rules.winner(Suit.YELLOW, cards) == 3, "Trump card wins"

    cards = (
        Card.make(Suit.BLACK,  10),
        Card.make(Suit.YELLOW, 30),
        Card.make(Suit.BLACK,  40),
        Card.make(Suit.YELLOW,  1),
    )
    assert rules.winner(Suit.YELLOW, cards) == 1, "High trump card"

    cards = (
        Card.make(Suit.RED,    1),
        Card.make(Suit.BLACK, 30),
        Card.make(Suit.BLACK, 40),
        Card.make(Suit.BLACK, 10),
    )
    assert rules.winner(Suit.YELLOW, cards) == 0, "High lead suit"

    cards = (
        Card.make(Suit.RED,    1),
        Card.make(Suit.BLACK, 30),
        Card.make(Suit.BLACK, 40),
        Card.make(Suit.RED,   10),
    )
    assert rules.winner(Suit.YELLOW, cards) == 3, "High lead suit"

    cards = (
        BEAR_CARD,
        Card.make(Suit.BLACK, 30),
        Card.make(Suit.BLACK, 40),
        Card.make(Suit.RED,   10),
    )
    assert rules.winner(Suit.YELLOW, cards) == 2, \
        "High lead suit with Bear start"

    cards = (
        BULL_CARD,
        Card.make(Suit.BLACK, 30),
        Card.make(Suit.BLACK, 40),
        Card.make(Suit.RED,   10),
    )
    assert rules.winner(Suit.YELLOW, cards) == 2, \
        "High lead suit with Bull start"

    cards = (
        BULL_CARD,
        BEAR_CARD,
        Card.make(Suit.BLACK,  1),
        Card.make(Suit.RED,   10),
    )
    assert rules.winner(Suit.YELLOW, cards) == 2, \
        "High lead suit with Bull and Bear start"

    
def test_score_hand():
    cards = (
        Card.make(Suit.BLACK,  1),
        Card.make(Suit.YELLOW, 1),
        Card.make(Suit.RED,    1),
        Card.make(Suit.GREEN,  1),
    )
    assert rules.score_hand(cards) == 0

    cards = (
        Card.make(Suit.BLACK,  1),
        Card.make(Suit.YELLOW, 40),
        Card.make(Suit.RED,    1),
        Card.make(Suit.GREEN,  1),
    )
    assert rules.score_hand(cards) == 40_000

    cards = (
        Card.make(Suit.BLACK,  40),
        Card.make(Suit.YELLOW, 40),
        Card.make(Suit.RED,    40),
        Card.make(Suit.GREEN,  40),
    )
    assert rules.score_hand(cards) == 160_000

    cards = (
        Card.make(Suit.BLACK,  40),
        Card.make(Suit.YELLOW, 40),
        Card.make(Suit.RED,    40),
        BULL_CARD,
    )
    assert rules.score_hand(cards) == 240_000, "Bull doubles"

    cards = (
        Card.make(Suit.BLACK,  40),
        Card.make(Suit.YELLOW, 40),
        Card.make(Suit.RED,    40),
        BEAR_CARD,
    )
    assert rules.score_hand(cards) == 0, "Bear cancels"

    cards = (
        Card.make(Suit.BLACK,  40),
        Card.make(Suit.YELLOW, 40),
        BULL_CARD,
        BEAR_CARD,
    )
    assert rules.score_hand(cards) == 0, "Bear seconds cancels"

    cards = (
        BULL_CARD,        
        Card.make(Suit.BLACK,  40),
        Card.make(Suit.YELLOW, 40),
        BEAR_CARD,
    )
    assert rules.score_hand(cards) == 0, \
        "Bear seconds cancels (different order)"

    cards = (
        Card.make(Suit.BLACK,  40),
        Card.make(Suit.YELLOW, 40),
        BEAR_CARD,        
        BULL_CARD,
    )
    assert rules.score_hand(cards) == 160_000, "Bull seconds doubles"

    cards = (
        BEAR_CARD,
        Card.make(Suit.BLACK,  40),
        Card.make(Suit.YELLOW, 40),
        BULL_CARD,
    )
    assert rules.score_hand(cards) == 160_000, \
        "Bull seconds doubles (different order)"

    cards = (
        TIGER_CARD,
        Card.make(Suit.BLACK,  40),
        Card.make(Suit.YELLOW, 40),
        Card.make(Suit.BLACK,   1),
    )
    assert rules.score_hand(cards) == 80_000, "Tiger is 0"


def test_valid_play():
    hand = (
        Card.make(Suit.BLACK, 4),
        Card.make(Suit.YELLOW, 2),
        Card.make(Suit.GREEN, 1),
        Card.make(Suit.BLACK, 2),
        TIGER_CARD,
        Card.make(Suit.RED, 1),
        Card.make(Suit.BLACK, 3),
        Card.make(Suit.BLACK, 8),
        Card.make(Suit.GREEN, 5),
        Card.make(Suit.BULL, 0),
        Card.make(Suit.YELLOW, 5),
        Card.make(Suit.YELLOW, 15),
        Card.make(Suit.GREEN, 2),
    )
    card = Card.make(Suit.BLACK, 4)
    trick = []
    assert rules.valid_play(card=card,
                            hand=hand,
                            trick=trick,
                            trump=Suit.BLACK,
                            trump_broken=False,
    ) == False, "Trumps aren't broken"
    
    hand = (
        Card.make(Suit.BLACK, 4),
        Card.make(Suit.YELLOW, 2),
        Card.make(Suit.GREEN, 1),
        Card.make(Suit.BLACK, 2),
        TIGER_CARD,
        Card.make(Suit.RED, 1),
        Card.make(Suit.BLACK, 3),
        Card.make(Suit.BLACK, 8),
        Card.make(Suit.GREEN, 5),
        Card.make(Suit.BULL, 0),
        Card.make(Suit.YELLOW, 5),
        Card.make(Suit.YELLOW, 15),
        Card.make(Suit.GREEN, 2),
    )
    card = Card.make(Suit.BLACK, 4)
    trick = []
    assert rules.valid_play(card=card,
                            hand=hand,
                            trick=trick,
                            trump=Suit.BLACK,
                            trump_broken=True,
    ) == True, "Trumps are broken"

    hand = (
        Card.make(Suit.BLACK, 4),
        Card.make(Suit.YELLOW, 2),
        Card.make(Suit.GREEN, 1),
        Card.make(Suit.BLACK, 2),
        TIGER_CARD,
        Card.make(Suit.RED, 1),
        Card.make(Suit.BLACK, 3),
        Card.make(Suit.BLACK, 8),
        Card.make(Suit.GREEN, 5),
        Card.make(Suit.BULL, 0),
        Card.make(Suit.YELLOW, 5),
        Card.make(Suit.YELLOW, 15),
        Card.make(Suit.GREEN, 2),
    )
    card = TIGER_CARD
    trick = []
    assert rules.valid_play(card=card,
                            hand=hand,
                            trick=trick,
                            trump=Suit.BLACK,
                            trump_broken=False,
    ) == False, "Trumps aren't broken (Tiger is trump)"
    
