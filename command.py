import pandas as pd
from model.crf import CRF_model
from helpers.mongodb.query import *

def analyze():
    print(">> Reading from file")
    xl = pd.ExcelFile("afterEliminate.xlsx")
    listOfWords = pd.DataFrame()
    # listOfWords = pd.('testFile.csv')
    for sheet_names in xl.sheet_names:
        temp = xl.parse(sheet_names)
        listOfWords = listOfWords.append(temp, ignore_index = True)


if __name__ == '__main__':
    documents = get_arr_value(collection = "corpus", require = ["content", "from_school"])
    crf = CRF_model()
    resultOfWords = pd.DataFrame(columns = ['word', 'total_appear', 'corpus_appear', 'LHP_corpus_appear', 'total_LHP_appear', 'LHP_corpus', 'last_appear'])
    count = 0
    for doc in documents:
        content = doc["content"]
        print("=====================================================")
        print(content + "\n \n")
        print("-----------")
        print("Generating...")

        count += 1
        listOfWords = crf.train(content)
        # print(listOfWords.groupby(['word']).word)
        temp = listOfWords.groupby(['word']).size().tolist()
        print(temp)

        for index, row in listOfWords.iterrows():
            condition_row = resultOfWords.loc[resultOfWords.word == row['word'], 'word']

            if not condition_row.empty:

                index = condition_row.index[0]
                resultOfWords['total_appear'][index] += 1
                if doc["from_school"].strip() == "Le Hong Phong":
                    resultOfWords['total_LHP_appear'][index] += 1

                if resultOfWords['last_appear'][index] != count:
                    resultOfWords['corpus_appear'][index] += 1
                    if doc["from_school"].strip() == "Le Hong Phong":
                        resultOfWords['LHP_corpus_appear'][index] += 1
                    resultOfWords['last_appear'][index] = count

            else:

                newRow = pd.DataFrame(columns = ['word', 'total_appear', 'corpus_appear', 'LHP_corpus_appear', 'total_LHP_appear', 'LHP_corpus', 'last_appear'])
                if doc["from_school"].strip() == "Le Hong Phong":
                    newRow = pd.DataFrame([[row['word'], 1, 1, 1, 1, 1, count]] ,\
                        columns = ['word', 'total_appear', 'corpus_appear', 'LHP_corpus_appear', 'total_LHP_appear', 'LHP_corpus', 'last_appear'])
                else:
                    newRow = pd.DataFrame([[row['word'], 1, 1, 0, 0, 0, count]] ,\
                        columns = ['word', 'total_appear', 'corpus_appear', 'LHP_corpus_appear', 'total_LHP_appear', 'LHP_corpus', 'last_appear'])
                
                if row['word'] == "tuithuongnguoita":
                    print("****************")
                    print(newRow)                
                resultOfWords = resultOfWords.append(newRow, ignore_index = True)
        
        print("====================================================== \n \n")

    
    print(resultOfWords)