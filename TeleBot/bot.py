import datetime
import re

from pyrogram import Client
from pyrogram.types import Message, CallbackQuery
from TeleBot.constant import MessageSend, start_button_normal, start_button_admin, Keyboards, \
    see_food_menue_for_change_price, see_food_menue_for_order, see_food, list_of_oder, give_dept_person, see_all_person

from DB.Model_Impletation import find_user_by_id, add_new_user, update_user_step, update_user_name, \
    find_order_of_one_week_of_one_person, find_food_by_name, add_food, find_all_food, update_food_price, find_all_user, \
    update_user_dept, find_week, add_order, update_week_number, update_week_day, find_order_of_one_day_of_one_week_all, \
    find_user_by_name, read_flag_ready_food, update_flag_ready_food

is_food_today_run = read_flag_ready_food()


def find_information_of_massage_sender(message: Message):
    chat_id = message.from_user.id
    name_in_telegram = message.from_user.first_name
    last_name_in_telegram = message.from_user.last_name
    if name_in_telegram is None:
        name_in_telegram = ""
    if last_name_in_telegram is None:
        last_name_in_telegram = ""
    new_name = "_".join((name_in_telegram, last_name_in_telegram))
    user_name = message.from_user.username
    if user_name is None:
        user_name = "not found"

    return chat_id, new_name, user_name


def step_start_for_not_exist(client: Client, chat_id):
    print("hi_mr")

    add_new_user(chat_id, '', 'step_start_for_not_exist')
    client.send_message(chat_id, MessageSend.you_are_not_exist)


def is_valid_name(name):
    return re.match(r'^[a-zA-Z.-]+$', name)


def stop_day_order(client: Client, chat_id):
    global is_food_today_run

    week = find_week()
    time_of_this_day = datetime.datetime.now()
    how_much_day_spend = (time_of_this_day - datetime.datetime.strptime(week.get("date"), '%Y-%m-%d %H:%M:%S.%f')).days
    print("how_much_day_spend " + str(how_much_day_spend))
    if how_much_day_spend == 0 and is_food_today_run:
        how_much_day_spend = 1

    if int(week.get("week_day")) + how_much_day_spend > 7:

        update_week_number(int(week.get("week_number")) + 1)
        update_week_day((int(week.get("week_day")) + how_much_day_spend) % 7 + 1)
    elif how_much_day_spend > 0:
        update_week_day(int(week.get("week_day")) + how_much_day_spend)

    list_of_order_of_person_in_day = find_order_of_one_day_of_one_week_all(str(week.get("week_number")),
                                                                           str(week.get("week_day")))
    print(week.get("week_number"))
    print(week.get("week_day"))
    msg = list_of_oder(list_of_order_of_person_in_day)
    client.send_message(chat_id, msg)
    is_food_today_run = False
    update_flag_ready_food(is_food_today_run)


def step_two_start_for_not_exist(client: Client, chat_id, first_last_name, user_name,
                                 name_that_want_to_be_in_data_base):
    name_validity = True if is_valid_name(name_that_want_to_be_in_data_base) else False
    status = update_user_name(chat_id, name_that_want_to_be_in_data_base)
    if name_validity and status.get('status') == 200:
        update_user_step(chat_id, 'Start')
        client.send_message(chat_id, MessageSend.Add_successfully)
        client.send_message(chat_id, MessageSend.start_message_normal, reply_markup=start_button_normal())

    elif not name_validity:
        client.send_message(chat_id, MessageSend.this_name_is_invalid)

    elif status.get('status') == 400:
        client.send_message(chat_id, MessageSend.this_name_found)


def make_message_for_orders(orders):
    sum_week = 0
    message_res = ''
    for item in orders:
        name_food = item.get("food_name")
        food_price = find_food_by_name(name_food).get("price")
        date = item.get("date")
        sum_week += int(food_price)
        message_res += MessageSend.order_summer.format(name_food=name_food, food_price=food_price, date=date)

    message_res = message_res + "\n" + f'{sum_week}جمع کل هفته : '
    return message_res


def bot_do_job(bot: Client):
    # week_of_today = 2
    # number_of_week = 1
    @bot.on_message()
    def handle_message(client: Client, message: Message):
        if message.text is not None:
            chat_id, new_name, user_name = find_information_of_massage_sender(message)
            user = find_user_by_id(chat_id)
            user_exist = False

            if user is not None:
                user_exist = True
                step_user_list = user.get("step").split("@")
                step_user = step_user_list[0]
                type_user = user.get("type")
            if not user_exist:
                step_start_for_not_exist(client, chat_id)

            else:
                if message.text == '/start' and step_user != 'step_start_for_not_exist' and type_user == 'Normal':
                    update_user_step(chat_id, 'Start')
                    client.send_message(chat_id, MessageSend.start_message_normal, reply_markup=start_button_normal())
                elif message.text == '/start' and step_user != 'step_start_for_not_exist' and type_user == 'Admin':
                    update_user_step(chat_id, 'Start')
                    client.send_message(chat_id, MessageSend.start_message_admin, reply_markup=start_button_admin())

                elif step_user == "step_start_for_not_exist":
                    name = message.text
                    step_two_start_for_not_exist(client, chat_id, new_name, user_name, name)

                elif message.text == Keyboards.my_dept and type_user == "Normal":
                    print("dept of person ")
                    dept = user.get("dept")
                    client.send_message(chat_id, MessageSend.send_dept.format(dept=dept))

                elif message.text == Keyboards.see_list_of_buy_in_week and type_user == "Normal":
                    print("find out list of buy")
                    update_user_step(chat_id, "Give_Number_Week_Normal")
                    week = find_week()
                    number_of_week = week.get("week_number")
                    client.send_message(chat_id, MessageSend.give_me_number_of_week.format(number=number_of_week))
                elif str(message.text).isnumeric() and step_user == 'Give_Number_Week_Normal' and type_user == "Normal":
                    orders = find_order_of_one_week_of_one_person(user.get("person_name"), message.text)
                    message_orders = make_message_for_orders(orders)
                    client.send_message(chat_id, message_orders)
                elif message.text == Keyboards.add_new_food and type_user == "Admin":
                    print("add new food")
                    update_user_step(chat_id, "Add_Name_Of_Food")
                    client.send_message(chat_id, MessageSend.add_name_of_your_food)

                elif type_user == "Admin" and step_user == "Add_Name_Of_Food":
                    update_user_step(chat_id, "Add_Price_Of_Food@" + message.text)
                    client.send_message(chat_id, MessageSend.give_price_of_your_food)
                elif type_user == "Admin" and step_user == "Add_Price_Of_Food" and str(message.text).isnumeric():
                    update_user_step(chat_id, "Start")
                    name = step_user_list[1]
                    add_food(name, int(message.text))
                    client.send_message(chat_id, MessageSend.add_food_successful)
                elif type_user == "Admin" and message.text == Keyboards.update_food_price:
                    all_food_in_list_of_dic = find_all_food()
                    xb = see_food_menue_for_change_price(all_food_in_list_of_dic)
                    client.send_message(chat_id, MessageSend.add_name_of_your_food, reply_markup=xb)

                elif type_user == "Admin" and step_user == "change_price_food" and str(message.text).isnumeric():
                    food_name = step_user_list[1]
                    update_food_price(food_name, int(message.text))
                    client.send_message(chat_id, MessageSend.update_food_successful)

                elif type_user == "Admin" and message.text == Keyboards.create_menu_for_next_day:
                    global is_food_today_run
                    stop_day_order(client, chat_id)
                    all_food_in_list_of_dic = find_all_food()
                    xb = see_food_menue_for_order(all_food_in_list_of_dic)
                    is_food_today_run = True
                    update_flag_ready_food(is_food_today_run)
                    client.send_message(chat_id, MessageSend.add_name_of_your_food, reply_markup=xb)

                elif type_user == "Admin" and message.text == Keyboards.see_who_one_wants_food:
                    week = find_week()
                    list_of_order_of_person_in_day = find_order_of_one_day_of_one_week_all(str(week.get("week_number")),
                                                                                           str(week.get("week_day")))
                    # print(week.get("week_number"))
                    # print(week.get("week_day"))
                    msg = list_of_oder(list_of_order_of_person_in_day)

                    client.send_message(chat_id, msg)


                elif type_user == "Admin" and message.text == Keyboards.stop_next_day_food_request:
                    stop_day_order(client, chat_id)
                    # week = find_week()
                    # time_of_this_day = datetime.datetime.now()
                    # how_much_day_spend = (time_of_this_day - datetime.datetime.strptime(week.get("date"))).days
                    # if how_much_day_spend == 0:
                    #     how_much_day_spend = 1
                    #
                    # if week.get("week_day") + how_much_day_spend > 7:
                    #     list_of_order_of_person_in_day = find_order_of_one_day_of_one_week_all(week.get("week_number"),
                    #                                                                            week.get("week_day"))
                    #
                    #     msg = list_of_oder(list_of_order_of_person_in_day)
                    #
                    #     client.send_message(chat_id, msg)
                    #
                    #     update_week_number(int(week.get("week_number")) + 1)
                    #     update_week_day(week.get("week_day") + how_much_day_spend % 7 + 1)
                    # else:
                    #     update_week_day(int(week.get("week_day")) + 1)


                elif type_user == "Admin" and message.text == Keyboards.person_dept:

                    all_person = find_all_user()

                    msg = give_dept_person(all_person)

                    client.send_message(chat_id, msg)


                elif type_user == "Admin" and message.text == Keyboards.pardakht_yek_shakhs:

                    update_user_step(chat_id, "Decrease_Dept")
                    all_person = find_all_user()
                    msg = see_all_person(all_person)
                    client.send_message(chat_id, msg)


                elif type_user == "Admin" and step_user == "Decrease_Dept" and "/" in message.text:

                    name_of_user = message.text.split('/')[1]
                    user_person = find_user_by_name(name_of_user)

                    if user_person is None:
                        client.send_message(chat_id, MessageSend.this_person_is_invalid)

                    else:
                        update_user_step(chat_id, "Decrease_Dept2@" + name_of_user)
                        client.send_message(chat_id, MessageSend.give_how_much_money_get)

                elif type_user == "Admin" and step_user == "Decrease_Dept2" and str(message.text).isnumeric():

                    person_want_update = find_user_by_name(step_user_list[1])
                    update_user_dept(person_want_update.get("user_id"), -1 * int(message.text))
                    update_user_step(chat_id, "Start")
                    client.send_message(chat_id, MessageSend.update_person_successful_dept)
                    client.send_message(person_want_update.get("user_id"), MessageSend.update_your_dept)
                else:

                    print("No whrere :(")

    @bot.on_callback_query()
    def handle_callback_query(client: Client, query: CallbackQuery):
        id_chat = query.from_user.id
        user = find_user_by_id(id_chat)
        type_user = user.get("type")
        name_user = user.get("name")
        id_inline = query.message.message_id
        callback_query_list = query.data.split('@')
        if callback_query_list[0] == 'change_price_food' and type_user == "Admin":
            update_user_step(id_chat, "change_price_food@" + callback_query_list[1])
            client.send_message(id_chat, MessageSend.give_price_of_your_food)
        elif callback_query_list[0] == 'order_for_next_day' and type_user == "Admin":
            food = find_food_by_name(callback_query_list[1])
            all_user = find_all_user()
            week = find_week()
            number_of_week = week.get("week_number")
            week_of_today = week.get("week_day")
            client.edit_message_text(id_chat, id_inline,
                                     MessageSend.accept_this_food.format(food=callback_query_list[1]))

            for user in all_user:
                client.send_message(user.get("user_id"), MessageSend.next_day_food,
                                    reply_markup=see_food(food, number_of_week, week_of_today))
        elif callback_query_list[0] == 'Order_For_Next_Day_Accept':
            date_today = str(datetime.datetime.now())
            week = find_week()
            if week.get("week_number") == int(callback_query_list[3]) and week.get("week_day") == int(
                    callback_query_list[4]):
                update_user_dept(id_chat, int(callback_query_list[1]))
                add_order(callback_query_list[2], name_user, date_today, callback_query_list[3], callback_query_list[4])
                client.edit_message_text(id_chat, id_inline, MessageSend.order_accept)

            else:
                client.edit_message_text(id_chat, id_inline, MessageSend.time_ended)

    bot.run()
