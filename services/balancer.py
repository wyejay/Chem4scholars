
from chempy import balance_stoichiometry

def balance_equation(equation: str) -> str:
    if '->' not in equation:
        raise ValueError("Equation must contain '->'.")
    left, right = [s.strip() for s in equation.split('->', 1)]
    reactants = set(s.strip() for s in left.split('+'))
    products = set(s.strip() for s in right.split('+'))
    reac_stoich, prod_stoich = balance_stoichiometry(reactants, products)
    def fmt(side):
        return " + ".join(f"{int(v)} {k}" for k, v in side.items())
    return f"{fmt(reac_stoich)} -> {fmt(prod_stoich)}"
