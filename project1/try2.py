# -*- coding: utf-8 -*-

try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import pickle
try:
    from sets import Set
except ImportError:
    Set = set
import numpy as np
import lda
from bs4 import BeautifulSoup


##BASE_URL='http://www.amazon.com/Powerbeats-Wireless-In-Ear-Headphone-Black/product-reviews/B00IYA2ZJW/ref=cm_cr_pr_btm_link_2?ie=UTF8&showViewpoints=1&sortBy=recent&pageNumber='
BASE_URL='http://www.amazon.com/Bose-QuietComfort-Acoustic-Cancelling-Headphones/product-reviews/B00M1NEUKK/ref=cm_cr_dp_see_all_summary?ie=UTF8&showViewpoints=1&sortBy=recent&pageNumber='
all_reviews=[]
page_no=1
total_reviews=-1
max_page=100

#%%
while total_reviews!=0 and page_no<=max_page:
    print ('Page No: %d' %(page_no))
    try:
        fname=urllib2.urlopen(BASE_URL+str(page_no))
        soup=BeautifulSoup(fname,"html.parser")
        tags_rvw_sec=soup.find_all("div",{"class":"a-section review"})
        total_reviews=len(tags_rvw_sec)
        for sections in tags_rvw_sec:
            tags_review=sections.find("span",{"class":"a-size-base review-text"})
            tags_rating=sections.find("span",{"class":"a-icon-alt"})
            tags_user=sections.find("span",{"class":"a-size-base a-color-secondary review-byline"})
            tags_date=sections.find("span",{"class":"a-size-base a-color-secondary review-date"})
            tags_valid_purchase = sections.find("span",{"class":"a-size-mini a-color-state a-text-bold"})



            review=dict()
            review['rating']=float(tags_rating.get_text()[:3])
            review['user']=tags_user.find('a').get_text()
            review['review']=tags_review.get_text()
            review['date']=tags_date.get_text()[3:]
            """
            if tags_valid_purchase != None:
                review['valid_purchase'] = tags_valid_purchase.get_text()
            else:
                review['valid_purchase'] = "Not Valid Purchase"

            """
            try:
                review['valid_purchase'] = tags_valid_purchase.get_text()
            except:
                print ("Not a valid Purchase")
                review['valid_purchase'] = 'Not Valid Purchase'



            for tag in sections.find_all('a'):
                if('review-title' in tag['class']):
                    review['title']=tag.get_text()
                    break
            for tag in sections.find_all('a'):
                if('review-title' in tag['class']):
                    review['title']=tag.get_text()
                    break

            all_reviews.append(review)
        page_no+=1
    except:
        print ('Exception...Trying again')

pickle.dump(all_reviews,open('amazon_data','wb'))


"""
To Create a list of all reviews
"""
num_of_reviews = len(all_reviews)

review_set = []
tokens = []
for each in all_reviews:
    review_str = each['review']
    review_set.append(review_str)





#%%
from nltk.tokenize import RegexpTokenizer
# To remove stop words
from stop_words import get_stop_words

from nltk.stem.porter import PorterStemmer
#tokenizer = RegexpTokenizer(r'\w+')
tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')

texts = []
# To get the stop words like you're,can.myself,itself,i etc
en_stop = get_stop_words('en')


# Remove stemmings from stopped tokems
p_stemmer = PorterStemmer()

# Tokenizing each review and removing stop words
for each in review_set:

    lower_case_review = each.lower()
    tokens = tokenizer.tokenize(lower_case_review)

    stopped_tokens = [i for i in tokens if not i in en_stop]

    texts = texts + (stopped_tokens)

tokenized_words_set = Set(texts)



capital_letters_count = np.zeros((num_of_reviews),np.int)
special_letters_count = np.zeros((num_of_reviews),np.int)





num_of_tokens = len(tokenized_words_set)

tokens = list(tokenized_words_set)

dict_tokens = {tokens[i].lower():i for i in range(num_of_tokens)}

review_to_word_map = np.zeros((num_of_reviews,num_of_tokens),np.int)



for i in range(len(review_set)):
    sentence      = review_set[i]
    #if "!" in sentence or "?" in sentence or "'"  or "$"in sentence:
    # calculates the number of special_letters and capital letters in reviews

    for each_char in sentence:
        if  not each_char.isalpha() or each_char.isdigit():
            special_letters_count[i]=special_letters_count[i]+1
        if not each_char.lower() == each_char:
            capital_letters_count[i]=capital_letters_count[i]+1

    list_of_str = tokenizer.tokenize(sentence)
    for each in list_of_str:
        if each.lower() in dict_tokens:
            #print each
            word_idx = dict_tokens[each.lower()]
            # calculating the number of times each word of the entire vocabulary occurs in a review
            review_to_word_map[i][word_idx] = review_to_word_map[i][word_idx]+1





"""
Using our review_to_word_map to calculate meaningful clusters using LDA
"""
model = lda.LDA(n_topics=15, n_iter=500, random_state=1)
model.fit(review_to_word_map)
topic_word = model.topic_word_  # model.components_ also works

# printing top words
n_top_words = 25
for i, topic_dist in enumerate(topic_word):
    topic_words = np.array(tokens)[np.argsort(topic_dist)][:-n_top_words:-1]
    print('Topic {}: {}'.format(i, ' '.join(topic_words)))
