import pandas as pd
import numpy as np
import os
import re

listOfCharacters = [u'a', u'ă', u'â', u'b', u'c', u'd', u'đ', u'e', u'ê', u'g', u'h', u'i', u'k', u'l', u'm', u'n',
u'o', u'ô', u'ơ', u'p', u'q', u'r', u's', u't', u'u', u'ư', u'v', u'x', u'y',
u'á', u'à', u'ả', u'ạ', u'ã',
u'ắ', u'ằ', u'ẳ', u'ặ', u'ẵ',
u'ấ', u'ầ', u'ẩ', u'ậ', u'ẫ',
u'é', u'è', u'ẻ', u'ẹ', u'ẽ',
u'ế', u'ề', u'ể', u'ệ', u'ễ',
u'ó', u'ò', u'ỏ', u'ọ', u'õ',
u'ố', u'ồ', u'ổ', u'ộ', u'ỗ',
u'ớ', u'ờ', u'ở', u'ợ', u'ỡ',
u'ú', u'ù', u'ủ', u'ụ', u'ũ',
u'ứ', u'ừ', u'ử', u'ự', u'ữ',
u'í', u'ì', u'ỉ', u'ị', u'ĩ',
u'ý', u'ỳ', u'ỷ', u'ỵ', u'ỹ', u'f', u'z', u'j', u' ',
'1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '/', '-', '.', '(', ')', ',']

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
pattern = '!|"'
pattern_obj = re.compile(pattern, re.MULTILINE)

def icon_cleaning(each_post):
    # Repalce :3, <3, :)), =))
    words = each_post.split(' ')
    newWords = []
    for index in range(len(words)):
        if len(words[index]) > 1 and (type(words[index]) is str):
            temp = words[index]
            words[index] = words[index].lower()
            conditionFirstLetter = (words[index][0] == ':' or words[index][0] == '<' or words[index][0] == ';')
            conditionSecondLetter = (words[index][1] == ')' or words[index][1] == '3' or words[index][1] == 'D' or words[index][1] == 'P' or words[index][1] == '(')
            if not (conditionFirstLetter and conditionSecondLetter):
                newWords.append(temp)
                words[index] = temp
        else:
            newWords.append(words[index])
    each_post = " ".join(newWords)

    # Add . to complete sentence first
    sentences = each_post.split('\n')
    for index in range(len(sentences)):
        sentences[index] = sentences[index].strip()
        if (len(sentences[index]) > 0) and (not sentences[index].endswith(".")):
            sentences[index] = sentences[index] + '.'
        
    each_post = " ".join(sentences)
    # Cleaning all strange character
    each_post = pattern_obj.sub('', each_post)
    each_post = each_post.replace('?', '').replace('!', '').replace('\n', ' ')
    each_post = emoji_pattern.sub(r'', each_post)

    # each_post = each_post.lower()
    afterCleaning = ""
    for eachChar in each_post:
        if eachChar.lower() in listOfCharacters:
            afterCleaning = afterCleaning + eachChar
    afterCleaning = " ".join(afterCleaning.split())
    # each_post = re.sub(r'!\w?\w\n\w"\w', '', each_post)
    # each_post = each_post.replace('"', '')
    # each_post = " ".join(each_post.split())
    afterCleaning = afterCleaning.strip()
    return afterCleaning
    # return each_post

# input is DataFrame from facebook scraper
# output is only array content
def cleaning_posts(posts):
    message = posts['status_message']
    message = message.dropna(how='all')
    message = message.apply(icon_cleaning)
    return message
