



import sys
import os



class Node:
    def __init__(self, state, parent=None, g=0, h=0, action=None):
        self.state = state
        self.parent = parent
        self.g = g  # cost so far
        self.h = h  # heuristic
        self.f = g + h  # eval funct
        self.action = action     

    def __lt__(self, other):
        return self.f < other.f  # priority queue 


def read_bwp(filename):
    with open(filename) as f:
        lines = [line.rstrip("\n") for line in f] 
        # print(lines)

    s, b, m = map(int, lines[0].split())
    print("moves num:", m)
    sep_index = lines.index(">>>>>>>>>>")

    initial_lines = lines[sep_index+1:sep_index+1+s]
    sep_index2 = lines.index(">>>>>>>>>>", sep_index+1)
    sep_index3 = lines.index(">>>>>>>>>>", sep_index2+1)
    goal_lines = lines[sep_index2+1:sep_index3]

    initial_state = tuple(tuple(stack) for stack in initial_lines)
    goal_state = tuple(tuple(stack) for stack in goal_lines)

    print("inital state: ", initial_state)
    print_state(initial_state)

    print("goal state: ", goal_state)
    print_state(goal_state)

    return initial_state, goal_state

def successors(state):
    """give all possible successor states."""
    states = []
    for i, stack in enumerate(state):
        if not stack:  
            continue
        block = stack[-1]  # top block
        new_stack_from = stack[:-1]  # remove it
        for j in range(len(state)):
            if i == j:
                continue
            new_stack_to = state[j] + (block,)
            new_state = list(state)
            new_state[i] = new_stack_from
            new_state[j] = new_stack_to
            move_desc = f"move {block} from stack {i+1} to stack {j+1}"
            states.append((tuple(new_state), move_desc))
    return states

def print_state(state):
    """Print the inital and goal nicely"""
    max_height = max(len(stack) for stack in state)
    for level in range(max_height - 1, -1, -1):
        row = []
        for stack in state:
            if len(stack) > level:
                row.append(stack[level])
            else:
                row.append(" ")
        print("  ".join(row))
    print("-" * (3 * len(state) - 2))  # divider

# ---------------- Heuristics ---------------- #

def h0(state, goal):
    """BFS"""
    return 0

def h2(state, goal):
    """Number of blocks out of place."""
    misplaced = 0
    for s1, s2 in zip(state, goal):
        for k in range(min(len(s1), len(s2))):
            if s1[k] != s2[k]:
                misplaced += 1
        misplaced += abs(len(s1) - len(s2))
    return misplaced

def h1(state, goal):
    """Number of blocks in place + number of blocks misplaced within correct stack"""
    # print(" -------- HEURISTIC -------- ")
    total_block = 0
    
    for s1, s2 in zip(state, goal):
        # print("s1&s2", s1, s2)
        total_block += len(s1) + len(s2)
        for k in range(min(len(s1), len(s2))):
            if s1[k] == s2[k]:
                total_block -= 1
            elif s1[k] in s2:
                for i in range (len(s2)-1, 0, -1):
                    if s1[k] == s2[i]:
                        continue
                    else:
                        total_block += 1
            else:
                continue
        # print("heuristic value: ", total_block)
    return total_block

def h_best(state, goal):
    return h1(state, goal)


# ---------------- A* Search ---------------- #

def reconstruct_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return list(reversed(path))


def a_star_search(start, goal, successors_fn, h_fn, max_iters=100000):
    """
    start: initial state (tuple of stacks)
    goal: goal state
    successors_fn: function(state) -> list of successor states
    h_fn: heuristic function(state, goal) -> estimated cost to goal
    """
    import heapq

    frontier = []
    start_node = Node(start, g=0, h=h_fn(start, goal))
    heapq.heappush(frontier, start_node)

    reached = {start: start_node}
    iterations = 0
    maxq = 1

    while frontier and iterations < max_iters:
        iterations += 1
        node = heapq.heappop(frontier)
        print(f"iter={iterations}, depth={node.g}, pathcost={node.g}, heuristic={node.h}, score={node.f}, children=", end='')

        children = successors_fn(node.state)
        print(f"{len(children)}, Qsize={len(frontier)}")

        if node.state == goal:
            return reconstruct_path(node), iterations, maxq

        for succ, move in successors_fn(node.state):  # succ = new_state
            
            g = node.g + 1  # every move costs 1
            h = h_fn(succ, goal)
            child = Node(succ, parent=node, g=g, h=h, action=move)

            if succ not in reached or g < reached[succ].g:
                reached[succ] = child
                heapq.heappush(frontier, child)
                # print(f"\nGenerated child (g={g}, h={h}, f={g+h}):")
                # print_state(succ)

        maxq = max(maxq, len(frontier))


    return None, iterations, maxq

# ---------------- MAIN ---------------- #

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python blocksworld.py <filename> [-H H0|H1|Hbest] [-MAX_ITERS N]")
        sys.exit(1)
    filename = os.path.join("probs", sys.argv[1])
    heuristic_flag = "Hbest"
    max_iters = 100000

    if "-H" in sys.argv:
        heuristic_flag = sys.argv[sys.argv.index("-H")+1]
    if "-MAX_ITERS" in sys.argv:
        max_iters = int(sys.argv[sys.argv.index("-MAX_ITERS")+1])

    if heuristic_flag == "H0":
        heuristic = h0
    elif heuristic_flag == "H1":
        heuristic = h1
    elif heuristic_flag == "H2":
        heuristic = h2
    else:
        heuristic = h_best

    start, goal = read_bwp(filename)

    print("Using heuristic:", heuristic.__name__)

    solution, iters, maxq = a_star_search(start, goal, successors, heuristic, max_iters)
    

    # Get just the file name, e.g. "probA05.bwp"
    problem_name = os.path.basename(filename)

    # Prepare result line
    if solution:
        planlen = len(solution) - 1
        result_line = f"{problem_name:<14} | {planlen:>7} | {iters:>7} | {maxq:>7}\n"
    else:
        result_line = f"{problem_name:<14} | {'FAILED':>7} | {iters:>7} | {maxq:>7}\n"


    if solution:
        planlen = len(solution) - 1
        print(f"success! iter={iters}, cost={planlen}, depth={planlen}, max queue size={maxq}")

        for i, state in enumerate(solution):
            g = i
            h = heuristic(state, goal)
            f = g + h
            print(f"move {i}, pathcost={g}, heuristic={h}, f(n)=g(n)+h(n)={f}")
            for stack in state:
                print("".join(stack) if stack else "_")
            print(">>>>>>>>>>")

        # Print final statistics line (mimic instructor format)
        print(f"statistics: probs/{problem_name} method Astar planlen {planlen} iter {iters} maxq {maxq}")

    else:
        print(f"FAILED after {iters} iterations, maxq={maxq}")

    # # Write to results.txt
    # results_path = "results.txt"
    # if not os.path.exists(results_path):
    #     with open(results_path, "w") as f:
    #         f.write("File           | Planlen | Iter   | MaxQ\n")
    #         f.write("----------------+---------+--------+-------\n")

    # with open(results_path, "a") as f:
    #     f.write(result_line)

    # Also print to terminal as before
    # if solution:
    #     print(f"success! planlen={planlen} iter={iters} maxq={maxq}")
    #     for depth, state in enumerate(solution):
    #         print(f"\nmove {depth}")
    #         for stack in state:
    #             print("".join(stack) if stack else "_")
    #         print(">>>>>>>>>>")
    # else:
    #     print(f"FAILED after {iters} iterations, maxq={maxq}")


