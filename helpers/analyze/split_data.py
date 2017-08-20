import sys
import logging
import pandas as pd

from sklearn.model_selection import train_test_split

if __name__ == "__main__":


    print(">> Reading reactions from file")
    reactions = read_reactions('data/raw')
    print(">> Total interactions: %d" % len(reactions))

    reactions['author_id'] = reactions['author_id'].astype(str)

    # Get person has most interaction
    user_id = reactions.drop_duplicates(['author_id'], keep = 'last').drop(['status_id', 'reaction_status'], axis = 1)
    print(">> Number of people liked page: %d" % len(user_id))

    count = reactions.groupby(['author_id'], as_index=False).size().reset_index().rename(columns={0:'count'})['count'].tolist()
    user_id = user_id.assign(num_reactions = count)
    print(user_id)

    user_id.to_excel("Reactions.xlsx")


    # Keep reactions since facebook had 5 reactions
    print(">> Reading from file")
    posts = read_many_file(["lhpconfessions"], 'data/raw')
    print(">> Len before eliminate %d" % len(posts))

    posts = posts[posts['num_reactions'] - posts['num_likes'] > 0]
    print(">> Len after eliminate %d" % len(posts))

    # print(">> Reading reactions from file")
    # reactions = read_reactions('data/raw')
    # print(">> Total interactions: %d" % len(reactions))

    status_id = posts['status_id'].tolist()
    reactions = reactions[reactions['status_id'].isin(status_id)]
    print(">> Total reactions in the time: %d" % len(reactions))

    # Divide train, cros, test
    train = cros = test = pd.DataFrame()
    user_id = reactions.drop_duplicates(['author_id'], keep = 'last')
    status_id = reactions.drop_duplicates(['status_id'], keep = 'last')

    count = 0
    for key, row in user_id.iterrows():
        count += 1
        if count % 100:
            sys.stdout.flush()
            sys.stdout.write("\r>> process to %d over %d" % (count, len(user_id)))
        
        temp = reactions[reactions['author_id'] == row['author_id']]
        if len(temp) > 3:
            n_train, n_temp = train_test_split(temp, test_size = 0.4)
            n_cros, n_test = train_test_split(n_temp, test_size = 0.5)
            train = train.append(n_train)
            cros = cros.append(n_cros)
            test = test.append(n_test)

    train['author_id'] = train['author_id'].astype(str)
    cros['author_id'] = cros['author_id'].astype(str)
    test['author_id'] = test['author_id'].astype(str)

    print("\nLen of train, cros and test: %d %d %d" % (len(train), len(cros), len(test)))
    print(">> Output to xlsx")
    writer = pd.ExcelWriter('mf_data.xlsx')
    train.to_excel(writer, 'train')
    cros.to_excel(writer, 'cros')
    test.to_excel(writer, 'test')
    writer.save()
