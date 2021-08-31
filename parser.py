import json

UNSIGS_MINTED = 31119


def csv_split(s):
    # seperate items in a csv string and return in list format
    return s.split(',')

if __name__ == "__main__":
    # convert file to parsable data
    my_file = open("unsig.json", "r")
    data = my_file.readlines()
    json_str = data[0].replace("'", "") # note removal of
                                        # single quotation 
                                        # needed to clean json
    unsig_json = json.loads(json_str)

    # parse data
    print(unsig_json[0])
    print(unsig_json[0][0])



