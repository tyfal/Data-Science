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
import plotly.plotly as py
from plotly.graph_objs import *
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
        links = n_links
        
        return links
        
        
    def text(self):
        
        #page text (dirty)
        texts = self.soup.find_all(text=True)
        n_texts = []
        for line in texts:
            n_line = line.split(' ')
            [n_texts.append(word) for word in n_line]
        text = n_texts
        
        return text
        
        
    def network(self):
        
        dict_links = {}
        matrix = []

        #dictionary from self.list outputs
        links = WikiWeb(self.url).links()
        wiki = 'https://en.wikipedia.org'
        for link in links:
            if link not in dict_links:
                dict_links[link] = (WikiWeb(wiki+link).links())
                
        #matrix mapping connections
        for a_link in links:
            array = []
            for b_link in links:
                if b_link in dict_links[a_link]:
                    array.append(1)
                else: 
                    array.append(0)
                    
            matrix.append(array)
                

        #from https://plot.ly/ipython-notebooks/networks/

        def scatter_edges(G, pos, line_color=None, line_width=1):
            trace = Scatter(x=[], y=[], mode='lines')
            for edge in G.edges():
                trace['x'] += [pos[edge[0]][0],pos[edge[1]][0], None]
                trace['y'] += [pos[edge[0]][1],pos[edge[1]][1], None]  
                trace['hoverinfo']='none'
                trace['line']['width']=line_width
                if line_color is not None: # when it is None a default Plotly color is used
                    trace['line']['color']=line_color
            return trace            
        
        def scatter_nodes(pos, labels=None, color=None, size=20, opacity=1):
            # pos is the dict of node positions
            # labels is a list  of labels of len(pos), to be displayed when hovering the mouse over the nodes
            # color is the color for nodes. When it is set as None the Plotly default color is used
            # size is the size of the dots representing the nodes
            #opacity is a value between [0,1] defining the node color opacity
            L=len(pos)
            trace = Scatter(x=[], y=[],  mode='markers', marker=Marker(size=[]))
            for k in range(L):
                trace['x'].append(pos[k][0])
                trace['y'].append(pos[k][1])
            attrib=dict(name='', text=labels , hoverinfo='text', opacity=opacity) # a dict of Plotly node attributes
            trace=dict(trace, **attrib)# concatenate the dict trace and attrib
            trace['marker']['size']=size
            return trace   
        
        width=500
        height=500
        axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
                  zeroline=False,
                  showgrid=False,
                  showticklabels=False,
                  title='' 
                  )
        layout=Layout(title= 'Fruchterman Reingold  layout',  #
            font= Font(),
            showlegend=False,
            autosize=False,
            width=width,
            height=height,
            xaxis=XAxis(axis),
            yaxis=YAxis(axis),
            margin=Margin(
                l=40,
                r=40,
                b=85,
                t=100,
                pad=0,
               
            ),
            hovermode='closest',
            plot_bgcolor='#EFECEA', #set background color            
            )
        
        def make_annotations(pos, text, font_size=14, font_color='rgb(25,25,25)'):
            L=len(pos)
            if len(text)!=L:
                raise ValueError('The lists pos and text must have the same len')
            annotations = Annotations()
            for k in range(L):
                annotations.append(
                    Annotation(
                        text=text[k], 
                        x=pos[k][0], y=pos[k][1],
                        xref='x1', yref='y1',
                        font=dict(color= font_color, size=font_size),
                        showarrow=False)
                )
            return annotations  
            
        
        np_trix = np.array(matrix)
        Gr = nx.from_numpy_matrix(np_trix)
        pos = nx.spring_layout(Gr)
        labels = links
        traceE=scatter_edges(Gr, pos)
        traceN=scatter_nodes(pos, labels=labels)
        
        layout.update(title='Wiki Network: '+self.url)
        data1=Data([traceE, traceN])
        fig = Figure(data=data1, layout=layout)
        fig['layout'].update(annotations=make_annotations(pos, [str(k) for k in range(len(pos))]))  
        py.iplot(fig, filename='wiki-network')
        
        
'''
To Do:
    1. get a crawler up and running
    2. create a relationship matrix for all of the pages the crawler spans
    3. visualize the matrix (make it worthwhile, i.e., cool and interactive)
'''                
        