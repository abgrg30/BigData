"""
@file   : wos_scraper.py
@author : Group 2 SOCG
@a program to scrape web of science
"""


import time
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import pickle
from bs4 import BeautifulSoup

BASE_URL='https://apps.webofknowledge.com/full_record.do?product=UA&search_mode=GeneralSearch&qid=2&SID=4DtZvCrpVra5Dq3ViUd&page=1&doc='
all_records = []

page_no  = 10001
max_page = 10001
tries    = 1
max_try  = 5

while page_no <= max_page:
    print ('Page No: %d' %(page_no))
    
    try:
        tries=0
        fname = urllib2.urlopen(BASE_URL+str(page_no))
        soup  = BeautifulSoup(fname,"html.parser")
        tags_journal = soup.find_all("p",{"class":"sourceTitle"})
        tags_fields  = soup.find_all("p",{"class":"FR_field"})
        title_tag    = soup.find_all("div",class_="title");
        if title_tag:
            """
            val          = title_tag[0].find('value')
            if val:
                title = str(val.get_text())
            else:
                val = title_tag[0].find('nodes')
            
                title = str(val.get_text())
            """
            title = str(title_tag[0].get_text()).strip()            
        list_of_names_univs=[]
        for each in tags_fields:
            #f = each.find_all('a')
            #if f:
                #for all_names in f:
                    #list_of_names_univs.append(all_names.get_text())
            #else:
            print (each)
            f= each.find_all('Address')
        names     = []
        univ_map  = []
        univ_name = []
        univ = []
        for tg in tags_fields:
            a = tg.find('span',class_='FR_label')
            if a and 'Published' in a.get_text():
                try:
                    date = str(tg.find('value').get_text()).strip()
                except:
                    text = tg.get_text()
                    text = text.encode('ascii','ignore')
                    text = text.replace(':','')
                    text = text.replace("'","")
                    text = text.lstrip()        
                    date = text.replace("Published","")
                    date = date.lstrip()
                break;
        
        for i in range(len(list_of_names_univs)):
            items = str(list_of_names_univs[i])
            if items and items[0]=='[':
                univ_name.append(items[6:].strip())
            else:
                if items and items.isdigit():
                    if int(items)<7:
                        univ_map.append(int(items))
                elif items and '@' not in items and ':' not in items:
                    names.append(items)
        if len(univ_map)==0:
            uni_l = len(names)
            for each in tags_fields:
                text = each.get_text()
                if 'Address' in text:
                    u_address =  text.encode('ascii','ignore')
                    start_idx = u_address.rfind('Uni')
                    uni = u_address[start_idx-1:]
                    break;
            univ = [uni for ids in names]
        if len(univ_map)>0:        
            names = names[0:len(univ_name)]
            univ = univ_name
        record = dict()
        record['author'] = names;
        record['universities']  = univ;
        if title_tag:
            record['title']=title
        record['journal_type']=str(tags_journal[0].get_text()).strip()
        record['date'] = date
                
        page_no=page_no+1    
        all_records.append(record)            
    except:
        page_no = page_no+1            
        continue
    