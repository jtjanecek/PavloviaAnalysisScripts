import pandas as pd
import numpy as np
import os
import glob

input_folder = 'EmoPS'
datafiles = glob.glob(os.path.join(input_folder, '*.csv'))

def analyze(logfile):
	stats = {'id': logfile.split("_EmoPS")[0]}
	df = pd.read_csv(logfile)
	test_trials = df.dropna(subset=['TestTrial'])
	test_trials = test_trials[['Condition', 'test_resp.keys', 'test_resp.rt']]

	for condition in set(test_trials['Condition'].values):
		corr_resp = 'f' if 'Targ' in condition else 'j'
		cond_mask = test_trials['Condition'] == condition
		j_mask = test_trials['test_resp.keys'] == 'j'
		f_mask = test_trials['test_resp.keys'] == 'f'
		this_condition = test_trials[(cond_mask) & (j_mask | f_mask)]
		stats['{}_CorrRate'.format(condition)] = sum(this_condition['test_resp.keys'] == corr_resp) / len(this_condition)
	return stats

all_stats = []
for datafile in datafiles:
	stats = analyze(datafile)
	all_stats.append(stats)

df = pd.DataFrame(all_stats)
df.to_csv('results.csv')
