

# -*- coding: utf-8 -*-
#%%
import time

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

import pickle

from bs4 import BeautifulSoup


BASE_URL='https://apps.webofknowledge.com/full_record.do?product=UA&search_mode=GeneralSearch&qid=2&SID=4FBcNDiPfTzTN4xKSlv&page=1&doc='

all_records=[]

page_no=8801
max_page=9000

nono = 10742

tries=0
max_try=5

while page_no<=max_page:

    print ('Page No: %d' %(page_no))

    try:

        fname=urllib2.urlopen(BASE_URL+str(page_no))

        soup=BeautifulSoup(fname,"html.parser")

        tags_journal=soup.find_all("p",{"class":"sourceTitle"})

        tags_fields=soup.find_all("p",{"class":"FR_field"})

        tags_address=soup.find_all("td",{"class":"fr_address_row2"})

        record=dict()

        address=tags_address[0].get_text()

        record['journal']=str(tags_journal[0].find('value').get_text())

        record['address']=str(address.split('\n')[0])
        try:

            org_address=address.split('Organization-Enhanced Name(s)')[1]

            org_address=''.join([i for i in org_address if ord(i) < 128])
           
            record['organization']=str(org_address[1:-1].replace('\n',';'))
#
        except:
    
            record['organization']=''
    
    
        for tags_field in tags_fields:
            
            address1 = tags_field.find('p',{'class','FR_field'})
            
            
    
            field_name=str(tags_field.find('span',{'class','FR_label'}).get_text())
    
            if('By:' in field_name):
    
                value=str(tags_field.get_text())
    
                record['author']=value[value.find('(')+1:value.find(')')]
    
            if('Published:' in field_name):
    
                record['year']=int(tags_field.find('value').get_text()[-4:])
    
                break
    
        all_records.append(record)
    
        page_no+=1
        tries=0
    
    except:
        """
        tries+=1
        if(tries>max_try):
            page_no+=1
        print 'Exception...Trying again'
        """
        page_no = page_no+1            
        continue;
    
pickle.dump(all_records,open('sdata9','wb'))


