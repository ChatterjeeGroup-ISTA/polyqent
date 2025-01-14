import os
import shutil
from enum import Enum
from typing import Any

ABS_PATH = os.path.dirname(os.path.abspath(__file__))


class Theorem(Enum):
    """
    Theorem is a class which is used to define the type of theorems that can be used in the solver.
    """
    FARKAS = 'farkas'
    HANDELMAN = 'handelman'
    PUTINAR = 'putinar'


class AvailabilityDict(dict):
    """
    AvailabilityDict is a class which is used to define a dictionary that can
    be used to hierarchically check the availability of commands in the system,
    given an array of possible commands.
    
    Parameters
    ----------
    *args : Any
        The arguments that are passed to the dictionary.
    **kwargs : Any
        The keyword arguments that are passed to the dictionary.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.items():
            if not isinstance(value, list):
                self[key] = [value]

    def __getitem__(self, key: Any) -> Any:
        """
        Retrieve the first available command from the list of possible commands.

        Parameters
        ----------
        key : Any
            The key to be retrieved from the dictionary.

        Returns
        -------
        Any
            The first available command from the list of possible commands.
        """
        possible_values = super().__getitem__(key)
        for value in possible_values:
            if AvailabilityDict.available(value):
                return value
        return None

    def __setitem__(self, key: Any, value: Any) -> None:
        if not isinstance(value, list):
            value = [value]
        super().__setitem__(key, value)

    @staticmethod
    def available(item):
        return shutil.which(item) is not None


class Constant:
    """
    This class consist of some constant dictionaries which are used for configuration of the solvers.
    """
    options = {
        'z3': '(set-option :print-success false)\n' +
              '(set-option :produce-models true)\n',
        'mathsat': '(set-option :print-success false)\n' +
                   '(set-option :produce-models true)\n',
        'default': ''
    }

    default_path = AvailabilityDict({
        'z3': ['z3', os.path.join(ABS_PATH, '..', '..', 'solver', 'z3')],
        'mathsat': ['mathsat', os.path.join(ABS_PATH, '..', '..', 'solver', 'mathsat')],
        'default': ''
    })

    command = {
        'z3': '',
        'mathsat': '',
        'default': ''
    }
