import pandas as pd
import numpy as np
import os

def read_data():
    # path = "../../raw_input/lhpconfessions_facebook_statuses.csv"
    # filenames = glob.glob(path)
    print(">> Reading posts")
    posts = pd.read_csv(os.path.join(os.path.dirname(__file__), "../raw_input/Confessions/lhpconfessions_facebook_statuses.csv"))
    # posts = pd.read_csv("lhpconfessions_facebook_statuses.csv")
    print(">> Reading reactions")
    reactions = pd.read_csv(os.path.join(os.path.dirname(__file__), "../raw_input/Confessions/lhpconfessions_facebook_reactions.csv"))
    # reactions = pd.read_csv("lhpconfessions_facebook_reactions.csv")
    return posts, reactions

def read_many_file(filenames, directory):    
    posts = pd.DataFrame()
    for i in range(0, len(filenames)):
        # print(os.path.exists(newDir))
        temp = pd.read_csv(os.path.join(os.getcwd(), directory, filenames[i] + "_facebook_statuses.csv"))
        posts = posts.append(temp, ignore_index = True)
    return posts

def read_reactions(directory):
    reactions = pd.read_csv(os.path.join(os.getcwd(), directory, "lhpconfessions_facebook_reactions.csv"))
    return reactions

def read_full_data(directory):
    train = pd.read_excel(os.path.join(os.getcwd(), directory), sheetname="train")
    cros = pd.read_excel(os.path.join(os.getcwd(), directory), sheetname="cros")
    test = pd.read_excel(os.path.join(os.getcwd(), directory), sheetname="test")
    return train, cros, test