# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 19:39:03 2016

@author: Abhinav
"""

# -*- coding: utf-8 -*-

#%%
import time

import urllib.request as urllib2

import pickle

from bs4 import BeautifulSoup
import re

BASE_URL='https://apps.webofknowledge.com/full_record.do?product=UA&search_mode=GeneralSearch&qid=2505&SID=4DjnbB9QA6LJkyGLgPl&page=1&doc='

all_records=[]

page_no=1

max_page=1500
tries=0
max_try=5

while page_no<=max_page:

    print('Page No: %d'%(page_no))

    try:
        fname = urllib2.urlopen(BASE_URL + str(page_no))
        soup = BeautifulSoup(fname,"html.parser")
    except:
        page_no += 1 
        continue
    
    tags_journal=soup.find_all("p",{"class":"sourceTitle"})

    tags_fields=soup.find_all("p",{"class":"FR_field"})

    tags_address=soup.find_all("td",{"class":"fr_address_row2"})

    record=dict()
    
    record['journal']=str(tags_journal[0].find('value').get_text())

    if len(tags_address):
        address=tags_address[0].get_text()
        record['address']=str(address.split('\n')[0])
    else:
        record['address'] = 'unknown'

    add_list=[]
    
    for tag_a in tags_address:
        try:
            add = tag_a.get_text()
            br_idx = add.find(']')
            tmp_add = (add[br_idx+1:].strip())
            
            org_address=tmp_add.split('Organization-Enhanced Name(s)')[1:]
            ##print('code reached refinement')
            refined_add = re.sub(r'[^\x00-\x7f]',r' ',org_address[0]).strip()
            refined_list = re.sub(r'[\n\t'  ']+',r'',refined_add).split('  ')
            refined_orgs = ""
            for el in refined_list:
                refined_orgs=refined_orgs+el
                if not el=='':
                    refined_orgs=refined_orgs+','
                    
            add_list.append(refined_orgs[:-1])
        
        except:
              continue  
        record['organization']=add_list;            
            
            
#        
        
    for tags_field in tags_fields:
        
        address1 = tags_field.find('p',{'class','FR_field'})
        acc_no = tags_field.find('span',{'class','FR_label'})        
        
        field_name = tags_field.find('span',{'class','FR_label'})
        
        if field_name:

            field_name=str(field_name.get_text())
            

            if('By:' in field_name):
                record['author']=[]
                value=str(tags_field.get_text())
                
                new_val = value
                while 1:
                    author_st = new_val.find('(')
                    author_en = new_val.find(')')
                    if author_st==-1 or author_en==-1:
                        break
                    temp_author = new_val[author_st+1:author_en].strip()
                    record['author'].append(temp_author)
                    new_val = new_val[author_en+1:]
                
                
                #record['author']=value[value.find('(')+1:value.find(')')]
                #break;    
            if('Published:' in field_name):
                value = tags_field.find('value')
                
                if value:
                    record['year']=int(value.get_text()[-4:])
    
            if('DOI:' in field_name):
                ##print('found')
                value = tags_field.find('value')
                
                if value:
                    value = str(tags_field.find('value').get_text())
                    record['DOI']=value
                
            if('Accession Number:' in field_name):
                print('found')
                value = tags_field.find('value')
                
                if value:
                    value = str(value.get_text())
                    record['ID']=value[4:]                
                
    ##print('code reached here')        
    all_records.append(record)

    page_no+=1
    tries=0
    

    #%%

pickle.dump(all_records,open('naya','wb'))