"""
Session 14 · Example 3: reinforcement learning - Q-learning in a grid world
---------------------------------------------------------------------------
An agent (a delivery robot) starts at S and must reach the goal G on a 4 x 5
campus map. Walls (#) block movement; a puddle (~) costs -10; every step
costs -1; reaching G gives +20. Nobody tells the robot the route: it learns
from rewards by trial and error, updating a Q-table:
    Q[s, a] <- Q[s, a] + alpha * (reward + gamma * max Q[s', :] - Q[s, a])
Run:  python session-14_reinforcement_learning.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

GRID = ["S..#.",
        ".#.~.",
        ".#...",
        "...#G"]
ROWS, COLS = len(GRID), len(GRID[0])
ACTIONS = {0: (-1, 0, "↑"), 1: (1, 0, "↓"), 2: (0, -1, "←"), 3: (0, 1, "→")}
start = (0, 0)

def step(state, action):
    dr, dc, _ = ACTIONS[action]
    r, c = state[0] + dr, state[1] + dc
    if not (0 <= r < ROWS and 0 <= c < COLS) or GRID[r][c] == "#":
        return state, -2, False                    # bumped into a wall or the edge
    cell = GRID[r][c]
    if cell == "G":
        return (r, c), 20, True
    return (r, c), (-10 if cell == "~" else -1), False

rng = np.random.default_rng(0)
Q = np.zeros((ROWS, COLS, 4))
alpha, gamma, episodes = 0.5, 0.95, 400
returns = []
for ep in range(episodes):
    epsilon = max(0.05, 1 - ep / 250)              # explore a lot first, then exploit
    state, total, done, steps = start, 0, False, 0
    while not done and steps < 100:
        if rng.random() < epsilon:
            action = int(rng.integers(4))           # explore: random action
        else:
            action = int(Q[state].argmax())          # exploit: best known action
        nxt, reward, done = step(state, action)
        Q[state][action] += alpha * (reward + gamma * Q[nxt].max() * (not done) - Q[state][action])
        state, total, steps = nxt, total + reward, steps + 1
    returns.append(total)

print(f"average return, first 50 episodes: {np.mean(returns[:50]):7.1f}")
print(f"average return, last 50 episodes : {np.mean(returns[-50:]):7.1f}")

print("\nLearned policy (best action in each cell):")
for r in range(ROWS):
    print("  " + " ".join(GRID[r][c] if GRID[r][c] in "#G" else ACTIONS[int(Q[r, c].argmax())][2] for c in range(COLS)))

state, path, done = start, [start], False
while not done and len(path) < 20:
    state, _, done = step(state, int(Q[state].argmax()))
    path.append(state)
print("greedy route:", " -> ".join(f"({r},{c})" for r, c in path), f"| {len(path) - 1} steps, puddle avoided:",
      all(GRID[r][c] != "~" for r, c in path))

fig, ax = plt.subplots(figsize=(7, 3.4))
smooth = np.convolve(returns, np.ones(20) / 20, mode="valid")
ax.plot(returns, color="#A78BFA", alpha=0.35, label="return per episode")
ax.plot(range(19, episodes), smooth, color="#FF6B1A", lw=2, label="20-episode average")
ax.set_xlabel("episode"); ax.set_ylabel("total reward"); ax.legend()
ax.set_title("The agent learns from rewards: returns rise as exploration falls")
fig.tight_layout(); fig.savefig("session-14_reinforcement_learning.png", dpi=100)
print("Saved session-14_reinforcement_learning.png")
