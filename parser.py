import json
from multiprocessing import Process, Manager, Pool

from image_down import *

global unsig_json

def pp(index):
    #pretty print
    print("\n\tlooking at " + str(index)) 
    index = int(unsig_json[index][0]['index'])
    print("\nunsig_" + str(index))
    print("Properties: " + str(unsig_json[index][1]['properties'][0]))
    for item in unsig_json[index][2]['colors']:
        print("{0:<6}".format(item), end=" |")
    print("")
    
    for item in unsig_json[index][3]['distributions']:
        print("{0:<6}".format(item), end=" |")
    print("")
    
    for item in unsig_json[index][4]['rotations']:
        print("{0:<6}".format(item), end=" |")
    print("")
    
    for item in unsig_json[index][5]['multipliers']:
        print("{0:<6}".format(item), end=" |")
    
    print("")
    return

def x_finder(i, shared_list):
    # check for properties where multipliers all == 1
    num_of_pattern = 0
    i = int(unsig_json[i][0]['index'])
    #print("checking unsig " + str(unsig_json[i][0]['index']), end="")

    try:
        for idx, val in enumerate(unsig_json[i][5]['multipliers']):
            #print(str(i)+ "\nat " + str(val) + " of " + str(unsig_json[i][5]['multipliers']))
            if float(val) != 1.0:
                #print("\treturn "+ str(val) +" != 1.0")
                #print("")
                return
    except ValueError:
        # value error for unsig00000
        pass
    
    shared_list.append(i)
    #print(" ... potential X found!")

    return
    


def star_finder(i, shared_list):
    # check index i for rotations of 90 and 270 with a multiplier of 2
    # if we find at least two in any category add the index to the
    # shared list
    i = int(unsig_json[i][0]['index'])
    num_of_pattern = 0

    try:
        for idx, val in enumerate(unsig_json[i][4]['rotations']):
            if int(val) == 90 or int(val) == 180:
                if float(unsig_json[i][5]['multipliers'][idx]) == 2:
                    num_of_pattern = num_of_pattern + 1
    except ValueError:
        return
    
    if num_of_pattern >= 2:
        shared_list.append(i)
        #print("Potential star found!",end="\r")

    return
    

def check(unsig_json):
    return 
        




    
if __name__ == "__main__":
    # convert json file to parsable list
    f = open("unsig.json", "r")
    data = f.readlines()
    unsig_json = json.loads(data[0])

    # sort the json based on index
    #unsig_json = sorted(unsig_json, key=lambda i: i[0]['index'])

    # multiprocessing vars   
    manager = Manager()
    shared_list = manager.list() # shared dict
    # run multiple process for a given function (star_finder)
    for i in range(0, len(unsig_json)):
        p = Process(target=x_finder, args=(i, shared_list))
        #p = Process(target=star_finder, args=(i, shared_list))
        p.start()
        #os.system('cls' if os.name == 'nt' else 'clear')
        print("Progress " + str("{:05d}".format(i)) + "/" + str("{:05d}".format(len(unsig_json))),end="\r")
    print("")
    res = list(shared_list)
    print(res)
    print("Results: found \"" + str(len(res)) + "\" with defined pattern")
    percentage = float( len(res) / len(unsig_json) ) * 100.0
    print(str(percentage)+"%")

    destination = input("Please name download destination folder:\n> ")
    download_list_of_images(res, destination)

