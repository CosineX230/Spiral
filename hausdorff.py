import cmath
import math
import numpy as np

def compute_dimension(c, num_iter):
    #Calculate beta fixed point
    b1 = (1 + cmath.sqrt(1 - 4 * c)) / 2
    b2 = (1 - cmath.sqrt(1 - 4 * c)) / 2
    beta = b1 if abs(b1) > abs(b2) else b2

    #Calculate inverse branches
    current_points = [(beta, "")]
    next_points = []
    for n in range(num_iter):
        next_points = []
        for (w, address) in current_points:
            
            z = cmath.sqrt(w - c)

            next_points.append((z, address + "0"))
            next_points.append((-z, address + "1"))

        current_points = next_points

    points = {}

    for z, address in current_points:
        points[address] = z



    def build_matrix(points, s):
        addresses = sorted(points.keys())

        N = len(addresses)

        index = {
            addr: i
            for i, addr in enumerate(addresses)
        }

        M = np.zeros((N, N))

        n = len(addresses[0])

        for addr in addresses:

            row = index[addr]

            z = points[addr]

            weight = abs(2 * z) ** (-s)

            child0 = addr[1:] + "0"
            child1 = addr[1:] + "1"

            M[row, index[child0]] = weight
            M[row, index[child1]] = weight

        return M

    def spectral_radius(M):
        eigvals = np.linalg.eigvals(M)
        return max(abs(eigvals))

    s_low = 0
    s_high = 2

    for _ in range(50):

        s_mid = (s_low + s_high) / 2

        M = build_matrix(points, s_mid)

        rho = spectral_radius(M)

        if rho > 1:
            s_low = s_mid
        else:
            s_high = s_mid

    print(rho)
    return s_mid


n = 12
dim = compute_dimension(-1, n)
print(n, dim)