#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 00:45:52 2016

@author: tfalcoff
"""
from bs4 import BeautifulSoup
from networkx.readwrite import json_graph
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import requests, string


class WikiWeb:
    
    
    def __init__(self, url):
        
        self.url = url
        self.page = requests.get(self.url).text
        self.soup = BeautifulSoup(self.page, 'lxml')
                
    
    def links(self):
        
        #page title
        n_title = ''
        for char in self.soup.title:
            if char in string.punctuation:
                char = ' '
            n_title += char
        l_title = n_title.split(' ')
        l_title = l_title[:-2]            
        title = '_'.join(l_title)
        
        #wiki links    
        links=[]
        [links.append(link['href']) for link in self.soup.find_all('a', href=True)]
        n_links=[]
        for link in links:
            if link[:6] == '/wiki/' and ':' not in link:
                if 'Main_Page' not in link and link[6:] != title:
                    n_links.append(link)
        self.links = n_links
        
        return self.links
        
        
    def text(self):
        
        #page text (dirty)
        texts = self.soup.find_all(text=True)
        n_texts = []
        for line in texts:
            n_line = line.split(' ')
            [n_texts.append(word) for word in n_line]
        self.text = n_texts
        
        return self.text
        
        
    def crawl(self):
        
        dict_links = {}
        matrix = []

        #dictionary from self.list outputs
        n_links = WikiWeb(self.url).links()
        wiki = 'https://en.wikipedia.org'
        for link in n_links:
            if link not in dict_links:
                dict_links[link] = (WikiWeb(wiki+link).links())
                
        #matrix mapping connections
        for a_link in n_links:
            array = []
            for b_link in n_links:
                if b_link in dict_links[a_link]:
                    array.append(1)
                else: 
                    array.append(0)
                    
            matrix.append(array)
                
        self.crawl = matrix
        
        return self.crawl
        
    
    def network(self):
        
        #network vis connection
        self.G = nx.Graph()
        matrix = self.crawl()
        n_links = WikiWeb(self.url).links()
        for x in matrix:
            for y in x:
                if y == 1:
                    self.G.add_edge(n_links[matrix.index(x)], n_links[x.index(y)])
        
        return self.G
        
        
    def chord(self):
        
        n_G = WikiWeb(self.url).network()
        #data = json_graph.adjacency_data(n_G)
        
        plt.figure(figsize=(18,18))
        nx.draw_circular(n_G,node_color='g', edge_color='#909090', node_size=900)
        plt.axis('equal')
        
        
    #def matrix(self):
            
        
        
'''
To Do:
    1. get a crawler up and running
    2. create a relationship matrix for all of the pages the crawler spans
    3. visualize the matrix (make it worthwhile, i.e., cool and interactive)
'''                
        