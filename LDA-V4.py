# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 13:06:18 2016

@author: TFalcoff
"""

from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from gensim import corpora, models
import string, time, requests, bs4



class LDA:

    def __init__(self, url):
       
        page = requests.get(url)

        soup = bs4.BeautifulSoup(page, 'html.parser')
        
        text = soup.find_all('a')
        
        new_str = ''
        
        for char in text:
            
            if str(char) == char:
                if char in string.punctuation:
                    char = ''
                new_str += char.lower()
                    
        tokenizer = RegexpTokenizer(r'\w+')
        
        tokens = tokenizer.tokenize(new_str)
            
        en_stop = get_stop_words('en')
        
        p_stemmer = PorterStemmer()
        
        texts = []
    
        stopped_tokens = []
        [stopped_tokens.append(i) for i in tokens if i not in en_stop]
        
        stemmed_tokens = []
        [stemmed_tokens.append(p_stemmer.stem(i)) for i in stopped_tokens]
            
        texts.append(stemmed_tokens)
        
        self.texts = texts
        
        list_tops = []
        
        fin_text = []
        
        for text in texts:    
            
            for n in range(len(text)):
                    
                try:
                    
                    fin_text.append(text[n:n+10])
                        
                except IndexError: pass
        
        dictionary = corpora.Dictionary(fin_text)
                
        corpus = [dictionary.doc2bow(tn) for tn in fin_text]
                
        ldamodel = models.ldamodel.LdaModel(corpus, num_topics=10,
                                        iterations = 500, 
                                    id2word = dictionary, passes=100)
                            
        for topic in ldamodel.print_topics(num_topics = 10, num_words = 1):    
                                         
            num_words = 1    
            print('\n{}'.format(topic))
                                            
            str_out = '{}'.format(topic)
            
            split_topic = str_out.split("+")
                                
            for top in split_topic:
                if split_topic.index(top) < (num_words - 1):        
                    list_tops.append(top[(top.find("*")+1):].strip())
                else:
                    list_tops.append(top[(top.find("*")+1):-2])
                
        self.list_tops = list_tops
    

