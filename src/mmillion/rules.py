#!/usr/bin/env python

from enum import Enum
from enum import IntEnum
from enum import auto
from typing import List
from typing import Union
from typing import Dict
from typing import Tuple
from typing import Type


MIN_BID = 175_000
GOAL_AMOUNT = 1_000_000


class Suit(Enum):
    RED = auto()
    YELLOW = auto()
    BLACK = auto()
    GREEN = auto()
    # REVISIT(peter): is it better to have the animals as separate suits?
    # REVISIT(peter): could instead of bitfield so that TIGER could be (TIGER | TRUMP)?
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


def rank_as_str(x: int) -> str:
    if x in MONEY_CARDS:
        return f'${x:d},000'
    else:
        return f'{x:d}'


class Card:
    _cache: Dict[Tuple[Suit, int], object] = {}
    
    def __new__(cls: Type[object], suit: Suit, rank: int):
        key = (suit, rank)
        try:
            return cls._cache[key]
        except KeyError:
            card = object.__new__(cls)
            cls._cache[key] = card
            return card
    
    def __init__(self, suit: Suit, rank: int) -> None:
        self.suit = Suit(suit)
        self.rank = int(rank)
        assert self.rank in RANKS

    def value(self) -> int:
        if self.rank in MONEY_CARDS:
            return self.rank * 1000
        else:
            return 0

    def __repr__(self):
        rank = rank_as_str(self.rank)
        return f'<Card: {self.suit.name} {rank}>'

    def __str__(self):
        if self.suit in ANIMAL_SUITS:
            return self.suit.name
        else:
            rank = rank_as_str(self.rank)
            return f'{self.suit.name} {rank}'


TIGER_CARD = Card(Suit.TIGER, rank=41)
BEAR_CARD = Card(Suit.BEAR, rank=0)
BULL_CARD = Card(Suit.BULL, rank=0)


def make_deck() -> List[Card]:
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

    deck: List[Card] = []
    for suit in NON_ANIMAL_SUITS:
        deck.extend(make_suit(suit))
    deck.append(BEAR_CARD)
    deck.append(BULL_CARD)
    deck.append(TIGER_CARD)
    return deck


def find_lead_suit(cards: List[Card]) -> Union[Suit, None]:
    for card in cards:
        # TODO(peter): does leading the tiger mean trump is lead card?
        if card.suit == Suit.TIGER or card.suit in NON_ANIMAL_SUITS:
            return card.suit
    else:
        return None


def winner(trump: Suit, cards: List[Card]) -> int:
    hidx = 0
    lead = find_lead_suit(cards)
    assert lead is not None, "Unable to determine lead suit!"
    if lead == Suit.TIGER:
        lead = trump
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


def score_hand(cards: List[Card]) -> int:
    score = sum([c.value() for c in cards])
    for card in reversed(cards):
        if card.suit == Suit.BEAR:
            score = 0
            break
        elif card.suit == Suit.BULL:
            score *= 2
            break
    return score


def shuffle_deck(cards: List[Card]) -> List[Card]:
    from random import shuffle
    shuffle(cards)
    return cards


def valid_play(card: Card,
               hand: List[Card],
               trick: List[Card],
               trump: Suit,
               trump_broken: bool,
               ) -> bool:
    if card not in hand:
        assert False, "Tried to play card not in hand"
        return False
    assert card not in trick, \
        "Trying to play card already in trick, must have been duplicate"
    if not trick:  # first card to be played
        if card.suit in (Suit.BEAR, Suit.BULL):
            # can only lead with Bear or Bull if no other options
            hand_wo_card = [c for c in hand if c != card]
            assert len(hand_wo_card) == (len(hand) - 1)
            valid = [
                c for c in hand_wo_card
                if valid_play(c, hand_wo_card, trick, trump, trump_broken)
            ]
            return not valid
        elif card.suit == trump or card.suit == Suit.TIGER:
            return trump_broken
        else:
            return True

    assert trick, "This play is not leading"
    lead = find_lead_suit(trick)
    if card.suit == lead:
        return True
    if card.suit == Suit.TIGER and lead == trump:
        return True
    other_valid = [c for c in hand if c != card and c.suit == lead]
    return not other_valid
    
