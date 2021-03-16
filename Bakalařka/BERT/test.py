import transformers
from transformers import BertModel, BertTokenizer, AdamW, get_linear_schedule_with_warmup
import torch
import numpy as np
import pandas as pd
import seaborn as sns
from pylab import rcParams
import matplotlib.pyplot as plt
from matplotlib import rc
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
from collections import defaultdict
from textwrap import wrap
from torch import nn, optim
from torch.utils.data import Dataset, DataLoader
import nltk



f = open("trainingReviews.csv", "r",encoding='utf8')
#print(len(f.read().split('////')[0].split('====')[0].split('\n')))
posCnt=0
negCnt=0
revDict=dict()
revList=list()
sentiment=''
for x in f.read().split('////'):
	xList=x.split('====')
	if xList[-1].strip()=='pos':
		sentiment='pos'
		#posCnt+=len(xList[0].split('\n'))
	else:
		sentiment='neg'

	for y in xList[0].split('\n\n'):
		revDict[y.strip()]=sentiment
		revList.append({"text":y.strip(),"sentiment":sentiment})
#token_lens=[5,78,32,12,41,86,45,1,132,78,16,31,21,224,7,79]
#sns.distplot(token_lens)
#plt.xlim([0, 256]);
#plt.xlabel('Token count')
#print(revList[-1]["text"])
RANDOM_SEED=42
df_train, df_test = train_test_split(
	revList,
	test_size=0.1,
	random_state=RANDOM_SEED
)
df_val, df_test = train_test_split(
	df_test,
	test_size=0.5,
	random_state=RANDOM_SEED
)
print(len(revList))
print(len(df_val))
print('\n\n\n')
print(len(df_test))
print('\n\n\n')
print(len(df_train))
print('\n\n\n')