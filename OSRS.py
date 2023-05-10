import requests

# The API site requested we make a user-agent to let them know what it is being used for
headers = {
    "User-Agent": "Project for school, Getting price data and finding most proffitable items to flip in game. Thank you for this service! Please contact ----- via discord if the frequency of requests is unreasonable "
}
# Get item IDs and names from mapping API
mapping_url = "https://prices.runescape.wiki/api/v1/osrs/mapping"
mapping_response = requests.get(mapping_url, headers=headers)
mapping_data = mapping_response.json()
item_map = {int(item["id"]): item["name"] for item in mapping_data}

# Get item prices from price API
prices_url = "https://prices.runescape.wiki/api/v1/osrs/latest"
prices_response = requests.get(prices_url, headers=headers)
prices_data = prices_response.json()

# Calculate profit margins, some values in the json have no price data, so we check for that here
profit_margins = {}  # create empty dictionary to store profit margins
for item_id, data in prices_data["data"].items():
    high = data["high"]
    low = data["low"]
    if high is not None and low is not None:
        margin = high - low
        name = item_map.get(int(item_id), "Unknown")
        profit_margins[item_id] = {"name": name, "margin": margin}

# Sort items by profit margin and print top x
sorted_items = sorted(
    profit_margins.items(), key=lambda x: x[1]["margin"], reverse=True
)
for item_id, data in sorted_items[:10]:  # adjust to amount you want to see atm
    name = data["name"]
    margin = data["margin"]
    print(f"{name} (ID: {item_id}) - Margin: {margin}")
