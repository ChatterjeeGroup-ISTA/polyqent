import matplotlib.pyplot as plt
import pandas as pd


list_of_xs = {'base':[], 'h1':[], 'h2':[], 'h12':[]}
list_of_ys = {'base':[], 'h1':[], 'h2':[], 'h12':[]}

df = pd.read_csv('Results-Termination.csv')
df2 = pd.read_csv('Results-Non-termination.csv')
for dia in ['base', 'h1', 'h2', 'h12']:
    for col_name in ['mathsat-time', 'z3-time']:
        list_of_x = sorted([x/1000 for x in df[dia + '-' + col_name].dropna()] + [x/1000 for x in df2[dia + '-' + col_name].dropna()])
        list_of_y = [i+1 for i in range(len(list_of_x))]
        list_of_xs[dia].append(list_of_x)
        list_of_ys[dia].append(list_of_y)
    list_of_x = sorted([x/1000 for x in df['direct-z3--time'].dropna()] + [x/1000 for x in df2['direct-z3--time'].dropna()])
    list_of_y = [i+1 for i in range(len(list_of_x))]
    list_of_xs[dia].append(list_of_x)
    list_of_ys[dia].append(list_of_y)

    list_of_x = sorted([x/1000 for x in df['cvc5--time'].dropna()] + [x/1000 for x in df2['cvc5--time'].dropna()])
    list_of_y = [i+1 for i in range(len(list_of_x))]
    list_of_xs[dia].append(list_of_x)
    list_of_ys[dia].append(list_of_y)


fig, ((ax0, ax1), (ax2, ax3)) = plt.subplots(nrows=2, ncols=2, figsize=(8, 6))
ms = 2
plot_shapes = ['s', '^', 'o', 'o']
plot_colors = ['r', 'b', 'k', 'g']
labels = ['PolyQEnt MS',
          'PolyQEnt Z3',
          'Direct Z3',
          'Direct CVC5']

for i in range(len(list_of_xs['base'])):
    ax0.plot(list_of_xs['base'][i], list_of_ys['base'][i], plot_shapes[i], color=plot_colors[i], label=labels[i], markersize=ms)
ax0.set_ylabel('number of SAT proved')
ax0.set_title('No Heuristics')
ax0.set_xscale('log')
ax0.set_yscale('log')
# ax0.legend()
ax0.grid()
for i in range(len(list_of_xs['h1'])):
    ax1.plot(list_of_xs['h1'][i], list_of_ys['h1'][i], plot_shapes[i], color=plot_colors[i], label=labels[i], markersize=ms)
ax1.set_title('Assume SAT')
ax1.set_xscale('log')
ax1.set_yscale('log')
# ax1.legend()
ax1.grid()
for i in range(len(list_of_xs['h2'])):
    ax2.plot(list_of_xs['h2'][i], list_of_ys['h2'][i], plot_shapes[i], color=plot_colors[i], label=labels[i], markersize=ms)
ax2.set_ylabel('number of SAT proved')
ax2.set_xlabel('time(s)')
ax2.set_title('UNSAT Core')
ax2.set_xscale('log')
ax2.set_yscale('log')
# ax2.legend()
ax2.grid()
for i in range(len(list_of_xs['h12'])):
    ax3.plot(list_of_xs['h12'][i], list_of_ys['h12'][i], plot_shapes[i], color=plot_colors[i], label=labels[i], markersize=ms)
ax3.set_xlabel('time(s)')
ax3.set_title('Assume SAT & UNSAT Core')
ax3.set_xscale('log')
ax3.set_yscale('log')
ax3.legend()
ax3.grid()

fig.tight_layout()
plt.show()
plt.savefig("fig1-left.png")