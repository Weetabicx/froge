from json import load

def ReadToken():
    with open("config.json", "r") as data:  # Opens a file in read mode
        config = load(data)  # Loads file as a json
    
    return config["token"]