import pandas as pd
import numpy as np

def calc_stats(input_filename, output_filename, gold_label, ann_label):
	df = pd.read_csv(input_filename, index_col=0, header=0)
	results_cols = ['label', 'p', 'n', 'tp', 'tn', 'fp', 'fn', 'accuracy', 'precision', 'recall', 'specificity', 'f1']
	results_list = []

	total = df[gold_label].shape[0]

	tp = df[(df[gold_label] == 1) & (df[ann_label] == 1)].shape[0]
	tn = df[(df[gold_label] == 0) & (df[ann_label] == 0)].shape[0]
	fp = df[(df[gold_label] == 0) & (df[ann_label] == 1)].shape[0]
	fn = df[(df[gold_label] == 1) & (df[ann_label] == 0)].shape[0]

	if tp+fp == 0:
		precision = np.nan
	else:
		precision = float(tp)/float(tp + fp)
	if tp+fn == 0:
		recall = np.nan
	else:
		recall = float(tp)/float(tp + fn)

	if tn+fp == 0:
		specificity = 0
	else:
		specificity = float(tn)/float(tn+fp)
	accuracy = float(tp + tn)/float(total)
	f1 = 2*(precision*recall)/(precision + recall)
	results_list.append({'label':gold_label, 'p':tp+fn,'n':tn+fp, 'tp':tp, 'tn':tn, 'fp':fp, 'fn':fn, 'accuracy':accuracy, 'precision':precision, 'recall':recall, 'specificity': specificity, 'f1':f1})
	
	results_df = pd.DataFrame(results_list)
	results_df = results_df[results_cols]
	results_df.to_csv(output_filename)

import matplotlib.pyplot as plt


# x = ['Patient care preferences','Goals of care conversations', 'Code status limitations', 'Communication with family', 'Full code status']

# y = (76.0, 37.2, 94.3, 43.6, 90.9)
# z=(92.0, 85.7, 95.9, 90.7, 98.5)

# n_groups = 5

# fig, ax = plt.subplots()

# index = np.arange(n_groups)
# bar_width = 0.25
# rects1 = ax.bar(index, y, bar_width,
#                  color='b', 
#                 label='Regular Expression')
# rects2 = ax.bar(index + bar_width, z, bar_width,
#                  color='oran',    
#                 label='Neural Network')

# ax.set_xlabel('Domain')
# ax.set_ylabel('F1-score')
# ax.set_title('F1-score comparison by domain')
# ax.set_xticks(index + bar_width / 2)
# ax.set_xticklabels(('Patient care preferences','Goals of care conversations', 'Code status limitations', 'Communication with family', 'Full code status'), rotation=15)
# ax.legend()

# fig.tight_layout()
# plt.show()

notes = [64,128,192,256,320,384,448,512]
accuracy = [83.6, 85.9,93.0,91.4, 96.1, 89.8,92.2, 93.0]
ppv = [74.3, 78.5, 91.1, 84.4, 94.6, 81.8, 86.9, 85.0]
specificity = [0.753424658,0.808219178,0.931506849,0.863013699,
0.95890411,
0.835616438,
0.890410959,
0.876712329]
sp = [x*100 for x in specificity]
sensitivity = [0.945454545,
0.927272727,
0.927272727,
0.981818182,
0.963636364,
0.981818182,
0.963636364,
1]
sn = [x*100 for x in sensitivity]
f1 = [0.832,
0.85,
0.918918919,
0.907563025,
0.954954955,
0.892561983,
0.913793103,
0.924369748]
f = [x*100 for x in f1]

plt.plot(notes, accuracy, '.b-', label='accuracy')
plt.plot(notes, ppv, '.r-', label='positive predictive value')
plt.plot(notes, f, '.g-', label='f1-score')
plt.plot(notes, sn, '.m-', label='sensitivity')
plt.plot(notes, sp, '.y-', label='specificity')
plt.xlabel('Performance (%)')
plt.ylabel('Number of Training Notes')
plt.title('Learning Curve')
plt.legend()
plt.show()
