#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=no-self-use, pointless-statement, missing-docstring

import pytest
import six

from ..match import Match, Matches, group_neighbors
from ..pattern import StringPattern


class TestMatchClass(object):
    pattern = StringPattern("test")

    def test_str(self):
        match1 = Match(self.pattern, 1, 3, value="es")

        assert str(match1) == 'Match<span=(1, 3), value=\'es\'>'

    def test_equality(self):
        match1 = Match(self.pattern, 1, 3, value="es")
        match2 = Match(self.pattern, 1, 3, value="es")

        other = object()

        assert hash(match1) == hash(match2)
        assert hash(match1) != hash(other)

        assert match1 == match2
        assert not match1 == other

    def test_inequality(self):
        match1 = Match(self.pattern, 0, 2, value="te")
        match2 = Match(self.pattern, 2, 4, value="st")
        match3 = Match(self.pattern, 0, 2, value="other")

        other = object()

        assert hash(match1) != hash(match2)
        assert hash(match1) != hash(match3)

        assert match1 != other
        assert match1 != match2
        assert match1 != match3

    def test_length(self):
        match1 = Match(self.pattern, 0, 4, value="test")
        match2 = Match(self.pattern, 0, 2, value="spanIsUsed")

        assert len(match1) == 4
        assert len(match2) == 2

    def test_compare(self):
        match1 = Match(self.pattern, 0, 2, value="te")
        match2 = Match(self.pattern, 2, 4, value="st")

        other = object()

        assert match1 < match2
        assert match1 <= match2

        assert match2 > match1
        assert match2 >= match1

        if six.PY3:
            with pytest.raises(TypeError):
                match1 < other

            with pytest.raises(TypeError):
                match1 <= other

            with pytest.raises(TypeError):
                match1 > other

            with pytest.raises(TypeError):
                match1 >= other


class TestMatchesClass(object):
    pattern = StringPattern("test")

    match1 = Match(pattern, 0, 2, value="te")
    match2 = Match(pattern, 2, 3, value="s")
    match3 = Match(pattern, 3, 4, value="t")
    match4 = Match(pattern, 2, 4, value="st")

    def test_base(self):
        matches = Matches()
        matches.append(self.match1)

        assert len(matches) == 1
        assert list(matches.starting(0)) == [self.match1]
        assert list(matches.ending(2)) == [self.match1]

        matches.append(self.match2)
        matches.append(self.match3)
        matches.append(self.match4)

        assert len(matches) == 4
        assert list(matches.starting(2)) == [self.match2, self.match4]
        assert list(matches.starting(3)) == [self.match3]
        assert list(matches.ending(3)) == [self.match2]
        assert list(matches.ending(4)) == [self.match3, self.match4]

        matches.remove(self.match1)
        assert len(matches) == 3
        assert len(matches.starting(0)) == 0
        assert len(matches.ending(2)) == 0

        matches.clear()

        assert len(matches) == 0
        assert len(matches.starting(0)) == 0
        assert len(matches.starting(2)) == 0
        assert len(matches.starting(3)) == 0
        assert len(matches.ending(2)) == 0
        assert len(matches.ending(3)) == 0
        assert len(matches.ending(4)) == 0

    def test_get_slices(self):
        matches = Matches()
        matches.append(self.match1)
        matches.append(self.match2)
        matches.append(self.match3)
        matches.append(self.match4)

        slice_matches = matches[1:3]

        assert isinstance(slice_matches, Matches)

        assert len(slice_matches) == 2
        assert slice_matches[0] == self.match2
        assert slice_matches[1] == self.match3

    def test_remove_slices(self):
        matches = Matches()
        matches.append(self.match1)
        matches.append(self.match2)
        matches.append(self.match3)
        matches.append(self.match4)

        del matches[1:3]

        assert len(matches) == 2
        assert matches[0] == self.match1
        assert matches[1] == self.match4

    def test_set_slices(self):
        matches = Matches()
        matches.append(self.match1)
        matches.append(self.match2)
        matches.append(self.match3)
        matches.append(self.match4)

        matches[1:3] = self.match1, self.match4

        assert len(matches) == 4
        assert matches[0] == self.match1
        assert matches[1] == self.match1
        assert matches[2] == self.match4
        assert matches[3] == self.match4

    def test_set_index(self):
        matches = Matches()
        matches.append(self.match1)
        matches.append(self.match2)
        matches.append(self.match3)

        matches[1] = self.match4

        assert len(matches) == 3
        assert matches[0] == self.match1
        assert matches[1] == self.match4
        assert matches[2] == self.match3

    def test_iterator_constructor(self):
        matches = Matches([self.match1, self.match2, self.match3, self.match4])

        assert len(matches) == 4
        assert list(matches.starting(0)) == [self.match1]
        assert list(matches.ending(2)) == [self.match1]
        assert list(matches.starting(2)) == [self.match2, self.match4]
        assert list(matches.starting(3)) == [self.match3]
        assert list(matches.ending(3)) == [self.match2]
        assert list(matches.ending(4)) == [self.match3, self.match4]

    def test_constructor(self):
        matches = Matches(self.match1, self.match2, self.match3, self.match4)

        assert len(matches) == 4
        assert list(matches.starting(0)) == [self.match1]
        assert list(matches.ending(2)) == [self.match1]
        assert list(matches.starting(2)) == [self.match2, self.match4]
        assert list(matches.starting(3)) == [self.match3]
        assert list(matches.ending(3)) == [self.match2]
        assert list(matches.ending(4)) == [self.match3, self.match4]


class TestMatchFunctions(object):
    def test_group_neighbors(self):
        input_string = "abc.def._._.ghi.klm.nop.qrs.tuv.wyx.z"

        matches = StringPattern("abc", "def", "ghi", "nop", "qrs.tuv", "z").matches(input_string)
        matches_groups = list(group_neighbors(Matches(matches), input_string, "._"))

        assert len(matches_groups) == 3
        assert len(matches_groups[0]) == 3
        assert len(matches_groups[1]) == 2
        assert len(matches_groups[2]) == 1

        abc, def_, ghi = matches_groups[0]
        assert abc.value == "abc"
        assert def_.value == "def"
        assert ghi.value == "ghi"

        nop, qrstuv = matches_groups[1]
        assert nop.value == "nop"
        assert qrstuv.value == "qrs.tuv"

        z__ = matches_groups[2][0]
        assert z__.value == "z"
