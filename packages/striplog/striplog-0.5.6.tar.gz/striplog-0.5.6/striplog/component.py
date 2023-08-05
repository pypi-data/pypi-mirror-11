#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Defines components for holding properties of rocks or samples or whatevers.

:copyright: 2015 Agile Geoscience
:license: Apache 2.0
"""
import re


class ComponentError(Exception):
    """
    Generic error class.
    """
    pass


class Component(object):
    """
    Initialize with a dictionary of properties. You can use any
    properties you want e.g.:

        - lithology: a simple one-word rock type
        - colour, e.g. 'grey'
        - grainsize or range, e.g. 'vf-f'
        - modifier, e.g. 'rippled'
        - quantity, e.g. '35%', or 'stringers'
        - description, e.g. from cuttings

    You can include as many other things as you want, e.g.

        - porosity
        - cementation
        - lithology code
    """

    def __init__(self, properties):
        for k, v in properties.items():
            if k and v:
                setattr(self, k.lower(), v.lower())

    def __repr__(self):
        s = str(self)
        return "Component({0})".format(s)

    def __str__(self):
        s = []
        for key in self.__dict__:
            t = '"{key}":"{value}"'
            s.append(t.format(key=key, value=self.__dict__[key]))
        return ', '.join(s)

    def __getitem__(self, key):
        """
        So we can get at attributes with variables.
        """
        return self.__dict__.get(key)

    def __bool__(self):
        if not self.__dict__.keys():
            return False
        else:
            return True

    # For Python 2
    __nonzero__ = __bool__

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        # Weed out empty elements
        s = {k: v for k, v in self.__dict__.items() if v}
        o = {k: v for k, v in other.__dict__.items() if v}

        # Compare
        if s == o:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    # If we define __eq__ we also need __hash__ otherwise the object
    # becomes unhashable. All this does is hash the frozenset of the
    # keys. (You can only hash immutables.)
    def __hash__(self):
        return hash(frozenset(self.__dict__.keys()))

    def _repr_html_(self):
        """
        IPython Notebook magic repr function.
        """
        rows = ''
        s = '<tr><td><strong>{k}</strong></td><td>{v}</td></tr>'
        for k, v in self.__dict__.items():
            rows += s.format(k=k, v=v)
        html = '<table>{}</table>'.format(rows)
        return html

    @classmethod
    def from_text(cls, text, lexicon, required=None, first_only=True):
        """
        Generate a Component from a text string, using a Lexicon.

        Args:
            text (str): The text string to parse.
            lexicon (Lexicon): The dictionary to use for the
                categories and lexemes.
            first_only (bool): Whether to only take the first
                match of a lexeme against the text string.

        Returns:
            Component: A Component object, or None if there was no
                must-have field.
        """
        component = lexicon.get_component(text, first_only=first_only)
        if required and (required not in component):
            return None
        else:
            return cls(component)

    def summary(self, fmt=None, initial=True, default=''):
        """
        Given a format string, return a summary description of a component.

        Args:
            component (dict): A component dictionary.
            fmt (str): Describes the format with a string. Use '%'
                to signal a field in the component, which is analogous
                to a dictionary. If no format is given, you will
                just get a list of attributes.
            initial (bool): Whether to capitialize the first letter.
            default (str): What to give if there's no component defined.

        Returns:
            str: A summary string.

        Example:

            r = Component({'colour': 'Red',
                           'grainsize': 'VF-F',
                           'lithology': 'Sandstone'})

            r.summary()  -->  'Red, vf-f, sandstone'
        """
        if default and not self.__dict__:
            return default

        if not fmt:
            string, flist = '', []
            for item in self.__dict__:
                string += '{}, '
                flist.append(item)
            string = string.strip(', ')
        else:
            fmt = re.sub(r'  ', '_dblspc_', fmt)
            string = re.sub(r'\{(\w+)\}', '{}', fmt)
            flist = re.findall(r'\{(\w+)\}', fmt)

        words = []
        for key in flist:
            word = self.__dict__.get(key.lower())
            if word and key[0].isupper():
                word = word.capitalize()
            if word and key.isupper():
                word = word.upper()
            if not word:
                word = ''
            words.append(word)

        try:
            summary = string.format(*words)
        except KeyError as e:
            raise ComponentError("No such attribute, "+str(e))

        if initial and summary:
            summary = summary[0].upper() + summary[1:]

        # Tidy up double spaces
        summary = re.sub(r'  ', ' ', summary)
        summary = re.sub(r'_dblspc_', '  ', summary)

        return summary
