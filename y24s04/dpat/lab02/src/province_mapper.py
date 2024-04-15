#!/usr/bin/env python3


NOAA_MAP: dict = {
    1: "Cherkasy Region",
    2: "Chernihiv Region",
    3: "Chernivtsi Region",
    4: "Republic of Crimea Region",
    5: "Dnipropetrovsk Region",
    6: "Donetsk Region",
    7: "Ivano-Frankivsk Region",
    8: "Kharkiv Region",
    9: "Kherson Region",
    10: "Khmelnytskyi Region",
    11: "Kyiv Region",
    12: "Kyiv City",
    13: "Kirovohrad Region",
    14: "Luhansk Region",
    15: "Lviv Region",
    16: "Mykolaiv Region",
    17: "Odesa Region",
    18: "Poltava Region",
    19: "Rivne Region",
    20: "Sevastopol Region",
    21: "Sumy Region",
    22: "Ternopil' Region",
    23: "Zakarpattia Region",
    24: "Vinnytsia Region",
    25: "Volyn Region",
    26: "Zaporizhia Region",
    27: "Zhytomyr Region",
}


REGIONAL_CENTER_MAP: dict = {
    1: "Republic of Crimea Region",
    2: "Vinnytsia Region",
    3: "Volyn Region",
    4: "Dnipropetrovsk Region",
    5: "Donetsk Region",
    6: "Zhytomyr Region",
    7: "Zakarpattia Region",
    8: "Zaporizhia Region",
    9: "Ivano-Frankivsk Region",
    10: "Kyiv Region",
    11: "Kyiv City",
    12: "Kirovohrad Region",
    13: "Luhansk Region",
    14: "Lviv Region",
    15: "Mykolaiv Region",
    16: "Odesa Region",
    17: "Poltava Region",
    18: "Rivne Region",
    19: "Sumy Region",
    20: "Ternopil Region",
    21: "Kharkiv Region",
    22: "Kherson Region",
    23: "Khmelnytskyi Region",
    24: "Cherkasy Region",
    25: "Chernihiv Region",
    26: "Chernivtsi Region",
    27: "Sevastopol Region"
}


def get_mapped_provinces():
    
    temp = {name: id for id, name in REGIONAL_CENTER_MAP.items()}
    
    mapped: dict = {
        old_id: {
            "name": name,
            "id": temp[name]
        } for old_id, name in NOAA_MAP.items() if name in temp
    }

    return mapped
