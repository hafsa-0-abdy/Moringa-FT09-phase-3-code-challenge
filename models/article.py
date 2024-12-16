from database.connection import get_db_connection
from models.author import Author
from models.magazine import Magazine

class Article:
    def __init__(self, id=None, title=None, author=None, magazine=None):
        if not title or not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters.")
        
        if not isinstance(author, Author):
            raise ValueError("Author must be an instance of Author.")
        
        if not isinstance(magazine, Magazine):
            raise ValueError("Magazine must be an instance of Magazine.")
        
        self._id = id
        self._title = title
        self._author = author
        self._magazine = magazine
        
        if id is None:
            self.save()

    def save(self):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()

                if self._id is None:
                    # Insert into the database
                    cursor.execute("""
                        INSERT INTO articles (title, author_id, magazine_id)
                        VALUES (?, ?, ?)
                    """, (self._title, self._author.id, self._magazine.id))
                    self._id = cursor.lastrowid

                else:
                    # Update the existing article
                    cursor.execute("""
                        UPDATE articles
                        SET title = ?, author_id = ?, magazine_id = ?
                        WHERE id = ?
                    """, (self._title, self._author.id, self._magazine.id, self._id))
            
        except Exception as e:
            # Handle exception if needed (e.g., logging the error)
            print(f"Error saving article: {e}")
            raise

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def magazine(self):
        return self._magazine

    def __repr__(self):
        return f"<Article {self.title}, Author: {self.author.name}, Magazine: {self.magazine.name}>"
    
    def insert_article_content(self, content):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE articles
                SET content = ?
                WHERE articles.id = ?
            """, (content, self._id))

