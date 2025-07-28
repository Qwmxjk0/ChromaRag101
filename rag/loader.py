import json

def load_forecast_data(filepath="data/tmd_forecast.json"):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    docs = []
    for entry in data:
        province = entry["location"].get("province", "ไม่ทราบจังหวัด")
        region = entry.get("region_name", "ไม่ทราบภูมิภาค")
        lat = entry["location"].get("lat")
        lon = entry["location"].get("lon")

        for forecast in entry.get("forecasts", []):
            time = forecast.get("time")
            weather = forecast.get("data", {})
            tc = weather.get("tc")
            rh = weather.get("rh")
            cond = weather.get("cond")

            text = f"""จังหวัด: {province}
ภูมิภาค: {region}
ตำแหน่ง: lat={lat}, lon={lon}
เวลา: {time}
อุณหภูมิ: {tc} °C
ความชื้นสัมพัทธ์: {rh}%
สภาพอากาศ: {cond}"""

            doc_id = f"{province}_{time}"
            docs.append({
                "id": doc_id,
                "text": text,
                "province": province,
                "region": region
            })

    return docs
