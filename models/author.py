from database.connection import get_db_connection
from models.article import Article
from models.magazine import Magazine

class Author:
    def __init__(self, id, name):
        self._id = id
        self.name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if not isinstance(name, str):
            raise TypeError("name must be of type str")
        if len(name) == 0:
            raise ValueError("name must be longer than 0 characters")
        if hasattr(self, '_name'):
            raise AttributeError("name cannot be changed once set")
        self._name = name

    def _fetch_articles(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, title, content, author_id, magazine_id
            FROM articles
            WHERE author_id = ?
        ''', (self.id,))
        article_info = cursor.fetchall()
        conn.close()
        return [Article(*article) for article in article_info]

    @property
    def articles(self):
        if not hasattr(self, '_articles'):
            self._articles = self._fetch_articles()
        return self._articles

    def _fetch_magazines(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT m.id, m.name, m.category
            FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        ''', (self.id,))
        magazine_info = cursor.fetchall()
        conn.close()
        return [Magazine(*magazine) for magazine in magazine_info]

    @property
    def magazines(self):
        if not hasattr(self, '_magazines'):
            self._magazines = self._fetch_magazines()
        return self._magazines

    def __repr__(self):
        article_titles = ", ".join(article.title for article in self.articles) if self.articles else "None"
        magazine_titles = ", ".join(magazine.name for magazine in self.magazines) if self.magazines else "None"
        return f'<Author: {self.name} | id: {self.id} | MAGAZINES: {magazine_titles} | ARTICLES: {article_titles}>'

