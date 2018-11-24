#!/usr/bin/env python


# import mmillion.rules as rules
import rules


def test_rank_as_str():
    assert rules.rank_as_str(40) == "$40,000"
    assert rules.rank_as_str(10) == ""
    
