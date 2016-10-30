# -*- coding: utf-8 -*-
"""
Created on Sat Jul 16 13:06:18 2016

@author: TFalcoff
"""

from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from gensim import corpora, models

import string

import time

def input_and_process():
    surv_name = input("survey name here (don't forget .txt): ")
    
    surv = (open(surv_name))
    
    r_surv = surv.read()
    
    text = str(r_surv)
    
    surv.close()
    
    new_str = ''
    
    for char in text:
            
        if char in string.punctuation:
            char = ''
        new_str += char.lower()
    
    tokenizer = RegexpTokenizer()
        
    tokens = tokenizer.tokenize(text)
 
    en_stop = get_stop_words('en')
    
    p_stemmer = PorterStemmer()
    
    texts = []

    stopped_tokens = []
    [stopped_tokens.append(i) for i in tokens if i not in en_stop]
    
    stemmed_tokens = []
    [stemmed_tokens.append(p_stemmer.stem(i)) for i in stopped_tokens]
        
    texts.append(stemmed_tokens)
        
    return texts

def run_LDA(texts):
    
    list_topics = []
    
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
                list_topics.append(top[(top.find("*")+1):].strip())
            else:
                list_topics.append(top[(top.find("*")+1):-2])
            
    return list_topics
    
def hist_tops(list_tops):
    
    hist_tops = []
    for top in list_tops:
        top_count = list_tops.count(top)
        fin_top = (top_count, top)
        
        if fin_top in hist_tops:
            continue
       
        else:            
            hist_tops.append(fin_top)
    
    for fin_top in sorted(hist_tops):
        print(fin_top)
    
    return hist_tops
        
def prox_tops(list_tops,texts):
    
    prox_list = []
    dupless_tops = []
    for top in list_tops:
        form_top = top.strip()
        if form_top not in dupless_tops:
            dupless_tops.append(form_top)
    
    for res in texts:
        res_tops = []
        for top in dupless_tops:
            if top in res:
                top_tup = (res.index(top),top)
                res_tops.append(top_tup)
        sort_tops = sorted(res_tops)
        for top_dex in sort_tops:
            prox_list.append(top_dex[1])
                    
        prox_list.append("end_res")
        
    prox_str = " ".join(prox_list)
    prox = prox_str.split("end_res")
    
    fin_prox = []
    for fin in prox:
        fin_count = prox.count(fin)
        fin_top = (fin_count,fin)
        if fin_top in fin_prox or fin == '' or fin == ' ':
            continue
        else:
            fin_prox.append(fin_top)
    sort_fin = sorted(fin_prox)
    
    for fin in sort_fin[::-1]:
        print(fin)
        
def vis_hist(hist_tops):
    
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    fig.canvas.draw()
    labels = [item.get_text() for item in ax.get_xticklabels()]
    tops = []
    [tops.append(top[1]) for top in hist_tops]
    labels = tops
    ax.set_xticklabels(labels)
    plt.title('Buzzwords')
    counts = []
    for count in hist_tops:
        for n in range(count[0]):
            counts.append(hist_tops.index(count))
    plt.hist(counts, bins = len(hist_tops))
    
                       
def main():
    t0 = time.time()
    texts = input_and_process()
    run_LDA(texts)
    t1 = time.time()
    print('\n{} minutes wall time'.format(round((t1-t0)/60),4))
main()
    