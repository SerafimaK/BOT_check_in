data = {}


def add_info(key, value):
    data[key] = value
    db = open("user data.txt", "w")
    db.write(str(data))
    db.close()



