from __future__ import annotations

from fractions import Fraction
from typing import List, Union

import numpy as np

from .UnknownVariable import UnknownVariable


class Element:
    """
    A class that represent an element.

    It consists a rational constant and a set of variables which should be
    multiplied together to form the element.

    Examples
    -------
    - The term `2*a*b` is an element where 2 is the constant and a, b are variables.
        
        >>> Element(2, [UnknownVariable('a'), UnknownVariable('b')])
        
    - The term `1/2*c*c*c` is an element where 1/2 is the constant and c is the variable.
        
        >>> Element(1/2, [UnknownVariable('c'), UnknownVariable('c'), UnknownVariable('c')])


    Parameters
    ----------
    constant : Union[float, str, Fraction]
        It is the constant to multiply with other variables
    variables : List[UnknownVariable], optional
        The sorted list of variables that should be multiplied together, by default []


    Attributes
    ----------
    constant : Fraction
        The constant of the element
    variables : List[UnknownVariable]
        The sorted list of variables that should be multiplied together
    """

    def __init__(self, constant: Union[float, str, Fraction], variables: List[UnknownVariable] = []):
        self.constant = Fraction(constant)
        variables.sort()
        self.variables = variables

    def __str__(self) -> str:
        """
        Convert Element to string.

        Returns
        -------
        str
            String representation of the Element.
        """
        return '*'.join([str(self.constant)] + [str(var) for var in self.variables])

    def __mul__(self, other: Element) -> Element:
        """
        Multiply two elements.

        Parameters
        ----------
        other : Element
            The other factor for multiplication

        Returns
        -------
        Element
            New element that is the product of two elements
        """
        return Element((self.constant * other.constant), (self.variables + other.variables))

    def __add__(self, other: Element) -> Element:
        """
        Add two elements.

        Parameters
        ----------
        other : Element
            The other element that should be added

        Returns
        -------
        Element
            New element that is the sum of two elements
        """
        return Coefficient([self, other])

    def __lt__(self, other: Element) -> bool:
        """
        Compare two elements (less than).

        The comparison is based on their length of set of variable and if that
        is equal based on the set of variable lexicographically and if that is
        equal too based on their constant.

        Parameters
        ----------
        other : Element
            The other element that should be compared to.

        Returns
        -------
        bool
            Boolean that determine which one is less than the other.
        """
        if len(self.variables) == len(other.variables):
            for i in range(len(self.variables)):
                if not (self.variables[i] == other.variables[i]):
                    return self.variables[i] < other.variables[i]
            return self.constant < other.constant
        else:
            return len(self.variables) < len(other.variables)

    def __eq__(self, other: Element) -> bool:
        """
        Compare two elements (equal).

        The comparison is based on their length of set of variable and if that
        is equal and all variables are equal they are equal.      

        Parameters
        ----------
        other : Element
            The other element that should be compared to.

        Returns
        -------
        bool
            Boolean that determine are they equal or not.
        """

        if len(self.variables) == len(other.variables):
            for i in range(len(self.variables)):
                if not (self.variables[i] == other.variables[i]):
                    return False
            return True
        else:
            return False

    def __neg__(self) -> Element:
        """
        Negate an element.

        For negating an element it is sufficient to just negate the constant.

        Returns
        -------
        Element
            A new element that is the negated form of the element.
        """
        return Element(-self.constant, self.variables)

    def convert_to_preorder(self) -> str:
        """
        Convert Element to preorder format string.

        Returns
        -------
        str
            String in preorder format of the class
        """
        if self.constant == 0:
            return '0'
        if self.constant.denominator == 1:
            preorder = str(self.constant.numerator)
            if self.constant < 0:
                preorder = f'(- {-self.constant.numerator})'
        else:
            preorder = f'(/ {self.constant.numerator} {self.constant.denominator})'
            if self.constant < 0:
                preorder = f'(- (/ {-self.constant.numerator} {self.constant.denominator}))'
        if len(self.variables) == 0:
            return preorder
        preorder = '(* 1 ' + preorder + ' '
        for var in self.variables:
            preorder += str(var) + ' '
        preorder += ' )'
        return preorder


class Coefficient:
    """
    A class that represent a coefficient.

    It consists a list of elements that should be added together to form the coefficient.

    Examples
    --------
    For example `2*a*b + 1/2*c*c*c + 3.5` is a coefficient.

    >>> Coefficient(
    ...     [
    ...         Element(2, [UnknownVariable('a'), UnknownVariable('b')]),
    ...         Element(1/2, [UnknownVariable('c'), UnknownVariable('c'), UnknownVariable('c')]),
    ...         Element(3.5)
    ...     ])
    

    Parameters
    ----------
    elements : List[Element], optional
        The list of elements that should be added together, by default []

    Attributes
    ----------
    elements : List[Element]
        The list of elements that should be added together    
    """

    def __init__(self, elements: List[Element] = []):
        elements.sort()
        self.elements = elements

    def __str__(self) -> str:
        """
        Convert Coefficient to string.

        Returns
        -------
        str
            String representation of the Coefficient.
        """
        if len(self.elements) == 0:
            return '0'
        return '+'.join([str(element) for element in self.elements])

    def __mul__(self, other: Coefficient) -> Coefficient:
        """
        Multiply two Coefficient.

        Parameters
        ----------
        other : Coefficient
            The other factor for multiplication

        Returns
        -------
        Coefficient
            New coefficient that is the product of two coefficients
        """
        return Coefficient(
            np.array(
                np.matmul(
                    np.array(self.elements).reshape(1, -1).T,
                    np.array(other.elements).reshape(1, -1)
                )
            ).reshape(1, -1)[0]
        ).revise()

    def __add__(self, other: Union[Coefficient, Element]) -> Coefficient:
        """
        Add two Coefficient.

        Parameters
        ----------
        other : Union[Coefficient, Element]
            The other element that should be added to the Coefficient

        Returns
        -------
        Coefficient
            New coefficient that is the sum of two coefficients
        """
        if type(other) is Coefficient:
            return Coefficient(self.elements + other.elements).revise()
        if type(other) is Element:
            return Coefficient(self.elements + [other]).revise()

    def revise(self) -> Coefficient:
        """ 
        Revise the Coefficient.

        It sorts the elements and combines the elements with the same variables.

        Examples
        --------
        For example `3*a + 2*a*b + 1*a` is a Coefficient and after revise it returns `4*a + 2*a*b`.

        Returns
        -------
        Coefficient
            The revised format of the Coefficient.
        """
        self.elements.sort()
        new_list = []
        i = 0
        while i < len(self.elements):
            constant = Fraction('0')
            j = i
            while j < len(self.elements):
                if self.elements[i] == self.elements[j]:
                    constant += self.elements[j].constant
                else:
                    break
                j += 1
            new_list.append(Element(constant, self.elements[i].variables))
            i = j

        return Coefficient(new_list)

    def __neg__(self) -> Coefficient:
        """
        Negate a Coefficient.

        For negating a Coefficient it is sufficient to negate each element.

        Returns
        -------
        Coefficient
            A new coefficient that is the negated form of the Coefficient.
        """
        elements = [-element for element in self.elements]
        return Coefficient(elements)

    def __sub__(self, other: Coefficient) -> Coefficient:
        """
        Subtract two Coefficient.

        Subtract of two Coefficient is adding one with the negated of the other.

        Parameters
        ----------
        other : Coefficient
            The other Coefficient that should be subtracted.

        Returns
        -------
        Coefficient
            New coefficient that is subtracted of two Coefficient
        """
        return self + (-other)

    def convert_to_preorder(self) -> str:
        """
        Convert Coefficient to preorder format string.

        Returns
        -------
        str
            String in preorder format of the class
        """
        if len(self.elements) == 0:
            return '0'
        if len(self.elements) == 1:
            return self.elements[0].convert_to_preorder()
        preorder = '(+ 0 '
        not_zero = False
        for i in range(0, len(self.elements)):
            if self.elements[i].constant == 0:
                continue
            else:
                not_zero = True
            preorder += self.elements[i].convert_to_preorder() + ' '
        preorder += ')'
        if not_zero:
            return preorder
        else:
            return '0'
