import torch
import re
import nltk
import spacy
import unidecode
from nltk.stem import WordNetLemmatizer 
from corpy.morphodita import Tagger
import json
import database

class Class_analysis():
	def __init__(self,language):
		self.language = language
		self.FILE_PREFIX = "D:/Users/Šimon/Desktop/Github/KNoT/Bakalařka/sentiment_8"

		#loads model and pytorch fields
		#self.model = torch.load(self.FILE_PREFIX + "/bin/"+self.language+"/class_analyzer/class_model.pt",map_location=torch.device('cpu'))
		self.text = torch.load(self.FILE_PREFIX + "/bin/"+self.language+"/class_analyzer/text_field.pt",map_location=torch.device('cpu'))
		self.label = torch.load(self.FILE_PREFIX + "/bin/"+self.language+"/class_analyzer/label_field.pt",map_location=torch.device('cpu'))
		self.class_list = ["one_star","two_star","three_star","four_star","five_star"]


	def predict_class(self,review):
		self.model.eval()

		#tokenize the document into words
		tokenized = tokenizer(review,self.language)

		#preprocess the words
		if(self.language =="cz"):
			tokenized = text_preprocess_cz(tokenized)
		else:
			tokenized = text_preprocess(tokenized)

		#indexes the tokenized words using loaded pytorch field
		indexed = [self.text.vocab.stoi[t] for t in tokenized]
		length = [len(indexed)]
		tensor = torch.LongTensor(indexed)
		tensor = tensor.unsqueeze(1)
		length_tensor = torch.LongTensor(length)
		#makes a prediction using loaded model
		prediction = self.model(tensor, length_tensor)
		return prediction
		

x=Class_analysis('cz')