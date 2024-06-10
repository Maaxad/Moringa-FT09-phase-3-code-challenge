from database.connection import get_db_connection

class Magazine:
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category
        self._create_magazine()

    def __repr__(self):
        return f'<Magazine {self.name}>'

    def _create_magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO magazines (id, name, category) VALUES (?, ?, ?)
        ''', (self.id, self.name, self.category))
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
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string")
        self._category = value

    def article_titles(self, articles):
        return [article.title for article in articles if article.magazine_id == self.id]

    def contributors(self, articles, authors):
        author_ids = {article.author_id for article in articles if article.magazine_id == self.id}
        return [author.id for author in authors if author.id in author_ids]


    def contributing_authors(self, articles, authors):
        author_article_counts = {}
        for article in articles:
            if article.magazine_id == self.id:
                if article.author_id in author_article_counts:
                    author_article_counts[article.author_id] += 1
                else:
                    author_article_counts[article.author_id] = 1
        return [author.id for author in authors if author_article_counts.get(author.id, 0) > 2]