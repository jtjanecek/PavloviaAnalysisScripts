import pandas as pd
import numpy as np
import os
import glob

'''
Analysis script for MDTT
'''

input_folder = 'MDTT'
datafiles = glob.glob(os.path.join(input_folder, '*.csv'))

def analyze(logfile):
	stats = {'id': logfile}
	df = pd.read_csv(logfile)
	test_trials = df.dropna(subset=['Right_Image'])
	test_trials = test_trials[['Condition', 'test_resp.keys', 'test_resp.rt', 'LeftIdx', 'RightIdx']]

	condition_map = {0: 'Far', 1: 'Adjacent', 7: 'Short', 8: 'Short', 9:'Short',
					15: 'Middle', 16: 'Middle', 17: 'Middle'}
	test_trials['Condition'] = test_trials['Condition'].map(condition_map)
	print(test_trials)
	def get_corr_resp(row):
		if row['LeftIdx'] < row['RightIdx']:
			return 'f'
		elif row['RightIdx'] < row['LeftIdx']:
			return 'j'
		raise Exception
	test_trials['Corr_resp'] = test_trials.apply(get_corr_resp, axis=1)
	print(test_trials)

	for condition in set(test_trials['Condition'].values):
		cond_mask = test_trials['Condition'] == condition
		j_mask = test_trials['test_resp.keys'] == 'j'
		f_mask = test_trials['test_resp.keys'] == 'f'
		this_condition = test_trials[(cond_mask) & (j_mask | f_mask)]
		print(this_condition)
		stats['{}_CorrRate'.format(condition)] = sum(this_condition['test_resp.keys'] == this_condition['Corr_resp']) / len(this_condition)
	return stats

all_stats = []
for datafile in datafiles:
	stats = analyze(datafile)
	all_stats.append(stats)

df = pd.DataFrame(all_stats)
df.to_csv('results.csv')
