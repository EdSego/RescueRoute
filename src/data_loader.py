import json

def load_file(json_file):
    try:
        with open(json_file,"r") as file:
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("Cannot find file!")