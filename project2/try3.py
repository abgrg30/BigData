# -*- coding: utf-8 -*-
"""
Created on Fri Feb 19 21:06:59 2016

@author: abhijit
"""

"""
This file is to preprocess the data gathered from web of science
We will have to make a sequence of all the universities associated with a researcher
"""
import pickle
from optimalMatching import  OptimalMatching
import os
os.chdir('F:\\UCSD\\socg')

file_ptr = open('wos_data','rb')
records  = pickle.load(file_ptr)
file_ptr.close()

file_ptr = open('abhinav','rb')
records  = records + pickle.load(file_ptr)
file_ptr.close()

file_ptr = open('amit','rb')
records  = records + pickle.load(file_ptr)
file_ptr.close()

dict_author_univ = dict()
authors = []
for each_record in records:
    author = each_record['author']
    authors.append(author)

set_of_authors = set(authors)
# To Remove Duplicates from all the set
authors = list(set_of_authors)

corresponding_journals = [[] for z in authors]


jtag_list = []

corresponding_univs = [[] for z in authors] # A list of list to store all univeristies a author has worked at
for each_record in records:
    author = each_record['author']
    ## Now a loop for each  

    author_idx = authors.index(author)
    varsity = each_record['organization']
    if varsity=='':
        varsity = 'unknown'
        if corresponding_univs[author_idx]:
            varsity=corresponding_univs[author_idx][-1]
    jtag = each_record['journal']
    jtag_list.append(jtag)
    corresponding_univs[author_idx].append(varsity.strip())
    corresponding_journals[author_idx].append(jtag.strip())

idx = []
multiple_univs = []

#%% Filtering out unuseful parameters

useful_data_list = []


for j in range(len(corresponding_univs)):
    if len(corresponding_journals[j])>1:
        idx.append(j)
        useful_data = dict()
        useful_data['organization'] = corresponding_univs[j] 
        useful_data['author'] = records[j]['author']
        useful_data['journal'] = corresponding_journals[j]
        useful_data_list.append(useful_data)        
        for each in corresponding_univs[j]:
            multiple_univs.append(each)

#%%
def read_tags_from_file(file_name):
    s = []    
    with open(file_name,'r') as f:
        for each_line in f:
            last_space = each_line.rfind("=")
            tag = each_line[:last_space]
            s.append(tag.upper())
    return s
    
    



#%% Filtering out universities where one is unknown
sociology_tags = sociology_tags = read_tags_from_file("tags_filtered_refined.txt")

#%%
filtered_rec = []
for each_record in useful_data_list:
    tags_of_journal = each_record['journal']
    c = 0
    for tag in tags_of_journal:
        if tag in sociology_tags:
            c=c+1
    if(c>=2):
        filtered_rec.append(each_record)
    

#%%
"""
more_than_three_rec = []
for each_record in useful_data_list:
    tags_of_journal = each_record['journal']
    c = 0
    for tag in tags_of_journal:
        if tag in sociology_tags:
            c=c+1
    if(c>=3):
        more_than_three_rec.append(each_record)
"""
            
#%%

journal_ids = [[] for all in filtered_rec]
non_soc_tag = len(sociology_tags)
for i,item in enumerate(filtered_rec):
    list_of_journals = item['journal']
    journal_ids[i] = [sociology_tags.index(x) if x in sociology_tags else non_soc_tag for x in list_of_journals]
    
    
#%% Now Let's do sequence analysis
#all_unique_addresses = []
#f = open('univ_text','r')
#for each in f:
#    all_unique_addresses.append(each.strip())
#f.close()    
#%%


    
#%% Take Rankings from Txt file
import numpy as np
ranking = np.genfromtxt('tag_tier.txt',delimiter='\n')
rank_list = list(ranking)

regions = np.genfromtxt('regions.txt',delimiter='\n')
region_list = list(regions)

#%% Now Assign sequence Id's to all

seq_tier = [[] for all in filtered_rec]
for i,all in enumerate(journal_ids):
    seq_tier[i] = [rank_list[x] for x in all]
    
#%% Now Compute A MxM Matrix calculating sequence distance between sequences
len_seqs  = len(seq_tier)
rank_dist = np.zeros((len_seqs,len_seqs))
for i in range(len_seqs):
    for j in range(len_seqs):
        rank_dist[i][j] = OptimalMatching(seq_tier[i],seq_tier[j])
    
    
#%%
import numpy as np
import random as rnd

distance = rank_dist
k = 4

num_samples =  np.shape(distance)[0]
samples = np.array(rnd.sample(range(num_samples),k))

old_medoid = np.zeros(k)
new_medoid = np.zeros(k)    
curr_medoid = np.array(samples)

new_labels = np.zeros(num_samples)

max_itrs = 100
itr = 0;
"""while not (np.array_equal(old_medoid,curr_medoid)):"""
while itr<max_itrs:
    cluster = [[] for x in range(k)]
# Compute the Cluster to be Assigned to  the point
    for i in range(num_samples):
        dist_from_medoid = distance[i][samples]
        min_dist_idx = np.argmin(dist_from_medoid)
        label = samples[min_dist_idx]
        new_labels[i] = label
        cluster[min_dist_idx].append(i)
        
# Calculate Groups of each of the cluster
    for w in range(len(samples)):
        curr_cluster = cluster[w]
        d = np.zeros((len(curr_cluster)))
        for i in range(len(curr_cluster)):
            d[i] = np.sum(distance[curr_cluster[i],curr_cluster])
        medoid_idx = np.argmin(d)
        new_medoid[w] = curr_cluster[medoid_idx]

    old_medoid[:] = curr_medoid[:]   
    curr_medoid[:] = new_medoid[:] 
    samples = list(new_medoid)    
    itr = itr+1
    
#%%
final = []

for idx,i in enumerate(filtered_rec):        
    if int(new_labels[idx])==4:
        s = filtered_rec[idx]
        s['tier'] = 'Tier1'
        final.append(s)
        
for idx,i in enumerate(filtered_rec):         
    if int(new_labels[idx])==1:
        s = filtered_rec[idx]
        s['tier'] = 'Tier2'
        final.append(s)
        
for idx,i in enumerate(filtered_rec):        
    if int(new_labels[idx])==0:
        s = filtered_rec[idx]
        s['tier'] = 'Tier3'
        final.append(s)
        
for idx,i in enumerate(filtered_rec):
    if int(new_labels[idx])==8:
        s = filtered_rec[idx]
        s['tier'] = 'Tier4'
        final.append(s)      

#%%
import xlwt


book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")

x = 0



for idx,i in enumerate(final):
    y = 0
    x+=1
    
    sheet1.write(x, y, i['author'])
    y+=1
    xx = x
    
    for j in i['journal']:
        sheet1.write(x, y, str(j))
        x+=1
    y+=1
    
    x = xx
    for j in i['organization']:
        sheet1.write(x, y, str(j))
        x+=1
    y+=1
    
    x = xx
    for j in seq_tier[filtered_rec.index(i)]:
        sheet1.write(x, y, str(j))
        x+=1
    y+=1
    

    sheet1.write(xx, y, i['tier'])

        
    y+=1
    
    
book.save("Listnow.xls")        
    
    
    
#%%
f = open('jtag_list','w')
for each in jtag_list:
    f.write(each+'\n')


          