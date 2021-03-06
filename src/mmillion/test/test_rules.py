#!/usr/bin/env python

import mmillion.rules as rules
from mmillion.rules import Card
from mmillion.rules import Suit
from mmillion.rules import TIGER_CARD
from mmillion.rules import BULL_CARD
from mmillion.rules import BEAR_CARD


def test_card_is_flyweight():
    assert Card(Suit.TIGER, 41) is Card(Suit.TIGER, 41)
    assert Card(Suit.YELLOW, 1) is Card(Suit.YELLOW, 1)

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
        Card(Suit.YELLOW, 1),
        Card(Suit.BLACK,  2),
        Card(Suit.YELLOW, 3),
        Card(Suit.GREEN,  4),
    )
    assert rules.find_lead_suit(cards) == Suit.YELLOW

    cards = (
        BEAR_CARD,
        Card(Suit.BLACK,  2),
        Card(Suit.YELLOW, 3),
        Card(Suit.GREEN,  4),
    )
    assert rules.find_lead_suit(cards) == Suit.BLACK, \
        "Skip bear if first card"

    cards = (
        BULL_CARD,
        Card(Suit.BLACK,  2),
        Card(Suit.YELLOW, 3),
        Card(Suit.GREEN,  4),
    )
    assert rules.find_lead_suit(cards) == Suit.BLACK, \
        "Skip bull if first card"

    cards = (
        TIGER_CARD,
        Card(Suit.BLACK,  2),
        Card(Suit.YELLOW, 3),
        Card(Suit.GREEN,  4),
    )
    assert rules.find_lead_suit(cards) == Suit.TIGER, \
        "Tiger first means trump is lead"

    assert rules.find_lead_suit([]) is None, \
        "Handle no cards in trick"


def test_winner():
    cards = (
        Card(Suit.BLACK, 40),
        Card(Suit.BLACK, 30),
        Card(Suit.BLACK, 10),
        TIGER_CARD,
    )
    assert rules.winner(Suit.BLACK, cards) == 3, "Tiger always wins"

    cards = (
        Card(Suit.BLACK, 10),
        Card(Suit.BLACK, 30),
        Card(Suit.BLACK, 40),
        Card(Suit.BLACK, 1),
    )
    assert rules.winner(Suit.YELLOW, cards) == 2, "High card of lead suit"
    
    cards = (
        Card(Suit.BLACK, 10),
        Card(Suit.BLACK, 30),
        Card(Suit.BLACK, 40),
        Card(Suit.YELLOW, 1),
    )
    assert rules.winner(Suit.YELLOW, cards) == 3, "Trump card wins"

    cards = (
        Card(Suit.BLACK,  10),
        Card(Suit.YELLOW, 30),
        Card(Suit.BLACK,  40),
        Card(Suit.YELLOW,  1),
    )
    assert rules.winner(Suit.YELLOW, cards) == 1, "High trump card"

    cards = (
        Card(Suit.RED,    1),
        Card(Suit.BLACK, 30),
        Card(Suit.BLACK, 40),
        Card(Suit.BLACK, 10),
    )
    assert rules.winner(Suit.YELLOW, cards) == 0, "High lead suit"

    cards = (
        Card(Suit.RED,    1),
        Card(Suit.BLACK, 30),
        Card(Suit.BLACK, 40),
        Card(Suit.RED,   10),
    )
    assert rules.winner(Suit.YELLOW, cards) == 3, "High lead suit"

    cards = (
        BEAR_CARD,
        Card(Suit.BLACK, 30),
        Card(Suit.BLACK, 40),
        Card(Suit.RED,   10),
    )
    assert rules.winner(Suit.YELLOW, cards) == 2, \
        "High lead suit with Bear start"

    cards = (
        BULL_CARD,
        Card(Suit.BLACK, 30),
        Card(Suit.BLACK, 40),
        Card(Suit.RED,   10),
    )
    assert rules.winner(Suit.YELLOW, cards) == 2, \
        "High lead suit with Bull start"

    cards = (
        BULL_CARD,
        BEAR_CARD,
        Card(Suit.BLACK,  1),
        Card(Suit.RED,   10),
    )
    assert rules.winner(Suit.YELLOW, cards) == 2, \
        "High lead suit with Bull and Bear start"

    
def test_score_hand():
    cards = (
        Card(Suit.BLACK,  1),
        Card(Suit.YELLOW, 1),
        Card(Suit.RED,    1),
        Card(Suit.GREEN,  1),
    )
    assert rules.score_hand(cards) == 0

    cards = (
        Card(Suit.BLACK,  1),
        Card(Suit.YELLOW, 40),
        Card(Suit.RED,    1),
        Card(Suit.GREEN,  1),
    )
    assert rules.score_hand(cards) == 40_000

    cards = (
        Card(Suit.BLACK,  40),
        Card(Suit.YELLOW, 40),
        Card(Suit.RED,    40),
        Card(Suit.GREEN,  40),
    )
    assert rules.score_hand(cards) == 160_000

    cards = (
        Card(Suit.BLACK,  40),
        Card(Suit.YELLOW, 40),
        Card(Suit.RED,    40),
        BULL_CARD,
    )
    assert rules.score_hand(cards) == 240_000, "Bull doubles"

    cards = (
        Card(Suit.BLACK,  40),
        Card(Suit.YELLOW, 40),
        Card(Suit.RED,    40),
        BEAR_CARD,
    )
    assert rules.score_hand(cards) == 0, "Bear cancels"

    cards = (
        Card(Suit.BLACK,  40),
        Card(Suit.YELLOW, 40),
        BULL_CARD,
        BEAR_CARD,
    )
    assert rules.score_hand(cards) == 0, "Bear seconds cancels"

    cards = (
        BULL_CARD,        
        Card(Suit.BLACK,  40),
        Card(Suit.YELLOW, 40),
        BEAR_CARD,
    )
    assert rules.score_hand(cards) == 0, \
        "Bear seconds cancels (different order)"

    cards = (
        Card(Suit.BLACK,  40),
        Card(Suit.YELLOW, 40),
        BEAR_CARD,        
        BULL_CARD,
    )
    assert rules.score_hand(cards) == 160_000, "Bull seconds doubles"

    cards = (
        BEAR_CARD,
        Card(Suit.BLACK,  40),
        Card(Suit.YELLOW, 40),
        BULL_CARD,
    )
    assert rules.score_hand(cards) == 160_000, \
        "Bull seconds doubles (different order)"

    cards = (
        TIGER_CARD,
        Card(Suit.BLACK,  40),
        Card(Suit.YELLOW, 40),
        Card(Suit.BLACK,   1),
    )
    assert rules.score_hand(cards) == 80_000, "Tiger is 0"


def test_valid_play():
    hand = (
        Card(Suit.BLACK, 4),
        Card(Suit.YELLOW, 2),
        Card(Suit.GREEN, 1),
        Card(Suit.BLACK, 2),
        TIGER_CARD,
        Card(Suit.RED, 1),
        Card(Suit.BLACK, 3),
        Card(Suit.BLACK, 8),
        Card(Suit.GREEN, 5),
        Card(Suit.BULL, 0),
        Card(Suit.YELLOW, 5),
        Card(Suit.YELLOW, 15),
        Card(Suit.GREEN, 2),
    )
    card = Card(Suit.BLACK, 4)
    trick = []
    assert rules.valid_play(card=card,
                            hand=hand,
                            trick=trick,
                            trump=Suit.BLACK,
                            trump_broken=False,
    ) == False, "Trumps aren't broken"
    
    hand = (
        Card(Suit.BLACK, 4),
        Card(Suit.YELLOW, 2),
        Card(Suit.GREEN, 1),
        Card(Suit.BLACK, 2),
        TIGER_CARD,
        Card(Suit.RED, 1),
        Card(Suit.BLACK, 3),
        Card(Suit.BLACK, 8),
        Card(Suit.GREEN, 5),
        Card(Suit.BULL, 0),
        Card(Suit.YELLOW, 5),
        Card(Suit.YELLOW, 15),
        Card(Suit.GREEN, 2),
    )
    card = Card(Suit.BLACK, 4)
    trick = []
    assert rules.valid_play(card=card,
                            hand=hand,
                            trick=trick,
                            trump=Suit.BLACK,
                            trump_broken=True,
    ) == True, "Trumps are broken"

    hand = (
        Card(Suit.BLACK, 4),
        Card(Suit.YELLOW, 2),
        Card(Suit.GREEN, 1),
        Card(Suit.BLACK, 2),
        TIGER_CARD,
        Card(Suit.RED, 1),
        Card(Suit.BLACK, 3),
        Card(Suit.BLACK, 8),
        Card(Suit.GREEN, 5),
        Card(Suit.BULL, 0),
        Card(Suit.YELLOW, 5),
        Card(Suit.YELLOW, 15),
        Card(Suit.GREEN, 2),
    )
    card = TIGER_CARD
    trick = []
    assert rules.valid_play(card=card,
                            hand=hand,
                            trick=trick,
                            trump=Suit.BLACK,
                            trump_broken=False,
    ) == False, "Trumps aren't broken (Tiger is trump)"

    hand = (
        Card(Suit.BLACK, 4),
        Card(Suit.YELLOW, 2),
        Card(Suit.GREEN, 1),
        Card(Suit.BLACK, 2),
        TIGER_CARD,
        Card(Suit.RED, 1),
        Card(Suit.BLACK, 3),
        Card(Suit.BLACK, 8),
        Card(Suit.GREEN, 5),
        Card(Suit.BULL, 0),
        Card(Suit.YELLOW, 5),
        Card(Suit.YELLOW, 15),
        Card(Suit.GREEN, 2),
    )
    card = TIGER_CARD
    trick = [Card(Suit.YELLOW, 40)]
    assert rules.valid_play(card=card,
                            hand=hand,
                            trick=trick,
                            trump=Suit.BLACK,
                            trump_broken=False,
    ) == False, "Not following lead color when have other options"

    hand = (
        TIGER_CARD,
        BEAR_CARD,
        BULL_CARD
    )
    card = TIGER_CARD
    trick = []
    assert rules.valid_play(card=card,
                            hand=hand,
                            trick=trick,
                            trump=Suit.BLACK,
                            trump_broken=False,
    ) == True, "Only animal cards so can lead tiger"

    hand = (
        Card(Suit.YELLOW, 8),
        Card(Suit.GREEN, 30),
        Card(Suit.RED, 10),
        Card(Suit.BLACK, 15),
        Card(Suit.YELLOW, 7),
        Card(Suit.GREEN, 4),
        Card(Suit.YELLOW, 40),
        TIGER_CARD,
        Card(Suit.GREEN, 7),
        Card(Suit.RED, 30),
        Card(Suit.GREEN, 10),
        Card(Suit.RED, 8),
        Card(Suit.GREEN, 2),
    )
    card = Card(Suit.GREEN, 2)
    trick = [
        Card(Suit.YELLOW, 9),
        Card(Suit.BLACK, 7),
        Card(Suit.GREEN, 9),
    ]
    assert rules.valid_play(card=card,
                            hand=hand,
                            trick=trick,
                            trump=Suit.RED,
                            trump_broken=True,
    ) == False, "Not following lead suit"

    hand = (
        Card(Suit.YELLOW, 40),
        Card(Suit.RED, 8),
        Card(Suit.RED, 11),
        Card(Suit.GREEN, 2),
        Card(Suit.RED, 10),
        Card(Suit.RED, 40),
        Card(Suit.GREEN, 7),
        Card(Suit.YELLOW, 30),
        Card(Suit.YELLOW, 11),
        Card(Suit.RED, 30),
        Card(Suit.GREEN, 4),
        Card(Suit.GREEN, 15),
        Card(Suit.BLACK, 11),
    )
    card = Card(Suit.BLACK, 11)
    trick = [
        Card(Suit.BLACK, 7),
        Card(Suit.YELLOW, 5),
        Card(Suit.YELLOW, 15),
    ]
    assert rules.valid_play(card=card,
                            hand=hand,
                            trick=trick,
                            trump=Suit.GREEN,
                            trump_broken=False,
    ) == True

    hand = (
        Card(Suit.GREEN, 30),
        Card(Suit.BLACK, 5),
        Card(Suit.GREEN, 9),
        Card(Suit.GREEN, 8),
        Card(Suit.BLACK, 3),
        Card(Suit.YELLOW, 5),
        Card(Suit.GREEN, 5),
        Card(Suit.RED, 7),
        Card(Suit.BLACK, 8),
        Card(Suit.YELLOW, 1),
        BEAR_CARD,
        Card(Suit.RED, 5),
        Card(Suit.GREEN, 15),
    )
    card = Card(Suit.BLACK, 5)
    trick = [
        Card(Suit.BLACK, 1),
        Card(Suit.BLACK, 11),
        Card(Suit.RED, 1),
    ]
    assert rules.valid_play(card=card,
                            hand=hand,
                            trick=trick,
                            trump=Suit.BLACK,
                            trump_broken=True,
    ) == True
    
    hand = (
        Card(Suit.YELLOW, 10),
        Card(Suit.YELLOW, 9),
        Card(Suit.YELLOW, 5),
        Card(Suit.YELLOW, 3),
        TIGER_CARD,
    )
    card = Card(Suit.YELLOW, 3)
    trick = [
        Card(Suit.GREEN, 8),
        Card(Suit.RED, 8),
        Card(Suit.RED, 4),
    ]
    assert rules.valid_play(card=card,
                            hand=hand,
                            trick=trick,
                            trump=Suit.BLACK,
                            trump_broken=False,
    ) == True
    
