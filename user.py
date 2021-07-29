data = {}


def add_info(key, value):
    data[key] = value
    db = open("user data.txt", "w")
    db.write(str(data))
    db.close()


def full_name(text):
    m = Mystem()
    name = {}
    for word in text.split():
        analysis = m.analyze(word)[0]['analysis'][0]
        gr = analysis['gr'].split(',')
        if len(gr) > 1:
            if gr[1] == 'имя':
                name['FirstName'] = analysis['lex'].title()
            elif gr[1] == 'фам':
                name['LastName'] = analysis['lex'].title()
            elif gr[1] == 'отч':
                name['MiddleName'] = analysis['lex'].title()
    if (len(name) == 3) or (len(name) == 2 and not name['MiddleName']):
        return True
    else:
        return False
