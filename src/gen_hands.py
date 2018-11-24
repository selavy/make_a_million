#!/usr/bin/env python

import mmillion.rules as mm


deck = mm.make_deck()
mm.shuffle_deck(deck)


def print_hand(hand):
    print("    hand = (")
    for card in hand:
        print(f"        Card(Suit.{card.suit.name}, {card.rank}),")
    print("    )")


hand = deck[:13]
print_hand(hand)
