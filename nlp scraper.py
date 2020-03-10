# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 19:00:52 2020

@author: jvan1
"""

from textblob import TextBlob
import os
import glob
import pandas as pd

def tryNamePurposeDict(text):
    split = text.split('", "')
    name = []
    purpose = []
    for curr_split in split:
        name.append(curr_split.split(':')[0])
        purpose.append(curr_split.split(':')[1])
    return name, purpose
def tryNamePurposeIndivid(text):
    split = text.split('Name: ')[1:]
    name = []
    purpose = []
    if 'Purpose: ' in split[0]:
        split[-1] = split[-1].strip('\n')
        for curr_split in split:
            name.append(curr_split.split('Purpose: ')[0])
            purpose.append(curr_split.split('Purpose: ')[1])
    else:
        for curr_split in split:
            name.append(curr_split)
        split = text.split('Purpose: ')[1:]
        for curr_split in split:
            purpose.append(curr_split)
    return name, purpose
    
def getFiles():
    data = pd.DataFrame()
    data['Name'] = ''
    data['Purpose'] = ''
    txt_file_list = glob.glob('*.txt')
    csv_file_list = glob.glob('*.csv')
    for file in txt_file_list:
        f= open(file,"r+")
        text = f.read()
        if 'Name' not in text:
            name, purpose = tryNamePurposeDict(text)
            curr_df = pd.DataFrame(list(zip(name,purpose)), 
               columns =['Name', 'Purpose'])
            
        elif len(text.split('Name'))>2:
            name, purpose = tryNamePurposeIndivid(text)
            curr_df = pd.DataFrame(list(zip(name,purpose)), 
               columns =['Name', 'Purpose'])
        else:
            curr_df = pd.read_csv(file,delimiter='\t')
        data = data.append(curr_df,ignore_index=True)
    data['Name'] = data['Name'].astype(str)
    data['Purpose'] = data['Purpose'].astype(str)
    data['Name'] = data['Name'].apply(lambda x: x.strip(',').strip('(').strip('\'').strip('\"').strip(')').strip('\"').strip('\n').strip('{').strip('}'))
    data['Purpose'] = data['Purpose'].apply(lambda x: x.strip(',').strip('(').strip('\'').strip('\"').strip(')').strip('\"').strip('\n').strip('{').strip('}'))

    for file in csv_file_list:
        if file == 'Sentiment.csv':
            continue
        curr_df = pd.read_csv(file)
        if 'Name'  not in list(curr_df.columns):
            curr_df['Name'] = curr_df['name']
            curr_df = curr_df.drop('name',axis=1)
        if 'Purpose' not in list(curr_df.columns):
            curr_df['Purpose'] = curr_df['purpose']
            curr_df = curr_df.drop('purpose',axis=1)
        data = data.append(curr_df,ignore_index=True)
    data['Name'] = data['Name'].astype(str)
    data['Purpose'] = data['Purpose'].astype(str)
    data['Name'] = data['Name'].apply(lambda x: x.strip(',').strip('(').strip('\'').strip('\"').strip(')').strip('"').strip('\n').strip('{').strip('}'))
    data['Purpose'] = data['Purpose'].apply(lambda x: x.strip(',').strip('(').strip('\'').strip('\"').strip(')').strip('"').strip('\n').strip('{').strip('}'))
    return data

def getSentimentList(data):
    data['Blob'] = data['Purpose'].apply(lambda x: TextBlob(x))
    data['Sentiment Score'] = data['Blob'].apply(lambda x: x.sentiment.polarity)
    return data.sort_values(by='Sentiment Score',ascending=False)
if __name__ == '__main__':
    data = pd.DataFrame()
    data = getFiles()
    data = getSentimentList(data)
    data.to_csv('Sentiment.csv')
    