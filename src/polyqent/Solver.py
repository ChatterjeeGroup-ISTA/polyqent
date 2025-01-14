from typing import List

from .Coefficient import Element
from .Constraint import CoefficientConstraint
from .DNF import DNF
from .Polynomial import Coefficient, Monomial, Polynomial, UnknownVariable


class Solver:
    """ 
    This class consist of some static method which are used in other classes
    """

    @staticmethod
    def find_equality_constraint(LHS: Polynomial, RHS: Polynomial) -> List[CoefficientConstraint]:
        """ 
        Given two polynomials that should be equal together, this function 
        finds constraints for the equality. Moreover, all the Coefficient of
        each Monomial in each side should be equal.

        Parameters
        ----------
        LHS : Polynomial
            left hand side of the equality
        RHS : Polynomial
            right hand side of the equality

        Returns
        -------
        List[CoefficientConstraint]
            list of the constraints that needs to be true for equality
        """
        all_degree = set(
            LHS.dict_from_degrees_to_monomials.keys()
        ).union(
            set(RHS.dict_from_degrees_to_monomials.keys())
        )

        all_constraint = []
        for degree in all_degree:
            mono1 = LHS.get_monomial_by_degree(degree)
            mono2 = RHS.get_monomial_by_degree(degree)
            constraint = CoefficientConstraint(
                mono1.coefficient - mono2.coefficient, '=')
            all_constraint.append(constraint)

        return all_constraint

    @staticmethod
    def get_constant_polynomial(variables: List[UnknownVariable], constant) -> Polynomial:
        """
        Generate new polynomial with one monomial and a constant as its coefficient.

        Parameters
        ----------
        variables : List[UnknownVariable]
            Polynomial variables
        constant : str
            The constant of the new polynomial

        Returns
        -------
        Polynomial
            Polynomial with constant as its coefficient
        """
        return Polynomial(variables,
                          [Monomial(
                              variables, [0] * len(variables),
                              Coefficient(
                                  [Element(constant, [])]
                              )
                          )]
                          )

    @staticmethod
    def get_variable_polynomial(variables: List[UnknownVariable], name: str, type_of_var: str = None) -> Polynomial:
        """
        Generate new polynomial with one monomial and a new generated variable as its coefficient

        Parameters
        ----------
        variables : List[UnknownVariable]
            Polynomial variables
        name : str
            Name of the new variable
        type_of_var : str, optional
            Type of the new variable, by default None

        Returns
        -------
        Polynomial
            Polynomial with new variable as its coefficient
        """
        new_variable = UnknownVariable(name=name, type_of_var=type_of_var)
        return Polynomial(variables,
                          [Monomial(
                              variables, [0] * len(variables),
                              Coefficient(
                                  [Element('1', [new_variable])]
                              )
                          )]
                          )

    @staticmethod
    def get_degree_polynomial(variables: List[UnknownVariable], degrees: List[int]) -> Polynomial:
        """ 
        Generate new polynomial with one monomial and given degrees

        Parameters
        ----------
        variables : List[UnknownVariable]
            Polynomial variables
        degrees : List[int]
            Degree of the monomial

        Returns
        -------
        Polynomial
            Polynomial with given degree set
        """
        return Polynomial(variables,
                          [Monomial(
                              variables, degrees,
                              Coefficient(
                                  [Element('1', [])]
                              )
                          )]
                          )

    @staticmethod
    def convert_constraints_to_smt_format(all_constraint: List[DNF], precondition: List[List[DNF]], names: List[str] = None) -> str:
        """ 
        Generate string for declaring constraint in smt format

        Parameters
        ----------
        all_constraint : List[DNF]
            Constraints that should be converted to smt format
        precondition : List[List[DNF]]
            List of precondition that should be added to the constraints
        names : List[str], optional
            List of name for each constraint, by default None

        Returns
        -------
        str
            SMT string format of constraints
        """
        smt_string = ''
        for i, constraint in enumerate(all_constraint):
            if names is None:
                smt_string = smt_string + \
                    f'(assert  {constraint.convert_to_preorder()} )\n'
            else:
                smt_string = smt_string + \
                    f'(assert ( ! {constraint.convert_to_preorder()} :named {names[i]}))\n'

        for constraint in precondition:
            if len(constraint) == 1:
                smt_string = smt_string + \
                    f'(assert  {constraint[0].convert_to_preorder()} )\n'
            elif len(constraint) == 2:
                smt_string = smt_string + \
                    f'(assert (=> {constraint[0].convert_to_preorder()} {constraint[1].convert_to_preorder()}))\n'
        return smt_string

    @staticmethod
    def smt_declare_variable_phase(all_constraint: List[DNF], real: bool = True,
                                   pre_variables: List[UnknownVariable] = []) -> str:
        """
        Generate string format for declaring the variables in smt format.

        Parameters
        ----------
        all_constraint : List[DNF]
            Constraint that their variable should be generated
        real : bool, optional
            Variables should be declared as integer or real valued, by default True
        pre_variables : List[UnknownVariable], optional
            List of variables that should be defined but might not be in constraints, by default []

        Returns
        -------
        str
            SMT string format of declaration phase
        """
        all_variables = Solver.get_all_variable(all_constraint, pre_variables)

        smt_string = ''

        for var in all_variables:
            if real:
                smt_string = smt_string + f'(declare-const {var} Real)\n'
            else:
                smt_string = smt_string + f'(declare-const {var} Int)\n'

        return smt_string

    @staticmethod
    def get_all_variable(all_constraints: List[DNF], pre_variables: List[UnknownVariable] = []) -> List[UnknownVariable]:
        """ 
        Find all the variables in a list of constraint.

        Parameters
        ----------
        all_constraints : List[DNF]
            List of constraints
        pre_variables : List[UnknownVariable], optional
            List of variables that should be defined but might not be in constraints, by default []

        Returns
        -------
        List[UnknownVariable]
            List of variables used in constraints
        """
        all_variables = set(pre_variables)
        for dnf in all_constraints:
            for literal in dnf.literals:
                for constraint in literal:
                    for element in constraint.coefficient.elements:
                        all_variables = all_variables.union(
                            set([var for var in element.variables]))

        return all_variables
