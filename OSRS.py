import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
import requests


class Item:
    def __init__(self, id, name, high, low):
        # Initialize the Item object with it's attributes
        self.id = id  # ID of the item
        self.name = name  # Name of the item
        self.high = high  # High price of the item
        self.low = low  # Low price of the item

    def margin(self):
        # Calculate the margin (difference between high and low prices) of the item
        if self.high is not None and self.low is not None:
            return self.high - self.low  # Return the margin


class PriceScraper:
    headers = {  # The API site asked that we make a "user-agent" so that they know what the API is being used for
        "User-Agent": "Personal project, Getting price data and finding most profitable items to flip in game. Thank you for this service! Please contact ----# via discord if the frequency of requests is unreasonable "
    }
    mapping_url = "https://prices.runescape.wiki/api/v1/osrs/mapping"
    prices_url = "https://prices.runescape.wiki/api/v1/osrs/latest"

    def fetch_data(self):
        item_map = {}  # Dictionary to store item mapping data (item ID to name)

        # Fetch the mapping data from the API, we use our custom header to add that information from before
        mapping_response = requests.get(self.mapping_url, headers=self.headers)
        mapping_data = mapping_response.json()

        # Extract item mapping data and store it in the item_map dictionary
        for item in mapping_data:
            item_map[int(item["id"])] = item["name"]

        # Fetch the latest prices data from the API, we use our custom header to add that information from before
        prices_response = requests.get(self.prices_url, headers=self.headers)
        prices_data = prices_response.json()

        # Return the item mapping data (item_map) and prices data (prices_data)
        return item_map, prices_data


class ItemSearcher:
    def __init__(self, item_map, prices_data):
        # Initialize the ItemSearcher object with item mapping data and prices data
        self.item_map = item_map  # Dictionary containing item ID to name mapping
        self.prices_data = prices_data  # Data containing prices information

    def find_item(self, search_term):
        # Check if search term is an integer, indicating an item ID search
        try:
            item_id = int(search_term)
            if item_id in self.prices_data["data"]:
                data = self.prices_data["data"][str(item_id)]
                # Create a list with item details for the found item
                return [
                    {
                        "id": item_id,
                        "name": self.item_map.get(item_id, "Unknown"),
                        "margin": data["high"] - data["low"],
                        "average_price": self.calculate_average_price(
                            data["high"], data["low"]
                        ),
                    }
                ]
        except ValueError:
            pass

        # Search for items by name
        search_term = search_term.lower()
        matches = []
        for item_id, data in self.prices_data["data"].items():
            name = self.item_map.get(int(item_id), "Unknown")
            if search_term in name.lower():
                # Create a list with item details for each matching item
                matches.append(
                    {
                        "id": item_id,
                        "name": name,
                        "margin": data["high"] - data["low"],
                        "average_price": self.calculate_average_price(
                            data["high"], data["low"]
                        ),
                    }
                )
        # Sort the matching items based on margin in descending order
        return sorted(matches, key=lambda x: x["margin"], reverse=True)

    def find_top_profitable_items(self, num_items):
        items = []
        for item_id, data in self.prices_data["data"].items():
            name = self.item_map.get(int(item_id), "Unknown")
            high = data.get("high")
            low = data.get("low")
            if high is not None and low is not None:
                # Create an Item object for each item with available high and low prices
                items.append(Item(item_id, name, high, low))

        # Sort the items based on margin in descending order
        sorted_items = sorted(items, key=lambda x: x.margin(), reverse=True)
        # Return the top 'num_items' most profitable items
        return sorted_items[:num_items]

    def calculate_average_price(self, high, low):
        # Calculate and return the average price between the high and low prices
        return f"{(high + low) // 2:,}"


class GUI:
    def __init__(self):
        # Create the main window for the GUI
        self.window = tk.Tk()
        self.window.title("OSRS Item Searcher")
        self.window.geometry("700x800")
        self.window.configure(bg="gray")  # Set the background color of the window

        # Initialize the PriceScraper to fetch item data and create the ItemSearcher
        self.price_scraper = PriceScraper()
        self.item_map, self.prices_data = self.price_scraper.fetch_data()
        self.searcher = ItemSearcher(self.item_map, self.prices_data)

        self.menu_frame = None  # Store the reference to the menu frame

        self.create_menu_page()

    def create_menu_page(self):
        # Remove the previous menu frame, if it exists
        if self.menu_frame is not None:
            self.menu_frame.pack_forget()

        # Create the menu frame with a gray background
        self.menu_frame = tk.Frame(
            self.window, bg="gray"  # Set the background color of the menu frame
        )
        self.menu_frame.pack(fill=tk.BOTH, expand=True)

        # Add a title label to the menu frame
        title_label = tk.Label(
            self.menu_frame,
            text="OSRS Item Search",
            font=("Arial", 18, "bold"),
            bg="gray",  # Set the background color of the title label
            fg="white",
        )
        title_label.pack(pady=20)

        # Add a button to open the search item page
        search_button = tk.Button(
            self.menu_frame,
            text="Search Item",
            command=self.open_search_item_page,
            bg="blue",
            fg="white",
        )
        search_button.pack(pady=20)

        # Add a button to open the top profitable items page
        top_items_button = tk.Button(
            self.menu_frame,
            text="Top Profitable Items",
            command=self.open_top_items_page,
            bg="blue",
            fg="white",
        )
        top_items_button.pack(pady=10)

    def open_search_item_page(self):
        self.menu_frame.pack_forget()  # Remove the menu frame

        # Create a new frame for the search page
        search_frame = tk.Frame(self.window, bg="gray")
        search_frame.pack(fill=tk.BOTH, expand=True)

        # Create a label to display the instruction for the search input field
        search_label = tk.Label(
            search_frame,
            text="Enter an item name or ID:",
            font=("Arial", 18, "bold"),
            bg="gray",
            fg="white",
        )
        search_label.pack(pady=10)

        # Create an entry field where the user can enter the item name or ID to search for
        search_entry = tk.Entry(search_frame, font=("Arial", 12))
        search_entry.pack(pady=10)

        # Create a button to initiate the search when clicked
        search_button = tk.Button(
            search_frame,
            text="Search",
            command=lambda: self.search_item(search_entry.get(), search_text),
            bg="blue",
            fg="white",
        )
        search_button.pack(pady=10)

        # Create a button to save the search results when clicked
        save_button = tk.Button(
            search_frame,
            text="Save Items",
            command=lambda: self.save_items(search_text.get("1.0", tk.END)),
            bg="blue",
            fg="white",
        )
        save_button.pack(pady=10)

        # Create a button to go back to the menu page when clicked
        back_button = tk.Button(
            search_frame,
            text="Back to Menu",
            command=self.back_to_menu,
            bg="blue",
            fg="white",
        )
        back_button.pack(pady=10)

        # Create a scrolled text widget where the search results will be displayed
        search_text = scrolledtext.ScrolledText(
            search_frame,
            width=60,
            height=50,
            font=("Arial", 12),
            bg="gray",
        )
        search_text.pack(pady=10)

        # There was a bug where when you hovered over the text widget it would "dissapear" I think this was just hard to see with the gray background
        # These next binds fix that issue
        # Bind the "<Enter>" event (hovering the cursor over the search text widget) to change the cursor style to "arrow"
        search_text.bind("<Enter>", lambda _: search_text.config(cursor="arrow"))

        # Bind the "<Leave>" event (moving the cursor away from the search text widget) to remove the custom cursor style
        search_text.bind("<Leave>", lambda _: search_text.config(cursor=""))

    def open_top_items_page(self):
        self.menu_frame.pack_forget()  # Remove the menu frame

        # Create a new frame for the top items page with a gray background
        top_items_frame = tk.Frame(
            self.window, bg="gray"  # Set the background color of the top items frame
        )
        top_items_frame.pack(fill=tk.BOTH, expand=True)

        # Create a label to prompt the user to enter the number of top items
        num_items_label = tk.Label(
            top_items_frame,
            text="Enter the number of top items:",
            font=("Arial", 18, "bold"),
            bg="gray",
            fg="white",
        )
        num_items_label.pack(pady=10)

        # Create an entry field where the user can enter the number of top items
        num_items_entry = tk.Entry(top_items_frame, font=("Arial", 12))
        num_items_entry.pack(pady=10)

        # Create a button to find the top items when clicked
        top_items_button = tk.Button(
            top_items_frame,
            text="Find Top Items",
            command=lambda: self.find_top_items(num_items_entry.get(), top_items_text),
            bg="blue",
            fg="white",
        )
        top_items_button.pack(pady=10)

        # Create a button to save the search results when clicked
        save_button = tk.Button(
            top_items_frame,
            text="Save Items",
            command=lambda: self.save_items(num_items_entry.get()),
            bg="blue",
            fg="white",
        )
        save_button.pack(pady=10)

        # Create a button to go back to the menu page when clicked
        back_button = tk.Button(
            top_items_frame,
            text="Back to Menu",
            command=self.back_to_menu,
            bg="blue",
            fg="white",
        )
        back_button.pack(pady=10)

        # Create a scrolled text widget where the top items will be displayed
        top_items_text = scrolledtext.ScrolledText(
            top_items_frame, width=60, height=50, font=("Arial", 12), bg="gray"
        )
        top_items_text.pack(pady=10)

        # Bug fix for cursor
        top_items_text.bind("<Enter>", lambda _: top_items_text.config(cursor="arrow"))
        top_items_text.bind("<Leave>", lambda _: top_items_text.config(cursor=""))

    def search_item(self, search_term, search_text):
        # Find items based on the search term
        search_results = self.searcher.find_item(search_term)

        # Clear the search text widget
        search_text.delete("1.0", tk.END)

        # Check if any matching items were found
        if not search_results:
            search_text.insert(tk.END, "No matching items found.")
        else:
            # Display the details of each matching item in the search text widget
            for result in search_results:
                search_text.insert(
                    tk.END,
                    f"ID: {result['id']}\nName: {result['name']}\nMargin: {result['margin']:,}\nAverage Price: {result['average_price']}\n\n",
                )

    def find_top_items(self, num_items, top_items_text):
        try:
            num_items = int(num_items)

            # Find the top profitable items based on the number specified by the user
            top_items = self.searcher.find_top_profitable_items(num_items)

            # Clear the top items text widget
            top_items_text.delete("1.0", tk.END)

            # Check if any top items were found
            if not top_items:
                top_items_text.insert(tk.END, "No top items found.")
            else:
                # Display the details of each top item in the top items text widget
                for item in top_items:
                    average_price = self.searcher.calculate_average_price(
                        item.high, item.low
                    )
                    top_items_text.insert(
                        tk.END,
                        f"ID: {item.id}\nName: {item.name}\nHigh: {item.high:,}\nLow: {item.low:,}\nMargin: {item.margin():,}\nAverage Price: {average_price}\n\n",
                    )
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number.")

    def save_items(self, items):
        try:
            with open("saved_items.txt", "w") as file:
                file.write(items)
            messagebox.showinfo(
                "Items Saved", "The items have been saved to 'saved_items.txt'"
            )
        except Exception as e:
            messagebox.showerror(
                "Error", f"An error occurred while saving the items: {str(e)}"
            )

    def back_to_menu(self):
        # Get the reference to the current frame being displayed
        current_frame = self.window.pack_slaves()[0]

        # Remove the current frame from the window
        current_frame.pack_forget()

        # Create and display the menu page
        self.create_menu_page()

    def run(self):
        # Start the main event loop of the GUI application
        self.window.mainloop()


if __name__ == "__main__":
    # Create an instance of the GUI class
    gui = GUI()
    # Start the GUI application
    gui.run()

