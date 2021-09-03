from multiprocessing import Process
import os
import time
import urllib.request

def download_list_of_images(lst, destination):
    """
    Takes a list of urls and a directory location.

    - Checks if the directory exists if not we create it
    - Iterates through the list of given urls

    @lst, list of urls
    @destination, location of destination download folder

    NOTE: uses wget_img for the specific use of getting unsigs
    """
    # make directory if it doesn't exist
    if os.path.isdir(destination) != True:
        os.mkdir(destination)
    # run multiple process of wget_img()
    for idx, i in enumerate(lst):
        
        img_file = destination + "/" + str("{:05d}".format(i)) + ".png"
        if os.path.isfile(img_file) == False:
            # if image doesn't exist download it
            p = Process(target=wget_img, args=(idx,i,destination))
            p.start()
            time.sleep(0.2)
        print("Image " + str(idx) + " of " + str(len(lst)),end="\r")
    print("\nDone...")


def wget_img(idx, i, destination):
    """
    specific function to download lowest quality unsig images
    """
    # create url image
    url = "https://s3-ap-northeast-1.amazonaws.com/unsigs.com/images/1024ds/"
    image_name = str("{:05d}".format(i)) + ".png"
    url = url + image_name

    image_name = destination + "/" + image_name
    urllib.request.urlretrieve(url, image_name)
    return 
