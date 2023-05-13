import tkinter as tk
from tkinter import messagebox
import requests


class Item:
    def __init__(self, id, name, high, low):
        self.id = id
        self.name = name
        self.high = high
        self.low = low

    def margin(self):
        if self.high is not None and self.low is not None:
            return self.high - self.low
        else:
            return None


class PriceScraper:
    def __init__(self):
        self.headers = {
            "User-Agent": "Project for school, Getting price data and finding most profitable items to flip in game. Thank you for this service! Please contact LivingAbortion#2463 via discord if the frequency of requests is unreasonable "
        }
        self.mapping_url = "https://prices.runescape.wiki/api/v1/osrs/mapping"
        self.prices_url = "https://prices.runescape.wiki/api/v1/osrs/latest"

    def fetch_data(self):
        item_map = {}
        mapping_response = requests.get(self.mapping_url, headers=self.headers)
        mapping_data = mapping_response.json()
        for item in mapping_data:
            item_map[int(item["id"])] = item["name"]

        prices_response = requests.get(self.prices_url, headers=self.headers)
        prices_data = prices_response.json()

        return item_map, prices_data


class ItemSearcher:
    def __init__(self, item_map, prices_data):
        self.item_map = item_map
        self.prices_data = prices_data

    def find_item(self, search_term):
        # Check if search term is an integer, indicating an item ID search
        try:
            item_id = int(search_term)
            if item_id in self.prices_data["data"]:
                data = self.prices_data["data"][str(item_id)]
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
        return sorted(matches, key=lambda x: x["margin"], reverse=True)

    def find_top_profitable_items(self, num_items):
        items = []
        for item_id, data in self.prices_data["data"].items():
            name = self.item_map.get(int(item_id), "Unknown")
            high = data.get("high")
            low = data.get("low")
            if high is not None and low is not None:
                items.append(Item(item_id, name, high, low))

        sorted_items = sorted(items, key=lambda x: x.margin(), reverse=True)
        return sorted_items[:num_items]

    def calculate_average_price(self, high, low):
        return (high + low) // 2


class GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("OSRS Item Search")
        self.window.geometry("500x500")

        self.price_scraper = PriceScraper()
        self.item_map, self.prices_data = self.price_scraper.fetch_data()
        self.searcher = ItemSearcher(self.item_map, self.prices_data)

        self.create_menu_page()

    def create_menu_page(self):
        menu_frame = tk.Frame(self.window, bg="gray")
        menu_frame.pack(fill=tk.BOTH, expand=True)

        search_button = tk.Button(
            menu_frame,
            text="Search Item",
            command=self.open_search_item_page,
            bg="blue",
            fg="white",
        )
        search_button.pack(pady=20)

        top_items_button = tk.Button(
            menu_frame,
            text="Top Profitable Items",
            command=self.open_top_items_page,
            bg="blue",
            fg="white",
        )
        top_items_button.pack(pady=10)

    def open_search_item_page(self):
        menu_frame = self.window.pack_slaves()[0]
        menu_frame.pack_forget()

        search_frame = tk.Frame(self.window, bg="gray")
        search_frame.pack(fill=tk.BOTH, expand=True)

        search_label = tk.Label(
            search_frame, text="Enter an item name or ID:", font=("Arial", 12)
        )
        search_label.pack(pady=10)

        search_entry = tk.Entry(search_frame, font=("Arial", 12))
        search_entry.pack(pady=10)

        search_button = tk.Button(
            search_frame,
            text="Search",
            command=lambda: self.search_item(search_entry.get()),
            bg="blue",
            fg="white",
        )
        search_button.pack(pady=10)

        back_button = tk.Button(
            search_frame,
            text="Back to Menu",
            command=self.back_to_menu,
            bg="blue",
            fg="white",
        )
        back_button.pack(pady=10)

    def open_top_items_page(self):
        menu_frame = self.window.pack_slaves()[0]
        menu_frame.pack_forget()

        top_items_frame = tk.Frame(self.window, bg="gray")
        top_items_frame.pack(fill=tk.BOTH, expand=True)

        num_items_label = tk.Label(
            top_items_frame, text="Enter the number of top items:", font=("Arial", 12)
        )
        num_items_label.pack(pady=10)

        num_items_entry = tk.Entry(top_items_frame, font=("Arial", 12))
        num_items_entry.pack(pady=10)

        top_items_button = tk.Button(
            top_items_frame,
            text="Find Top Items",
            command=lambda: self.find_top_items(num_items_entry.get()),
            bg="blue",
            fg="white",
        )
        top_items_button.pack(pady=10)

        back_button = tk.Button(
            top_items_frame,
            text="Back to Menu",
            command=self.back_to_menu,
            bg="blue",
            fg="white",
        )
        back_button.pack(pady=10)

    def search_item(self, search_term):
        results = self.searcher.find_item(search_term)
        if len(results) == 0:
            messagebox.showinfo("Search Result", "No results found.")
        else:
            result_text = ""
            for result in results:
                result_text += f"{result['name']} (ID: {result['id']}) - Margin: {result['margin']:,}, Average Price: {result['average_price']:,}\n"
            messagebox.showinfo("Search Result", result_text)

    def find_top_items(self, num_items):
        top_items = self.searcher.find_top_profitable_items(int(num_items))
        if len(top_items) == 0:
            messagebox.showinfo("Top Items", "No top items found.")
        else:
            top_items_text = ""
        for item in top_items:
            top_items_text += f"{item.name} (ID: {item.id}) - Margin: {item.margin():,}, Average Price: {self.searcher.calculate_average_price(item.high, item.low):,}\n"
        messagebox.showinfo("Top Items", top_items_text)

    def back_to_menu(self):
        self.clear_window()
        self.create_menu_page()

    def clear_window(self):
        for widget in self.window.pack_slaves():
            widget.pack_forget()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    gui = GUI()
    gui.run()

