#!/usr/bin/env python
# coding: utf-8

# In[49]:


import pandas as pd
import glob
import csv
import re
import nltk
import numpy as np

#nltk.download('all')
#nltk.download('stopwords')


from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from num2words import num2words
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer


from datetime import datetime


from bs4 import BeautifulSoup


from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from sklearn.feature_extraction.text import TfidfTransformer


# ## Initialize variables that mean names of folders with initial data, output data and final file with result in .csv

# In[50]:


input_data = '/Users/mashaverbytskaya/python_course/my_env/isw_data'

output_data = '/Users/mashaverbytskaya/python_course/my_env/ready_isw_data'
output_file = 'isw_report.csv'


# ## Check that all our files exist and can be opened without errors

# In[51]:


files_by_days = glob.glob(f"{input_data}/*.html")
len(files_by_days)


# In[52]:


all_data =[]

for file in files_by_days:
    
    d = {}
    #print(file)
    
    file_name = file.split("/")[-1].replace(".html", "")
    date = datetime.strptime(file_name,'%Y-%m-%d').date()
    #url = file_name[1].split(".")[0]
    print(date)
    
    with open (file, "r") as current_file:
        parsed_html = BeautifulSoup(current_file.read())
        title = parsed_html.head.find('title').text
        link = parsed_html.head.find('link', attrs ={'rel':'canonical'}, href=True).attrs["href"]
        
        text_title =  parsed_html.body.find ("h1", attrs={'id':'page-title'}).text
        text_main_raw = parsed_html.body.find ("div", attrs={'class':'field field-name-body field-type-text-with-summary field-label-hidden'})
        
        initials = text_main_raw.select('p:nth-of-type(2)')
        initials[0].replaceWith('')
        text_main = text_main_raw.text
        
        d ={
            "date":date,
            "title":title,
            "text_title":text_title,
            "main_html":text_main
        }
        
        all_data.append(d)


# In[53]:


df = pd.DataFrame.from_dict(all_data)


# In[54]:


df = df.sort_values(by = ['date'])


# ## Represent initial table with raw data

# In[55]:


df.head(10)


# ## Write data from html to .csv file
# 

# In[56]:


df.to_csv(f"{output_data}/{output_file}", sep = ';', index = False)


# ## Clean each html file to extract only useful info

# In[57]:


#select some row from previously created .csv file and print it to see which info we need to extract
some_row = df.iloc[46]
some_row_in_html = some_row['main_html']
print(some_row_in_html)


# ## Delete all [n] symbols

# In[58]:


df['main_html_1'] = df['main_html'].apply(lambda x : re.sub('\[(\d+)\]', "", x))
page_clean = df.iloc[46]['main_html_1']
print(page_clean)


# ## Delete all links

# In[59]:


df['main_html_2'] = df['main_html_1'].str.replace('\sdot ', '.', regex=True).apply(lambda x : re.sub('http://\S+|https://\S+|.$html', "", x))
page_clean_1 = df.iloc[46]['main_html_2']
print(page_clean_1)
#df.head(10)


# ## Delete all dates

# In[60]:


df['main_html_3'] = df['main_html_2'].apply(lambda y: re.sub(r'\n.{5,15}\d:\d.{0,9}', "", y))


# In[61]:


page_clean_2 = df.iloc[46]['main_html_3']
#print(page_clean_2)
df.head(10)


# ## Delete unnecessary columns and rename the remaining ones

# In[62]:


df_final_raw = df.drop(['main_html', 'main_html_1', 'main_html_2'], axis = 1)
old_to_new = {
    'main_html_3': 'main_text'
}
df_final = df_final_raw.rename(columns = old_to_new)
df_final.head(10)


# ## Rewrite .csv file with final data to store new data frame

# In[74]:


df_final.to_csv(f'{output_data}/{output_file}', sep = ';', index = False)


# In[75]:


input_data_parsed = '/Users/mashaverbytskaya/python_course/my_env/isw_data/isw_report.csv'

output_file_parsed = 'isw_report_parsed.csv'


# ## Remove words of one letter

# In[65]:


def remove_oneletter_words(data):
    words = word_tokenize(str(data), language="english")
    
    new_text =""
    
    for w in words:
        if len(w)>1:
            new_text= new_text + " " +w 
            
    return new_text 


# In[66]:


def convert_low (data):
    return np.char.lower(data)


# ## Remove stopwords from the text using nltk library with exception for 'no', 'not'

# In[67]:


def remove_stopwords(data):
    stop_words=set(stopwords.words('english'))
    not_stopwords ={'no','not'}
    stop_words=stop_words-not_stopwords
    
    words = word_tokenize(str(data), language="english")
    new_text=""
    
    for w in words:
        if w not in stop_words:
            new_text=new_text+" "+w
            
    
    return new_text


# ## Convert numbers into words with exception for words with numbers inside and ordinal numbers

# In[89]:


def convert_numbers(data):
    words = word_tokenize(str(data), language="english")
    
    new_text =""
    for w in words:
        if w.isdigit():
            if int(w)<1000000000:
                w=num2words(w)
            else:
                w=""
                
        new_text= new_text+" " + w
    new_text= np.char.replace(new_text,"-"," ")
    new_text= np.char.replace(new_text,","," ")
    
    return new_text


# ## Remove symbols and special characters

# In[69]:


def remove_signs(data):
    symbols="!\"#$%&()*+-—./:;<=>?@[\]^_'`{|}~\n"
    
    for i in range (len(symbols)):
        data=np.char.replace(data,symbols[i]," ")
        data=np.char.replace(data,"  "," ")
        data=np.char.replace(data,","," ")
    return data


# ## Stemming and Lemmatization functions

# In[70]:


def stemming(data):
    stemmer =PorterStemmer()
    
    words = word_tokenize(str(data), language="english")
    new_text=""
    
    for w in words:
        new_text=new_text+" "+stemmer.stem(w)
    return new_text

def lemmatizing(data):
    lemmatizer =WordNetLemmatizer()
    
    words = word_tokenize(str(data), language="english")
    new_text=""
    
    for w in words:
        new_text=new_text+" "+lemmatizer.lemmatize(w)
    return new_text


# In[71]:


def convert(data):
    data=remove_oneletter_words(data)
    data=convert_low(data)
    data=remove_stopwords(data)
    data=remove_signs(data)
    data=convert_numbers(data)
    data=remove_oneletter_words(data)
    data=stemming(data)
    return data

def convert2(data):
    data=remove_oneletter_words(data)
    data=convert_low(data)
    data=remove_stopwords(data)
    data=remove_signs(data)
    data=convert_numbers(data)
    data=remove_oneletter_words(data)
    data=lemmatizing(data)
    return data


# ## Convert data frame with raw data using listed functions above and display 5 first rows as an example

# In[76]:


withoutletters = convert(page_clean_1)
df_final['text_stemm'] = df_final["main_text"].apply(lambda x: convert(x))
df_final['text_lemm'] = df_final["main_text"].apply(lambda x: convert2(x))
df_final.head(5)


# ## Print 74 raw as an example of lemmatization

# In[79]:


docs = df_final["text_lemm"].tolist()
some_row = df_final.iloc[74]
some_row_in_html = some_row['text_lemm']
print(some_row_in_html)


# ## Display number of files to make sure we've not missed any of them

# In[80]:


len(docs)


# ## Create instance of count vectorizer to vectorize text data 

# In[81]:


cv = CountVectorizer(max_df=0.98,min_df=2)
word_count_vector= cv.fit_transform(docs)

word_count_vector.shape


# ## Create instance of TfidTransormet to count inversed document frequency (IDF)

# In[90]:


tfiidf_transformer=TfidfTransformer(smooth_idf=True,use_idf=True)
tfiidf_transformer.fit(word_count_vector)


# ## Vectorization

# In[86]:


df_idf = pd.DataFrame(tfiidf_transformer.idf_, index=cv.get_feature_names_out(), columns=["idf_weight"])
df_idf=df_idf.sort_values(by=["idf_weight"])


df_idf.head(15)


# ## Create final data frame which drops unnecessary columns from the previous one

# In[87]:


df_final_raw = df_final.drop(['date', 'title', 'text_title','main_text'], axis = 1)

df_final_raw.head(10)


# ## Store data frame in .csv file

# In[88]:


df_final_raw.to_csv(f"{output_data}/{output_file_parsed}", sep = ';', index = False)

