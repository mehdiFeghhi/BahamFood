import datetime

from pymongo import MongoClient

myclient = MongoClient("localhost", 27017)
mydb = myclient["Baham"]


def find_user_by_name(name):
    users = mydb["User"]
    user = users.find_one({"name": name})
    return user


def find_user_by_id(id):
    users = mydb["User"]
    user = users.find_one({"user_id": id})
    return user


def find_all_user():
    users = mydb["User"]
    return users.find()


def add_new_user(chat_id, name, step="Start", type_user="Normal", debt=0):
    mydict = {"user_id": chat_id, "name": name, "step": step, "type": type_user, "dept": debt}
    user_by_name = find_user_by_name(name)
    user_by_id = find_user_by_id(chat_id)

    if (user_by_name is None or len(user_by_name) == 0 or name == "") and (user_by_id is None or len(user_by_id) == 0):
        users = mydb["User"]
        users.insert_one(mydict)
        print("user add ")
        return {"status": 200}

    else:
        print("this name exist")
        return {"status": 400}


def delete_user_by_name(name):
    users = mydb["User"]
    id = users.delete_one({"name": name})


def delete_user_by_user_id(chat_id):
    users = mydb["User"]
    users.delete_one({"user_id": chat_id})


def update_user_name(chat_id, name):
    users = mydb["User"]
    user_by_name = find_user_by_name(name)
    if user_by_name is None or len(user_by_name) == 0:
        myquery = {"user_id": chat_id}
        newvalue = {"$set": {"name": name}}
        users.update_one(myquery, newvalue)
        print("name update")
        return {"status": 200}
    else:
        print("this name exist")
        return {"status": 400}


def update_user_step(chat_id, step):
    users = mydb["User"]
    myquery = {"user_id": chat_id}
    newvalue = {"$set": {"step": step}}
    users.update_one(myquery, newvalue)


def update_user_dept(chat_id, dept):
    users = mydb["User"]
    myquery = {"user_id": chat_id}
    person = find_user_by_id(chat_id)
    newvalue = {"$set": {"dept": person["dept"] + dept}}
    users.update_one(myquery, newvalue)


# def update_user_dept_by_name(name,dept):
#     users = mydb["User"]
#     myquery = {"name": name}
#     person = find_user_by_id(myquery)
#     newvalue = {"$set": {"dept": person["dept"] + dept}}
#     users.update_one(myquery, newvalue)


def find_food_by_name(name):
    foods = mydb["Food"]
    food = foods.find_one({"name": name})
    return food


def add_food(name, price):
    mydict = {"name": name, "price": price}

    food = find_food_by_name(name)
    if food is None:
        foods = mydb["Food"]
        foods.insert_one(mydict)
        return {"status": 200}
    else:
        print("this name exist")
        return {"status": 400}


def update_food_price(name, price):
    foods = mydb["Food"]
    myquery = {"name": name}
    newvalue = {"$set": {"price": price}}
    foods.update_one(myquery, newvalue)


def delete_food(name):
    foods = mydb["Food"]
    foods.delete_one({"name": name})


def find_all_food():
    foods = mydb["Food"]
    return foods.find()


# def add_week_day(week_number, week_day):
#
#     mydict = {"week_number": week_number, "week_day": week_day, "is_valid": True}
#     days = mydb["Day"]
#     days.insert_one(mydict)
#     return {"status": 200}
#
# def update_week_valid(week_number,week_day):


def add_order(food_name, person_name, date, week_number, week_day):
    mydict = {"food_name": food_name, "person_name": person_name, "date": date, "week_number": week_number,
              "week_day": week_day}
    foods = mydb["Order"]
    foods.insert_one(mydict)
    return {"status": 200}


def find_order_of_one_week_of_one_person(person_name, week_number):
    orders = mydb["Order"]
    orders_person = orders.find({"person_name": person_name, "week_number": week_number})
    return orders_person


def find_order_of_one_day_of_one_week_all(week_number, week_day):
    orders = mydb["Order"]
    orders_day = orders.find({"week_number": week_number, "week_day": week_day})
    return orders_day


def add_week(week_number, week_day):
    weeks = mydb["Week"]
    mydict = {"i": 1, "week_number": week_number, "week_day": week_day, "date": str(datetime.datetime.now())}
    weeks.insert_one(mydict)


def update_week_day(week_day):
    weeks = mydb["Week"]
    myquery = {"i": 1}
    newvalue = {"$set": {"week_day": week_day, "date": str(datetime.datetime.now())}}
    weeks.update_one(myquery, newvalue)


def update_week_number(week_number):
    weeks = mydb["Week"]
    myquery = {"i": 1}
    newvalue = {"$set": {"week_number": week_number, "date": str(datetime.datetime.now())}}
    weeks.update_one(myquery, newvalue)


def delete_week(i):
    weeks = mydb["Week"]
    weeks.delete_one({"i": i})


def find_week():
    weeks = mydb["Week"]
    return weeks.find_one({"i": 1})

def update_food_week_day(food):
    weeks = mydb["Week"]
    # food_name = food.get("name")
    # food_price = food.get("price")
    myquery = {"i": 1}
    newvalue = {"$set": {"food":food}}
    weeks.update_one(myquery, newvalue)

def write_flag_ready_food(flag_status):
    flags = mydb["Flags"]
    mydict = {"i": 1, "flag": flag_status}
    flags.insert_one(mydict)

def read_flag_ready_food():
    flags = mydb["Flags"]
    find_flags = flags.find_one({"i": 1})
    if find_flags is None:
        return False
    else:
        return find_flags.get("flag")


def update_flag_ready_food(flag_status):
    flags = mydb["Flags"]
    myquery = {"i": 1}
    newvalue = {"$set": {"flag": flag_status}}
    flags.update_one(myquery, newvalue)

