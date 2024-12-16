from database.connection import get_db_connection

class Author:
    def __init__(self, id=None, name=None):
        if not name or not isinstance(name, str):
            raise ValueError("Name must be a non-empty string.")
        
        self._id = id
        self._name = name
        
        if id is None:
            self.save()

    def save(self):
       
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if self._id is None:
                cursor.execute("INSERT INTO authors (name) VALUES (?)", (self._name,))
                self._id = cursor.lastrowid 
            else:  
                cursor.execute("UPDATE authors SET name = ? WHERE id = ?", (self._name, self._id))

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def articles(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, author_id, magazine_id
                FROM articles
                WHERE author_id = ?
            """, (self._id,))
            rows = cursor.fetchall()
            return rows

    def magazines(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT DISTINCT m.id, m.name, m.category
                FROM magazines m
                JOIN articles a ON m.id = a.magazine_id
                WHERE a.author_id = ?
            """, (self._id,))
            rows = cursor.fetchall()
            return rows

    def __repr__(self):
        return f"<Author {self.name}>"
