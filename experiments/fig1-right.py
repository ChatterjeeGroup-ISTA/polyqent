import math
import matplotlib.pyplot as plt
import pandas as pd


list_of_xs = []
list_of_ys = []

df = pd.read_csv('Results-Termination.csv')
df2 = pd.read_csv('Results-Non-termination.csv')
for col_name in ['base', 'h1', 'h2', 'h12']: #, 'direct-z3--time', 'cvc5--time']:
    times = []
    term_ms = df[col_name + '-mathsat-time']
    term_z3 = df[col_name + '-z3-time']
    
    for index in range(len(term_ms)):
        ms_time = term_ms[index]
        z3_time = term_z3[index]
        if math.isnan(ms_time) and math.isnan(z3_time):
            continue
        elif math.isnan(z3_time) or ms_time < z3_time:
            times.append(ms_time)
        else:
            times.append(z3_time)
    non_term_ms = df2[col_name + '-mathsat-time']
    non_term_z3 = df2[col_name + '-z3-time']
    non_term_time = []
    
    for index in range(len(non_term_ms)):
        ms_time = non_term_ms[index]
        z3_time = non_term_z3[index]
        if math.isnan(ms_time) and math.isnan(z3_time):
            continue
        elif math.isnan(z3_time) or ms_time < z3_time:
            times.append(ms_time)
        else:
            times.append(z3_time)
    list_of_x = sorted([x/1000 for x in times])
    list_of_y = [i+1 for i in range(len(list_of_x))]
    list_of_xs.append(list_of_x)
    list_of_ys.append(list_of_y)
    print(col_name, list_of_x)

list_of_x = sorted([x/1000 for x in df['direct-z3--time'].dropna()] + [x/1000 for x in df2['direct-z3--time'].dropna()])
list_of_y = [i+1 for i in range(len(list_of_x))]
list_of_xs.append(list_of_x)
list_of_ys.append(list_of_y)

list_of_x = sorted([x/1000 for x in df['cvc5--time'].dropna()] + [x/1000 for x in df2['cvc5--time'].dropna()])
list_of_y = [i+1 for i in range(len(list_of_x))]
list_of_xs.append(list_of_x)
list_of_ys.append(list_of_y)


fig, ax = plt.subplots()
plot_shapes = ['s', '^', '<', '>', 'o', 'x']
plot_colors = ['r', 'b', 'g', 'y', 'k', 'm']
labels = ['PolyQEnt, No Heuristics',
          'PolyQEnt, Assume SAT',
          'PolyQEnt, UNSAT Core',
          'PolyQEnt, Assume SAT & UNSAT Core',
          'Direct Z3',
          'Direct CVC5']
for i in range(len(list_of_xs)):
    ax.plot(list_of_xs[i], list_of_ys[i], plot_shapes[i], color=plot_colors[i], label=labels[i], markersize=3)

plt.xlabel('time(s)')
plt.ylabel('number of SAT proved')
ax.set_xscale('log')
ax.set_yscale('log')
plt.legend()
plt.grid()
plt.show()
plt.savefig("fig1-right.png")