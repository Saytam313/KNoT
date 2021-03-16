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

PRE_TRAINED_MODEL_NAME='DeepPavlov/bert-base-bg-cs-pl-ru-cased'
tokenizer = transformers.BertTokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME)
sample_txt='Pečivo, chleba čtyři rohlíky'

#tokens=tokenizer.tokenize(sample_txt)
tokens=nltk.word_tokenize(sample_txt,language="czech")
token_ids=tokenizer.convert_tokens_to_ids(tokens)


RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")



MAX_LEN = 200

class GPReviewDataset(Dataset):
	def __init__(self, reviews, targets, tokenizer, max_len):
		self.reviews = reviews
		self.targets = targets
		self.tokenizer = tokenizer
		self.max_len = max_len
	def __len__(self):
		return len(self.reviews)
	def __getitem__(self, item):
		review = str(self.reviews[item])
		target = self.targets[item]
		encoding = self.tokenizer.encode_plus(
			review,
			add_special_tokens=True,
			max_length=self.max_len,
			return_token_type_ids=False,
			padding='max_length',
			truncation=True,
			return_attention_mask=True,
			return_tensors='pt',
		)
		return {
			'review_text': review,
			'input_ids': encoding['input_ids'].flatten(),
			'attention_mask': encoding['attention_mask'].flatten(),
			'targets': torch.tensor(target, dtype=torch.long)
		}
df_train, df_test = train_test_split(
	df,
	test_size=0.1,
	random_state=RANDOM_SEED
)
df_val, df_test = train_test_split(
	df_test,
	test_size=0.5,
	random_state=RANDOM_SEED
)

def create_data_loader(df, tokenizer, max_len, batch_size):
	ds = GPReviewDataset(
		reviews=df.content.to_numpy(),
		targets=df.sentiment.to_numpy(),
		tokenizer=tokenizer,
		max_len=max_len
	)
	return DataLoader(
		ds,
		batch_size=batch_size,
		num_workers=4
	)
	
BATCH_SIZE = 16
train_data_loader = create_data_loader(df_train, tokenizer, MAX_LEN, BATCH_SIZE)
val_data_loader = create_data_loader(df_val, tokenizer, MAX_LEN, BATCH_SIZE)
test_data_loader = create_data_loader(df_test, tokenizer, MAX_LEN, BATCH_SIZE)

bert_model = BertModel.from_pretrained(PRE_TRAINED_MODEL_NAME)

data = next(iter(train_data_loader))

last_hidden_state, pooled_output = bert_model(
  input_ids=encoding['input_ids'],
  attention_mask=encoding['attention_mask']
)

class SentimentClassifier(nn.Module):
  def __init__(self, n_classes):
    super(SentimentClassifier, self).__init__()
    self.bert = BertModel.from_pretrained(PRE_TRAINED_MODEL_NAME)
    self.drop = nn.Dropout(p=0.3)
    self.out = nn.Linear(self.bert.config.hidden_size, n_classes)
  def forward(self, input_ids, attention_mask):
    _, pooled_output = self.bert(
      input_ids=input_ids,
      attention_mask=attention_mask
    )
    output = self.drop(pooled_output)
    return self.out(output

model = SentimentClassifier(len(class_names))
model = model.to(device)

input_ids = data['input_ids'].to(device)
attention_mask = data['attention_mask'].to(device)