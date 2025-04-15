import tkinter as tk
import pandas as pd
from PIL import Image, ImageTk

# Load the dataset
df = pd.read_csv("Books.csv")

# Create the main window
window = tk.Tk()
window.title("TBIR System")
window.geometry("800x600")  # Set the window size
window.configure(bg="#f0f0f0")  # Set background color

# Create a frame for input fields
input_frame = tk.Frame(window, bg="#f0f0f0")
input_frame.pack(pady=10, padx=10, fill='x')

# Create input fields for book information
fields_left = ["Title", "Author", "Description", "Category"]
fields_right = ["Publisher", "Price Starting With ($)", "Publish Date (Month)", "Publish Date (Year)"]
entries = {}

# Place fields in the left column
for i, field in enumerate(fields_left):
    label = tk.Label(input_frame, text=f"{field}:", bg="#f0f0f0", font=("Arial", 12))
    label.grid(row=i, column=0, padx=10, pady=5, sticky="e")
    entry = tk.Entry(input_frame, font=("Arial", 12))
    entry.grid(row=i, column=1, padx=10, pady=5, sticky="w")
    entries[field] = entry

# Place fields in the right column
for i, field in enumerate(fields_right):
    label = tk.Label(input_frame, text=f"{field}:", bg="#f0f0f0", font=("Arial", 12))
    label.grid(row=i, column=2, padx=10, pady=5, sticky="e")
    entry = tk.Entry(input_frame, font=("Arial", 12))
    entry.grid(row=i, column=3, padx=10, pady=5, sticky="w")
    entries[field] = entry

# Create a button to trigger the search
search_button = tk.Button(window, text="Search", command=lambda: search_books(), font=("Arial", 12, "bold"), bg="#4CAF50", fg="white")
search_button.pack(pady=10)

# Create a frame for displaying book information
display_frame = tk.Frame(window, bg="#f0f0f0")
display_frame.pack(pady=10, padx=10, fill='both', expand=True)

# Create a label to display the image
image_label = tk.Label(display_frame, bg="#f0f0f0")
image_label.pack(pady=10)

# Create a frame for the text widget and scrollbar
text_frame = tk.Frame(display_frame, bg="#f0f0f0")
text_frame.pack(pady=10, fill='both', expand=True)

# Create a text widget to display book information
info_text = tk.Text(text_frame, height=10, width=60, font=("Arial", 12), bg="#ffffff", fg="#333333", wrap='word')
info_text.pack(side='left', fill='both', expand=True)

# Create a scrollbar for the text widget
scrollbar = tk.Scrollbar(text_frame, command=info_text.yview)
scrollbar.pack(side='right', fill='y')
info_text.config(yscrollcommand=scrollbar.set)

# Create a button to display the next book
next_button = tk.Button(window, text="Next", command=lambda: show_next_book(), font=("Arial", 12, "bold"), bg="#2196F3", fg="white")
next_button.pack(pady=10)

# Initialize variables for book display
results = None
current_index = 0

def search_books():
    """Searches the dataset based on user input and displays results."""
    global results, current_index

    # Get user input
    title = entries["Title"].get()
    author = entries["Author"].get()
    description = entries["Description"].get()
    category = entries["Category"].get()
    publisher = entries["Publisher"].get()
    price = entries["Price Starting With ($)"].get()
    month = entries["Publish Date (Month)"].get()
    year = entries["Publish Date (Year)"].get()

    # Search the dataset
    results = df[
        (df["Title"].str.contains(title, case=False, na=False)) &
        (df["Authors"].str.contains(author, case=False, na=False)) &
        (df["Description"].str.contains(description, case=False, na=False)) &
        (df["Category"].str.contains(category, case=False, na=False)) &
        (df["Publisher"].str.contains(publisher, case=False, na=False)) &
        (df["Price Starting With ($)"].astype(str).str.startswith(price, na=False)) &
        (df["Publish Date (Month)"].astype(str).str.contains(month, case=False, na=False)) &
        (df["Publish Date (Year)"].astype(str).str.contains(year, case=False, na=False))
    ]

    current_index = 0
    show_next_book()

def show_next_book():
    """Displays the next book in the results."""
    global current_index
    if results is not None:
        if current_index < len(results):
            image_path = results.iloc[current_index]["Path"]
            img = Image.open(image_path)
            # Resize the image
            img = img.resize((200, 200))  # Set desired width and height
            photo = ImageTk.PhotoImage(img)
            image_label.config(image=photo)
            image_label.image = photo  # Keep a reference to avoid garbage collection

            # Display book information
            book_info = results.iloc[current_index]
            info_text.delete(1.0, tk.END)  # Clear previous text
            info_text.insert(tk.END, f"Title: {book_info['Title']}\n")
            info_text.insert(tk.END, f"Author: {book_info['Authors']}\n")
            info_text.insert(tk.END, f"Description: {book_info['Description']}\n")
            info_text.insert(tk.END, f"Category: {book_info['Category']}\n")
            info_text.insert(tk.END, f"Publisher: {book_info['Publisher']}\n")
            info_text.insert(tk.END, f"Price: ${book_info['Price Starting With ($)']}\n")
            info_text.insert(tk.END, f"Publish Date: {book_info['Publish Date (Month)']} {book_info['Publish Date (Year)']}\n")

            current_index += 1
        elif len(results) == 1:
            # Only one book found
            tk.messagebox.showinfo("Information", "Only one book found!")
        else:
            # No more books to show
            tk.messagebox.showinfo("Information", "No more books to show!")
    else:
        # No results found
        tk.messagebox.showinfo("Information", "No books found!")

# Run the GUI
window.mainloop()
