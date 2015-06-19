"""
Load data from Data_Liver_2009
"""
from utils import transpose
import re

def extract_treatment_variable(txt):
    print txt
    ans = re.findall(r":(.*?)i?:",txt) # grab everything between colons, ignoring terminal i if present
    return ans[0]

def extract_response_variable(txt):
    # could do this more simply, but should fail noisily if string not prepended with "DV:"
    return re.findall(r"DV:(.*)",txt)[0]
    
with open("Toy Model_data_2009") as f:
    lines = [line.strip().split(",") for line in f.readlines()]

header = lines[0]
data_lines = [map(float,line) for line in lines[1:]]
num_tr_variables = 9
num_experiments = 5

experiment_lines = [(data_lines[i],data_lines[num_experiments+i]) for i in range(num_experiments)]
for i,(before,after) in enumerate(experiment_lines):
    agreed = before[:num_tr_variables] == after[:num_tr_variables]
    print i,agreed
    if not agreed:
        print before[:num_tr_variables]
        print after[:num_tr_variables]

raw_exp_dicts = [{h:data for h,data in zip(header,transpose(experiment))} for experiment in experiment_lines]

toy_experimental_data = []
for red in raw_exp_dicts:
    # select treatment vars where at least one inhibitor or stimulus has been applied
    treatment_vars = {extract_treatment_variable(k):int("Stimuli" in k)
                      for (k,v) in red.items()
                      if k.startswith("TR:") and any(v) # consider only treatment vars where stim or inhib applied
                      and not "test" in k} # ignore cell line thing
    response_vars = {extract_response_variable(k):tuple(int(x>0.5) for x in v)
                     for k,v in red.items() if k.startswith("DV")}
    toy_experimental_data.append((treatment_vars,response_vars))

