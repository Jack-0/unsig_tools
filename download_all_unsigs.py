from image_down import *

if __name__ == "__main__":
    # convert json file to parsable list

    res = []
    for i in range(0,31119):
        res.append(i)

    download_list_of_images(res, "all_unsig_images")

