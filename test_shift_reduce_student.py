# -*-coding:utf-8 -*-
# Author: Jana Götze
# Date: 2022-11-18

from shift_reduce import ShiftReduceParser
from nltk.grammar import CFG


class TestShiftReduce():
    grammar_elephant = CFG.fromstring("""
        S -> NP VP
        PP -> P NP
        NP -> Det N | Det N | 'I'
        VP -> V NP | VP PP
        Det -> 'an' | 'my'
        N -> 'elephant' | 'pajamas'
        V -> 'shot'
        P -> 'in'
        """)

    def test_elephant_sentence_chart_length(self):
        parser = ShiftReduceParser()
        parser.parse(self.grammar_elephant,
                     ["I", "shot", "an", "elephant", "in", "my", "pajamas"]
                     )
        assert len(parser.items) == 8

    def test_elephant_short(self):
        parser = ShiftReduceParser()
        parse = parser.parse(self.grammar_elephant,
                             ["I", "shot", "an", "elephant"]
                             )
        assert parse is True

    def test_elephant_long(self):
        parser = ShiftReduceParser()
        parse = parser.parse(self.grammar_elephant,
                             ["I", "shot", "an", "elephant", "in", "my", "pajamas"]
                             )
        assert parse is True

    def test_elephant_ungrammatical(self):
        parser = ShiftReduceParser()
        parse = parser.parse(self.grammar_elephant,
                             ["I", "shot", "an", "elephant", "in", "my"]
                             )
        assert parse is False

    def test_elephant_sentence_short_chart_pos_0_len(self):
        parser = ShiftReduceParser()
        parser.parse(self.grammar_elephant,
                     ["I", "shot", "an", "elephant"]
                     )
        assert len(parser.items[0]) == 1

    def test_elephant_sentence_short_chart_pos_1_len(self):
        parser = ShiftReduceParser()
        parser.parse(self.grammar_elephant,
                     ["I", "shot", "an", "elephant"]
                     )
        assert len(parser.items[1]) == 2

    def test_elephant_sentence_short_chart_pos_2_len(self):
        parser = ShiftReduceParser()
        parser.parse(self.grammar_elephant,
                     ["I", "shot", "an", "elephant"]
                     )
        assert len(parser.items[2]) == 4

    def test_elephant_sentence_short_chart_pos_3_len(self):
        parser = ShiftReduceParser()
        parser.parse(self.grammar_elephant,
                     ["I", "shot", "an", "elephant"]
                     )
        assert len(parser.items[3]) == 8

    def test_elephant_sentence_short_chart_pos_4_len(self):
        parser = ShiftReduceParser()
        parser.parse(self.grammar_elephant,
                     ["I", "shot", "an", "elephant"]
                     )
        assert len(parser.items[4]) == 23
