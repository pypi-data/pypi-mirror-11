#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Abstract pattern class definition along with various implementations (regexp, string, functional)
"""

from abc import ABCMeta, abstractmethod, abstractproperty
import re

import six

from .match import Match
from .utils import find_all


@six.add_metaclass(ABCMeta)
class Pattern(object):
    """
    Definition of a particular pattern to search for.
    """

    def __init__(self, label=None, examples=None, tags=None, formatters=None):
        """
        :param label: Unique label for this pattern
        :type label: str
        :param examples: List of example strings that match this pattern
        :type examples: list[str]
        :param tags: List of tags related to this pattern
        :type tags: list[str]
        :param formatters: dict (name, func) of formatter to use with this pattern. name is the match name to support,
        and func a function(input_string) that returns the formatted string. A single formatter function can also be
        passed as a shortcut for {None: formatter}. The returned formatted string with be set in Match.value property.
        :type formatters: dict[str, func] || func
        """
        self.label = label
        self.examples = examples
        self.tags = tags
        self._default_formatter = lambda x: x
        if not formatters:
            formatters = self._default_formatter
        if not isinstance(formatters, dict):
            self.formatters = {None: formatters}
        else:
            self.formatters = formatters

    def matches(self, input_string):
        """
        Computes all matches for a given input

        :param input_string: the string to parse
        :type input_string: str
        :return: matches based on input_string for this pattern
        :rtype: iterator[Match]
        """
        for pattern in self.patterns:
            for match in self._match(pattern, input_string):
                if match.value is None:
                    value = input_string[match.start:match.end]
                    formatter = self.formatters.get(match.name, self._default_formatter)
                    value = formatter(value)
                    match.value = value
                for child in match.children:
                    if child.value is None:
                        value = input_string[child.start:child.end]
                        formatter = self.formatters.get(child.name, self._default_formatter)
                        value = formatter(value)
                        child.value = value
                yield match

    @abstractproperty
    def patterns(self):
        """
        List of base patterns defined

        :return: A list of base patterns
        :rtype: list
        """
        pass

    @abstractmethod
    def _match(self, pattern, input_string):  # pragma: no cover
        """
        Computes all matches for a given pattern and input

        :param pattern: the pattern to use
        :param input_string: the string to parse
        :type input_string: str
        :return: matches based on input_string for this pattern
        :rtype: iterator[Match]
        """
        pass


class StringPattern(Pattern):
    """
    Definition of one or many strings to search for.
    """

    def __init__(self, *patterns, **kwargs):
        super(StringPattern, self).__init__(**kwargs)
        self._patterns = patterns

    @property
    def patterns(self):
        return self._patterns

    def _match(self, pattern, input_string):
        for index in find_all(input_string, pattern):
            yield Match(self, index, index + len(pattern))


class RePattern(Pattern):
    """
    Definition of one or many regular expression pattern to search for.
    """

    def __init__(self, *patterns, **kwargs):
        super(RePattern, self).__init__(**kwargs)
        self._patterns = []
        for pattern in patterns:
            if isinstance(pattern, six.string_types):
                pattern = re.compile(pattern)
            elif isinstance(pattern, dict):
                pattern = re.compile(**pattern)
            elif hasattr(pattern, '__iter__'):
                pattern = re.compile(*pattern)
            self._patterns.append(pattern)

    @property
    def patterns(self):
        return self._patterns

    def _match(self, pattern, input_string):
        names = {v: k for k, v in pattern.groupindex.items()}
        for match_object in pattern.finditer(input_string):
            start = match_object.start()
            end = match_object.end()
            main_match = Match(self, start, end)

            if pattern.groups:
                for i in range(1, pattern.groups + 1):
                    name = names.get(i, None)
                    start = match_object.start(i)
                    end = match_object.end(i)
                    child_match = Match(self, start, end, name=name, parent=main_match)
                    main_match.children.append(child_match)

            yield main_match


class FunctionalPattern(Pattern):
    """
    Definition of one or many functional pattern to search for.
    """

    def __init__(self, *patterns, **kwargs):
        super(FunctionalPattern, self).__init__(**kwargs)
        self._patterns = patterns

    @property
    def patterns(self):
        return self._patterns

    def _match(self, pattern, input_string):
        ret = pattern(input_string)
        if ret:
            if isinstance(ret, dict):
                yield Match(self, **ret)
            else:
                yield Match(self, *ret)
