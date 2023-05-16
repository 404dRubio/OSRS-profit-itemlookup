# OSRS Item Searcher
This program is an OSRS (Old School RuneScape) Item Searcher that allows users to search for items and find the most profitable items to flip in the game. It fetches item data and prices from a RuneScape Wiki API and provides a graphical user interface (GUI) for easy interaction. 

(Does not account for recent in-game Tax change)

# Features
* Search for items by name or ID: Users can enter an item name or ID to search for and retrieve information about the item, including its ID, name, margin (difference between high and low prices), and average price.
* Find top profitable items: Users can specify the number of top profitable items they want to find, and the program will display a list of the most profitable items based on their margins.
* Save search results: Users can save the search results or top items to a text file for future reference.
* User-friendly GUI: The program provides a graphical user interface that makes it easy to interact with and navigate between different functionalities.

# Dependencies
This program uses the following dependencies:

* 'tkinter': The standard Python interface to the Tk GUI toolkit.
* 'requests': A library for making HTTP requests to fetch data from the RuneScape Wiki API.

Please make sure you have these dependencies installed before running the program.

# How to Use

1. Run the program: Execute the program in a Python environment.
2. Menu page: Upon running the program, a menu page will be displayed with the following options:
               
      * **Search Item**: Clicking this button will open the search item page.
      * **Top Profitable Items**: Clicking this button will open the top profitable items page.
3. Search Item page: In the search item page, you can search for items by entering their name or ID. Follow these steps:
      * Enter an item name or ID in the search entry field.
      * Click the **Search** button to initiate the search.
      * The search results will be displayed in the scrolled text widget below the search button.
      * To save the search results, click the **Save Items** button.
      * To go back to the menu page, click the **Back to Menu** button.
4. Top Profitable Items page: In the top profitable items page, you can find the most profitable items by specifying the number of top items. Follow these steps:
      * Enter the number of top items you want to find in the entry field.
      * Click the **Find Top Items** button to retrieve the top profitable items.
      * The top items will be displayed in the scrolled text widget below the search button.
      * To save the top items, click the **Save Items** button.
      * To go back to the menu page, click the **Back to Menu** button.
5. Saving items: When you click the **Save Items** button, the search results or top items will be saved to a text file named "saved_items.txt". You will receive a message indicating the success or failure of the save operation.

Note: that this program does **not** account for recent in-game tax changes. Be aware that the calculations in the program may not reflect the most current values. It's **recommended** to double-check the in-game tax rates before making any significant decisions based on the program's output.

Note: The program relies on fetching data from the RuneScape Wiki API, so an internet connection is required for it to function properly.
