import sys
import os
import re

def extract_time(line):
    tmp=line.split()[1]
    (minute,sec)=(tmp.split('m')[0],tmp.split('m')[1])
    minute=int(minute)
    sec=float(sec[:-1])
    return str(int((minute*60+sec)*1000))

def parse_output(file):
	result = "False"
	runtime = ""
	if os.path.isfile(file):
		with open(file,"r") as fr:
			lines = fr.readlines()
			for line in lines:
				if "sat" in line and "unsat" not in line:
					result="True"
				elif "Out" in line and "True" in line: # mathamtica
					result = "True"
				elif "redlog" in file and "true" in line:
					result = "True"
				elif "real" in line and result=="True":
					runtime=extract_time(line)
					break 
	return (result,runtime)



configs = ["base", "h1", "h2", "h12","direct-z3", "cvc5", "redlog", "mathematica"]
polyHorn_solvers = ["mathsat", "z3"]
quantifier_solvers = [""]

revterm = ["RevTerm", ["all", "best_config"]]
termination = ["Termination", ["linear", "poly"]]
AST = ["almost-sure-termination", ["cost-analysis-table-3", "higher-moment-tail-prob"]]
synth = ["polysynth",["linear", "poly"]]

benchmarks = [revterm, termination, AST, synth]

for bench_set in benchmarks:
	# columns =  name, (benchset[1][0], benchset[1][1]) for each config x solver
	print(bench_set)
	columns = []
	all_files = []
	for config in configs:
		if config=="direct-z3" or config=="cvc5" or config=="redlog" or config=="mathematica":
			solvers=quantifier_solvers
		else:
			solvers=polyHorn_solvers
		col_union = [f"{config}-{bench_set[0]}-union"]
		col_union_time = ["time"]
		for solver in solvers:
			col0 = [f"{config}-{solver}-{bench_set[0]}-{bench_set[1][0]}"]
			col1 = ["time"]
			col2 = [f"{config}-{solver}-{bench_set[0]}-{bench_set[1][1]}"]
			col3 = ["time"]
			
			col4 = [f"{config}-{solver}-{bench_set[0]}-union"]
			col5 = ["time"]


			input_dir = f"experiments/benchmarks/{bench_set[0]}/{bench_set[1][0]}/"
			dir1 = f"outputs/{config}/{solver}/benchmarks/{bench_set[0]}/{bench_set[1][0]}/"
			dir2 = f"outputs/{config}/{solver}/benchmarks/{bench_set[0]}/{bench_set[1][1]}/"
			# if os.path.exists(dir1):
			# 	files1 = os.listdir(dir1)
			# else:
			# 	files1 = []

			# if os.path.exists(dir2):
			# 	files2 = os.listdir(dir2)
			# else:
			# 	files2 = []
			# all_files = list(set(files1+files2))
			all_files = os.listdir(input_dir)
			all_files.sort()

			for file in all_files:
				(res1,runtime1)=parse_output(dir1+file)
				(res2,runtime2)=parse_output(dir2+file)
				col0.append(res1)
				col1.append(runtime1)
				col2.append(res2)
				col3.append(runtime2)
			
			for i in range(1,len(col0)):
				if col0[i]=="True" or col2[i]=="True":
					col4.append("True")
					x1=col1[i] if col1[i]!="" else 400000
					x2=col3[i] if col3[i]!="" else 400000
					col5.append(str(min(int(x1),int(x2))))
				else:
					col4.append("False")
					col5.append("")
			columns.append(col0)
			columns.append(col1)
			columns.append(col2)
			columns.append(col3)
			columns.append(col4)
			columns.append(col5)

			for i in range(1,len(col5)):
				if len(col_union)<=i:
					col_union.append("False")
					col_union_time.append("")
				if col4[i]=="True":
					col_union[i]="True"
					x=col_union_time[i] if col_union_time[i]!="" else 400000
					col_union_time[i]=str(min(int(x),int(col5[i])))
		columns.append(col_union)
		columns.append(col_union_time)
	all_files.insert(0,"name")
	# print(all_files)
	os.makedirs("spreadsheets",exist_ok=True)
	with open("spreadsheets/result-"+bench_set[0]+".csv","w") as fw:
		for i in range(len(all_files)):
			fw.write(all_files[i]+",")
			for j in range(len(columns)):
				fw.write(columns[j][i]+",")
			fw.write("\n")
	# break


		
