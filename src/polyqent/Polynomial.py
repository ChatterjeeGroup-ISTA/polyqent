from __future__ import annotations

from typing import List

import numpy as np

from .Coefficient import Coefficient
from .UnknownVariable import UnknownVariable


class Monomial:
    """
    A class that represent a Monomial.

    It consists a set of variables with corresponding degree in an array and a Coefficient.

    Example
    -------
    For example `(2*a*b + 1/2*c*c*c + 3.5)*x^2*y^3` is a Monomial.

    Parameters
    ----------
    variables : List[UnknownVariable]
        The sorted list of variables of the Monomial.
    degrees : List[int]
        Degree of each variable.
    coefficient : Coefficient
        The Coefficient of the Monomial

    Attributes
    ----------
    variables : List[UnknownVariable]
        The sorted list of variables of the Monomial.
    degrees : List[int]
        Degree of each variable.
    coefficient : Coefficient
        The Coefficient of the Monomial
    """

    def __init__(self, variables: List[UnknownVariable], degrees: List[int], coefficient: Coefficient):
        variables.sort()
        self.variables = variables
        self.degrees = degrees
        self.coefficient = coefficient

    def __str__(self) -> str:
        """
        Convert Monomial to string.

        Returns
        -------
        str
            String format of the class.
        """
        return '*'.join(['(' + str(self.coefficient) + ')'] +
                        [str(self.variables[i]) + '^' + str(self.degrees[i]) for i in range(len(self.degrees))])

    def __mul__(self, other: Monomial) -> Monomial:
        """
        Multiply two Monomials

        The result is a Monomial which the degree of each variable is sum of
        degrees in multiplicands and the coefficient is the multiply of the two
        coefficient in multiplicands.

        Parameters
        ----------
        other : Monomial
            The other Monomial that should be multiplied

        Returns
        -------
        Monomial
            New Monomial that is the result of multiplication of two Coefficient
        """
        return Monomial(self.variables, np.array(self.degrees) + np.array(other.degrees),
                        self.coefficient * other.coefficient)

    def __eq__(self, other: Monomial) -> bool:
        """
        Compare two Monomials (equality)

        The comparison is based on their length of set of variable and if that
        is equal and all variables and degree are equal they are equal.

        Parameters
        ----------
        other : Monomial
            The other Monomial that should be compared to.

        Returns
        -------
        bool
            Boolean that determine are they equal or not.
        """
        if len(self.variables) != len(other.variables):
            return False
        for i in range(len(self.variables)):
            if self.variables[i] != other.variables[i] or self.degrees[i] != other.degrees[i]:
                return False
        return True

    def __lt__(self, other: Monomial) -> bool:
        """
        Compare two Monomials (less than)

        The comparison is based on their length of set of variable and if that is equal
        based on degree in lexicographical order.

        Parameters
        ----------
        other : Monomial
            The other Monomial that should be compared to.

        Returns
        -------
        bool
            Boolean that determine which one is less than the other.
        """
        if len(self.variables) != len(other.variables):
            return len(self.variables) < len(other.variables)
        for i in range(len(self.variables)):
            if self.degrees[i] != other.degrees[i]:
                return self.degrees[i] < other.degrees[i]
        return True

    def __neg__(self) -> Monomial:
        """
        Negate a Monomial

        For negating a Monomial it is sufficient to just negate the Coefficient.

        Returns
        -------
        Monomial
            A Monomial that is the negated form of the Monomial.
        """
        return Monomial(self.variables, self.degrees, -self.coefficient)

    def is_mono(self) -> bool:
        """
        Determine if the Monomial is a monomial.

        Returns
        -------
        bool
            True if the Monomial is a monomial.
        """
        number_of_nonzero = 0
        for deg in self.degrees:
            if deg != 0 and deg != 1:
                return False
            number_of_nonzero += deg
        return (number_of_nonzero <= 1)

    def get_deg(self) -> int:
        """
        Determine the degree of Monomial.

        Returns
        -------
        bool
            The degree of Monomial
        """
        return np.sum(self.degrees)

    def convert_to_preorder(self) -> str:
        """
        Convert Monomial to preorder format.

        Returns
        -------
        str
            String in preorder format of the class.
        """
        preorder = '( * 1 '
        preorder += self.coefficient.convert_to_preorder()

        for i, var in enumerate(self.variables):
            for _ in range(self.degrees[i]):
                preorder += str(var)
        preorder += ' )'
        return preorder


class Polynomial:
    """
    A class that represent the Polynomial.

    It consists a set of Monomials which should be added together to form the
    Polynomial.

    Example
    -------
    For example `(2*a*b + 1/2*c*c*c + 3.5)*x^2*y^3 + (3 + 2*a*b)*x^0*y^1` is a
    Polynomial.

    Parameters
    ----------
    variables : List[UnknownVariable]
        The sorted list of variables of the Polynomial.
    monomials : List[Monomial]
        The sorted list of Monomials that should be added together.

    Attributes
    ----------
    variables : List[UnknownVariable]
        The sorted list of variables of the Polynomial.
    monomials : List[Monomial]
        The sorted list of Monomials that should be added together.
    dict_from_degrees_to_monomials : dictionary
        A dictionary that maps each degree to corresponding Monomial
    """

    def __init__(self, variables: List[UnknownVariable], monomials: List[Monomial]):
        variables.sort()
        monomials.sort()
        self.variables = variables
        self.monomials = monomials
        self.dict_from_degrees_to_monomials = {}
        for monomial in self.monomials:
            self.dict_from_degrees_to_monomials[tuple(
                monomial.degrees)] = monomial

    def get_monomial_by_degree(self, degree: List[int]) -> Monomial:
        """
        Get a Monomial by its degree.

        Parameters
        ----------
        degree : List[int]
            The degree of the Monomial.

        Returns
        -------
        Monomial
            The Monomial that has the same degree.
        """
        if degree in self.dict_from_degrees_to_monomials.keys():
            return self.dict_from_degrees_to_monomials[degree]
        return Monomial(self.variables, [0] * len(self.variables), Coefficient([]))

    def __str__(self) -> str:
        """
        Convert Polynomial to string.

        Returns
        -------
        str
            String format of the class.
        """
        if len(self.monomials) == 0:
            return '0'
        return '+'.join([str(monomial) for monomial in self.monomials])

    def __add__(self, other: Polynomial) -> Polynomial:
        """
        Sum of two Polynomials

        Sum of two Polynomial is a union of their Monomials.

        Parameters
        ----------
        other : Polynomial
            The other Polynomial that should be added.

        Returns
        -------
        Polynomial
            New Polynomial that is sum of two Coefficient
        """
        return Polynomial(self.variables, self.monomials + other.monomials).revise()

    def __neg__(self) -> Polynomial:
        """
        Negate a Polynomial

        For negating a Polynomial it is sufficient to negate all its Monomial.

        Returns
        -------
        Polynomial
            A Polynomial that is the negated form of the Polynomial.
        """
        monomials = [-monomial for monomial in self.monomials]
        return Polynomial(self.variables, monomials)

    def __sub__(self, other: Polynomial) -> Polynomial:
        """
        Subtract two Polynomial

        Subtract of two Polynomial is adding one with the negated of the other.

        Parameters
        ----------
        other : Polynomial
            The other Polynomial that should be subtracted.

        Returns
        -------
        Polynomial
            New Polynomial that is subtracted of two Polynomial
        """
        return self + (-other)

    def __mul__(self, other: Polynomial) -> Polynomial:
        """
        Multiply two Polynomial

        The result is a Polynomial which consist of Monomials that are equal to
        the multiply of two Monomial from each Polynomial. Numpy is used for
        that.

        Parameters
        ----------
        other : Polynomial
            The other Polynomial that should be multiplied

        Returns
        -------
        Polynomial
            New Polynomial that is multiplied of two Polynomial
        """
        return Polynomial(self.variables,
                          np.array(
                              np.matmul(
                                  np.array(self.monomials).reshape(1, -1).T,
                                  np.array(other.monomials).reshape(1, -1)
                              )
                          ).reshape(1, -1)[0]
                          ).revise()

    def revise(self) -> Polynomial:
        """
        Revise the Polynomial

        It means that the Monomials that are the same added together.

        Example
        -------
        For example `(3*a)*x^1 + (2*a*b + 1*a)*x^1`  is a Polynomial and after
        revise it returns `(3*a + 2*a*b + 1*a)*x^1`.

        Returns
        -------
        Polynomial
            The revised format of the Polynomial.
        """
        self.monomials.sort()
        new_list = []
        i = 0
        while i < len(self.monomials):
            coefficient = Coefficient([])
            j = i
            while j < len(self.monomials):
                if self.monomials[i] == self.monomials[j]:
                    coefficient += self.monomials[j].coefficient
                else:
                    break
                j += 1
            new_list.append(
                Monomial(self.monomials[i].variables, self.monomials[i].degrees, coefficient))
            i = j

        return Polynomial(self.variables, new_list)

    def add_variables(self, new_variables: List[UnknownVariable]) -> Polynomial:
        """
        This function adds a set of new variable to each Monomial of a
        Polynomial.

        Parameters
        ----------
        new_variables : List[UnknownVariable]
            The list of the new variables that should add to the Polynomial.

        Returns
        -------
        Polynomial
            New Polynomial with the new list of the variables.
        """
        monomials = []
        for monomial in self.monomials:
            monomials.append(Monomial(monomial.variables + new_variables,
                                      monomial.degrees +
                                      [0] * len(new_variables),
                                      monomial.coefficient)
                             )
        return Polynomial(self.variables + new_variables, monomials)

    def is_linear(self) -> bool:
        """
        Determine if the Polynomial is linear.

        Returns
        -------
        bool
            True if the Polynomial is linear.
        """
        for mono in self.monomials:
            if not mono.is_mono():
                return False
        return True

    def get_deg(self) -> int:
        """
        Determine degree of Polynomial.

        Returns
        -------
        int
            degree of Polynomial.
        """
        deg = 0
        for mono in self.monomials:
            deg = max(deg, mono.get_deg())
        return deg
    def convert_to_preorder(self) -> str:
        """
        Convert Polynomial to preorder format.

        Returns
        -------
        str
            String in preorder format of the class.
        """
        if len(self.monomials) == 0:
            return '0'
        if len(self.monomials) == 1:
            return self.monomials[0].convert_to_preorder()
        preorder = '( + 0 '
        for i in range(0, len(self.monomials)):
            preorder += self.monomials[i].convert_to_preorder() + ' '
        preorder += ' )'
        return preorder
