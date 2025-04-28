#!/usr/bin/env python3
import re
import sys

def tokenize(s):
    # Insert spaces around parentheses to simplify tokenization.
    s = re.sub(r'([\(\)])', r' \1 ', s)
    return s.split()

def parse_tokens(tokens):
    """Recursively parse tokens into a nested S-expression."""
    if not tokens:
        raise SyntaxError("Unexpected EOF while reading")
    token = tokens.pop(0)
    if token == '(':
        lst = []
        while tokens[0] != ')':
            lst.append(parse_tokens(tokens))
        tokens.pop(0)  # remove closing ')'
        return lst
    elif token == ')':
        raise SyntaxError("Unexpected )")
    else:
        return token

def parse_smt(s):
    tokens = tokenize(s)
    exprs = []
    while tokens:
        if tokens[0].strip() == "":
            tokens.pop(0)
        else:
            exprs.append(parse_tokens(tokens))
    return exprs

def convert(expr):
    """
    Recursively convert an SMT-LIB2 S-expression into a Redlog syntax string.
    This conversion translates quantifiers, logical connectives, and arithmetic operators.
    """
    if isinstance(expr, list):
        if not expr:
            return ""
        head = expr[0]
        
        # Process assertions by converting their inner formula.
        if head == 'assert':
            return convert(expr[1])
        
        # Universal quantifier: (forall ((x Real) (y Real)) body)
        if head == 'forall':
            # Expect: (forall (<bound-var-list>) body)
            if len(expr) < 3:
                raise ValueError("forall expects a bound variable list and a body")
            bound_list = expr[1]
            body = convert(expr[2])
            # Nest the quantifiers one at a time.
            for decl in reversed(bound_list):
                # Each declaration is like (x Real); take the variable name.
                if isinstance(decl, list) and len(decl) >= 1:
                    var = decl[0]
                    body = f"all ({var}, {body})"
                else:
                    raise ValueError("Invalid bound variable declaration in forall")
            return body
        
        # Existential quantifier: (exists ((x Real) (y Real)) body)
        if head == 'exists':
            if len(expr) < 3:
                raise ValueError("exists expects a bound variable list and a body")
            bound_list = expr[1]
            body = convert(expr[2])
            for decl in reversed(bound_list):
                if isinstance(decl, list) and len(decl) >= 1:
                    var = decl[0]
                    body = f"ex ({var}, {body})"
                else:
                    raise ValueError("Invalid bound variable declaration in exists")
            return body
        
        # Implication: (=> f g) is converted to ((not f) or g)
        if head == '=>':
            if len(expr) != 3:
                raise ValueError("=> expects exactly 2 arguments")
            left = convert(expr[1])
            right = convert(expr[2])
            return f"((not {left}) or {right})"
        
        # Logical conjunction.
        if head == 'and':
            args = [convert(arg) for arg in expr[1:]]
            return "(" + " and ".join(args) + ")"
        
        # Logical disjunction.
        if head == 'or':
            args = [convert(arg) for arg in expr[1:]]
            return "(" + " or ".join(args) + ")"
        
        # Negation.
        if head == 'not':
            if len(expr) != 2:
                raise ValueError("not expects one argument")
            return f"(not {convert(expr[1])})"
        
        # Equality.
        if head == '=':
            if len(expr) != 3:
                raise ValueError("= expects 2 arguments")
            left = convert(expr[1])
            right = convert(expr[2])
            return f"({left} = {right})"
        
        # Relational operators.
        if head in ['<', '>', '<=', '>=']:
            if len(expr) != 3:
                raise ValueError(f"{head} expects 2 arguments")
            left = convert(expr[1])
            right = convert(expr[2])
            return f"({left} {head} {right})"
        
        # Arithmetic operations.
        if head == '+':
            args = [convert(arg) for arg in expr[1:]]
            return "(" + " + ".join(args) + ")"
        if head == '*':
            args = [convert(arg) for arg in expr[1:]]
            return "(" + " * ".join(args) + ")"
        if head == '-':
            args = [convert(arg) for arg in expr[1:]]
            if len(args) == 1:
                return "(-" + args[0] + ")"
            elif len(args) == 2:
                return "(" + args[0] + " - " + args[1] + ")"
            else:
                return "(" + args[0] + " - (" + " + ".join(args[1:]) + "))"
        
        # Default: function application (or an unrecognized operator).
        args = [convert(arg) for arg in expr[1:]]
        if args:
            return f"{head}({', '.join(args)})"
        else:
            return head
    else:
        # Base case: variable, number, or symbol.
        return expr

def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_to_redlog.py <input_file.smt2>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    with open(input_file, "r") as f:
        content = f.read()

    int_or_real = "integers" if "RevTerm" in input_file else "reals"
    
    # Parse the SMT-LIB2 file into S-expressions.
    expressions = parse_smt(content)
    declared_vars = []
    converted_asserts = []
    
    # Process each expression:
    for expr in expressions:
        if isinstance(expr, list) and expr:
            head = expr[0]
            if head == 'declare-const':
                # Collect variables defined by declare-const.
                declared_vars.append(expr[1])
            elif head == 'assert':
                conv = convert(expr)
                if conv:
                    converted_asserts.append(conv)
            # Other commands (like check-sat or get-model) are ignored.
    
    # Combine multiple assertions using " and " if necessary.
    if converted_asserts:
        body = " and ".join(converted_asserts)
    else:
        body = "true"
    
    # Wrap the combined assertions with nested existential quantifiers
    # for each variable declared via declare-const.
    for var in reversed(declared_vars):
        body = f"ex ({var}, {body})"
    
    # Wrap the entire formula with the Redlog command rlqe( ... );
    redlog_formula = f"rlqe( {body} );"
    
    # print("Redlog Instance:")
    print(f"rlset {int_or_real};")
    print(redlog_formula)

if __name__ == "__main__":
    main()
