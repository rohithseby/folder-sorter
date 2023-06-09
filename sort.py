import os, json, shutil, time
import pandas as pd

with open("config.json", "r") as config:
    config = json.load(config)

path = config["path"]

cat_mapper = {}

for dir in config["categories"].keys():
    for ext in config["categories"][dir]:
        cat_mapper[ext] = dir

count = []

df = pd.DataFrame(
    {
        "file_name": [
            x
            for x in os.listdir(path=path)
            if x.lower()
            not in [
                x.lower()
                for x in list(config["categories"].keys()) + ["Others", "Folders"]
            ]
        ]
    }
)

df["file_path"] = path + "\\" + df.file_name if len(df) > 0 else None

df["extension"] = df.file_name.apply(lambda x: x.split(".")[-1] if "." in x else None)

df["file_flag"] = df.file_path.apply(lambda x: os.path.isfile(x))

df["category"] = df.extension.astype("str").str.lower().map(cat_mapper)

df.loc[(df.category.isna()) & (df.file_flag == True), "category"] = "Others"

df.loc[(df.category.isna()) & (df.file_flag == False), "category"] = "Folders"

file_list = df.to_dict(orient="records")

if len(df.category) > 0:
    for dir in df.category.tolist():
        try:
            os.mkdir(os.path.join(path, dir))
        except FileExistsError:
            count.append(dir)
            print(f"{dir} - folder already exists. Sorted files will get added to it")

c = input("Start sorting (y/n) ?? - ")

if c.lower() == "y":
    for file in file_list:
        src = os.path.join(path, file["file_name"])
        dst = os.path.join(path, file["category"], file["file_name"])
        try:
            shutil.move(src=src, dst=dst)
        except Exception as e:
            print(src, e)
            pass
    print("Sorted successfully")
    time.sleep(5)
else:
    print("Exiting")
    time.sleep(20)
