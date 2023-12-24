from collections import deque
import matplotlib.pyplot as plt

def ac3(csp, queue=None):
    if queue is None:
        queue = deque(csp.arcs)

    while queue:
        (xi, xj) = queue.popleft()
        if revise(csp, xi, xj):
            if not csp.domains[xi]:
                return False
            for xk in csp.neighbours[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True

def revise(csp, xi, xj):
    revised = False
    for x in csp.domains[xi][:]:
        if not any(csp.constraint(x, y) for y in csp.domains[xj]):
            csp.domains[xi].remove(x)
            revised = True
    return revised

def visualize_arcs(arcs):
    fig, ax = plt.subplots()

    for arc in arcs:
        row1, col1 = arc[0] // 9, arc[0] % 9
        row2, col2 = arc[1] // 9, arc[1] % 9
        ax.plot([col1 + 0.5, col2 + 0.5], [8.5 - row1, 8.5 - row2], color='red')

    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.set_xticks(range(10))
    ax.set_yticks(range(10))
    ax.grid(True)
    ax.set_aspect('equal')
    plt.show()