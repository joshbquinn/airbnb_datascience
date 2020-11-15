import csv
import os

wanted_headers = ["id", "host_id", "host_neighbourhood", "street", "neighbourhood", "neighbourhood_cleansed",
                  "neighbourhood_group_cleansed", "city", "state", "zipcode", "smart_location", "is_location_exact",
                  "property_type", "room_type", "accommodates", "bedrooms", "beds", "price"]

new_wanted_headers = wanted_headers

csv_files = os.listdir("./unclean")


def write(listings, file_name):
    with open(file_name, "w", newline="", encoding="windows-1252") as f:
        for line in listings:
            f.write(line)
        f.close()


def load(file_name):
    with open(file_name, "r", encoding="windows-1252") as table:
        print("Loading Data")
        rows = []  # [[cell for cell in row.strip().split(",")] for row in table]
        for row in table:
            new_row = []
            for cell in row.strip().split(","):
                new_row.append(cell)
            rows.append(new_row)
        return rows


def write_dict(file, data_dict, headers):
    print("5. Printing the cleaned dictionary to new csv file.")
    with open(file, 'w', encoding="windows-1252") as csv_file:
        CSV = ""
        for k, v in data_dict.items():
            line = "{},{}\n".format(k, ",".join(v))
            CSV += line
        for line in CSV:
            csv_file.write(line)
    print("6. Finished writing cleaned dictionary to file")


def load_dict(file):
    print("1. Loaded the uncleaned csv")
    dict_list = []
    with open(file, 'r', encoding="windows-1252") as reader:


        for row in reader:
            dict_list.append(row)
        print("2. Finished loading the uncleaned csv")
        return dict_list


def get_unwanted_headings():
    unwanted_headings = []
    actual_headings = load("unclean/listings19_1.csv")[0]

    for heading in actual_headings:
        if heading not in wanted_headers:
            unwanted_headings.append(heading)
    print("0. Retrieved the unwanted columns")
    unwanted_headings.append('number_of_reviews_l30d')
    unwanted_headings.append('bathrooms_text')
    return unwanted_headings


def load_clean_dict(file, unwanted):
    file_dict = load_dict(file)
    print("3. Removing unwanted columns")
    for row in file_dict:
        for unwanted_heading in unwanted:
            if unwanted_heading in row:
                del row[unwanted_heading]
    print("4. Finished removing unwanted columns")
    return file_dict


def get_prices_for_all(dict_lists, master_dict):
    for a_dict in dict_lists:
        count = 2
        for row in a_dict:
            for m_row in master_dict:
                if m_row['id'] == row['id']:
                    new_wanted_headers.append(f"price {count}")
                    master_dict[0].update({f"price {count}": row['price']})
                    break
        count += 1
    return master_dict


def get_ids(file):
    ids = []
    for row in file:
        ids.append(row[0])
    return ids


def compute(master_file, files):
    count = 2
    for file in files:
        print("file", count)
        ids = get_ids(file)
        for master_row in master_file:
            if master_row[0] not in ids:
                master_row.append(0)
                continue
            for row in file:
                if master_row[0] == "id":
                    master_row.append(row[17] + " " + str(count))
                    break
                if master_row[0] == row[0]:
                    master_row.append(row[17])
                    break
        count += 1
    return master_file


unwanted_cols = get_unwanted_headings()

clean_files = os.listdir("./clean")

for load_f, write_f in zip(csv_files, clean_files):
    write_dict("clean/" + write_f, load_clean_dict("unclean/" + load_f, unwanted_cols), wanted_headers)
    print("7. All cleaned dictionaries written to files\n")

print("8. Load the first clean airbnb listings csv file to compare the other airbnb listings against."
      "\nWe can append prices for each month over two years from all the csv's into this 'master' csv, where ids Match."
      "\nIf a master ID is not in any other CSV file, we append a ZERO for that month, denoting that it "
      "was not listed that month.")

master_list = csv_files[0]
clean_files.pop(0)

print("9. Load all the clean csv files (without unwanted columns) into a list")
all_files = []
for name in clean_files:
    all_files.append(load("clean/" + name))

print("10. Compare the Master CSV file against all the others. "
      "\nAppend a new column to master for the year.month price."
      "\nIterate through each csv file. Iterate through each master ROW. "
      "\nIf the master ROW's ID is not in the csv file we're comparing against. Append a zero for that month."
      "\n ")
write(compute(master_list, all_files), "master_listings.csv")
