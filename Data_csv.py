import numpy as np
import random
import pandas as pd
from datetime import datetime, timedelta
from slowchangevalues import generate_slow_values
# ==============================
# CONFIG
# ==============================

SECONDS = 100
START_TIME = datetime.now()   # ✅ Start from current time
OUTPUT_FILE = "dicv_sim_data_test.csv"
TAGS_CONFIG = ['']


def generate_csv():
    timestamps = [
        START_TIME + timedelta(seconds=i)
        for i in range(SECONDS)
    ]

    data = {"timestamp": timestamps}

    for tag in TAGS_CONFIG:
        print(f"Generating: {tag['tagname']}")
        data[tag["tagname"]] = generate_slow_values(
            tag["min"],
            tag["max"],
            SECONDS
        )

    df = pd.DataFrame(data)
    df.to_csv(OUTPUT_FILE, index=False)

    print(f"\n✅ CSV generated successfully: {OUTPUT_FILE}")

# ==============================

if __name__ == "__main__":
    generate_csv()
