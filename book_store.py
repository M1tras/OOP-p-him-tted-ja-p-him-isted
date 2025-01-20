class Book:
    """Represent book model."""

    def __init__(self, title: str, author: str, price: float, rating: float):
        """
        Class constructor. Each book has title, author, price, and rating.

        :param title: book's title
        :param author: book's author
        :param price: book's price
        :param rating: book's rating
        """
        self.title = title
        self.author = author
        self.price = price
        self.rating = rating


class Store:
    """Represent book store model."""

    def __init__(self, name: str, rating: float):
        """
        Class constructor.

        Each book store has a name and rating.
        There also should be an overview of all books present in the store.

        :param name: book store name
        :param rating: book store's rating
        """
        self.name = name
        self.rating = rating
        self.books_in_store = []

    def can_add_book(self, book: Book) -> bool:
        """
        Check if a book can be added.

        It is possible to add a book to the bookstore if:
        1. The book with the same author and title is not yet present in this bookstore.
        2. The book's own rating is >= the store's rating.

        :return: bool
        """
        for existing_book in self.books_in_store:
            if existing_book.title == book.title and existing_book.author == book.author:
                return False
        if book.rating < self.rating:
            return False
        return True

    def add_book(self, book: Book):
        """
        Add new book to book store if possible.

        :param book: Book
        Function does not return anything
        """
        if self.can_add_book(book):
            self.books_in_store.append(book)

    def can_remove_book(self, book: Book) -> bool:
        """
        Check if book can be removed from store.

        Book can be successfully removed if it is actually present in store

        :return: bool
        """
        return book in self.books_in_store

    def remove_book(self, book: Book):
        """
        Remove book from store if possible.

        Function does not return anything
        """
        if self.can_remove_book(book):
            self.books_in_store.remove(book)

    def get_all_books(self) -> list:
        """
        Return a list of all books in current store.

        :return: list of Book objects
        """
        return self.books_in_store

    def get_books_by_price(self) -> list:
        """
        Return a list of books ordered by price (from cheapest).

        :return: list of Book objects
        """
        return sorted(self.books_in_store, key=lambda book: book.price)

    def get_most_popular_book(self) -> list:
        """
        Return a list of book (books) with the highest rating.

        :return: list of Book objects
        """
        if not self.books_in_store:
            return []
        highest_rating = max(book.rating for book in self.books_in_store)
        return [book for book in self.books_in_store if book.rating == highest_rating]
