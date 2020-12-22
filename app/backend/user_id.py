current_user_id = ""

def GET_CURRENT_USER_ID():
    global current_user_id
    return current_user_id 

def SET_CURRENT_USER_ID(id):
	global current_user_id
	current_user_id = id