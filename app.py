from database.setup import create_tables
from database.connection import get_db_connection
from models.article import Article
from models.author import Author
from models.magazine import Magazine

def main():
    # Initialize the database and create tables
    create_tables()
    # Collect user input
    author_name = input("Enter author's name: ")
    magazine_name = input("Enter magazine name: ")
    magazine_category = input("Enter magazine category: ")
    article_title = input("Enter article title: ")
    article_content = input("Enter article content: ")

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()
    # Create an author
    author = Author(name=author_name)

    # Create a magazine
    magazine = Magazine(name=magazine_name, category=magazine_category)

    # Create an article
    article = Article(title=article_title, author=author, magazine=magazine)


    # Update the article content
    article.insert_article_content(article_content)
    conn.commit()

    # Query the database for inserted records.
    cursor.execute('SELECT * FROM magazines')
    magazines = cursor.fetchall()

    cursor.execute('SELECT * FROM authors')
    authors = cursor.fetchall()

    cursor.execute('SELECT * FROM articles')
    articles = cursor.fetchall()

    # Delete an article
    cursor.execute('DELETE FROM articles WHERE id = 1')
    conn.commit()
    conn.close()

    # Display results
    print("\nMagazines:")
    for mag in magazines:
        print(Magazine(mag[0], mag[1], mag[2]))

    print("\nAuthors:")
    for auth in authors:
        print(Author(auth[0], auth[1]))

    # print("\nArticles:")
    # for art in articles:
    #     print(Article(art[0], art[1], auth=Author(art[3]), mag=Magazine(art[4])))

if __name__ == "__main__":
    main()
