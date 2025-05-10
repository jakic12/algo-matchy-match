from puzzle import *
from visualize import *

complete_puzzle = generate_complete_graph_puzzle(5, 1)

solution = solve_complete_graph_puzzle(complete_puzzle)
print(solution)

# check if the solution is correct
print(solution.confirm_solution())

visualize_puzzle_solution(solution)
