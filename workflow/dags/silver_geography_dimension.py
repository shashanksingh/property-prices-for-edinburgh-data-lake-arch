import glob
import os
import pandas as pd

EXECUTION_DATE = "2021-08-09/"
DATA_FOLDER = "data/silver/"
TABLE_NAME = "geography_dimension.parquet"


def run():
    columns = ["ID", "NAMES_URI", "NAME1", "NAME1_LANG", "NAME2", "NAME2_LANG", "TYPE", "LOCAL_TYPE", "GEOMETRY_X",
               "GEOMETRY_Y", "MOST_DETAIL_VIEW_RES", "LEAST_DETAIL_VIEW_RES", "MBR_XMIN", "MBR_YMIN", "MBR_XMAX",
               "MBR_YMAX",
               "POSTCODE_DISTRICT", "POSTCODE_DISTRICT_URI", "POPULATED_PLACE", "POPULATED_PLACE_URI",
               "POPULATED_PLACE_TYPE",
               "DISTRICT_BOROUGH", "DISTRICT_BOROUGH_URI", "DISTRICT_BOROUGH_TYPE", "COUNTY_UNITARY",
               "COUNTY_UNITARY_URI",
               "COUNTY_UNITARY_TYPE", "REGION", "REGION_URI", "COUNTRY", "COUNTRY_URI", "RELATED_SPATIAL_OBJECT",
               "SAME_AS_DBPEDIA",
               "SAME_AS_GEONAMES"
               ]

    files_to_read = glob.glob(os.path.join('', "data/bronze/2021-08-09/opname_csv_gb/DATA/SO*.csv"))

    df_bronze_geography = pd.concat(map(lambda file: pd.read_csv(file, dtype={
        "ID": str,
        "NAMES_URI": str,
        "NAME1": str,
        "NAME1_LANG": str,
        "NAME2": str,
        "NAME2_LANG": str,
        "TYPE": str,
        "LOCAL_TYPE": str,
        "GEOMETRY_X": int,
        "GEOMETRY_Y": int,
        "MOST_DETAIL_VIEW_RES": 'Int64',
        "LEAST_DETAIL_VIEW_RES": 'Int64',
        "MBR_XMIN": 'Int64',
        "MBR_YMIN": 'Int64',
        "MBR_XMAX": 'Int64',
        "MBR_YMAX": 'Int64',
        "POSTCODE_DISTRICT": str,
        "POSTCODE_DISTRICT_URI": str,
        "POPULATED_PLACE": str,
        "POPULATED_PLACE_URI": str,
        "POPULATED_PLACE_TYPE": str,
        "DISTRICT_BOROUGH": str,
        "DISTRICT_BOROUGH_URI": str,
        "DISTRICT_BOROUGH_TYPE": str,
        "COUNTY_UNITARY": str,
        "COUNTY_UNITARY_URI": str,
        "COUNTY_UNITARY_TYPE": str,
        "REGION": str,
        "REGION_URI": str,
        "COUNTRY": str,
        "COUNTRY_URI": str,
        "RELATED_SPATIAL_OBJECT": str,
        "SAME_AS_DBPEDIA": str,
        "SAME_AS_GEONAMES": str
    }, names=columns), files_to_read))

    df_bronze_geography = df_bronze_geography[["ID", "NAME1", "POSTCODE_DISTRICT"]]
    df_bronze_geography = df_bronze_geography.rename(
        columns={"ID": "geography_dimension_id", "POSTCODE_DISTRICT": "postcode", "NAME1": "name"})
    df_bronze_geography.to_csv(f"{DATA_FOLDER}{EXECUTION_DATE}{TABLE_NAME}")
