# property-prices-for-edinburgh-data-lake-arch
a cloud agnostic data lake , with scraped house prices . Uses terraform, puppet, scrappy 

Phases
* Phase 1: ( terraform + puppet + ec2 + airflow setup )
* Phase 2 : ( terraform + puppet + ec2 + airflow + ecs ??? EKS ?? for jobs )
* Phase 3 : ( s3 delta lake )
* Phase 4: ( airflow jobs write into delta lake )
* Phase 5: ( Jupiter notebook read )

Data Schema
* bronze_geography: `ID,NAMES_URI,NAME1,
        NAME1_LANG,NAME2,NAME2_LANG,TYPE,LOCAL_TYPE,GEOMETRY_X,
        GEOMETRY_Y,MOST_DETAIL_VIEW_RES,LEAST_DETAIL_VIEW_RES,
        MBR_XMIN,MBR_YMIN,MBR_XMAX,MBR_YMAX,POSTCODE_DISTRICT,
        POSTCODE_DISTRICT_URI,POPULATED_PLACE,POPULATED_PLACE_URI,
        POPULATED_PLACE_TYPE,DISTRICT_BOROUGH,DISTRICT_BOROUGH_URI,
        DISTRICT_BOROUGH_TYPE,COUNTY_UNITARY,COUNTY_UNITARY_URI,COUNTY_UNITARY_TYPE,
        REGION,REGION_URI,COUNTRY,COUNTRY_URI,RELATED_SPATIAL_OBJECT,
        SAME_AS_DBPEDIA,SAME_AS_GEONAMES`
* bronze_property: `'price', 'type', 'address', 'url', 'agent_url', 'postcode',
       'number_bedrooms', 'search_date' , geography_dimension_id`
* silver_geography_dimension: `geography_dimension_id, postcode, name`
* silver_property_fact: `'price', 'type', 'address', 'url', 'postcode','search_date' , geography_dimension_id`

JOB
    geography_downloader --> silver_geography_dimension --> get_rightmove_prices --> silver_property_facts



UI Links

    Airflow: localhost:8080
    Flower: localhost:5555
