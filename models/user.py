class User():
    def __init__(self, id, first_name, last_name, email, bio, username, password, profile_image_url, created_on, active):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.bio = bio
        self.username = username
        self.password = password
        self.profile_image_url ='https://static.wikia.nocookie.net/disney/images/9/93/Ernestpworrell2017.jpg/revision/latest?cb=20170103211920'
        self.created_on = created_on
        self.active = active