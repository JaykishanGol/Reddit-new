# update_grid_replace.py
import sys
from bs4 import BeautifulSoup # Import BeautifulSoup for HTML parsing

# --- Configuration ---
INDEX_FILE = "index.html" # Name of your HTML file

# --- Helper Function to Create New Grid Item HTML ---
# (This function remains largely the same as before)
def create_grid_item_tag(soup_parser, title, reddit_link, poster_filename):
    """Creates a new BeautifulSoup Tag object for a grid item."""

    # Create the main div
    grid_item_div = soup_parser.new_tag("div", **{'class': 'grid-item'})

    # Create h2 element
    h2 = soup_parser.new_tag("h2")

    # Create link (a) element inside h2
    link = soup_parser.new_tag(
        "a",
        href=reddit_link,
        target="_blank",
        rel="noopener noreferrer"
    )
    link.string = title # Set the link text
    h2.append(link) # Add link to h2

    # Create image (img) element
    poster_id = title.lower().replace(" ", "-").replace(":", "") + "-poster"
    alt_text = f"Poster for {title}"
    placeholder_text = title.replace(" ", "+")
    onerror_handler = f"this.onerror=null; this.src='https://placehold.co/200x300/333333/eeeeee?text={placeholder_text}'; this.alt='Image not found'; console.error('Error loading image: {poster_filename}');"

    img = soup_parser.new_tag(
        "img",
        src=poster_filename,
        alt=alt_text,
        id=poster_id,
        **{'class': 'show-poster', 'onerror': onerror_handler}
    )

    # Append h2 and img to the main div
    grid_item_div.append(h2)
    grid_item_div.append(img)

    # Add newline characters for potentially better formatting (optional)
    # Note: BeautifulSoup might handle formatting differently when writing
    grid_item_div.insert(1, "\n            ") # Newline after opening div/before h2
    h2.insert(1, "\n                ") # Newline inside h2/before a
    h2.append("\n            ") # Newline inside h2/after a
    grid_item_div.insert(3, "\n            ") # Newline after h2/before img
    grid_item_div.append("\n        ") # Newline after img/before closing div

    return grid_item_div

# --- Main Script Logic ---
if __name__ == "__main__":
    print("--- Add New TV Show by Replacing First Empty Slot ---")

    # 1. Get input from user
    show_title = input("Enter TV Show Title: ")
    reddit_url = input("Enter Reddit Discussion URL: ")
    poster_file = input("Enter Poster Image Filename (e.g., show-poster.jpg): ")

    # Basic validation
    if not show_title or not reddit_url or not poster_file:
        print("Error: All fields are required.")
        sys.exit(1)

    try:
        # 2. Read the existing HTML file
        with open(INDEX_FILE, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 3. Parse the HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # 4. Find the FIRST empty grid item
        # Uses CSS selector: find a div with class 'grid-item' AND class 'empty'
        first_empty_div = soup.find('div', class_='grid-item empty')

        if not first_empty_div:
            print(f"Error: Could not find any '<div class=\"grid-item empty\"></div>' in {INDEX_FILE}.")
            print("Make sure you have empty placeholder divs remaining.")
            sys.exit(1)

        # 5. Create the new grid item HTML element (using the soup object for context)
        new_item_tag = create_grid_item_tag(soup, show_title, reddit_url, poster_file)

        # 6. Replace the empty div with the new item
        first_empty_div.replace_with(new_item_tag)
        print("Found the first empty div and replaced it.")

        # 7. Write the modified HTML back to the file
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            # Write the string representation; prettify() can sometimes mess up formatting
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
