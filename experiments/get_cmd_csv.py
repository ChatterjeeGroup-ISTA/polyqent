import sys 
import pandas as pd


def get_cmd(benchmark, config, solver, bench_set, bench_class):
	if config == "direct-z3":
		return f"./solver/z3 -smt2 experiments/benchmarks/{bench_set}/{bench_class}/{benchmark}"
	elif config == "cvc5":
		return f"./solver/cvc5 -m experiments/benchmarks/{bench_set}/{bench_class}/{benchmark}"
	elif config == "redlog":
		return f"./solver/redlog/usr/bin/rfcsl -b < experiments/benchmarks-redlog/{bench_set}/{bench_class}/{benchmark}"
	elif config == "mathematica":
		return f"math < experiments/benchmarks-mathematica/{bench_set}/{bench_class}/{benchmark}"
	else: 
		return f"./PolyQEnt experiments/benchmarks/{bench_set}/{bench_class}/{benchmark} experiments/configs-{config}/{solver}/benchmarks/{bench_set}/{bench_class}/{benchmark}.json"

configs = ["base", "h1", "h2", "h12", "direct-z3","cvc5", "redlog", "mathematica"]
solvers = ["mathsat", "z3"]

revterm = ["RevTerm", ["all", "best_config"]]
termination = ["Termination", ["linear", "poly"]]
AST = ["almost-sure-termination", ["cost-analysis-table-3", "higher-moment-tail-prob"]]
synth = ["polysynth",["linear", "poly"]]

benchmark_sets = [revterm, termination, AST, synth]


for bench_set in benchmark_sets:
	filename = f"spreadsheets/result-{bench_set[0]}.csv"
	# Read the CSV file
	df = pd.read_csv(filename)

	res_df = pd.DataFrame()
	benchmarks = df['name']
	res_df['name'] = benchmarks
	for config in configs: 
		for solver in solvers:
			min_time = [None]*len(benchmarks)
			best_cmd = [None]*len(benchmarks)
			for bench_class in bench_set[1]:
				if config == "direct-z3" or config == "cvc5" or config == "redlog" or config == "mathematica":
					solver = ""
				col = df[f"{config}-{solver}-{bench_set[0]}-{bench_class}"]
				next_col_index = df.columns.get_loc(col.name) + 1
				if next_col_index < len(df.columns):
					times = df.iloc[:, next_col_index]
				else:
					times = None
				
				for index,value in col.items():
					# print(index,value)
					if value == True:
						if min_time[index] is None or int(min_time[index]) > int(times[index]):
							min_time[index] = times[index]
							best_cmd[index] = get_cmd(benchmarks[index], config, solver, bench_set[0], bench_class)
			res_df[f"{config}-{solver}-cmd"] = best_cmd
			res_df[f"{config}-{solver}-time"] = min_time

	res_df.to_csv(f"spreadsheets/Results-{bench_set[0]}.csv", index=False)


				