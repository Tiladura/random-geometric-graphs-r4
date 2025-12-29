import random
import math
import networkx as nx
import matplotlib.pyplot as plt

N = 50
trials = 100          # Monte Carlo trials per r
num_r = 100           # number of r values
num_experiments = 10  # how many full curves

r_values = [0.01 + k * (1.0 - 0.01) / (num_r - 1) for k in range(num_r)]

all_avg_fractions = []   # list of curves
r_stars = []             # list of r* values

for exp in range(num_experiments):

    avg_fractions = []

    for r in r_values:
        fractions = []

        for _ in range(trials):
            points = [
                (random.random(), random.random(),
                 random.random(), random.random())
                for _ in range(N)
            ]

            G = nx.Graph()
            G.add_nodes_from(range(N))

            for i in range(N):
                for j in range(i + 1, N):
                    if math.dist(points[i], points[j]) < r:
                        G.add_edge(i, j)

            largest_cc = len(max(nx.connected_components(G), key=len))
            fractions.append(largest_cc / N)

        avg_fractions.append(sum(fractions) / trials)

    #compute slope for THIS curve
    grads = []
    for i in range(1, len(r_values) - 1):
        dr = r_values[i + 1] - r_values[i - 1]
        df = avg_fractions[i + 1] - avg_fractions[i - 1]
        grads.append(df / dr)

    max_i = max(range(len(grads)), key=lambda i: grads[i])
    r_star = r_values[max_i + 1]

    all_avg_fractions.append(avg_fractions)
    r_stars.append(r_star)

#PLOTTING
plt.figure(figsize=(8, 5))

# plot all curves
for curve in all_avg_fractions:
    plt.plot(r_values, curve, color='blue', alpha=0.15)

# plot all r* lines
for r in r_stars:
    plt.axvline(x=r, color='red', alpha=0.1)

# mean r*
mean_r_star = sum(r_stars) / len(r_stars)
plt.axvline(x=mean_r_star, color='black', linewidth=2,
            label=f"mean r* = {mean_r_star:.3f}")

plt.xlabel("Connection radius r")
plt.ylabel("Fraction in largest connected component")
plt.title("Connectivity transition in random geometric graph in R^4")
plt.legend()
plt.grid(True)
plt.show()
