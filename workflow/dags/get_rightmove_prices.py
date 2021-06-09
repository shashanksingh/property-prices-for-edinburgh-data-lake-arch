import rightmove_webscraper

rightmove_url = "https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E94346"

rm = rightmove_webscraper.rightmove_data(rightmove_url)
df_property_prices = rm.get_results
df_property_prices.to_csv("bronze_property")