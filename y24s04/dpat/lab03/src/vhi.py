
import os
import re
import requests
import pandas as pd

import province_mapper

from datetime import datetime
from bs4 import BeautifulSoup

print('[+] Successful setup...')

PROVINCES_COUNT: int = 27
DUMP_FOLDER: str = 'vhi_dump'
PROVINCES_MAP: dict = province_mapper.get_mapped_provinces()


def folder_init(
    folder_path: str,
    is_silent=False
) -> None:
    """
    Creates folder if it doesn't exist 
    :param folder_path: Path to the folder
    :param is_silent: If true, will hide print about existing folder!
    :return: None
    """

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f'[+] Created folder: {folder_path}')
    else:
        if not is_silent:
            print(f'[x] Folder {folder_path} already exists!')


def fetch(
    province_id: int,
    start_year: int,
    end_year: int
) -> None:
    """
    Fetches mean data from NOAA 
    :param province_id: Province ID based on the NOAA mapping
    :param start_year: The starting year for the requested time series data Format: (YYYY)
    :param end_year: The ending year for the requested time series data. Format: (YYYY)
    :return: None
    """

    if not validate_id(province_id):
        print('[!] Invalid province ID')
        return

    mapped_province_id = PROVINCES_MAP[province_id]["id"]
    mapped_province_name = PROVINCES_MAP[province_id]["name"]

    start_year, end_year = validate_years(start_year, end_year)

    if start_year is None or end_year is None:
        return

    print(f'[*] Fetching data:\n\t'
          f'Province ID: {province_id} | {mapped_province_name}\n\t'
          f'Start year: {start_year}\n\t'
          f'End year: {end_year}')

    url: str = f'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={province_id}&year1={start_year}&year2={end_year}&type=Mean'

    try:
        req = requests.get(url)

        if req.status_code != 200:
            print('[!] Request failed!')
            return

        # clearing response from html tags
        soup = BeautifulSoup(req.text, "html.parser")
        clear_data = soup.get_text()

        # assembling the file name
        timestamp = datetime.now().strftime('%Y-%m-%dT%H-%M')
        filename = f'vhi_{mapped_province_id}_{timestamp}.csv'

        # Deleting last comma in the data series that makes useless shift
        clear_data = re.sub(r',\s*$', '', clear_data, flags=re.MULTILINE)

        # changing province id based on the real mapping
        clear_data = re.sub(r"Province= \d+:", f"Province= {mapped_province_id}:", clear_data)
        print(
            f'[!] Province ID was changed to the real mapping: {province_id} (NOAA) -> {mapped_province_id} (UKR oblast centers mapping)')

        save(directory=DUMP_FOLDER, filename=filename, data=clear_data)
        # print(clear_data)

    except Exception as err:
        raise Exception(f'[!] Error happened: {err}')


def validate_years(
    start_year: int,
    end_year: int
) -> (int, int):
    """
    Checks if start_year and end_year are within the correct range
    :param start_year: The starting year for the requested time series data Format: (YYYY)
    :param end_year: The ending year for the requested time series data.
    Format: (YYYY). Set end_year to 9999 to validate only start_year for the format.
    :return: A tuple of two integers if start_year and end_year passed all checks. 
    """
    current_year: int = datetime.today().year
    year_pattern = r'^\d{4}$'

    if not re.match(year_pattern, str(start_year)) or not re.match(year_pattern, str(end_year)):
        print(f'[!] Invalid year format. Only allowed one is: YYYY (4 integers)')
        return None, None

    if end_year == 9999 and start_year:
        print(start_year)
        return start_year

    if start_year < 1982:
        print(f'[!] Start year should be greater or equal to 1982!')
        return None, None

    if end_year >= current_year:
        print(f'[!] For full data coverage, end_year({end_year}) should be less than current_year({current_year})!')
        return None, None

    if start_year > end_year:
        print(f'[!] start_year({start_year}) cannot be greater than end_year({end_year})')
        return None, None

    print(f'[+] Successful years range validation!')
    return start_year, end_year


def validate_id(
    province_id: int
) -> bool:
    """
    Checks if given province_id is in the mapped dictionary
    :param province_id: Province ID based on the NOAA mapping
    :return: Bool 
    """

    if province_id not in PROVINCES_MAP.keys():
        return False

    print(f'[+] Successful ID validation!')
    return True


def save(
    directory: str,
    filename: str,
    data: str
) -> None:
    """
    Saves given data to the file in the specific dir
    :param directory: Directory where the data is saved.
    :param filename: Name of the file to save the data to.
    :param data: Data to save.
    :return: 
    """

    folder_init(directory, is_silent=True)

    with open(f'{directory}/{filename}', 'w') as file:
        file.write(data)
        print(f'[+] Saved {filename} to {directory}/')

        file.close()


def fetch_bulk(
    start_id: int,
    end_id: int,
    start_year: int,
    end_year: int
) -> None:
    """
    Using fetch() to bulk-download VHI data for the specific range of regions
    :param start_id: The starting province(region) ID (NOAA list) to download
    :param end_id: The ending province(region) ID (NOAA list) to download
    :param start_year: The starting year for the requested time series data Format: (YYYY)
    :param end_year: The ending year for the requested time series data. Format: (YYYY)
    :return: None
    """

    for i in range(start_id, end_id + 1):
        print(f'[*] Fetch order: {i}')
        try:
            fetch(i, start_year, end_year)
        except Exception as err:
            print(f'[!] Error fetching: {err}')


def clear_dump_folder(
    directory: str
) -> None:
    """
    Cleans dump folder
    :param directory: Path to the folder
    :return: None
    """

    if not os.path.exists(directory):
        print(f'[!] Directory does not exist!')
        return

    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(f'[*] Deleted file: {file_path}')
        except Exception as err:
            print(f"[!] Failed to delete {file_path}. Reason: {err}")


def get_dataframe(
    directory: str
) -> pd.DataFrame | None:
    """
    Creates dataframe from the files in the directory
    :param directory: Path to the directory
    :return: Pandas dataframe
    """

    headers: list = ['Year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI']
    dataframes: list = []

    if not os.path.exists(directory):
        print(f'[!] Directory does not exist!')
        return

    for file in os.listdir(directory):
        if not file.endswith('.csv'):
            print(f'[!] File ({file}) is not a .csv. Skipping it!')
            continue
        file_path = os.path.join(directory, file)

        try:
            df = pd.read_csv(file_path, header=1, names=headers, skiprows=1)
            province_id = int(file.split('_')[1])
            df.insert(0, 'PID', province_id, True)
            dataframes.append(df)
        except Exception as err:
            print(f'[!] Failed to read {err}')

    if not dataframes:
        raise Exception('No files found!')

    return pd.concat(dataframes, ignore_index=True)


def get_province(
    province_id: int
) -> str | None:
    """
    Returns the province name 
    :param province_id: Province ID based on the real mapping
    :return: string
    """

    for region_key, region_info in PROVINCES_MAP.items():
        if region_info.get('id') == province_id:
            return region_info.get('name')

    return


def get_vhi(
    dataframe: pd.DataFrame,
    province_id: int,
    year: int
) -> pd.DataFrame | None:
    """
    Returns VHI series for the specified region and year.
    
    :param dataframe: Pandas DataFrame containing the data.
    :param province_id: Region ID as per 'PID' column in the DataFrame.
    :param year: Year as integer to filter the VHI series.
    :return: Pandas Series containing VHI values for the specified PID and year.
    """

    if province_id not in dataframe['PID'].unique():
        print(f"[!] PID {province_id} not found in the DataFrame.")
        return None

    if year not in dataframe['Year'].unique():
        print(f"[!] Year {year} not found in the DataFrame.")
        return None

    print(f' VHI data series for {province_id=} and {year=}')

    temp = dataframe[(dataframe['PID'] == province_id) & (dataframe['Year'] == year)]

    return temp['VHI'].reset_index(drop=True)


def get_max_min_vhi(
    dataframe: pd.DataFrame,
    provinces: list,
    years: list
) -> pd.DataFrame | None:
    """
    Returns Min VHI and Max VHI series for the specified provinces and years
    :param dataframe: Pandas DataFrame containing the data.
    :param provinces: List of provinces id (real regional mapping)
    :param years: List of years to retrieve
    :return: Pandas DataFrame or Nothing if error occurs
    """

    if not set(provinces).issubset(dataframe['PID'].unique()):
        print("[!] One or more specified provinces are not in the DataFrame.")
        print(f'[?] Possible PID in the given DateFrame: {suggest_values(dataframe)[0]}')
        return None

    if not set(years).issubset(dataframe['Year'].unique()):
        print("[!] One or more specified years are not in the DataFrame.")
        print(f'[?] Possible years in the given DateFrame: {suggest_values(dataframe)[1]}')
        return None

    tmp: list = []

    for pid in provinces:
        for year in sorted(years):

            temp = dataframe[(dataframe['PID'] == pid) & (dataframe['Year'] == year)]

            if temp.empty:
                continue

            min_vhi = temp['VHI'].min()
            max_vhi = temp['VHI'].max()

            tmp.append({'Province ID': pid,
                           'Year': year,
                           'Min VHI': min_vhi,
                           'Max VHI': max_vhi})

    output = pd.DataFrame(tmp)

    return output if not output.empty else None


def suggest_values(
    dataframe: pd.DataFrame
) -> (list, list):
    """
    Returns the unique years and province IDs from the DataFrame
    :param dataframe: Pandas DataFrame
    :return: A tuple containing two lists of years and province ids
    """

    if dataframe.empty:
        print(f'[!] DataFrame is empty :/')
        return

    years = dataframe['Year'].unique().tolist()
    ids = dataframe['PID'].unique().tolist()

    years.sort()
    ids.sort()

    return ids, years


def get_vhi_range(
    dataframe: pd.DataFrame,
    provinces: list,
    years: list
) -> pd.DataFrame | None:
    """
    Returns VHI series for the specified provinces and years
    :param dataframe: Pandas DataFrame containing the data.
    :param provinces: List of provinces id (real regional mapping)
    :param years: List of years to retrieve
    :return: Pandas DataFrame or Nothing if error occurs
    """

    if set(provinces).issubset(dataframe['PID'].unique()):
        if not set(years).issubset(dataframe['Year'].unique()):
            print("[!] One or more specified years are not in the DataFrame.")
            print(f'[?] Possible years in the given DateFrame: {suggest_values(dataframe)[1]}')
            return None

        result: pd.DataFrame = dataframe[dataframe['PID'].isin(provinces) & dataframe['Year'].isin(years)]

        if result.empty:
            print("[!] Some error happened, so no data is returned.")
            return

        result = result[['PID', 'Year', 'Week', 'VHI']]

        return result.reset_index(drop=True)

    print("[!] One or more specified provinces are not in the DataFrame.")
    print(f'[?] Possible PID in the given DateFrame: {suggest_values(dataframe)[0]}')
    return None


def get_droughts_count(
    dataframe: pd.DataFrame,
    vhi_min: int,
    vhi_max: int,
    percentage: int
) -> pd.DataFrame:
    num_provinces_affected = round((percentage / 100) * len(dataframe['PID'].unique()))

    droughts = dataframe[(dataframe['VHI'] >= vhi_min) & (dataframe['VHI'] <= vhi_max)]

    yearly_droughts = droughts.groupby(['Year', 'PID']).size().reset_index(name='count')

    years_with_extreme_droughts = yearly_droughts.groupby('Year')['PID'].agg(['count', list]).reset_index()

    years_affected = years_with_extreme_droughts[years_with_extreme_droughts['count'] >= num_provinces_affected]

    years_affected.columns = ['Year', 'Entries', 'Regions']

    return years_affected.reset_index(drop=True)
