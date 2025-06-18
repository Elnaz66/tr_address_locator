import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import time

def get_coordinates(row):
    combinations = [
        ['mahalle', 'köy', 'ilçe', 'il'],
        ['köy', 'ilçe', 'il'],
        ['ilçe', 'il'],
        ['il']
    ]

    geolocator = Nominatim(user_agent="turkey_location_finder")

    for combo in combinations:
        address_parts = []
        for col in combo:
            if col in row and pd.notna(row[col]):
                val = str(row[col]).strip()
                if val:
                    address_parts.append(val)
        address = ', '.join(address_parts) + ", Türkiye"
        try:
            location = geolocator.geocode(address, timeout=10)
            if location:
                return pd.Series([location.latitude, location.longitude])
        except GeocoderTimedOut:
            time.sleep(2)
            return get_coordinates(row)
        except Exception:
            return pd.Series([None, None])

    return pd.Series([None, None])


def process_excel(input_path, output_path):
    df = pd.read_excel(input_path)
    df[['enlem', 'boylam']] = df.apply(get_coordinates, axis=1)
    df.to_excel(output_path, index=False)
    print(f"✅ İşlem tamamlandı. Sonuç dosyası: {output_path}")
