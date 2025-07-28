import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("TMD_DATA_API_KEY")

BASE_URL = "https://data.tmd.go.th/nwpapi/v1/forecast/location/hourly"
HEADERS = {
    "accept": "application/json",
    "authorization": f"Bearer {API_KEY}"
}

region_map = {
    "C": "ภาคกลาง",
    "N": "ภาคเหนือ",
    "NE": "ภาคตะวันออกเฉียงเหนือ",
    "E": "ภาคตะวันออก",
    "S": "ภาคใต้",
    "W": "ภาคตะวันตก"
}


def fetch_forecast_by_region(region_code: str, duration: int = 6):
    url = f"{BASE_URL}/region"
    params = {
        "region": region_code,
        "fields": "tc,rh,cond",
        "duration": str(duration)
    }
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        return response.json().get("WeatherForecasts", [])
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")


def fetch_all_regions_and_save(output_path="data/tmd_forecast.json"):
    all_data = []
    for code, name in region_map.items():
        try:
            print(f"📥 ดึงข้อมูลจาก {name}")
            forecasts = fetch_forecast_by_region(code, duration=1)
            for f in forecasts:
                f["region_code"] = code
                f["region_name"] = name
            all_data.extend(forecasts)
            print(f"✅ สำเร็จ {name}, ได้ {len(forecasts)} จุด\n")
        except Exception as e:
            print(f"❌ ล้มเหลว {name}: {e}")

    # 🔽 Save to file
    os.makedirs("data", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"📦 บันทึกไฟล์แล้ว: {output_path}")


if __name__ == "__main__":
    fetch_all_regions_and_save()
