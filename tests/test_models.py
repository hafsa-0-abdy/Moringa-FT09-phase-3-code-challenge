import unittest
from models.author import Author
from models.article import Article
from models.magazine import Magazine

class TestModels(unittest.TestCase):
    def test_author_creation(self):
        author = Author(1, "John Doe")
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        author = Author(1, "John Doe")
        magazine = Magazine(1, "Tech Weekly", category="Technology")
        article = Article(1, "Test Title", author, magazine)
        self.assertEqual(article.title, "Test Title")
        self.assertEqual(article.author, author)
        self.assertEqual(article.magazine, magazine)

    def test_magazine_creation(self):
        magazine = Magazine(1, "Tech Weekly", category="Technology")
        self.assertEqual(magazine.name, "Tech Weekly")

if __name__ == "__main__":
    unittest.main()
