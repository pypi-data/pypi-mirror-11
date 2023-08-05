# -*- coding: utf-8 -*-
#
# This file is part of Invenio.
# Copyright (C) 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014,
# 2015 CERN.
#
# Invenio is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Invenio is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Invenio; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA 02111-1307, USA.

"""Define utilities for special formatting of records."""

import re

from invenio.utils.url import string_to_numeric_char_reference
from invenio.utils.shell import run_shell_command


def highlight_matches(text, compiled_pattern,
                      prefix_tag='<strong>', suffix_tag="</strong>"):
    """Highlight words in 'text' matching the 'compiled_pattern'.

    :param text: the text in which we want to "highlight" parts
    :param compiled_pattern: the parts to highlight
    :type compiled_pattern: a compiled regular expression
    :param prefix_tag: prefix to use before each matching parts
    :param suffix_tag: suffix to use after each matching parts
    :return: a version of input X{text} with words matching X{compiled_pattern}
             surrounded by X{prefix_tag} and X{suffix_tag}
    """
    # Add 'prefix_tag' and 'suffix_tag' before and after 'match'
    # FIXME decide if non english accentuated char should be desaccentuaded
    def replace_highlight(match):
        """Replace match.group() by prefix_tag + match.group() + suffix_tag."""
        return prefix_tag + match.group() + suffix_tag

    # Replace and return keywords with prefix+keyword+suffix
    return compiled_pattern.sub(replace_highlight, text)


def highlight(text, keywords=None, prefix_tag='<strong>',
              suffix_tag="</strong>", whole_word_matches=False):
    """Return text with all words highlighted with given tags.

    This function places 'prefix_tag' and 'suffix_tag' before and after words
    from 'keywords' in 'text'.

    For example set prefix_tag='<b style="color: black; background-color:
    rgb(255, 255, 102);">' and suffix_tag="</b>"

    :param text: the text to modify
    :param keywords: a list of string
    :param prefix_tag: prefix to use before each matching parts
    :param suffix_tag: suffix to use after each matching parts
    :param whole_word_matches: to use whole word matches
    :return: highlighted text
    """
    if not keywords:
        return text

    escaped_keywords = []
    for k in keywords:
        escaped_keywords.append(re.escape(k))
    # Build a pattern of the kind keyword1 | keyword2 | keyword3
    if whole_word_matches:
        pattern = '|'.join(['\\b' + key + '\\b' for key in escaped_keywords])
    else:
        pattern = '|'.join(escaped_keywords)
    compiled_pattern = re.compile(pattern, re.IGNORECASE)

    # Replace and return keywords with prefix+keyword+suffix
    return highlight_matches(text, compiled_pattern,
                             prefix_tag, suffix_tag)


def get_contextual_content(text, keywords, max_lines=2):
    """
    Returns some lines from a text contextually to the keywords in
    'keywords_string'

    :param text: the text from which we want to get contextual content
    :param keywords: a list of keyword strings ("the context")
    :param max_lines: the maximum number of line to return from the record
    :return: a string
    """

    def grade_line(text_line, keywords):
        """
        Grades a line according to keywords.

        grade = number of keywords in the line
        """
        grade = 0
        for keyword in keywords:
            grade += text_line.upper().count(keyword.upper())

        return grade

    # Grade each line according to the keywords
    lines = text.split('.')
    # print 'lines: ',lines
    weights = [grade_line(line, keywords) for line in lines]

    # print 'line weights: ', weights
    def grade_region(lines_weight):
        """
        Grades a region. A region is a set of consecutive lines.

        grade = sum of weights of the line composing the region
        """
        grade = 0
        for weight in lines_weight:
            grade += weight
        return grade

    if max_lines > 1:
        region_weights = []
        for index_weight in range(len(weights) - max_lines + 1):
            region_weights.append(
                grade_region(
                    weights[index_weight:(index_weight + max_lines)]))

        weights = region_weights
    # print 'region weights: ',weights
    # Returns line with maximal weight, and (max_lines - 1) following lines.
    index_with_highest_weight = 0
    highest_weight = 0
    i = 0
    for weight in weights:
        if weight > highest_weight:
            index_with_highest_weight = i
            highest_weight = weight
        i += 1
    # print 'highest weight', highest_weight

    if index_with_highest_weight + max_lines > len(lines):
        return lines[index_with_highest_weight:]
    else:
        return lines[
            index_with_highest_weight:index_with_highest_weight +
            max_lines]


def parse_tag(tag):
    """Parse a marc code and decompose it in a table.

    0-tag 1-indicator1 2-indicator2 3-subfield

    The first 3 chars always correspond to tag.  The indicators are optional.
    However they must both be indicated, or both ommitted.  If indicators are
    ommitted or indicated with underscore '_', they mean "No indicator".  "No
    indicator" is also equivalent indicator marked as whitespace.  The subfield
    is optional. It can optionally be preceded by a dot '.' or '$$' or '$'

    Any of the chars can be replaced by wildcard %

    THE FUNCTION DOES NOT CHECK WELLFORMNESS OF 'tag'

    Any empty chars is not considered

    For example:
    >> parse_tag('245COc') = ['245', 'C', 'O', 'c']
    >> parse_tag('245C_c') = ['245', 'C', '', 'c']
    >> parse_tag('245__c') = ['245', '', '', 'c']
    >> parse_tag('245__$$c') = ['245', '', '', 'c']
    >> parse_tag('245__$c') = ['245', '', '', 'c']
    >> parse_tag('245  $c') = ['245', '', '', 'c']
    >> parse_tag('245  $$c') = ['245', '', '', 'c']
    >> parse_tag('245__.c') = ['245', '', '', 'c']
    >> parse_tag('245  .c') = ['245', '', '', 'c']
    >> parse_tag('245C_$c') = ['245', 'C', '', 'c']
    >> parse_tag('245CO$$c') = ['245', 'C', 'O', 'c']
    >> parse_tag('245C_.c') = ['245', 'C', '', 'c']
    >> parse_tag('245$c') = ['245', '', '', 'c']
    >> parse_tag('245.c') = ['245', '', '', 'c']
    >> parse_tag('245$$c') = ['245', '', '', 'c']
    >> parse_tag('245__%') = ['245', '', '', '']
    >> parse_tag('245__$$%') = ['245', '', '', '']
    >> parse_tag('245__$%') = ['245', '', '', '']
    >> parse_tag('245  $%') = ['245', '', '', '']
    >> parse_tag('245  $$%') = ['245', '', '', '']
    >> parse_tag('245$%') = ['245', '', '', '']
    >> parse_tag('245.%') = ['245', '', '', '']
    >> parse_tag('245$$%') = ['245', '', '', '']
    >> parse_tag('2%5$$a') = ['2%5', '', '', 'a']

    :param tag: tag to parse
    :return: a canonical form of the input X{tag}
    """

    p_tag = ['', '', '', '']  # tag, ind1, ind2, code
    tag = tag.replace(" ", "")  # Remove empty characters
    tag = tag.replace("$", "")  # Remove $ characters
    tag = tag.replace(".", "")  # Remove . characters
    # tag = tag.replace("_", "") # Remove _ characters

    p_tag[0] = tag[0:3]  # tag
    if len(tag) == 4:
        p_tag[3] = tag[3]  # subfield

    elif len(tag) == 5:
        ind1 = tag[3]  # indicator 1
        if ind1 != "_":
            p_tag[1] = ind1

        ind2 = tag[4]  # indicator 2
        if ind2 != "_":
            p_tag[2] = ind2

    elif len(tag) == 6:
        p_tag[3] = tag[5]  # subfield

        ind1 = tag[3]  # indicator 1
        if ind1 != "_":
            p_tag[1] = ind1

        ind2 = tag[4]  # indicator 2
        if ind2 != "_":
            p_tag[2] = ind2

    return p_tag


re_bold_latex = re.compile(r'\$?\\\\textbf\{(?P<content>.*?)\}\$?')
re_emph_latex = re.compile(r'\$?\\\\emph\{(?P<content>.*?)\}\$?')
re_generic_start_latex = re.compile(r'\$?\\\\begin\{(?P<content>.*?)\}\$?')
re_generic_end_latex = re.compile(r'\$?\\\\end\{(?P<content>.*?)\}\$?')
re_verbatim_env_latex = re.compile(
    r'\\\\begin\{verbatim.*?\}(?P<content>.*?)\\\\end\{verbatim.*?\}')


def latex_to_html(text):
    """
    Do some basic interpretation of LaTeX input. Gives some nice
    results when used in combination with MathJax.

    :param text: input "LaTeX" markup to interpret
    :return: a representation of input LaTeX more suitable for HTML
    """
    # Process verbatim environment first
    def make_verbatim(match_obj):
        """Replace all possible special chars by HTML character
        entities, so that they are not interpreted by further commands"""
        return '<br/><pre class="tex2math_ignore">' + \
               string_to_numeric_char_reference(match_obj.group('content')) + \
               '</pre><br/>'

    text = re_verbatim_env_latex.sub(make_verbatim, text)

    # Remove trailing "line breaks"
    text = text.strip('\\\\')

    # Process special characters
    text = text.replace("\\%", "%")
    text = text.replace("\\#", "#")
    text = text.replace("\\$", "$")
    text = text.replace("\\&", "&amp;")
    text = text.replace("\\{", "{")
    text = text.replace("\\}", "}")
    text = text.replace("\\_", "_")
    text = text.replace("\\^{} ", "^")
    text = text.replace("\\~{} ", "~")
    text = text.replace("\\textregistered", "&#0174;")
    text = text.replace("\\copyright", "&#0169;")
    text = text.replace("\\texttrademark", "&#0153; ")

    # Remove commented lines and join lines
    text = '\\\\'.join([line for line in text.split('\\\\')
                        if not line.lstrip().startswith('%')])

    # Line breaks
    text = text.replace('\\\\', '<br/>')

    # Non-breakable spaces
    text = text.replace('~', '&nbsp;')

    # Styled text
    def make_bold(match_obj):
        "Make the found pattern bold"
        # FIXME: check if it is valid to have this inside a formula
        return '<b>' + match_obj.group('content') + '</b>'
    text = re_bold_latex.sub(make_bold, text)

    def make_emph(match_obj):
        "Make the found pattern emphasized"
        # FIXME: for the moment, remove as it could cause problem in
        # the case it is used in a formula. To be check if it is valid.
        return ' ' + match_obj.group('content') + ''
    text = re_emph_latex.sub(make_emph, text)

    # Lists
    text = text.replace('\\begin{enumerate}', '<ol>')
    text = text.replace('\\end{enumerate}', '</ol>')
    text = text.replace('\\begin{itemize}', '<ul>')
    text = text.replace('\\end{itemize}', '</ul>')
    text = text.replace('\\item', '<li>')

    # Remove remaining non-processed tags
    text = re_generic_start_latex.sub('', text)
    text = re_generic_end_latex.sub('', text)

    return text


def get_text_snippets(textfile_path, patterns, nb_chars, max_snippets):
    """
    Extract text snippets around 'patterns' from the file found at
    'textfile_path'. The snippets are meant to look similar to results of
    popular Internet search engines: using " ... " between snippets.
    For empty patterns it returns ""
    """
    # TODO: - distinguish the beginning of sentences and make the snippets
    #         start there
    #       - optimize finding patterns - first search for patterns apperaing
    #         next to each other, secondly look for each patten not for first
    #         occurances of any pattern

    if len(patterns) == 0:
        return ""

    max_lines = nb_chars / 40 + 2  # rule of thumb in order to catch nb_chars
    # Produce the big snippets from which the real snippets will be cut out
    cmd = "grep -i -C%s -m%s"
    cmdargs = [str(max_lines), str(max_snippets)]
    for p in patterns:
        cmd += " -e %s"
        cmdargs.append(" " + p)
    cmd += " %s"
    cmdargs.append(textfile_path)
    (dummy1, output, dummy2) = run_shell_command(cmd, cmdargs)
    # a fact to keep in mind with this call to grep is that if patterns appear
    # in two contigious lines, they will not be separated by '--' and
    # therefore treated as one 'big snippet'
    result = []
    big_snippets = output.split("--")

    # cut the snippets to match the nb_words_around parameter precisely:
    for s in big_snippets:
        small_snippet = cut_out_snippet(s, patterns, nb_chars)
        result.append(small_snippet)

    # combine snippets
    out = ""
    count = 0
    for snippet in result:
        if snippet and count < max_snippets:
            if out:
                out += "..."
            out += highlight(snippet, patterns, whole_word_matches=True)

    return out


def words_start_with_patterns(words, patterns):
    """
    Check whether the first word's beginning matches any of the patterns.
    The second argument is an array of patterns to match.
    """

    ret = False
    for p in patterns:
        # Phrase handling
        if ' ' in p:
            phrase = p
            phrase_terms = p.split()
            additional_term_count = len(phrase_terms) - 1
            possible_match = ' '.join(words[:additional_term_count + 1])
            if possible_match.lower() == phrase.lower():
                return True, additional_term_count
        else:
            lower_case = words[0].lower()
            if lower_case.startswith(str(p).lower()):
                ret = True
                break
    return ret, 0


def cut_out_snippet(text, patterns, nb_chars):
    """
    Cut out one snippet in such a way that it includes at most nb_chars or
    a few more chars until the end of last word.
    The snippet can include:
    - one pattern and "symmetrical" context
    - several patterns as long as they fit into the nb_chars limit (context
      is always "symmetrical")
    """
    # TODO: cut at begin or end of sentence

    words = text.split()
    snippet, start, finish = cut_out_snippet_core_creation(
        words, patterns, nb_chars)
    return cut_out_snippet_wrap(snippet, words, start, finish, nb_chars)


def cut_out_snippet_core_creation(words, patterns, nb_chars):
    """Stage 1.

    Creating the snipper core starts and finishes with a matched pattern The
    idea is to find a pattern occurance, then go on creating a suffix until the
    next pattern is found. Then the suffix is added to the snippet unless the
    loop brakes before due to suffix being to long.
    """
    snippet = ""
    suffix = ""
    i = 0
    start = -1  # start is an index of the first matched pattern
    finish = -1  # is an index of the last matched pattern
    # in this loop, the snippet core always starts and finishes with a matched
    # pattern
    while i < len(words) and len(snippet) + len(suffix) < nb_chars:
        word_matched_p, additional_term_count = words_start_with_patterns(
            words[i:], patterns
        )
        # if the first pattern was already found
        if len(snippet) == 0:
            # first occurance of pattern
            if word_matched_p:
                start = i
                suffix = ""
                if not additional_term_count:
                    snippet = words[i]
                    finish = i
                else:
                    snippet = ' '.join(words[i:i + additional_term_count + 1])
                    finish = i + additional_term_count
        else:
            if word_matched_p:
                if not additional_term_count:
                    # there is enough room for this pattern in the snippet
                    # because with previous word the snippet was shorter than
                    # nb_chars suffix starts with a space
                    snippet += suffix + " " + words[i]
                    finish = i
                else:
                    # suffix starts with a space
                    snippet += suffix + " " + \
                        ' '.join(words[i:i + additional_term_count + 1])
                    finish = i + additional_term_count
                suffix = ""
            else:
                suffix += " " + words[i]
        i += 1 + additional_term_count
    return snippet, start, finish


def cut_out_snippet_wrap(snippet, words, start, finish, nb_chars):
    """ Stage 2: Wrap the snippet core symetrically up to the nb_chars
        if snippet is non-empty, then start and finish will be set before
    """
    front = True
    while 0 < len(snippet) < nb_chars:
        if front and start == 0:
            front = False
        else:
            if not front and finish == len(words) - 1:
                front = True

        if start == 0 and finish == len(words) - 1:
            break

        if front:
            snippet = words[start - 1] + " " + snippet
            start -= 1
            front = False
        else:
            snippet += " " + words[finish + 1]
            finish += 1
            front = True
    return snippet
