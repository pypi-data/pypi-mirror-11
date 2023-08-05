import re
from itertools import groupby

from . import modifiers, parent_revision, revision
from ..datasources import diff
from ..languages import is_badword, is_misspelled
from .feature import Feature
from .util import MARKUP_RE, NUMERIC_RE, SYMBOLIC_RE

bytes_changed = revision.bytes - parent_revision.bytes
"""
Represents encoded content bytes changed in this edit. It uses UTF-8 encoding.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(655097130, [diff.bytes_changed]))
        [297]
"""

bytes_changed_ratio = bytes_changed / modifiers.max(parent_revision.bytes, 1)
"""
Represents ratio of bytes changed in this edit compared to parent revision
size (in bytes).

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(655097130, [diff.bytes_changed_ratio]))
        [0.012515275378197294]
"""

def process_segments_added(diff_added_segments):
    return len(diff_added_segments)

segments_added = Feature("diff.segments_added", process_segments_added,
                         returns=int, depends_on=[diff.added_segments])
"""
Represents number of segments added in this edit.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(655097130, [diff.segments_added]))
        [1]
"""
def process_segment_removed(diff_segments_removed):
    return len(diff_segments_removed)

segments_removed = Feature("segments_removed", process_segment_removed,
                           returns=int, depends_on=[diff.removed_segments])
"""
Represents number of segments removed in this edit.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(660405537, [diff.segments_removed]))
        [3]
"""
############################## Characters ######################################

def process_chars_added(diff_added_segments):
    return len("".join(diff_added_segments))

chars_added = Feature("diff.chars_added", process_chars_added,
                      returns=int, depends_on=[diff.added_segments])
"""
Represents number of characters added in this edit.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(655097130, [diff.chars_added]))
        [297]
"""

def process_chars_removed(diff_removed_segments):
    return len("".join(diff_removed_segments))

chars_removed = Feature("diff.chars_removed", process_chars_removed,
                        returns=int, depends_on=[diff.removed_segments])
"""
Represents number of characters removed in this edit.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(655097130, [diff.chars_removed]))
        [297]
"""

proportion_of_chars_removed = chars_removed / \
              modifiers.max(parent_revision.chars, 1)
"""
Represents ratio of characters removed in this edit compared to overall
characters in parent revision.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(
            extractor.extract(609079959, [diff.proportion_of_chars_removed]))
        [1.0]
"""
proportion_of_chars_added = chars_added / \
            modifiers.max(revision.chars, 1)
"""
Represents ratio of characters removed in this edit compared to overall
characters in revision.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(
            extractor.extract(655097130, [diff.proportion_of_chars_added]))
        [0.012366755496335776]
"""

def process_markup_chars_added(diff_added_segments):
    concat = "".join(diff_added_segments)
    return sum(len(m.group(0)) for m in MARKUP_RE.finditer(concat))

markup_chars_added = \
        Feature("diff.markup_chars_added", process_markup_chars_added,
                returns=int, depends_on=[diff.added_segments])
"""
Represents number of markup characters added in this edit.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(660405663, [diff.markup_chars_added]))
        [76]
"""
def process_markup_chars_removed(diff_removed_segments):
    concat = "".join(diff_removed_segments)
    return sum(len(m.group(0)) for m in MARKUP_RE.finditer(concat))

markup_chars_removed = \
        Feature("diff.markup_chars_removed", process_markup_chars_removed,
                returns=int, depends_on=[diff.removed_segments])
"""
Represents number of markup characters removed in this edit.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(656508079, [diff.markup_chars_removed]))
        [8]
"""
proportion_of_markup_chars_added = \
        markup_chars_added / modifiers.max(chars_added, 1)
"""
Represents ratio of markup characters added in this edit compared to overall
characters added in revision.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(
            extractor.extract(655097130, [diff.proportion_of_markup_chars_added]))
        [0.013468013468013467]
"""
added_markup_chars_ratio = \
        proportion_of_markup_chars_added / \
        modifiers.max(parent_revision.proportion_of_markup_chars, 0.001)
"""
Represents ratio of added markup characters in this edit compared to added
markup characters in the last edit.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(655097130, [diff.added_markup_chars_ratio]))
        [0.45635401635401635]
"""
def process_numeric_chars_added(diff_added_segments):
    concat = "".join(diff_added_segments)
    return sum(len(m.group(0)) for m in NUMERIC_RE.finditer(concat))

numeric_chars_added = \
        Feature("diff.numeric_chars_added", process_numeric_chars_added,
                returns=int, depends_on=[diff.added_segments])
"""
Represents number of numeric characters added in this edit.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(660405663, [diff.numeric_chars_added]))
        [52]
"""

def process_numeric_chars_removed(diff_removed_segments):
    concat = "".join(diff_removed_segments)
    return sum(len(m.group(0)) for m in NUMERIC_RE.finditer(concat))

numeric_chars_removed = \
        Feature("diff.numeric_chars_removed", process_numeric_chars_removed,
                returns=int, depends_on=[diff.removed_segments])
"""
Represents number of numeric characters removed in this edit.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(656508079, [diff.numeric_chars_removed]))
        [6]
"""

proportion_of_numeric_chars_added = \
    numeric_chars_added / modifiers.max(chars_added, 1)
"""
Represents ratio of numeric characters added compared to all characters added
in this edit.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(660405663, [diff.proportion_of_numeric_chars_added]))
        [0.0363382250174703]
"""

added_number_chars_ratio = \
        proportion_of_numeric_chars_added / \
        modifiers.max(parent_revision.proportion_of_numeric_chars, 0.001)
"""
Represents ratio of added numeric characters in this edit compared to added
numeric characters in the last edit.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(660405663, [diff.added_number_chars_ratio]))
        [0.8469149674896002]
"""
def process_symbolic_chars_added(diff_added_segments):
    concat = "".join(diff_added_segments)
    return sum(len(m.group(0)) for m in SYMBOLIC_RE.finditer(concat))

symbolic_chars_added = \
        Feature("diff.symbolic_chars_added", process_symbolic_chars_added,
                returns=int, depends_on=[diff.added_segments])
"""
Represents number of symbolic characters added in this edit.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(655097130, [diff.symbolic_chars_added]))
        [20]
"""
def process_symbolic_chars_removed(diff_removed_segments):
    concat = "".join(diff_removed_segments)
    return sum(len(m.group(0)) for m in SYMBOLIC_RE.finditer(concat))

symbolic_chars_removed = \
        Feature("diff.symbolic_chars_removed", process_symbolic_chars_removed,
                returns=int, depends_on=[diff.removed_segments])
"""
Represents ratio of symbolic characters removed compared to all characters added
in this edit.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(660405663, [diff.proportion_of_symbolic_chars_added]))
        [0.13277428371767994]
"""
proportion_of_symbolic_chars_added = symbolic_chars_added / modifiers.max(chars_added, 1)
"""
Represents ratio of symbolic characters added compared to overall characters
added in this edit.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(
            655097130, [diff.proportion_of_symbolic_chars_added]))
        [0.06734006734006734]
"""
added_symbolic_chars_ratio = \
        proportion_of_symbolic_chars_added / \
        modifiers.max(parent_revision.proportion_of_symbolic_chars, 0.001)
"""
Represents ratio of added symbolic characters in this edit compared to added
symbolic characters in the last edit.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(655097130, [diff.added_symbolic_chars_ratio]))
        [0.6290819445604794]
"""
def process_uppercase_chars_added(diff_added_segments):
    return sum((not c.lower() == c) for segment in diff_added_segments
                                    for c in segment)

uppercase_chars_added = \
        Feature("diff.uppercase_chars_added", process_uppercase_chars_added,
                returns=int, depends_on=[diff.added_segments])
"""
Represents number of uppercase characters added in this edit.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(655097130, [diff.uppercase_chars_added]))
        [9]
"""
def process_uppercase_chars_removed(diff_removed_segments):
    return sum((not c.lower() == c) for segment in diff_removed_segments
                                    for c in segment)

uppercase_chars_removed = \
        Feature("diff.uppercase_chars_removed", process_uppercase_chars_removed,
                returns=int, depends_on=[diff.removed_segments])
"""
Represents number of uppercase characters removed in this edit.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(659049823, [diff.uppercase_chars_removed]))
        [3]
"""
proportion_of_uppercase_chars_added = \
    uppercase_chars_added / modifiers.max(chars_added, 1)
"""
Represents ratio of uppercase characters added compared to overall characters
added in this edit.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(
            655097130, [diff.proportion_of_uppercase_chars_added]))
        [0.030303030303030304]
"""

added_uppercase_chars_ratio = \
        proportion_of_uppercase_chars_added / \
        modifiers.max(parent_revision.proportion_of_uppercase_chars, 0.001)
"""
Represents ratio of uppercase characters added compared to overall uppercase
characters in parent revision.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(
            extractor.extract(655097130, [diff.added_uppercase_chars_ratio]))
        [0.030303030303030304]
"""

def process_longest_repeated_char_added(diff_added_segments):
    try:
        return max(sum(1 for _ in group)
                   for segment in diff_added_segments
                   for _, group in groupby(segment.lower()))
    except ValueError:
        # Happens when there's no segments added
        return 1

longest_repeated_char_added = \
        Feature("diff.longest_repeated_char_added",
                process_longest_repeated_char_added,
                returns=int, depends_on=[diff.added_segments])
"""
Represents number of the most repeated character added.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(
            extractor.extract(655097130, [diff.longest_repeated_char_added]))
        [4]
"""
############################### Words ##########################################

def process_words_added(diff_added_words):
    return len(diff_added_words)

words_added = Feature("diff.words_added", process_words_added,
                      returns=int, depends_on=[diff.added_words])
"""
Represents number of added words in this edit.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(655097130, [diff.words_added]))
        [50]
"""
def process_words_removed(diff_removed_words):
    return len(diff_removed_words)

words_removed = Feature("diff.words_removed", process_words_removed,
                        returns=int, depends_on=[diff.removed_words])
"""
Represents number of words removed in this edit.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(659049823, [diff.words_removed]))
        [3]
"""
def process_badwords_added(is_badword, diff_added_words):
    return sum(is_badword(word) for word in diff_added_words)

badwords_added = Feature("diff.badwords_added", process_badwords_added,
                         returns=int, depends_on=[is_badword, diff.added_words])
"""
Represents number of 'badwords' added in this edit.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(655097130, [diff.badwords_added]))
        [2]
"""
proportion_of_badwords_added = badwords_added / modifiers.max(words_added, 1)
"""
Represents the ratio of 'badwords' added in this edit compared to the overall
words added in that edit.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(655097130, [diff.proportion_of_badwords_added]))
        [0.04]
"""
added_badwords_ratio = proportion_of_badwords_added / \
                       modifiers.max(parent_revision.proportion_of_badwords, 0.001)
"""
Represents the ratio of 'badwords' added in this edit compared to the overall
ratio of 'badwords' in the article before the edit was made.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(655097130, [diff.added_badwords_ratio]))
        [1.0923529411764705]
"""


def process_badwords_removed(is_badword, diff_removed_words):
   return sum(is_badword(word) for word in diff_removed_words)

badwords_removed = Feature("diff.badwords_removed", process_badwords_removed,
                           returns=int,
                           depends_on=[is_badword, diff.removed_words])
"""
Represents number of words 'badwords' removed in this edit.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(602101288, [diff.badwords_removed]))
        [4]
"""
proportion_of_badwords_removed = badwords_removed / modifiers.max(words_removed, 1)
"""
Represents ratio of 'badwords' words removed compared to overall words removed
in this edit.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(
            602101288, [diff.proportion_of_badwords_removed]))
        [0.04878048780487805]
"""
removed_badwords_ratio = proportion_of_badwords_removed / \
                         modifiers.max(parent_revision.proportion_of_badwords, 0.001)
"""
Represents ratio of removed 'badwords' in this edit compared to removed 'badwords'
in the last edit.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(602101288, [diff.removed_badwords_ratio]))
        [1.2790174710257742]
"""
def process_misspellings_added(is_misspelled, diff_added_words):
    return sum(is_misspelled(word) for word in diff_added_words)

misspellings_added = \
    Feature("diff.misspellings_added", process_misspellings_added,
            returns=int, depends_on=[is_misspelled, diff.added_words])
"""
Represents number of misspelled words added in this edit.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(655097130, [diff.misspellings_added]))
        [9]
"""
proportion_of_misspellings_added = \
        misspellings_added / modifiers.max(words_added, 1)
"""
Represents ratio of misspelled words added compared to overall words added
in this edit.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(
            655097130, [diff.proportion_of_misspellings_added]))
        [0.18]
"""
added_misspellings_ratio = \
        proportion_of_misspellings_added / \
        modifiers.max(parent_revision.proportion_of_misspellings, 0.001)
"""
Represents ratio of added misspelled words in this edit compared to
added misspelled words added in the last edit.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(655097130, [diff.added_misspellings_ratio]))
        [4.915588235294117]
"""
def process_misspellings_removed(is_misspelled, diff_removed_words):
    return sum(is_misspelled(word) for word in diff_removed_words)

misspellings_removed = \
        Feature("diff.misspellings_removed", process_misspellings_removed,
                returns=int, depends_on=[is_misspelled, diff.removed_words])
"""
Represents number of misspelled words removed in this edit.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(660405537, [diff.misspellings_removed]))
        [62]
"""
proportion_of_misspellings_removed = \
        misspellings_removed / modifiers.max(words_removed, 1)
"""
Represents ratio of misspelled words removed compared to overall words added
in this edit.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(
            660405537, [diff.proportion_of_misspellings_removed]))
        [0.29245283018867924]
"""
removed_misspellings_ratio = \
        proportion_of_misspellings_removed / \
        modifiers.max(parent_revision.proportion_of_misspellings, 0.001)
"""
Represents ratio of removed misspelled words in this edit compared to
removed misspelled words added in the last edit.

:Returns:
    float

:Example:
    ..code-block:: python

        >>> from revscoring.features import parent_revision
        >>> list(extractor.extract(660405537, [diff.removed_misspellings_ratio]))
        [292.45283018867923]
"""
############################## tokens ##########################################

def process_longest_token_added(diff_added_tokens):
    try:
        return max(len(token) for token in diff_added_tokens)
    except ValueError:
        # Happens when there's no tokens added
        return 1

longest_token_added = \
        Feature("diff.longest_token_added", process_longest_token_added,
                returns=int, depends_on=[diff.added_tokens])
"""
Represents length of the biggest token (e.g. word) added in this edit.

:Returns:
    int

:Example:
    ..code-block:: python

        >>> from revscoring.features import diff
        >>> list(extractor.extract(655097130, [diff.longest_token_added]))
        [12]
"""
