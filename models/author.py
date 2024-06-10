from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self._create_author()

    def __repr__(self):
        return f'<Author {self.name}>'

    def _create_author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO authors (id, name) VALUES (?, ?)
        ''', (self.id, self.name))
        conn.commit()
        conn.close()

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise TypeError("ID must be an integer")
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Name must be a non-empty string")
        self._name = value

    def articles(self, articles):
        return [article for article in articles if article.author_id == self.id]
    
    def magazines(self, articles, magazines):
        magazine_ids = {article.magazine_id for article in articles if article.author_id == self.id}
        return [magazine.id for magazine in magazines if magazine.id in magazine_ids]