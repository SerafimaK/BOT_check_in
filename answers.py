from pymystem3 import Mystem

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
    return len(name)


text = 'Калинин Никита В.'

print(full_name(text))