from Model_Impletation import *
import sys
import pandas as pd
import os


def add_user(chat_id, name, step="Start", type_user="Normal"):
    add_new_user(chat_id, name, step, type_user)


def add_user_file_cv(file_name):
    df = pd.read_csv(file_name)
    chat_id = df["id"]
    names = df["name"]
    type_user = df["type"]
    counter = 0
    for id in chat_id:
        add_user(id, names[counter], "Start", type_user[counter])


def get_csv_of_user(file_name):
    all_user = find_all_user()
    df = pd.DataFrame()

    for item in all_user:
        user_id = item.get("user_id")
        name = item.get("name")
        type_user = item.get("type")
        new_row = pd.DataFrame({"id": [user_id], "Name": [name], "type": [type_user]})
        df = pd.concat([new_row, df]).reset_index(drop=True)

    df.to_csv(file_name)


def use_helper():
    f = open("help.txt", "r")
    print(f.read())


def main():
    try:
        inputs = sys.argv[1:]
        func_name = inputs[0]
        if func_name == "add_user":
            if len(inputs) == 4 and inputs[1].isnumeric() and (inputs[3] == "Admin" or inputs[3] == "Normal"):
                add_user(int(inputs[1]), inputs[2],"Start",inputs[3])
            else:
                print("your input is wrong for see our option enter -help")
        elif func_name == "add_week":
            if len(inputs) == 3 and inputs[1].isnumeric() and inputs[0].isnumeric():
                day_number = int(inputs[1])
                week_number = int(inputs[0])
                delete_week(1)
                add_week(week_number,day_number)
            else:
                print("your input is wrong for see our option enter python work_with_DB.py -help")

        elif func_name == "now_week":
            res = find_week()
            print(res)

        elif func_name == "remove":
            if len(inputs) == 2:
                delete_user_by_name(inputs[1])
            else:
                print("your input is wrong for see our option enter python work_with_DB.py -help")
        elif func_name == "-help":
            use_helper()

    except:

        print("your input is wrong for see our option enter -help")


if __name__ == "__main__":
    main()