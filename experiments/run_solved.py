import pandas as pd
import os
import subprocess
import time
from tabulate import tabulate


columns = ['base-mathsat', 'base-z3', 'h1-mathsat', 'h1-z3', 'h2-mathsat', 'h2-z3', 'h12-mathsat', 'h2-z3', 'direct-z3','cvc5']

list_of_xs = {'base':[], 'h1':[], 'h2':[], 'h12':[]}
list_of_ys = {'base':[], 'h1':[], 'h2':[], 'h12':[]}

def run_commands(file_name):
    df = pd.read_csv(file_name)
    results = {}
    for col_name in columns:
        results[col_name] = {}
        df_no_nan = df.dropna(subset=[col_name + '-cmd'])
        for index, row in df_no_nan.iterrows():
            exp_name = row['name']
            command = row[col_name + '-cmd']

            print('>>> run experiment ' + exp_name + ' from ' + file_name)

            os.chdir("..")
            os.makedirs("work/", exist_ok=True)
            try:
                start = time.time()
                output = str(subprocess.check_output(f"timeout 180 {command}", shell=True))
                process_time = time.time() - start
                if "unsat" in output:
                    results[col_name][exp_name] = {'sat': False}
                elif "sat" in output:
                    results[col_name][exp_name] = {'sat': True, 'time': process_time}
                else:
                    results[col_name][exp_name] = {'sat': False}
                print(output)
            except subprocess.CalledProcessError as e:
                results[col_name][exp_name] = {'sat': None}
                print('timeout error!')
            print(command)
            os.chdir("experiments/")
    return results



all_results = [run_commands('Results-Termination.csv'), run_commands('Results-Non-termination.csv'), run_commands('Results-almost-sure-termination.csv'), run_commands('Results-polysynth.csv')]

table_data = [[None] + columns,
              ['Termination']+[None]*10,
              ['None_termination']+[None]*10,
              ['AST']+[None]*10,
              ['Polysynth']+[None]*10]
print('\n\n\n=======================================\nResults:\n===========================================\n')

for j in range(len(all_results)):
    for i in range(len(columns)):
        col_name = columns[i]
        count = 0
        time_sum = 0
        for exp_name in all_results[j][col_name]:
            if all_results[j][col_name][exp_name]['sat']:
                count += 1
                time_sum += all_results[j][col_name][exp_name]['time']
        if count==0:
            table_data[j+1][i+1] = str(count) + ': ' + "NA"
        else:
            table_data[j+1][i+1] = str(count) + ': ' + str(round(time_sum/count,2)) + '(s)'

print(tabulate(table_data))
