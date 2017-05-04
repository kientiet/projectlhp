import pandas as pd
import numpy as np
import os

def read_data():
    # path = "../../raw_input/lhpconfessions_facebook_statuses.csv"
    # filenames = glob.glob(path)
    print(">> Reading posts")
    # posts = pd.read_csv(os.path.join(os.path.dirname(__file__), "../raw_input/lhpconfessions_facebook_statuses.csv"))
    posts = pd.read_csv("lhpconfessions_facebook_statuses.csv")
    print(">> Reading reactions")
    # reactions = pd.read_csv(os.path.join(os.path.dirname(__file__), "../../raw_input/lhpconfessions_facebook_reactions.csv"))
    reactions = pd.read_csv("lhpconfessions_facebook_reactions.csv")
    return posts, reactions

def read_excel_file():
    xl = pd.ExcelFile("term_list.xlsx")
    bag_of_words = pd.DataFrame()
    for sheet_names in xl.sheet_names:
        # print(sheet_names)
        temp = xl.parse(sheet_names)
        bag_of_words = bag_of_words.append(temp, ignore_index = True)
    return bag_of_words, xl.sheet_names

def read_vocab():
    xl = pd.ExcelFile(os.path.join(os.path.dirname(__file__), "../raw_input/statistic_words_frequency.xlsx"))
    vocab = pd.DataFrame()
    for sheet_names in xl.sheet_names:
        temp = xl.parse(sheet_names)
        vocab = vocab.append(temp, ignore_index = True)

    return vocab['word'].tolist()

def read_many_file(filenames):
    posts = pd.DataFrame()
    for i in range(0, len(filenames)):
        temp = pd.read_csv(filenames[i] + "_facebook_statuses.csv")
        posts = posts.append(temp, ignore_index = True)
    return posts

def read_vocab_pandas():
    xl = pd.ExcelFile(os.path.join(os.path.dirname(__file__), "../raw_input/statistic_words_frequency.xlsx"))
    vocab = pd.DataFrame()
    for sheet_names in xl.sheet_names:
        temp = xl.parse(sheet_names)
        vocab = vocab.append(temp, ignore_index = True)

    return vocab

def read_batch_words():
    # xl = pd.ExcelFile(os.path.join(os.path.dirname(__file__), "../raw_input/results/batch_words.xlsx"))
    xl = pd.ExcelFile("experiment_1_1.xlsx")
    vocab = pd.DataFrame()
    for sheet_names in xl.sheet_names:
        temp = xl.parse(sheet_names)
        vocab = vocab.append(temp, ignore_index = True)

    vocab = vocab[vocab.word != ' ']
    return vocab;
