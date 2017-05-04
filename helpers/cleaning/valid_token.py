import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)

import pandas as pd
from mongodb.query import insert

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
u'ý', u'ỳ', u'ỷ', u'ỵ', u'ỹ', u'f', u'z', u'j', u'w', u' ']

sylabus = [u'a', u'ă', u'â', u'e', u'ê', u'i',
u'o', u'ô', u'ơ', u'u', u'ư',
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
u'ý', u'ỳ', u'ỷ', u'ỵ', u'ỹ', u' '
]

def toLowerCase(word):
    if type(word) is str:
        return word.lower()
    else:
        return word

def eliminate_duplicate(listOfWords):
    listOfWords = listOfWords.drop_duplicates(['word'], keep = "last")
    return listOfWords

def eliminate_strange(listOfWords):
    print(">> Eliminate strange character")
    newList = pd.DataFrame()
    # strangeChar = [u'/', u'?', u'-', u'!', u'_', u'.', u',', u'(', u')']
    for index, row in listOfWords.iterrows():
        isCorrect = True
        if type(row['word']) is str:            
            for char in row['word']:
                if not char in listOfCharacters:
                    isCorrect = False
                    break
            if isCorrect:
                newList = newList.append(row, ignore_index = True)
    return newList

def eliminate_same_character(listOfWords):
    print(">> Eliminate Same Character")
    newList = pd.DataFrame()
    for index, row in listOfWords.iterrows():
        isCorrect = True
        words = row['word'].split(' ')
        for i in range(len(words)):
            if i > 0 and words[i] == words[i - 1]:
                isCorrect = False
                break
        if not isCorrect: 
            continue

        for word in words:
            for i in range(len(word)):
                if i > 0 and word[i] == word[i - 1]:
                    isCorrect = False
                    break
            if not isCorrect:
                break
        
        if isCorrect: 
            newList = newList.append(row, ignore_index = True)
    
    return newList 

def eliminate_init(listOfWords):
    print(">> Eliminate init")
    newList = pd.DataFrame()
    for index, row in listOfWords.iterrows():
        if type(row['word']) is str:
            words = row['word'].split(' ')
            isCorrect = True
            for i in range(len(words)):
                if len(words[i]) == 1 and (not words[i] in sylabus):
                    isCorrect = False
                    break

            if isCorrect:
                newList = newList.append(row, ignore_index = True) 
    return newList    

def eliminate_word(listOfWords):
    print(">> Eliminate word")
    newList = pd.DataFrame()
    for index, row in listOfWords.iterrows():
        if type(row['word']) is str:
            words = row['word'].split(' ')
            if len(words) > 1:
                newList = newList.append(row, ignore_index = True) 
    return newList

def eliminate_unmeaning():
    print(">> Reading from file")
    xl = pd.ExcelFile("testFile.xlsx")
    listOfWords = pd.DataFrame()
    # listOfWords = pd.('testFile.csv')
    for sheet_names in xl.sheet_names:
        temp = xl.parse(sheet_names)
        listOfWords = listOfWords.append(temp, ignore_index = True)        
    
    print(">> Change to lowercase")
    listOfWords['word'] = listOfWords['word'].apply(toLowerCase)

    print(">> Sorting the list")
    listOfWords = listOfWords.sort(['word'], ascending = False, kind = 'quicksort')

    # Remove duplicate
    listOfWords = eliminate_duplicate(listOfWords)

    # Eleminate term has strange character
    listOfWords = eliminate_strange(listOfWords)

    # Eleminate init
    listOfWords = eliminate_init(listOfWords)

    # Eleminate word    
    listOfWords = eliminate_word(listOfWords)



    # Eleminate term has same character next to each other
    listOfWords = eliminate_same_character(listOfWords)    
    return listOfWords
# eliminate_unmeaning()
