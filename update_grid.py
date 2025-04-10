# update_grid.py
import sys
from bs4 import BeautifulSoup, Comment # Import BeautifulSoup for HTML parsing and Comment for finding the marker

# --- Configuration ---
INDEX_FILE = "index.html" # Name of your HTML file
INSERTION_COMMENT = "NEW_ITEM_INSERTION_POINT" # The comment marker in your HTML

# --- Helper Function to Create New Grid Item HTML ---
def create_grid_item(title, reddit_link, poster_filename):
    """Creates a new BeautifulSoup Tag object for a grid item."""

    # Create the main div
    grid_item_div = BeautifulSoup(features="html.parser").new_tag("div", **{'class': 'grid-item'})

    # Create h2 element
    h2 = BeautifulSoup(features="html.parser").new_tag("h2")

    # Create link (a) element inside h2
    link = BeautifulSoup(features="html.parser").new_tag(
        "a",
        href=reddit_link,
        target="_blank",
        rel="noopener noreferrer"
    )
    link.string = title # Set the link text
    h2.append(link) # Add link to h2

    # Create image (img) element
    # Generate a simple id based on the title
    poster_id = title.lower().replace(" ", "-").replace(":", "") + "-poster"
    # Generate alt text
    alt_text = f"Poster for {title}"
    # Generate placeholder text for onerror
    placeholder_text = title.replace(" ", "+")
    # Generate onerror handler
    onerror_handler = f"this.onerror=null; this.src='https://placehold.co/200x300/333333/eeeeee?text={placeholder_text}'; this.alt='Image not found'; console.error('Error loading image: {poster_filename}');"

    img = BeautifulSoup(features="html.parser").new_tag(
        "img",
        src=poster_filename,
        alt=alt_text,
        id=poster_id,
        **{'class': 'show-poster', 'onerror': onerror_handler} # Use dictionary for class attribute
    )

    # Append h2 and img to the main div
    grid_item_div.append(h2)
    grid_item_div.append(img)

    # Add newline characters for better formatting in the final HTML
    grid_item_div.insert(1, "\n        ") # Newline after opening div
    grid_item_div.insert(3, "\n            ") # Newline after opening h2
    grid_item_div.insert(5, "\n            ") # Newline after opening a
    grid_item_div.insert(7, "\n        ") # Newline after closing h2
    grid_item_div.insert(9, "\n        ") # Newline after opening img
    grid_item_div.append("\n    ") # Newline after closing div

    return grid_item_div

# --- Main Script Logic ---
if __name__ == "__main__":
    print("--- Add New TV Show to Grid ---")

    # 1. Get input from user
    show_title = input("Enter TV Show Title: ")
    reddit_url = input("Enter Reddit Discussion URL: ")
    poster_file = input("Enter Poster Image Filename (e.g., show-poster.jpg): ")

    # Basic validation
    if not show_title or not reddit_url or not poster_file:
        print("Error: All fields are required.")
        sys.exit(1) # Exit script with an error code

    try:
        # 2. Read the existing HTML file
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 3. Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # 4. Find the insertion point comment
        insertion_point = soup.find(string=lambda text: isinstance(text, Comment) and INSERTION_COMMENT in text)

        if not insertion_point:
            print(f"Error: Could not find the insertion point comment '{INSERTION_COMMENT}' in {INDEX_FILE}.")
            print("Please ensure the comment exists before the empty grid items.")
            sys.exit(1)

        # 5. Create the new grid item HTML element
        new_item = create_grid_item(show_title, reddit_url, poster_file)

        # 6. Insert the new item *before* the comment marker
        insertion_point.insert_before(new_item)
        # Add a newline before the new item for spacing
        insertion_point.insert_before("\n        ")


        # 7. Write the modified HTML back to the file
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            # Use prettify() for potentially better formatting, though it might alter existing spacing
            # f.write(soup.prettify())
            # Or write the string representation directly which usually preserves more original formatting
            f.write(str(soup))

        print("\nSuccess! index.html has been updated.")
        print(f"Remember to add '{poster_file}' to your Git repository.")
        print("Commit and push the changes to GitHub to deploy.")

    except FileNotFoundError:
        print(f"Error: {INDEX_FILE} not found in the current directory.")
        print("Make sure you are running this script in the same directory as your HTML file.")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

