#!/usr/bin/env python


import mmillion.rules as rules
# import rules


def test_rank_as_str():
    assert rules.rank_as_str(40) == "$40,000"
    assert rules.rank_as_str(30) == "$30,000"    
    assert rules.rank_as_str(10) == "$10,000"
    assert rules.rank_as_str(5)  == "$5,000"
    assert rules.rank_as_str(1)  == "1"
    assert rules.rank_as_str(3)  == "3"
    
