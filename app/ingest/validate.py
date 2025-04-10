# validate.py

REQUIRED_FIELDS = ["ts", "device", "temp", "humidity", "co", "lpg", "smoke", "motion", "light"]

def validate_record(record):
    """Validate a single sensor record."""
    if not all(field in record for field in REQUIRED_FIELDS):
        raise ValueError("Missing required field(s)")

    try:
        record["ts"] = float(record["ts"])
        record["temp"] = float(record["temp"])
        record["humidity"] = float(record["humidity"])
        record["co"] = float(record["co"])
        record["lpg"] = float(record["lpg"])
        record["smoke"] = float(record["smoke"])
        record["motion"] = bool(record["motion"])
        record["light"] = bool(record["light"])
    except Exception as e:
        raise ValueError(f"Field type error: {e}")

    return record
