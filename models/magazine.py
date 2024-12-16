from database.connection import get_db_connection

class Magazine:
    def __init__(self, id=None, name=None, category="General"):
        if not isinstance(name, str) or not (2 <= len(name) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        if not isinstance(category, str) or len(category) == 0:
            raise ValueError("Category must be a non-empty string.")
        
        self._id = id
        self._name = name
        self._category = category
        
        if id is None:
            self.save()

    def save(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            if self._id is None:
                cursor.execute(
                    "INSERT INTO magazines (name, category) VALUES (?, ?)",
                    (self._name, self._category),
                )
                self._id = cursor.lastrowid
            else:
                cursor.execute(
                    "UPDATE magazines SET name = ?, category = ? WHERE id = ?",
                    (self._name, self._category, self._id),
                )


    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        if self._name != value:  
            self._name = value
            self.save()

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string.")
        if self._category != value: 
            self._category = value
            self.save()

    def articles(self):
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, author_id, magazine_id
                FROM articles
                WHERE magazine_id = ?
            """, (self._id,))
            rows = cursor.fetchall()
            return rows 


    def contributors(self):
        with get_db_connection() as conn:
         cursor = conn.cursor()
         cursor.execute("""
             SELECT DISTINCT a.id, a.name
             FROM authors a
             JOIN articles ar ON a.id = ar.author_id
             WHERE ar.magazine_id = ?
         """, (self._id,))
         rows = cursor.fetchall()
         return rows
                
   