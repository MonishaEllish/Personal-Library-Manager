import json
import os
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

LIBRARY_FILE = "library.txt"

def load_library():
    """Loads the library from a file or creates an empty one if missing/corrupt."""
    if not os.path.exists(LIBRARY_FILE):
        return []

    try:
        with open(LIBRARY_FILE, "r") as file:
            data = file.read().strip()
            return json.loads(data) if data else []
    except json.JSONDecodeError:
        print(Fore.RED + "❌ Error: library.txt is corrupted. Resetting file.")
        return []

def save_library(library):
    """Saves the library to a file."""
    with open(LIBRARY_FILE, "w") as file:
        json.dump(library, file, indent=4)

def add_book(library):
    """Adds a new book to the library."""
    title = input(Fore.BLUE + "📖 Enter the book title: ").strip()
    author = input(Fore.BLUE + "✍️ Enter the author: ").strip()
    year = input(Fore.BLUE + "📅 Enter the publication year: ").strip()
    genre = input(Fore.BLUE + "🎭 Enter the genre: ").strip()
    read_status = input(Fore.BLUE + "✅ Have you read this book? (yes/no): ").strip().lower() == "yes"

    book = {"Title": title, "Author": author, "Year": year, "Genre": genre, "Read": read_status}
    library.append(book)
    save_library(library)

    print(Fore.GREEN + "📚 Book added successfully!")

def remove_book(library):
    """Removes a book from the library."""
    title = input(Fore.RED + "🗑️ Enter the title of the book to remove: ").strip()
    for book in library:
        if book["Title"].lower() == title.lower():
            library.remove(book)
            save_library(library)
            print(Fore.GREEN + f"✅ '{title}' removed successfully!")
            return
    print(Fore.RED + "❌ Book not found.")

def search_book(library):
    """Searches for a book by title or author."""
    print(Fore.YELLOW + "\n🔎 Search by: ")
    print("1. Title")
    print("2. Author")
    choice = input(Fore.YELLOW + "Enter your choice (1 or 2): ").strip()

    if choice == "1":
        keyword = input(Fore.BLUE + "📖 Enter the title: ").strip().lower()
        results = [book for book in library if keyword in book["Title"].lower()]
    elif choice == "2":
        keyword = input(Fore.BLUE + "✍️ Enter the author: ").strip().lower()
        results = [book for book in library if keyword in book["Author"].lower()]
    else:
        print(Fore.RED + "❌ Invalid choice.")
        return

    if results:
        print(Fore.GREEN + "\n📚 Matching Books:")
        for book in results:
            status = "✅ Read" if book["Read"] else "📖 Unread"
            print(f"- {book['Title']} by {book['Author']} ({book['Year']}) - {book['Genre']} - {status}")
    else:
        print(Fore.RED + "❌ No matching books found.")

def display_books(library):
    """Displays all books in the library."""
    if not library:
        print(Fore.RED + "📭 Your library is empty.")
        return

    print(Fore.MAGENTA + "\n📚 Your Library:")
    for index, book in enumerate(library, start=1):
        status = "✅ Read" if book["Read"] else "📖 Unread"
        print(f"{index}. {book['Title']} by {book['Author']} ({book['Year']}) - {book['Genre']} - {status}")

def display_statistics(library):
    """Displays statistics: total books and percentage read."""
    total_books = len(library)
    if total_books == 0:
        print(Fore.RED + "📭 No books in library.")
        return

    read_books = sum(1 for book in library if book["Read"])
    percentage_read = (read_books / total_books) * 100

    print(Fore.CYAN + "\n📊 Library Statistics:")
    print(f"📚 Total books: {total_books}")
    print(f"✅ Percentage read: {percentage_read:.1f}%")

def main():
    """Main menu function."""
    library = load_library()

    while True:
        print(Fore.MAGENTA + "\n📖 Personal Library Manager 📖")
        print(Fore.CYAN + "1. Add a book")
        print(Fore.CYAN + "2. Remove a book")
        print(Fore.CYAN + "3. Search for a book")
        print(Fore.CYAN + "4. Display all books")
        print(Fore.CYAN + "5. Display statistics")
        print(Fore.CYAN + "6. Exit")

        choice = input(Fore.YELLOW + "Enter your choice: ").strip()

        if choice == "1":
            add_book(library)
        elif choice == "2":
            remove_book(library)
        elif choice == "3":
            search_book(library)
        elif choice == "4":
            display_books(library)
        elif choice == "5":
            display_statistics(library)
        elif choice == "6":
            print(Fore.GREEN + "\n📂 Library saved. Goodbye!")
            save_library(library)
            break
        else:
            print(Fore.RED + "❌ Invalid choice. Please enter a number from 1-6.")

if __name__ == "__main__":
    main()
