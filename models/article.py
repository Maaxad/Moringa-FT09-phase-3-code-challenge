from database.connection import get_db_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    def __repr__(self):
        return f'<Article {self.title}>'

    @property
    def title(self):
        return self._title
    
    @title.setter
    def title(self, value):
        if hasattr(self, '_title'):
            raise AttributeError("Cannot change title after it has been set")
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        if not (5 <= len(value) <= 50):
            raise ValueError("Title must be between 5 and 50 characters")
        self._title = value

    def author(self):
        return get_author(self.author_id)

    def magazine(self):
        return get_magazine(self.magazine_id)

class Author:
    def __init__(self, id, name, bio):
        self.id = id
        self.name = name
        self.bio = bio

    def __repr__(self):
        return f'<Author {self.name}>'

class Magazine:
    def __init__(self, id, name, editor):
        self.id = id
        self.name = name
        self.editor = editor

    def __repr__(self):
        return f'<Magazine {self.name}>'

def get_author(author_id, conn):
    cursor = conn.cursor()
    sql = """
        SELECT *
        FROM authors
        WHERE id = ?
    """
    cursor.execute(sql, (author_id,))
    author_data = cursor.fetchone()

    if author_data:
        return Author(*author_data)
    else:
        return None

def get_magazine(magazine_id, conn):
    cursor = conn.cursor()
    sql = """
        SELECT *
        FROM magazines
        WHERE id = ?
    """
    cursor.execute(sql, (magazine_id,))
    magazine_data = cursor.fetchone()

    if magazine_data:
        return Magazine(*magazine_data)
    else:
        return None

