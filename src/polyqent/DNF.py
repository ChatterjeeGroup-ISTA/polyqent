from __future__ import annotations

from typing import List


class DNF:
    """
    A class that represents disjunctive normal form.

    Parameters
    ----------
    literals : List
        List of literals that are in DNF.

    Attributes
    ----------
    literals : List
        List of literals that are in DNF.
    """

    def __init__(self, literals: List):
        self.literals = literals

    def __or__(self, other: DNF) -> DNF:
        """ 
        Or two DNF.

        Or of two DNF is the union of literals of each.

        Parameters
        ----------
        other : DNF
            The other DNF that should be or with this class.

        Returns
        -------
        DNF
            New DNF that is or of two DNF.
        """
        return DNF(self.literals + other.literals)

    def __and__(self, other: DNF) -> DNF:
        """ 
        And two DNF.

        The result is a DNF where each of the literal is the union of two literal in each DNF.

        Parameters
        ----------
        other : DNF
            The other DNF that should be and with this class.

        Returns
        -------
        DNF
            New DNF that is and of two DNF.
        """
        if len(self.literals) == 0:
            return DNF(other.literals)
        if len(other.literals) == 0:
            return DNF(self.literals)

        literal_list = []
        for first_literal in self.literals:
            for second_literal in other.literals:
                literal_list.append(first_literal + second_literal)
        return DNF(literal_list)

    def __neg__(self) -> DNF:
        """ 
        Negate a DNF

        For negating a DNF it is sufficient to negate all its literal and And 
        them together. Negate a literal makes a DNF.

        Returns
        -------
        DNF
            New DNF that is negation of the previous DNF.
        """
        result_DNF = DNF([])
        for literal in self.literals:
            new_arr = []
            for item in literal:
                new_arr.append([-item])
            result_DNF = result_DNF & DNF(new_arr)
        return result_DNF

    def __str__(self) -> str:
        """
        Convert DNF to string.

        Returns
        -------
        str
            String format of the DNF.
        """
        res = ''
        for literal in self.literals:
            res += '\n  AND '.join(["\t" + str(item) for item in literal])
            res += '\n OR \n'
        return '(\n' + res + ')\n'

    def convert_to_preorder(self) -> str:
        """
        Convert DNF to preorder format.

        Returns
        -------
        str
            String in preorder format of the DNF.
        """
        res = '( or '
        for literal in self.literals:
            res += '( and '
            for item in literal:
                res += item.convert_to_preorder()
                res += ' '
            res += ') '
        res += ' )'
        return res
