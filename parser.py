import json


if __name__ == "__main__":
    # convert file to parsable data
    f = open("unsig.json", "r")
    data = f.readlines()
    unsig_json = json.loads(data[0])

    # parse data
    print(unsig_json[0])
    print(unsig_json[0][0])
