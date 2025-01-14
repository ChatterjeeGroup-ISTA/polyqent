import matplotlib.pyplot as plt
import pandas as pd


list_of_xs = []
list_of_ys = []

df = pd.read_csv('Results-Termination.csv')
df2 = pd.read_csv('Results-Non-termination.csv')
for col_name in ['base time', 'h1 time', 'h2 time', 'h12 time', 'direct-z3-time']:
    list_of_x = sorted([x/1000 for x in df[col_name].dropna()] + [x/1000 for x in df2[col_name].dropna()])
    list_of_y = [i+1 for i in range(len(list_of_x))]
    list_of_xs.append(list_of_x)
    list_of_ys.append(list_of_y)


fig, ax = plt.subplots()
plot_shapes = ['s', '^', '<', '>', 'o']
plot_colors = ['r', 'b', 'g', 'y', 'k']
labels = ['PolyQEnt, No Heuristics',
          'PolyQEnt, Assume SAT',
          'PolyQEnt, UNSAT Core',
          'PolyQEnt, Assume SAT & UNSAT Core',
          'Direct Z3']
for i in range(len(list_of_xs)):
    ax.plot(list_of_xs[i], list_of_ys[i], plot_shapes[i], color=plot_colors[i], label=labels[i], markersize=4)

plt.xlabel('time(s)')
plt.ylabel('number of SAT proved')
ax.set_xscale('log')
ax.set_yscale('log')
plt.legend()
plt.grid()
plt.savefig("fig1-right.png")