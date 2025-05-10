from puzzle import *
from visualize import *
import numpy as np
import time
import matplotlib.pyplot as plt
from tqdm import tqdm

n_range = range(3, 100)
results = np.zeros((len(n_range), 3))
retry = 200
for i, n in enumerate(tqdm(n_range)):
    for j, m in enumerate([0, n // 2, n - 1]):
        _ = solve_complete_graph_puzzle(generate_complete_graph_puzzle(n, m))

        retry_times = np.zeros(retry)
        for k in range(retry):
            # Generate a complete graph puzzle with n nodes and m uncolored nodes
            # and measure the time taken to solve it
            puzzle = generate_complete_graph_puzzle(n, m)
            start = time.perf_counter()
            solution = solve_complete_graph_puzzle(puzzle)
            end = time.perf_counter()
            if not solution.confirm_solution():
                visualize_puzzle_solution(solution)
                raise "Solution is incorrect"
            retry_times[k] = end - start
        results[i, j] = retry_times.mean()

num_edges = [n * (n - 1) // 2 for n in n_range]
plt.plot(num_edges, results[:, 0] * 1000, label=f"0 nepobarvanih vozlišč")
plt.plot(num_edges, results[:, 1] * 1000, label=f"50% nepobarvanih vozlišč")
plt.plot(num_edges, results[:, 2] * 1000, label=f"1 nepobarvano vozlišče")
plt.xlabel("Število povezav")
plt.ylabel("Porabljen čas (ms)")
plt.title("Časovna kompleksnost reševanja uganke z polnim grafom")
plt.legend()
plt.grid()
plt.savefig("time_complexity_1.png")
plt.show()

from sklearn.linear_model import LinearRegression

avg_results = results.mean(axis=1)
X = np.array(num_edges)
y = avg_results
model = LinearRegression()
model.fit(X.reshape(-1, 1), y)
print(f"Linear regression: y = {model.coef_[0]} * x + {model.intercept_}")
print(f"R^2: {model.score(X.reshape(-1, 1), y)}")

plt.plot(X, y, label="Povprečeni porabljeni čas")
plt.plot(
    X,
    model.predict(X.reshape(-1, 1)),
    label=f"y = {model.coef_[0]} * x + {model.intercept_}",
    linestyle="--",
)
plt.xlabel("Število povezav")
plt.ylabel("Porabljen čas (ms)")
plt.title("Časovna kompleksnost reševanja uganke polnega grafa")
plt.legend()
plt.grid()
plt.savefig("time_complexity_regression_1.png")
plt.show()
