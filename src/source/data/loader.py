from pandas import DataFrame, read_csv

class Files:
    CRIME = 'database.zip'
    FPS   = 'fps.csv'
    CONTROLS = 'controls.csv'

class CrimeSchema:
    EVENT_ID     = 'eventid'
    EVENT_LABEL  = 'eventtype'
    GROUP        = 'group'
    CATEGORY     = 'category'
    SUB_CATEGORY = 'sub_category'
    DATE         = 'occurence_date' 
    MONTH_NAME   = 'monthname'
    DAYOFWEEK    = 'dayofweek'
    HOUR         = 'hour'
    WINDOW       = 'window'
    DISTRICT     = 'district'
    STREET       = 'street'
    LATITUDE     = 'latitude'
    LONGITUDE    = 'longitude'
    CLUSTER      = 'cluster'
    STAT         = 'stat'
    SOURCE_NAME  = 'source_name'
    IS_HOLIDAY   = 'is_holliday'
    HOLIDAY_NAME ='holiday_name'
    WEIGHT='weight'
    AREA= 'area'
    GEOMETRY= 'geometry'
    OCCURENCES = 'occurences'
    PROBABILITY = 'prob(%)'

def load_crime_data(path:str, sub_dir:str) -> DataFrame:
    filename = path.joinpath(f"{sub_dir}/{Files.CRIME}")
    """load the data from the CSV file"""
    data = read_csv(
        filename,
        compression='zip',
        dtype={
            CrimeSchema.LATITUDE:float,
            CrimeSchema.LONGITUDE:float,
            CrimeSchema.DATE:str
        },
        parse_dates=[CrimeSchema.DATE],
        encoding='utf-8'
    )
    return data