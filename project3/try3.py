# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 13:50:27 2016
@author: abhijit
"""

import urllib.request as urllib2
import pickle
import os
os.chdir('F:\\UCSD\\socg\\3')

from bs4 import BeautifulSoup
import re

list_of_pubs = []
dict_pub = dict()
    
for i in range(5):

    soup = BeautifulSoup(open('savedrecs('+str(i+1)+').html'),'html.parser')
    
    tr_tags = soup.findAll('tr')
    td_tags = soup.findAll('td')
    
    max_iter = len(tr_tags)
    
    for i in range(max_iter):
        tr_current = tr_tags[i].get_text()
        td_1 = td_tags[2*i+0].get_text().strip()
        if(td_1=='PT'):
            dict_pub=dict()
        elif (td_1=='AU'):
            list_of_authors = tr_current.strip()[3:].split('\n')
            stripped_list_of_authors = [el.strip() for el in list_of_authors]
            dict_pub['author'] = stripped_list_of_authors
        elif (td_1=='TI'):
            dict_pub['title'] = tr_current.strip()[3:]
        elif (td_1=='SO'):
            dict_pub['tag'] = tr_current.strip()[3:]
        elif (td_1=='VL'):
            dict_pub['volume'] = tr_current.strip()
        elif(td_1=='IS') or (td_1=='SI') or td_1=='BP' or td_1=='EP':
            continue
        elif(td_1=='PD'):
            dict_pub['Date'] = tr_current.strip()[3:]
        elif(td_1=='PY'):
            dict_pub['year'] = tr_current.strip()[3:]
        elif(td_1=='AB'):
            dict_pub['abstract'] = tr_current.strip()
        elif(td_1=='DI'):
            dict_pub['doc_id'] = tr_current.strip()[3:]
        elif(td_1=='ER'):
            list_of_pubs.append(dict_pub)    
        elif(td_1=='UT'):
            dict_pub['accession_num']=tr_current.strip()[3:]
        else:
            continue
        
#%%

pickle.dump(list_of_pubs, open('HTMLscraped.txt', 'wb'))

#%%
import pickle
amit = pickle.load(open('newscrape', 'rb'))

#%%
final = []

for i in range(len(rec)):
    if 'accession_num' in rec[i]:
        if 'ID' in amit[i]:
            if amit[i]['ID'] == rec[i]['accession_num'][4:]:
                final.append(rec[i])
                
                if 'organization' in amit[i]:
                    final[i]['organization'] = amit[i]['organization']
                else:
                    final[i]['organization'] = 'unknown'
                    
#%%
                    
pickle.dump(final, open('combined.txt', 'wb'))

#%%
import pickle
import re
amit = pickle.load(open('newscrape', 'rb'))

f = open('uni.txt', 'r')
uni = []
var = f.readline()

while var:
    uni.append(var)
    var = f.readline()
    
f.close()

f = open('tier.txt', 'r')
tier = []
var = f.readline()

while var:
    tier.append(var)
    var = f.readline()
    
f.close()

count = 0
f = open('savedrecs.txt', 'r')
g = open('uniadded.isi', 'w')

var = f.readline()

while var:
    g.write(var)
    
    if var.count('WOS'):
        t = []
        g.write('UN ')
        if 'organization' in amit[count]:
            for i in amit[count]['organization']:
                g.write(i)
                g.write(', ')
                               
                flag = True
                
                for j in uni:
                    if re.match(i, j):
                        flag = False
                        t.append(tier[uni.index(j)].split('\n')[0])
                        break
                    
                if flag:
                    t.append('R3')
        else:
            g.write('unknown')
            t.append('R3')
            
        g.write('\n')
        g.write('TR ')
        
        for j in t:                 
            g.write(j + ', ')        
        g.write('\n')
        
        count += 1
    
    var = f.readline()

f.close()
g.close()

#%%
count = 0

for k in range(5):
    f = open('savedrecs('+str(k+1)+').html', 'r')
    g = open('html'+str(k+1)+'.html', 'w')
    
    var = f.readline()
    
    while var:
        g.write(var)
        
        if var.count('WOS'):
            g.write('</tr>\n\n')
            g.write('<tr>\n<td valign="top">UN </td><td>')
            for i in final[count]['organization']:
                g.write(i)
                g.write(', ')
            g.write('</td>\n')
            count += 1    
        
        var = f.readline()
    
    f.close()
    g.close()
    
#%%
    
count = 0

for k in range(5):
    f = open('savedrecs('+str(k+1)+').html', 'r')
    g = open('html'+str(k+1)+'.html', 'w')
    
    var = f.readline()
    
    while var:
        g.write(var)
        
        if var.count('WOS:'):
            g.write('UN ')
            for i in final[count]['organization']:
                g.write(i)
                g.write(', ')
            g.write('\n')
            count += 1    
        
        var = f.readline()
    
    f.close()
    g.close()
    
#%%
f = open('uni.txt', 'r')
uni = []
var = f.readline()

while var:
    uni.append(var)
    var = f.readline()
    
f.close()

f = open('tier.txt', 'r')
tier = []
var = f.readline()

while var:
    tier.append(var)
    var = f.readline()
    
f.close()

#%%

import re

f = open('final_uni_added.isi', 'r')
g = open('abhinav.isi', 'w')

univ = []
var = f.readline()

while var:
    g.write(var)
    
    if var[:3] == ('UN '):
        
        l = var[3:].split(', ')
        ll = []
        for k in l:
            ll += k.split(',')
        l = ll
        
        if l[-1] == '\n':
            l.pop(-1)
        if '\n' in l[-1]:
            l.append(l.pop(-1).split('\n')[0])
        
        univ.append(l)
        vote = []
        
        for i in l:
                       
            if 'unknown' in i:
                vote.append('R4')
            else:
                flag = True
                
                for j in uni:
                    ll = j.split(',')
                    
                    for k in ll:
                        if re.match(i, k):
                            flag = False
                            vote.append(tier[uni.index(j)].split('\n')[0])
                            break
                        
                    if flag == False:
                        break
                    
                if flag:
                    vote.append('R3')
    
        g.write('TR ')        
        for j in vote:                 
            g.write(j + ', ')        
        g.write('\n')
        
    var = f.readline()
        
f.close()
g.close()

#%%
import pickle
pickle.dump(uni, open('univ', 'wb'))

#%%

import functools
l = lambda x,y : x if (x>y) else y
y = reduce(lambda x,y : x if (x>y) else y, [2,3,4,6,5,7,3,1,0])
        
        