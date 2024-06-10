from database.connection import get_db_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id
        self._create_article()

    def __repr__(self):
        return f'<Article {self.title}>'

    def _create_article(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO articles (id, title, content, author_id, magazine_id) VALUES (?, ?, ?, ?, ?)
        ''', (self.id, self.title, self.content, self.author_id, self.magazine_id))
        conn.commit()
        conn.close()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not (5 <= len(value) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters")
        self._title = value

    def author(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM authors WHERE id = ?
        ''', (self.author_id,))
        author = cursor.fetchone()
        conn.close()
        return author

    def magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM magazines WHERE id = ?
        ''', (self.magazine_id,))
        magazine = cursor.fetchone()
        conn.close()
        return magazine