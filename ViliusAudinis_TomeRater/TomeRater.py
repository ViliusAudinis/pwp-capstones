class User(object):

    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.books = {}

    def get_email(self):
        return self.email

    def change_email(self, address):
        self.email = address
        print("{name}'s email address has been changed to {email}".format(name = self.name, email = self.email))

    def read_book(self, book, rating = None):
        self.books[book] = rating

    def get_average_rating(self):
        sum = 0
        count_ratings = 0
        for rating in self.books.values():
            if rating != None:
                sum += rating
                count_ratings += 1
        return sum / count_ratings

    def __repr__(self):
        return "User {name}, e-mail: {address}, books read: {num_books}".format(name=self.name, address=self.email, num_books=len(self.books))

    def __eq__(self, other_user):
        return self.name == other_user.name and self.email == other_user.email


class Book(object):
    def __init__(self, title, isbn):
        self.title = title
        self.isbn = isbn
        self.ratings = []
    
    def get_title(self):
        return self.title

    def get_isbn(self):
        return self.isbn

    def set_isbn(self, isbn):
        self.isbn = isbn
        print("ISBN number has been changed to " + str(self.isbn))

    def add_rating(self, rating):

        # Only interested in ratings between 0 and 4 inclusive
        if rating > 0 or rating < 5:
            self.ratings.append(rating)
        else:
            print("Invalid Rating")

    def get_average_rating(self):
        if len(self.ratings) == 0:
            return None

        sum = 0
        for rating in self.ratings:
                sum += rating
        return sum/len(self.ratings)

    def __eq__(self, other_book):
        return self.title == other_book.title and self.isbn == other_book.isbn

    def __hash__(self):
        return hash((self.title, self.isbn))


class Fiction(Book):
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        self.author = author

    def get_author(self):
        return self.author

    def __repr__(self):
        return "{title} by {author}".format(title = self.title, author = self.author)


class Non_Fiction(Book):
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        self.subject = subject
        self.level = level

    def get_subject(self):
        return self.subject

    def get_level(self):
        return self.level

    def __repr__(self):
        return "{title}, a {level} manual on {subject}".format(title=self.title, level=self.level, subject=self.subject)


class TomeRater():
    def __init__(self):
        self.users = {}
        self.books = {}

    def create_book(self, title, isbn):
        return Book(title, isbn)
        
    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)

    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)
        
    def add_book_to_user(self, book, email, rating = None):
        if email not in self.users:
            print("No user with e-mail {email}!".format(email=email))
        else:
            self.users[email].read_book(book, rating)

            if rating != None:
                book.add_rating(rating)

            if book in self.books:
                self.books[book] += 1
            else:
                self.books[book] = 1

    def add_user(self, name, email, user_books = None):
        if email in self.users:
            print("Error: User already exists.")

        else:
            user = User(name, email)
            self.users[email] = user

            if user_books != None:
                for book in user_books:
                    self.add_book_to_user(book, email)

    def print_catalog(self):
        for book in self.books.keys():
            print(book)

    def print_users(self):
        for user in self.users.values():
            print(user)

    def most_read_book(self):
        return max(self.books, key = lambda key: self.books[key])
        
    def highest_rated_book(self):
        highest_rated = None
        highest_rating = 0

        for book in self.books.keys():
            rating = book.get_average_rating()

            if rating > highest_rating:
                highest_rated = book                
                highest_rating = rating

        return highest_rated

    def most_positive_user(self):
        positive_user = None
        highest_rating = 0

        for user in self.users.values():
            avg_user_rating = user.get_average_rating()

            if avg_user_rating > highest_rating:
                positive_user = user
                highest_rating = avg_user_rating
                
        return positive_user

    def get_n_most_read_books(self, n):
        sorted_by_value = sorted(self.books.items(), key = lambda k:k[1], reverse = True)
        return sorted_by_value[0:n]

    def get_n_most_prolific_readers(self, n):
        prolific_readers = []

        for email in self.users:
            books_read = len(self.users[email].books)
            prolific_readers.append((books_read, email))

        prolific_readers.sort(reverse = True)

        prolific_users = []

        # Avoiding index out of range issues
        if n > len(prolific_readers):
            for i in range(len(prolific_readers)):
                prolific_users.append(self.users[prolific_readers[i][1]])

            return prolific_users

        for i in range(n):
            prolific_users.append(self.users[prolific_readers[i][1]])

        return prolific_users