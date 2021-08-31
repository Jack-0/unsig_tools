from bs4 import BeautifulSoup
from html.parser import HTMLParser
from multiprocessing import Process, Manager, Pool
import time
import requests
import json

UNSIG_URL = "https://www.unsigs.com/details/"
UNSIGS_MINTED = 31119


def find_between( s, first, last ):
    # find a substring between two given strings
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

def csv_split(s):
    # separate items in a csv string and return in list format
    return s.split(',')

def unsig_job(i, unsig_list):
    # scrapes given url for unsig data, creates a dict adds dict
    # to a multiprocess list
    
    index = str("{:05d}".format(i)) # pad zeros in front of int
    url = UNSIG_URL + index

    # Make a GET request to fetch the raw HTML content
    try:
        # get the html for unsig 'i'
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, "lxml")
        res = soup.find_all("li")
        res = str(res)
        # parse the html 
        properties = csv_split(find_between(res, "This unsig NFT has <b>","</b>"))
        colors = csv_split(find_between(res, "Colors:</b> [","]"))
        distributions = csv_split(find_between(res, "Distributions:</b> [","]"))
        rotations = csv_split(find_between(res, "Rotations:</b> [","]"))
        multipliers = csv_split(find_between(res, "Multipliers:</b> [","]"))
        # format the data
        data = [{'index': i},
            {'properties': properties},
            {'colors':colors},
            {'distributions':distributions},
            {'rotations':rotations},
            {'multipliers':multipliers}
            ]
        unsig_list.append(data)
        return
    except ConnectionRefusedError:
        # error wait and recursively try again
        time.sleep(0.1)
        unsig_job(i, unsig_list)

if __name__ == "__main__":
    
    # multiprocessing vars
    manager = Manager()
    unsig_list = manager.list() # shared dict
    
    # run multiple process for the function unsig_job(_,_)
    for i in range (0, UNSIGS_MINTED):
        p = Process(target=unsig_job, args=(i, unsig_list))
        p.start()
        # wait 1/10 second to avoid socket errors and OS threading errors
        time.sleep(0.1)
        print("Progress " + str("{:05d}".format(i)) + "/" + str("{:05d}".format(UNSIGS_MINTED)))
     
    # wait until all processes are done
    while len(unsig_list) != UNSIGS_MINTED:
        pass
    
    # convert multithreaded proxy list into standard list for json
    unsig_list = list(unsig_list)
    # save to file
    with open("unsig.json", "w") as outfile:
        json.dump(unsig_list, outfile)

    print("finished... unsig data saved to unsig.json")
