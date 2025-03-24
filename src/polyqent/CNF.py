from __future__ import annotations

from typing import List


class CNF:
    """
    A class that represents conjunctive normal form.

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

    def __or__(self, other: CNF) -> CNF:
        """ 
        Or two CNF.

        Or of two CNF is the union of literals of each.

        Parameters
        ----------
        other : CNF
            The other CNF that should be or with this class.

        Returns
        -------
        CNF
            New CNF that is or of two CNF.
        """
        if len(self.literals) == 0:
            return CNF(other.literals)
        if len(other.literals) == 0:
            return CNF(self.literals)

        literal_list = []
        for first_literal in self.literals:
            for second_literal in other.literals:
                literal_list.append(first_literal + second_literal)
        return CNF(literal_list)

    def __and__(self, other: CNF) -> CNF:
        """ 
        And two CNF.

        The result is a CNF where each of the literal is the union of two literal in each CNF.

        Parameters
        ----------
        other : CNF
            The other CNF that should be and with this class.

        Returns
        -------
        CNF
            New CNF that is and of two CNF.
        """
        return CNF(self.literals + other.literals)

    def __neg__(self) -> CNF:
        """ 
        Negate a CNF

        For negating a CNF it is sufficient to negate all its literal and And
        them together. Negate a literal makes a CNF.

        Returns
        -------
        CNF
            New CNF that is negation of the previous CNF.
        """
        result_CNF = CNF([])
        for literal in self.literals:
            new_arr = []
            for item in literal:
                new_arr.append([-item])
            result_CNF = result_CNF & CNF(new_arr)
        return result_CNF

    def __str__(self) -> str:
        """
        Convert CNF to string.

        Returns
        -------
        str
            String format of the CNF.
        """
        res = ''
        for literal in self.literals:
            res += '\n  OR '.join(["\t" + str(item) for item in literal])
            res += '\n AND \n'
        return '(\n' + res + ')\n'

    def convert_to_preorder(self) -> str:
        """
        Convert CNF to preorder format.

        Returns
        -------
        str
            String in preorder format of the CNF.
        """
        res = '( and '
        for literal in self.literals:
            res += '( or '
            for item in literal:
                res += item.convert_to_preorder()
                res += ' '
            res += ') '
        res += ' )'
        return res
