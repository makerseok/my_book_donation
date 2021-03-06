import re
import time
from glob import glob

import pandas as pd

cid_to_cat = {
    "1": "Novel_Poem",
    "170": "Economic_Management",
    "1230": "Home_Cook_Beauty",
    "1237": "Religion_Mysticism",
    "517": "Art_Culture",
    "76001": "Reference_Book",
    "55890": "Health_Hobby_Leisure",
    "987": "Science",
}

if __name__ == "__main__":
    today = "2021-06-18"

    filenames = glob(f"./crawling_data/cid-*{today}.csv")
    get_cid = re.compile("cid-[0-9]+")
    datas = []

    for filename in filenames:
        print(filename)
        cid = get_cid.search(filename).group()[4:]
        df = pd.read_csv(filename)
        df["category"] = cid_to_cat[cid]
        datas.append(df)

    data = pd.concat(datas, ignore_index=True)

    print(data.head())
    print(data.shape)
    print(data["category"].value_counts())

    data.to_csv(f"./data/raw_{len(data)}_{today}.csv", index=False)
