from pyrogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton, CallbackQuery, KeyboardButton


def IKM(data):
    return InlineKeyboardMarkup([[InlineKeyboardButton(text, cbd)] for text, cbd in data])


class MessageSend:
    you_are_not_exist = "شما در این بات عضو نیستید برای عضویت یک نام کاربری برای خود اتخاذ نمایید.\n " \
                        "نام می تواند شامل تمامی ترکیبات شامل حروف انگلیسی باشد. \n"
    start_message_normal = "سلام و درود بر کاربر گرامی"
    start_message_admin = "سلام و درود خدمت ادمین محترم\n" \
                          "چه خدمتی می تونم برای شما انجام بدم."

    error_400 = "ورودی شما غیرقابل استفاده است ."
    this_name_is_invalid = 'این نام نامعتبر است .'
    this_name_found = 'این نام در دیتابیس وجود دارد.'
    Add_successfully = "شما به دیتابس اضافه شدید با نامی که انتخاب کردید.\n"

    send_dept = "مقدار بدهکاری : **{dept}** .\n"
    give_me_number_of_week = "عدد هفته مربوطه را وارد نمایید( هفته فعلی  هفته **{number}** می باشد):"
    order_summer = "نام غذا: **{name_food}**\n" \
                   "\n **{food_price}** :قیمت غذا" \
                   "\n **{date}** : تاریخ"

    add_name_of_your_food = "نام غذایی مورد نظر را وارد نمایید"
    give_price_of_your_food = "قیمت غذا را وارد نمایید ."
    add_food_successful = "غذا مورد نظر با موفقیت اضافه شد."
    update_food_successful = "غذا قیمت اش با موفقیت آپدیت شد."
    update_person_successful_dept = "بدهی شخص موردنظر با موفقیت آپدیت شد."
    next_day_food = "غذا فردا به این شکل است :"
    order_accept = "درخواست شما تایید شد."
    time_ended = "مهلت شما برای انتخاب این غذا تمام شده است."
    this_person_is_invalid = "این شخص در داده های ما نیست."
    give_how_much_money_get = "چه مبلغی پرداخت کرده است"
    update_your_dept = "حساب شما توسط آدمین آپدیت شد."
    accept_this_food = "غذای فردا {food}"


class Keyboards:
    my_dept = 'چقدر در سیستم بدهکار هستید.'
    see_list_of_buy_in_week = "لیست خرید های شما در یکی از هفته های دلخواه"

    add_new_food = "افزودن یک غذای جدید"
    update_food_price = "آپدیت کردن قیمت یک غذا"
    create_menu_for_next_day = "ساخت اعلان برای غذای فردا"
    see_who_one_wants_food = "دیدن لیست افرادی که برای فردا ثبت غذا انجام داده اند."
    stop_next_day_food_request = "بستن لیست سفارش فردا"
    pardakht_yek_shakhs = "وارد کردن پرداختی یک شخص"

    food = "{price} : {food}"
    person_dept = "دیدن لیست حساب کتاب افراد"


def start_button_admin():
    my_keyboard = [[KeyboardButton(text=Keyboards.add_new_food)],
                   [KeyboardButton(text=Keyboards.update_food_price)],
                   [KeyboardButton(text=Keyboards.create_menu_for_next_day)],
                   [KeyboardButton(text=Keyboards.see_who_one_wants_food)],
                   [KeyboardButton(text=Keyboards.stop_next_day_food_request)],
                   [KeyboardButton(text=Keyboards.person_dept)],
                   [KeyboardButton(text=Keyboards.pardakht_yek_shakhs)]]

    return ReplyKeyboardMarkup(keyboard=my_keyboard, resize_keyboard=True)


def see_food(food, number_week, week_number_today):
    button = [(Keyboards.food.format(price=food.get("price"), food=food.get("name")),
               "@".join(("Order_For_Next_Day_Accept", str(food.get("price")), food.get("name"), str(number_week),
                         str(week_number_today))))]
    return IKM(button)


def start_button_normal():
    # return IKM([(Keyboards.see_accounting, "See_ACCOUNTING"),
    #             (Keyboards.see_five_accounting, "See_Five_Last_ACCUNTING"),
    #             (Keyboards.get_csv_with_all_detail, "DETAIL_ACCOUNTING"),
    #             (Keyboards.get_user_list, "USER_LIST")])

    my_keyboard = [[KeyboardButton(text=Keyboards.my_dept)],
                   [KeyboardButton(text=Keyboards.see_list_of_buy_in_week)]]

    return ReplyKeyboardMarkup(keyboard=my_keyboard, resize_keyboard=True)


def see_food_menue_for_change_price(food_menu_dic):
    # [(Keyboards.add_user, "@".join(("add_new_user", str(chat_id)))),
    #  (Keyboards.reject_request, "@".join(("reject_add_new_user", str(chat_id))))]
    #
    list_of_button = []
    for food in food_menu_dic:
        list_of_button.append((Keyboards.food.format(price=food.get("price"), food=food.get("name")),
                               "@".join(("change_price_food", food.get("name")))))

    return IKM(list_of_button)


def see_food_menue_for_order(food_menu_dic):
    # [(Keyboards.add_user, "@".join(("add_new_user", str(chat_id)))),
    #  (Keyboards.reject_request, "@".join(("reject_add_new_user", str(chat_id))))]
    #
    list_of_button = []
    for food in food_menu_dic:
        list_of_button.append((Keyboards.food.format(price=food.get("price"), food=food.get("name")),
                               "@".join(("order_for_next_day", food.get("name")))))

    return IKM(list_of_button)


def list_of_oder(list_of_order_of_person_in_day):
    msg = 'لیست افراد که سفارش دادند:'
    number = 0
    for person in list_of_order_of_person_in_day:
        print(person)
        msg += "\n"
        msg += person.get("person_name")
        number += 1

    msg += "\n"
    msg += f'{number} : number'
    return msg


def give_dept_person(list_of_person):
    msg = "لیست افراد :"
    for person in list_of_person:
        msg += "\n"
        print(person)
        msg += person.get("name") + " " + str(person.get("dept"))

    return msg


def see_all_person(list_of_person):
    msg = "لیست افراد :"

    for person in list_of_person:
        if not person.get("name") == "":
            msg += "\n"
            msg += '/' + person.get("name")
    return msg
