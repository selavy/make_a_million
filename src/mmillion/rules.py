#!/usr/bin/env python

from enum import Enum
from enum import IntEnum
from enum import auto


class Suit(Enum):
    RED = auto()
    YELLOW = auto()
    BLACK = auto()
    GREEN = auto()
    # REVISIT(peter): is it better to have the animals as separate
    #                 suits or 
    BEAR = auto()
    BULL = auto()
    TIGER = auto()


NON_ANIMAL_SUITS = {
    Suit.RED, Suit.YELLOW, Suit.BLACK, Suit.GREEN,
}


ANIMAL_SUITS = {
    Suit.BEAR, Suit.BULL, Suit.TIGER,
}


# Tiger -> 41
# Bear, Bull -> 0
RANKS = [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 15, 30, 40, 41]
RESERVED_RANKS = [0, 41]
MONEY_CARDS = {5, 10, 15, 30, 40}


def rank_as_str(x):
    if x in MONEY_CARDS:
        return f'${x:d},000'
    else:
        return f'{x:d}'
    

class Card:
    def __init__(self, suit, rank):
        self.suit = Suit(suit)
        self.rank = int(rank)
        assert self.rank in RANKS

    def __repr__(self):
        # if self.rank in MONEY_CARDS:
        #     rank = f'${self.rank},000'
        # else:
        #     rank = self.rank
        rank = rank_as_str(self.rank)
        return f'<Card: {self.suit.name} {rank}>'

    def __str__(self):
        rank = rank_as_str(self.rank)
        return f'{self.suit.name} {rank}'


TIGER_CARD = Card(Suit.TIGER, rank=41)
BEAR_CARD = Card(Suit.BEAR, rank=0)
BULL_CARD = Card(Suit.BULL, rank=0)


def make_suit(suit):
    deck = []
    for i in RANKS:
        if i == 6:  # NOTE(peter); no 6 card for some reason
            continue
        elif i in RESERVED_RANKS:
            continue
        else:
            deck.append(Card(suit, rank=i))
    return deck


def make_deck():
    deck = []
    for suit in NON_ANIMAL_SUITS:
        deck.extend(make_suit(suit))
    deck.append(BEAR_CARD)
    deck.append(BULL_CARD)
    deck.append(TIGER_CARD)
    return deck


# TODO(peter): maybe the interface should be wins(trump, lead, cards) -> index
# def wins(trump, lead, c1, c2):
#     if c1.suit == trump and c2.suit != trump:
#         return True
#     if c1.suit != trump and c2.suit == trump:
#         return False
#     if c1.suit == lead and c2.suit != lead:
#         return True
#     if c1.suit != lead and c2.suit == lead:
#         return False
#     if c1.rank == c2.rank:  # NOTE(peter): to handle weird case of bear vs bull
#         return True
#     else:
#         return c1.rank > c2.rank

def find_lead_suit(cards):
    for card in cards:
        # TODO(peter): does leading the tiger mean trump is lead card?
        if card.suit == Suit.TIGER or card.suit in NON_ANIMAL_SUITS:
            return card.suit
    else:
        assert False, "Unable to find a lead suit!"
        return None


def winner(trump, cards):
    hidx = 0
    lead = find_lead_suit(cards) or trump
    for i, card in enumerate(cards):
        high = cards[hidx]
        if high.suit == Suit.TIGER:
            break
        elif card.suit == Suit.TIGER:
            hidx = i
            break
        elif high.suit == trump and card.suit != trump:
            continue
        elif high.suit != trump and card.suit == trump:
            hidx = i
        elif high.suit == lead and card.suit != lead:
            continue
        elif high.suit != lead and card.suit == lead:
            hidx = i
        else:
            assert high.suit != Suit.TIGER
            assert card.suit != Suit.TIGER
            assert (high.suit != trump) == (card.suit != trump)
            assert (high.suit != lead) == (card.suit != lead)
            if card.rank > high.rank:
                hidx = i
    return hidx

