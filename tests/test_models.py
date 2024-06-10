import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine
from database.setup import create_tables
from database.connection import get_db_connection

class TestModels(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        create_tables()
        cls.conn = get_db_connection()

    @classmethod
    def tearDownClass(cls):
        cls.conn.close()

    def setUp(self):
        self.conn.execute('DELETE FROM articles')
        self.conn.execute('DELETE FROM authors')
        self.conn.execute('DELETE FROM magazines')
        self.conn.commit()

        self.author = Author(id=1, name="John Doe")
        self.magazine = Magazine(id=1, name="Tech Monthly", category="Technology")
        self.article = Article(id=1, title="The Future of AI", content="Content about AI", author_id=self.author.id, magazine_id=self.magazine.id)

    def test_article_creation(self):
        article = Article(id=2, title="AI in 2024", content="Content about AI in 2024", author_id=self.author.id, magazine_id=self.magazine.id)
        self.assertEqual(article.title, "AI in 2024")
        self.assertEqual(article.content, "Content about AI in 2024")
        self.assertEqual(article.author_id, self.author.id)
        self.assertEqual(article.magazine_id, self.magazine.id)

    def test_author_articles(self):
        articles = [self.article]
        author_articles = self.author.articles(articles)
        self.assertEqual(len(author_articles), 1)
        self.assertEqual(author_articles[0].title, "The Future of AI")

    def test_author_creation(self):
        self.assertEqual(self.author.name, "John Doe")

    def test_author_magazines(self):
        articles = [self.article]
        author_magazines = self.author.magazines(articles, [self.magazine])
        self.assertEqual(len(author_magazines), 1)
        self.assertEqual(author_magazines[0], self.magazine.id)

    def test_magazine_article_titles(self):
        articles = [self.article]
        article_titles = self.magazine.article_titles(articles)
        self.assertEqual(len(article_titles), 1)
        self.assertEqual(article_titles[0], "The Future of AI")

    def test_magazine_articles(self):
        articles = [self.article]
        self.assertIn(self.article, articles)
        self.assertEqual(len(articles), 1)

    def test_magazine_contributing_authors(self):
        articles = [self.article]
        authors = self.magazine.contributors(articles, [self.author])
        self.assertEqual(len(authors), 1)
        self.assertEqual(authors[0], self.author.id)

    def test_magazine_contributors(self):
        articles = [self.article]
        contributors = self.magazine.contributors(articles, [self.author])
        self.assertEqual(len(contributors), 1)
        self.assertEqual(contributors[0], self.author.id)

    def test_magazine_creation(self):
        self.assertEqual(self.magazine.name, "Tech Monthly")
        self.assertEqual(self.magazine.category, "Technology")

if __name__ == "__main__":
    unittest.main()