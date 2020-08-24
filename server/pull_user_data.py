import requests
import json
import pandas as pd
from datetime import datetime

questions_data = requests.get("http://localhost:3000/api/questions").json()
data = requests.get("http://localhost:3000/api/data").json()


question_data_list = []
main_data_list = []

for elems in questions_data:
    question_data_list.append([elems["_id"], elems["question_text"], elems["tags"]])


# print(question_data_list)

for elems in data:
    for ting in elems["questions"]:
        main_data_list.append(
            [
                elems["_id"],
                ting["question_id"],
                ting["correct"],
                ting["time_spent"],
                ting["tries"],
            ]
        )

# for i in range(len(main_data_list)):
# print(main_data_list[i][1])

for i in range(len(main_data_list)):
    for elems in question_data_list:
        if main_data_list[i][1] == elems[0]:
            main_data_list[i].append(elems[1])
            main_data_list[i].append(elems[2])

# print(main_data_list)
temp = []
temp_complete = []

for i in range(len(main_data_list)):
    temp.append(main_data_list[i][3])

print(temp)

for i in range(len(temp)):
    try:
        if temp[i] > temp[i - 1]:
            temp[i] = temp[i] - temp[i - 1]
        # else:
        # 	temp[i] = temp[i] - temp[i-1]
    except:
        continue


print(temp)


# df = pd.DataFrame(main_data_list)

# # #print(df)
# file_headers = ['session_id', 'question_id', 'correct(bool)', 'time_spent(seconds since start of session)', 'num of tries', 'question_text', 'tags']

# df.to_csv('elendig_navn7.csv')

# file = pd.read_csv('elendig_navn7.csv', header=None, skiprows=1, names = file_headers)

# file.to_excel('final_file.xlsx', header=True)


# print(file.head())
