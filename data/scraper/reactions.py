import urllib.request
import json
import datetime
import csv
import time
import codecs

app_id = "1624118484537383"
app_secret = "96feeb7700b912a59e69f28138712762"

file_id = "lhpconfessions"

access_token = app_id + "|" + app_secret

def request_until_succeed(url):
    req = urllib.request.Request(url)
    success = False
    while success is False:
        try:
            response = urllib.request.urlopen(req)
            if response.getcode() == 200:
                success = True
        except Exception as e:
            print(e)
            time.sleep(5)

            print("Error for URL %s: %s" % (url, datetime.datetime.now()))
            print("Retrying.")

            if '400' in str(e):
                return None;

    return response.read().decode('utf-8')


# Needed to write tricky unicode correctly to csv
def unicode_normalize(text):
    return text.translate({ 0x2018:0x27, 0x2019:0x27, 0x201C:0x22,
                            0x201D:0x22, 0xa0:0x20 }).encode('utf-8')

def getFacebookReactionsFeedData(status_id, access_token, num_reaction):
    base = "https://graph.facebook.com/v2.6"
    node = "/%s/reactions" % status_id
    fields = "?fields=id,name,type"
    parameters = "&limit=%s&access_token=%s" % \
            (num_reaction, access_token)
    url = base + node + fields + parameters

    # print(url)
    # retrieve data
    data = request_until_succeed(url)
    # print(data)
    if data is None:
        return None
    else:
        return json.loads(data)


def processFacebookReaction(reaction, status_id):
    author_name = unicode_normalize(reaction['name'])
    reaction_status = reaction['type']
    author_id = reaction['id']
    return (status_id, author_id, author_name, reaction_status)

def scrapeFacebookPageFeedReactions(page_id, access_token):
    with open('%s_facebook_reactions.csv' % file_id, 'w', newline='', encoding='utf-8') as file:
        w = csv.writer(file)
        w.writerow(["status_id", "author_id", "author_name", "reaction_status"])

        num_processed = 0   # keep a count on how many we've processed
        scrape_starttime = datetime.datetime.now()

        print("Scraping %s Reactions From Posts: %s\n" % \
                (file_id, scrape_starttime))

        with open('%s_facebook_statuses.csv' % file_id, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for status in reader:
                has_next_page = True

                reactions = getFacebookReactionsFeedData(status['status_id'],
                        access_token, 100)

                # print(">>" % reactions)
                while has_next_page and reactions is not None:
                    for reaction in reactions['data']:
                        # print(reaction)
                        w.writerow(processFacebookReaction(reaction,
                            status['status_id']))

                        # output progress occasionally to make sure code is not
                        # stalling
                        num_processed += 1
                        if num_processed % 1000 == 0:
                            print("%s Reactions Processed: %s" %
                                  (num_processed, datetime.datetime.now()))

                    if 'paging' in reactions:
                        if 'next' in reactions['paging']:
                            reactions = json.loads(request_until_succeed(
                                        reactions['paging']['next']))
                        else:
                            has_next_page = False
                    else:
                        has_next_page = False

        print("\nDone!\n%s Reactions Processed in %s" %
              (num_processed, datetime.datetime.now() - scrape_starttime))


if __name__ == '__main__':
    scrapeFacebookPageFeedReactions(file_id, access_token)
