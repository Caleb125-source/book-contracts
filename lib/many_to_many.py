# Many-to-Many: Book Contracts
#
# Models a publishing system where:
#   - An Author can have many Books through Contracts
#   - A Book can have many Authors through Contracts
#   - Contract is the JOIN model bridging Author <-> Book
#
# All three classes live in this single module so that
# test_many_to_many.py can import them from one place:
#   from many_to_many import Author, Book, Contract


# Author Class
# Represents a book author in the system.
# An Author can be linked to many Books via Contracts.
class Author:

    # Class-level registry — every Author instance is appended here
    all = []

    def __init__(self, name):
        # Property setter runs type validation before value is stored
        self.name = name
        Author.all.append(self)  # register this instance globally

    # ----------------------------------------------------------
    # Property: name
    # Enforces that name must be a non-empty string.
    # Raises Exception immediately if an invalid value is passed.
    # ----------------------------------------------------------
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise Exception("Name must be a string.")
        if len(value.strip()) == 0:
            raise Exception("Name must not be empty.")
        self._name = value

    # ----------------------------------------------------------
    # contracts()
    # Scans the global Contract.all registry and returns every
    # Contract where this Author instance is the associated author.
    # Uses identity check (is) not equality (==) to be precise.
    # ----------------------------------------------------------
    def contracts(self):
        return [c for c in Contract.all if c.author is self]

    # ----------------------------------------------------------
    # books()
    # Traverses the many-to-many bridge:
    #   Author -> Contract -> Book
    # Uses contracts() as the intermediary to reach Book objects.
    # ----------------------------------------------------------
    def books(self):
        return [c.book for c in self.contracts()]

    # ----------------------------------------------------------
    # sign_contract(book, date, royalties)
    # Convenience method: creates and returns a new Contract
    # linking this Author to the given Book.
    # All validation is handled inside Contract.__init__ via
    # its property setters, so no duplicate checks needed here.
    # ----------------------------------------------------------
    def sign_contract(self, book, date, royalties):
        return Contract(self, book, date, royalties)

    # ----------------------------------------------------------
    # total_royalties()
    # Sums the royalties field across all of this author's
    # contracts. Returns 0 if the author has no contracts yet.
    # ----------------------------------------------------------
    def total_royalties(self):
        return sum(c.royalties for c in self.contracts())

    def __repr__(self):
        return f"<Author name='{self.name}'>"


# Book Class
# Represents a published book in the system.
# A Book can be linked to many Authors via Contracts.
class Book:

    # Class-level registry — every Book instance is appended here
    # so Contract queries can scan all books when needed
    all = []

    def __init__(self, title):
        # Property setter runs type validation before value is stored
        self.title = title
        Book.all.append(self)   # register this instance globally

    # ----------------------------------------------------------
    # Property: title
    # Enforces that title must be a non-empty string.
    # Raises Exception immediately if an invalid value is passed.
    # ----------------------------------------------------------
    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str):
            raise Exception("Title must be a string.")
        if len(value.strip()) == 0:
            raise Exception("Title must not be empty.")
        self._title = value

    # ----------------------------------------------------------
    # contracts()
    # Scans the global Contract.all registry and returns every
    # Contract where this Book instance is the associated book.
    # Uses identity check (is) not equality (==) to be precise.
    # ----------------------------------------------------------
    def contracts(self):
        return [c for c in Contract.all if c.book is self]

    # ----------------------------------------------------------
    # authors()
    # Traverses the many-to-many bridge:
    #   Book -> Contract -> Author
    # Uses contracts() as the intermediary to reach Author objects.
    # ----------------------------------------------------------
    def authors(self):
        return [c.author for c in self.contracts()]

    def __repr__(self):
        return f"<Book title='{self.title}'>"

# Contract Class
# The JOIN model that creates the many-to-many relationship
# between Author and Book.
# Every Contract belongs to exactly ONE Author and ONE Book,
# but an Author can appear in many Contracts and so can a Book.
class Contract:

    # Class-level registry — every Contract instance is appended here.
    # This is the single source of truth that both Author.contracts()
    # and Book.contracts() filter against.
    all = []

    def __init__(self, author, book, date, royalties):
        # Each property setter validates its type before storing.
        # If any value is invalid, an Exception is raised immediately
        # and the Contract is never added to Contract.all.
        self.author    = author       # must be an Author instance
        self.book      = book         # must be a Book instance
        self.date      = date         # must be a str
        self.royalties = royalties    # must be an int
        Contract.all.append(self)     # only reached if all validation passes

    # ----------------------------------------------------------
    # Property: author
    # Validates that the value is an instance of Author.
    # Raises Exception for strings, None, or any other type.
    # ----------------------------------------------------------
    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, Author):
            raise Exception("author must be an instance of the Author class.")
        self._author = value

    # ----------------------------------------------------------
    # Property: book
    # Validates that the value is an instance of Book.
    # Raises Exception for strings, None, or any other type.
    # ----------------------------------------------------------
    @property
    def book(self):
        return self._book

    @book.setter
    def book(self, value):
        if not isinstance(value, Book):
            raise Exception("book must be an instance of the Book class.")
        self._book = value

    # ----------------------------------------------------------
    # Property: date
    # Validates that date is stored as a string.
    # Accepts any string format e.g. "01/01/2001" or "2001-01-01".
    # Raises Exception for integers, None, or any other type.
    # ----------------------------------------------------------
    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, value):
        if not isinstance(value, str):
            raise Exception("date must be a string.")
        self._date = value

    # ----------------------------------------------------------
    # Property: royalties
    # Validates that royalties is stored as an integer.
    # Note: booleans are a subclass of int in Python, so we
    # explicitly exclude them to prevent accidental misuse.
    # Raises Exception for strings, floats, or any other type.
    # ----------------------------------------------------------
    @property
    def royalties(self):
        return self._royalties

    @royalties.setter
    def royalties(self, value):
        if isinstance(value, bool) or not isinstance(value, int):
            raise Exception("royalties must be an integer.")
        self._royalties = value

    # ----------------------------------------------------------
    # Class Method: contracts_by_date(date)
    # Scans Contract.all and returns every contract whose date
    # exactly matches the date string passed as the argument.
    # Preserves insertion order so results are deterministic.
    # Called on the class directly: Contract.contracts_by_date(...)
    # ----------------------------------------------------------
    @classmethod
    def contracts_by_date(cls, date):
        return [c for c in cls.all if c.date == date]

    def __repr__(self):
        return (
            f"<Contract author='{self.author.name}' "
            f"book='{self.book.title}' "
            f"date='{self.date}' "
            f"royalties={self.royalties}>"
        )