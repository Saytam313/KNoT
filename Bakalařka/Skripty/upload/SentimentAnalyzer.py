import requests
import justext
import transformers
from transformers import BertModel, BertTokenizer, AdamW, get_linear_schedule_with_warmup
import torch
from torch import nn
class SentimentClassifier(nn.Module):
  def __init__(self, n_classes):
    super(SentimentClassifier, self).__init__()
    self.bert = BertModel.from_pretrained(PRE_TRAINED_MODEL_NAME)
    self.drop = nn.Dropout(p=0.3)
    self.out = nn.Linear(self.bert.config.hidden_size, n_classes)
  def forward(self, input_ids, attention_mask):
    _, pooled_output = self.bert(
      input_ids=input_ids,
      attention_mask=attention_mask,
      return_dict=False
    )
    output = self.drop(pooled_output)
    return self.out(output)


PRE_TRAINED_MODEL_NAME='/mnt/minerva1/nlp/projects/sentiment10/models/DeepPavlov_bert-base-bg-cs-pl-ru-cased'
tokenizer = transformers.BertTokenizer.from_pretrained(PRE_TRAINED_MODEL_NAME, return_dict=False)
device = torch.device("cpu")
class_names = ['neg','pos']
model = SentimentClassifier(len(class_names))
model.load_state_dict(torch.load('/mnt/minerva1/nlp/projects/sentiment10/models/best_model_state.bin'))
model = model.to(device)

#ze zadaneho URL vyhodnoti sentiment
def Sentiment_from_url(url):
	response = requests.get(url)
	try:
		f = justext.justext(response.content.decode(errors='replace'), justext.get_stoplist("Czech"))
	except:
		print(url)
	MAX_LEN = 200

	cnt = 0
	result = 0


	for y in f: #rozdeleni clanku na odstavce
		if (not y.is_boilerplate): 
			if(len(y.text)>70): #oddeleni nadpisu
				review_text=y.text
				encoded_review = tokenizer.encode_plus( 
					review_text,
					max_length=MAX_LEN,
					add_special_tokens=True,
					return_token_type_ids=False,
					padding='max_length',
					return_attention_mask=True,
					return_tensors='pt',
				)
				cnt+=1

				input_ids = encoded_review['input_ids'].to(device)
				attention_mask = encoded_review['attention_mask'].to(device)
				output = model(input_ids, attention_mask)
				_, prediction = torch.max(output, dim=1)
				if(prediction>0):
					result+=1
	#vypocet prumeru ze vsech odstavcu webu
	if(cnt>0):
		if((result/cnt)>0.5):
		    return('pos')
		else:
		    return('neg')
	else:
		return('??')
