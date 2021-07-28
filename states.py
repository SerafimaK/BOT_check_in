dialog_state = {}


def get_current_state(user_id):
    try:
        return dialog_state[user_id]
    except KeyError:
        return 'Start'


def set_state(user_id, value):
    try:
        dialog_state[user_id] = value
        return True
    except:
        # тут желательно как-то обработать ситуацию
        return False