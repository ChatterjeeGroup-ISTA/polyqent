import os
import subprocess
from pathlib import Path


heuristics = ["base", "h1", "h2", "h12"]
solvers = ["mathsat", "z3"]
linpol = ["linear", "poly"]
AST = ["cost-analysis-table-3", "higher-moment-tail-prob"]
RevTerm = ["all", "best_config"]

def run_polyqent(benchmark, config, output):
    print(f"./PolyHorn experiments/{benchmark} experiments/{config}")
    
    os.chdir("..")
    os.makedirs("work/",exist_ok=True)
    os.makedirs(Path(output).parent.absolute(),exist_ok=True)

    subprocess.run(f"timeout 180 ./PolyHorn experiments/{benchmark} experiments/{config} > {output}", shell=True)

    os.chdir("experiments/")

def run_z3(benchmark, output):
    print(f"z3 experiments/{benchmark}")

    os.chdir("..")
    os.makedirs(Path(output).parent.absolute(),exist_ok=True)
    
    subprocess.run(f"timeout 180 z3 experiments/{benchmark} > {output}", shell=True)

    os.chdir("experiments/")

# Termination
for config in linpol:
    path = f"benchmarks/Termination/{config}"
    onlyfiles = sorted([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
    for benchmark in onlyfiles:
        input_file = f"{path}/{benchmark}"
        for heuristic in heuristics:
            for solver in solvers:
                config_file = f"configs-{heuristic}/{solver}/{path}/{benchmark}.json"
                output_file = f"outputs/{heuristic}/{solver}/{path}/{benchmark}.out"
                run_polyqent(input_file, config_file,output_file)
        run_z3(input_file, f"outputs/direct-z3/{benchmark}.out")

# Non-Termination
for config in RevTerm:
    path = f"benchmarks/RevTerm/{config}"
    onlyfiles = sorted([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
    for benchmark in onlyfiles:
        input_file = f"{path}/{benchmark}"
        for heuristic in heuristics:
            for solver in solvers:
                config_file = f"configs-{heuristic}/{solver}/{path}/{benchmark}.json"
                output_file = f"outputs/{heuristic}/{solver}/{path}/{benchmark}.out"
                run_polyqent(input_file, config_file,output_file)
        run_z3(input_file, f"outputs/direct-z3/{benchmark}.out")

#Almost sure termination
for config in AST:
    path = f"benchmarks/almost-sure-termination/{config}"
    onlyfiles = sorted([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
    for benchmark in onlyfiles:
        input_file = f"{path}/{benchmark}"
        for heuristic in heuristics:
            for solver in solvers:
                config_file = f"configs-{heuristic}/{solver}/{path}/{benchmark}.json"
                output_file = f"outputs/{heuristic}/{solver}/{path}/{benchmark}.out"
                run_polyqent(input_file, config_file,output_file)
        run_z3(input_file, f"outputs/direct-z3/{benchmark}.out")

#Synthesis
for config in linpol:
    path = f"benchmarks/polysynth/{config}"
    onlyfiles = sorted([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
    for benchmark in onlyfiles:
        input_file = f"{path}/{benchmark}"
        for heuristic in heuristics:
            for solver in solvers:
                config_file = f"configs-{heuristic}/{solver}/{path}/{benchmark}.json"
                output_file = f"outputs/{heuristic}/{solver}/{path}/{benchmark}.out"
                run_polyqent(input_file, config_file,output_file)
        run_z3(input_file, f"outputs/direct-z3/{benchmark}.out")

