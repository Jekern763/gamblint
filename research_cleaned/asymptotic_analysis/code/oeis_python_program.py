import sympy as sp

n, u = sp.symbols("n u")


def generate_triangle(n_max):
    T = {0: sp.Integer(1)}

    triangle = []

    for t in range(1, n_max + 1):
        # Boundary value T(t,t) = T(t,t-1)
        boundary = T[t - 1].subs(n, t)

        # dT(n,t)/dn = 2t*T(n,t-1)
        integrand = 2 * t * T[t - 1].subs(n, u)

        T[t] = sp.expand(boundary + sp.integrate(integrand, (u, t, n)))

    for row_n in range(1, n_max + 1):
        row = [T[t].subs(n, row_n) for t in range(1, row_n + 1)]
        triangle.append(row)

    return triangle


def print_triangle(triangle):
    """Print the triangle in a human-readable form."""
    for row in triangle:
        print(str(row).replace("[", "").replace("]", ""))


with open("b_file.txt", "w") as file:
    index_counter = 1  # Track the continuous index for every item

    for row in generate_triangle(100):
        for item in row:
            # Write the index and value separated by a space, followed by a newline
            file.write(f"{index_counter} {item}\n")
            index_counter += 1
