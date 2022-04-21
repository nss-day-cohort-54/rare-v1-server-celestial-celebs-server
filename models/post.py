<<<<<<< HEAD

class Post():
    def __init__(self, id, user_id, category_id, title, publication_date, image_url, content, approved):
=======
class Post:
    def __init__(self, id, user_id, category_id, title, publication_date, content):
>>>>>>> main
        self.id = id
        self.user_id = user_id
        self.category_id = category_id
        self.title = title
        self.publication_date = publication_date
<<<<<<< HEAD
        self.image_url = image_url
        self.content = content
        self.approved = approved
        
=======
        self.content = content
        self.user = None
        self.category = None
>>>>>>> main
