import os
import sys
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if not path in sys.path:
    sys.path.insert(1, path)

from function.read import read_many_file
from mongodb.query import insert, fetch, update
from cleaning.preprocessing_content import icon_cleaning

def push_value(filenames):
    for filename in filenames:
        # get name
        school_name = ""
        if filename == "lhpconfessions":
            school_name = "Le Hong Phong"
        else: 
            if filename == "NthersConfessions":
                school_name = "Nguyen Thuong Hien"
            else:
                if filename == "PtnkConfession":
                    school_name = "Pho Thong Nang Khieu"
                else:
                    school_name = "rmit"

        print(school_name)
        posts = read_many_file([filename])

        # Drop na
        posts['link_name'] = posts['link_name'].fillna(" ")
        posts['status_type'] = posts['status_type'].fillna(" ")
        posts['status_message'] = posts['status_message'].fillna(" ")
        
        count = 0
        # sql = "INSERT INTO confessions (status_id, status_type, status_message, link_name, status_published, num_reactions, num_comments, num_shares, num_likes, num_loves, num_wows, num_hahas, num_sads, num_angrys, from_school) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        for index, row in posts.iterrows():
            count += 1
            print(count)
            insert('corpus', key = ['status_id', 'status_type', 'status_message', 'link_name', 'status_published', 'num_reactions', 'num_comments', 'num_shares', 'num_likes', 'num_loves', 'num_wows', 'num_hahas', 'num_sads', 'num_angrys', 'from_school'], \
                    value = [row['status_id'], row['status_type'], row['status_message'], row['link_name'], \
                            row['status_published'], str(row['num_reactions']), str(row['num_comments']), \
                            str(row['num_shares']), str(row['num_likes']), str(row['num_loves']), str(row['num_wows']), \
                            str(row['num_hahas']), str(row['num_sads']), str(row['num_angrys']), school_name])
    
def transform_post():
    corpus = fetch('corpus')
    for document in corpus:
        _id = document["_id"]
        content = icon_cleaning(document["status_message"])
        update(collection_name = "corpus", _id = _id, key = ['content'], value = [content])

# push_value(['lhpconfessions', 'NthersConfessions', 'PtnkConfession', 'rmitvnconf'])
# transform_post()