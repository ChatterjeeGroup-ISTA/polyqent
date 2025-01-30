# PolyQEnt

PolyQEnt is a solver for Polynomial Quantified Entailments (PQE). 

Given an input PQE in SMT-LIB format and an optional config file, PolyQEnt finds a valuation of the unknown variables in the input such that all the PQEs are satisfied. 


## Getting Started
PolyQEnt is written in Python and can be run as a standalone tool or as a Python library. Either way, the input to PolyQEnt is an SMT-LIB instance containing the PQE and an optional config file specifying the theorem and solver to be used. 

The tool is tested for Python >=3.9 and requires the installation of:
- `Z3` many package managers provide Z3 as a package. For example, in Ubuntu, Z3 can be installed using `apt-get install z3`. Otherwise, you can find more information [here](https://github.com/Z3Prover/z3)
- `MathSAT` can be downloaded from [here](http://mathsat.fbk.eu/download.html).
- GNU C library `glibc` and Gnu Multiprecision Library `GMP` are also required.
- `pysmt` python library.

Next, we can install the package using the following command:
```bash
pip install polyqent
```

## Experiments
The `experiments` folder contains the material to run all the experiments presented in the tool paper. Please see `experiments/README.md` for detailed instructions.

## Standalone tool

To try PolyQEnt, first, clone this repository.
When using the tool via the commandline, you can use the accompanying solvers from the subfolder `solver/`. For this you do not require any installation, however, in order to run PolyQEnt, Z3 and MathSAT, the following command should be executed first:

```
chmod +x PolyQEnt solver/z3 solver/mathsat
```

Also add solvers to PATH:

```
export PATH=$PATH:[polyqent]/solver
```
where `[polyqent]` is the directory where PolyQEnt is cloned.

### Running PolyQEnt 

To run PolyQEnt on `input-example.smt2` the following command should be executed:

```
./PolyQEnt input-example.smt2
```

To run PolyQEnt on `input-example.smt2` with `config-example.json` the following command should be executed:

```
./PolyQEnt input-example.smt2 config-example.json
```

Alternatively, you can directly run PolyQEnt's main python source file as follows:

```
python3 src/polyqent/main.py --smt2 input-example.smt2 --config config-example.json
```


## API Access

PolyQEnt can be used as a Python library. The following code snippet shows how to use PolyQEnt as a library after the whole installation process is completed.

```python
from polyqent.main import execute

input_file = "input-example.smt2"
config_file = "config-example.json"

is_sat, model = execute(input_file, config_file)
```

The `execute` function allows for several different input combinations. The first argument can be the path to an `.smt2` input file or an instance os the `pysmt.solvers.solver.Solver` class with the assertions already added. The second argument can be the path to a `.json` config file or a dictionary with the configuration parameters. 

A further example of how to use PolyQEnt as a library can be found in the `example_api.py` file.


## Input Syntax

The input syntax of PolyQEnt follows the SMTLIB syntax:

 - `(declare-const [var name] Real)` is used for defining new unknown variables. 
 - `(assert phi)` is used for adding either (i) a quantifier free constraint on the unknown variables, or (ii) a PQE of the following form:
 ```
 (assert (forall ((variable type) ... ) (=> phi psi) ))
 ```
 where `phi` and `psi` are polynomial predicates over the unknown variables and the variables defined in the `forall` fragment of the assertion. 
 - the `(check-sat)` command at the end specifies that PolyQEnt should run an SMT-solver after obtaining a fully existential system of polynomials. 
 - the `(get-model)` command means that in case the SMT-solver returned `sat`, the values for unknown variables should be printed. 

 See `input-example.smt2` as an example. 

 ## Config files (Optional)

 The config file must be in `.json` format containing the following fields:
 - `theorem_name` which is one of `"farkas"`, `"handelman"` or `"putinar"`.
 - `solver_name` which is one of `"z3"` or `"mathsat"`.
 - (optional) `output_path` which should be the path to a file where PolyQEnt will store the obtained polynomial system. If not set, PolyQEnt will create a temporary file for it and will delete it in the end of execution.
 - (optional) `int_value` which is assigned `false` or `true`. When `true`, PolyQEnt tries to find integer values for unknown variables. 
 - In case `handelman` is chosen for `theorem_name`, an additional integer parameter `degree_of_sat` should be specified. This is the only parameter required by Handelman's Positivestellensatz. See the tool paper for more details.
 - In case `putinar` is chosen for `theorem_name`, four parameters should be specified in the config file: (i) `degree_of_sat` the degree of SOS polynomials considered when the LHS of PQEs are assumed satisfying, (ii) `degree_of_nonstrict_unsat`, (iii) `degree_of_strict_unsat` and (iv) `max_d_of_strict`, for the remaining three degree parameters of Putinar's positivestellensatz. The names are self-explanatory and the details can be found in the tool paper.
 - `SAT_heuristic` which should be set to `true` if the `Assume-SAT` heuristic should be used.
 - `unsat_core_heuristic` which should be set to `true` if the `UNSAT Core` heuristic should be used. 

The default value is 0 for all integer parameters and `false` for all boolean parameters. Default theorem is set based on the degree of PQEs and default solver is z3. Also, all heuristics are set to false as default.

See `config-example.json` as an example. 

## Citing

To cite PolyQEnt, please use the following reference:\
K. Chatterjee, A. K. Goharshady, E. K. Goharshady, M. Karrabi, M. Saadat, M. Seeliger, D. Zikelic\
PolyQEnt: A Polynomial Quantified Entailment Solver\
arXiv 2025, [https://arxiv.org/abs/2408.03796]


