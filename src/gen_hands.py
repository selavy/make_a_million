#!/usr/bin/env python

import mmillion.rules as mm
from mmillion.rules import Suit
import random


deck = mm.make_deck()
mm.shuffle_deck(deck)

def fmt_card(card):
    if card.suit == Suit.TIGER:
        return "TIGER_CARD"
    elif card.suit == Suit.BEAR:
        return "BEAR_CARD"
    elif card.suit == Suit.BULL:
        return "BULL_CARD"
    else:
        return f"Card(Suit.{card.suit.name}, {card.rank})"


def print_hand(hand, card, trick, trump, trump_broken):
    print(f"    hand = (")
    for card in hand:
        print(f"        {fmt_card(card)},")
    print(f"    )")
    print(f"    card = {fmt_card(card)}")
    if trick:
        print(f"    trick = [")
        for c in trick:
            print(f"        {fmt_card(c)},")
        print(f"    ]")
    else:
        print(f"    trick = []")
    print(f"    assert rules.valid_play(card=card,")
    print(f"                            hand=hand,")
    print(f"                            trick=trick,")
    print(f"                            trump={trump},")
    print(f"                            trump_broken={trump_broken},")
    print(f"    ) == True")


suits = [Suit.RED, Suit.BLACK, Suit.YELLOW, Suit.GREEN,]
hand = deck[:13]
card = hand[0]
trick = []
trick_cards = 3
for i in range(trick_cards):
    trick.append(deck[random.randint(14, len(deck)-1)])
trump = suits[random.randint(0, 3)]
trump_broken = bool(random.randint(0, 1))
print_hand(hand, card, trick, trump, trump_broken)

