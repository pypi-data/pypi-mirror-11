from contoml.elements import abstracttable, factory
from contoml.elements.common import Element
from contoml.elements.metadata import CommentElement, NewlineElement, WhitespaceElement


class TableElement(abstracttable.AbstractTable):
    """
    An Element containing an unnamed top-level table.

    Implements dict-like interface.

    Assumes input sub_elements are correct.
    """

    def __init__(self, sub_elements):
        abstracttable.AbstractTable.__init__(self, sub_elements)

    def __setitem__(self, key, value):
        if key in self:
            self._update(key, value)
        else:
            self._insert(key, value)

    def _update(self, key, value):
        _, value_i = self._find_key_and_value(key)
        self._sub_elements[value_i] = value if isinstance(value, Element) else factory.create_element(value)

    def _find_insertion_index(self):
        """
        Returns the self.sub_elements index in which new entries should be inserted.
        """

        non_metadata_elements = tuple(self._enumerate_non_metadata_sub_elements())

        if not non_metadata_elements:
            return 0

        last_entry_i = non_metadata_elements[-1][0]
        following_newline_i = self._find_following_line_terminator(last_entry_i)

        return following_newline_i + 1

    def _detect_indentation_size(self):
        """
        Detects the level of indentation used in this table.
        """

        def lines():
            # Returns a sequence of sequences of elements belonging to each line
            start = 0
            for i, element in enumerate(self.elements):
                if isinstance(element, (CommentElement, NewlineElement)):
                    yield self.elements[start:i+1]
                    start = i+1

        def indentation(line):
            # Counts the number of whitespace tokens at the beginning of this line
            try:
                first_non_whitespace_i = next(i for (i, e) in enumerate(line) if not isinstance(e, WhitespaceElement))
                return sum(space.length for space in line[:first_non_whitespace_i])
            except StopIteration:
                return 0

        try:
            return min(indentation(line) for line in lines() if len(line) > 1)
        except ValueError:  # Raised by ValueError when no matching lines found
            return 0

    def _insert(self, key, value):

        value_element = value if isinstance(value, Element) else factory.create_element(value)

        indentation_size = self._detect_indentation_size()
        indentation = [factory.create_whitespace_element(self._detect_indentation_size())] if indentation_size else []

        inserted_elements = indentation + [
            factory.create_element(key),
            factory.create_whitespace_element(),
            factory.create_operator_element('='),
            factory.create_whitespace_element(),
            value_element,
            factory.create_newline_element(),
        ]
        
        insertion_index = self._find_insertion_index()
        
        self._sub_elements = \
            self.sub_elements[:insertion_index] + inserted_elements + self.sub_elements[insertion_index:]

        # if self:    # If not empty
        #     insertion_index = len(self.sub_elements)   # Index of last value + 1
        #     elements = [
        #         factory.create_newline_element(),
        #         factory.create_element(key),
        #         factory.create_whitespace_element(),
        #         factory.create_operator_element('='),
        #         factory.create_whitespace_element(),
        #         value_element,
        #         factory.create_newline_element(),
        #     ]
        #     self._sub_elements = self.sub_elements[:insertion_index] + elements + self.sub_elements[insertion_index:]
        # else:
        #     self._sub_elements = [
        #         factory.create_element(key),
        #         factory.create_whitespace_element(),
        #         factory.create_operator_element('='),
        #         factory.create_whitespace_element(),
        #         value_element,
        #         factory.create_newline_element(),
        #     ]

    def __delitem__(self, key):
        begin, _ = self._find_key_and_value(key)
        preceding_newline = self._find_preceding_newline(begin)
        if preceding_newline >= 0:
            begin = preceding_newline
        end = self._find_following_newline(begin)
        if end < 0:
            end = len(tuple(self._sub_elements))
        self._sub_elements = self.sub_elements[:begin] + self.sub_elements[end:]

    def value(self):
        return self
