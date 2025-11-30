import sys

# counter for DPLL calls number (glocal)
dpll_calls = 0


def parse_kb(filename):
    """
    Read CNF file
    """
    clauses = []
    # symbols = set()
    symbols = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            # skip blank lines and comments
            if not line or line.startswith("#"):
                continue
            tokens = line.split()
            clause = []
            for tok in tokens:
                clause.append(tok)
                sym = tok.lstrip('-')
                if sym not in symbols:
                    symbols.append(sym)
                # symbols.add(sym)
            clauses.append(clause)
    return clauses, symbols


def add_command_line_literals(clauses, symbols, extra_literals):
    """
    extra_literals gives extra info provided by user and such is taken as literals and added into the kb
    """
    for lit in extra_literals:
        if not lit:
            continue
        clauses.append([lit])
        sym = lit.lstrip('-')
        if sym not in symbols:
            symbols.append(sym)
        # symbols.add(sym)
def literal_value(lit, model):
    """
    Returns:
      1 == true
     -1 == false
      0 == unknown
    """
    if lit.startswith('-'):
        sym = lit[1:]
        sign = -1
    else:
        sym = lit
        sign = 1

    val = model.get(sym, 0)  # default unknown
    if val == 0:
        return 0
    # if symbol’s truth matches the literal sign, literal is true
    return 1 if val == sign else -1

def is_clause_satisfied(clause, model):
    """Return True if any literal in the clause is true"""
    for lit in clause:
        if literal_value(lit, model) == 1:
            return True
    return False

def is_clause_false(clause, model):
    """
    Return True if all literals in the clause are false.
    """
    all_false = True
    for lit in clause:
        lv = literal_value(lit, model)
        if lv == 1:      # clause already satisfied
            return False
        if lv == 0:      # undecided
            all_false = False
    return all_false
def find_unit_clause(clauses, model):
    """
    Find a clause that has one unassigned literal
    and no true literals. Return literal or None
    """
    for clause in clauses:
        if is_clause_satisfied(clause, model):
            continue  # already satisfied, not unit

        unassigned_lit = None
        num_unassigned = 0

        for lit in clause:
            v = literal_value(lit, model)
            if v == 0:  # unknown
                num_unassigned += 1
                unassigned_lit = lit
            elif v == 1:
                # satisfied; we would have caught this above,
                # but just in case, break
                unassigned_lit = None
                num_unassigned = 0
                break

        if num_unassigned == 1:
            return unassigned_lit

    return None
def choose_unassigned_symbol(clauses, model):
    # for sym in symbols:
    #     if model.get(sym, 0) == 0:
    #         return sym
    for c in clauses:
        if is_clause_satisfied(c, model) or is_clause_false(c, model):
            continue
        # get unassigned literal from this clause
        for lit in c:
            sym = lit.lstrip('-')
            if model.get(sym, 0) == 0:
                return sym
    return None
def dpll(clauses, symbols, model):
    """
    DPLL algorithm
    returns boolean and model
    1 means True
    0 means unknown
    -1 means False
    """
    global dpll_calls
    dpll_calls += 1
    print(f"model: {model}")

    # Check all clauses
    all_satisfied = True
    for c in clauses:
        if is_clause_satisfied(c, model):
            continue
        if is_clause_false(c, model):
            return False, model  # contradiction
        all_satisfied = False
    if all_satisfied:
        return True, model  # all clauses satisfied

    #Unit Clause heuristic
    unit_lit = find_unit_clause(clauses, model)
    if unit_lit is not None:
        # Assign the unit literal in the model
        if unit_lit.startswith('-'):
            sym = unit_lit[1:]
            val = -1
        else:
            sym = unit_lit
            val = 1
        current_val = model.get(sym, 0)
        # if conflicting assignment branch is unsatisfiable
        if current_val not in (0, val):
            return False, model
        new_model = model.copy()
        new_model[sym] = val
        # new_symbols = set(symbols)
        new_symbols = [s for s in symbols if s != sym]
        # if sym in new_symbols:
        #     new_symbols.remove(sym)
        return dpll(clauses, new_symbols, new_model)
    #No unit clause choose a symbol and branch
    sym = choose_unassigned_symbol(clauses, model)
    if sym is None:
        # should not be false as not all clauses satisfied
        # but no unassigned symbols left.
        return False, model
    print(f"branch on {sym}")
    # remaining_symbols = set(symbols)
    remaining_symbols = [s for s in symbols if s != sym]
    # remaining_symbols.remove(sym)
    # for sym == True
    for val in (1, -1):
        print(f"trying {sym} = {val}")
        new_model = model.copy()
        new_model[sym] = val
        sat, final_model = dpll(clauses, remaining_symbols, new_model) # recursive call
        if sat:
            return True, final_model
        print(f"backtracking from {sym} = {val}")
    # both branches fail
    return False, model

def print_solution(model):
    print("solution:")
    for sym in sorted(model.keys()):
        print(f"{sym}: {model[sym]}")
def main():
    kb_filename = sys.argv[1]
    extra_literals = sys.argv[2:]
    clauses, symbols = parse_kb(kb_filename)
    # print("Parsed clauses:", clauses)
    # print("Parsed symbols:", symbols)
    add_command_line_literals(clauses, symbols, extra_literals)
    # print("After adding command-line")
    # print("Clauses:", clauses)
    # print("Symbols:", symbols)
    # Initialize model: all symbols unknown (0)
    model = {sym: 0 for sym in symbols}
    global dpll_calls
    dpll_calls = 0
    sat, final_model = dpll(clauses, symbols, model)
    if sat:
        print_solution(final_model)
    else:
        print("unsatisfiable")

    print(f"total DPLL calls: {dpll_calls}")
if __name__ == "__main__":
    main()