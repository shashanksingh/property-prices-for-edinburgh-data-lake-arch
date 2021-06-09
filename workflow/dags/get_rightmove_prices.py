import rightmove_webscraper

rightmove_url = "https://www.rightmove.co.uk/property-for-sale/find.html?searchType=SALE&locationIdentifier=REGION%5E94346"
EXECUTION_DATE = "2021-08-09/"
DATA_FOLDER = "data/"
TABLE_NAME = "bronze_property"

rm = rightmove_webscraper.rightmove_data(rightmove_url)
df_property_prices = rm.get_results
df_property_prices.to_csv(f"{DATA_FOLDER}{EXECUTION_DATE}{TABLE_NAME}")