class User:
    def __init__(self, email, password, role, is_active=False, is_verify=False):
        self.email = email
        self.password = password
        self.role = role
        self.is_active = is_active
        self.is_verify = is_verify

class Societymember:
    def __init__(self, firstname, lastname, contact_no, block_no, pic, user_id):
        self.firstname = firstname
        self.lastname = lastname
        self.contact_no = contact_no
        self.block_no = block_no
        self.pic = pic
        self.user_id = user_id



