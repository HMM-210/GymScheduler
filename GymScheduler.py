#import libraries
import json
import os
import time
import shutil
from os import path
from telegram import KeyboardButton, ReplyKeyboardMarkup, Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, ContextTypes ,MessageHandler, filters

#setup
TOKEN = "Your_Token_Here"
app=Application.builder().token(TOKEN).build()

#keyboard buttons the first step
admin_commands = [[KeyboardButton("اضافة مستخدم جديد")], [KeyboardButton("حذف مستخدم موجود")]]
commands = [[KeyboardButton("انشاء جدول تمارين جديد")], [KeyboardButton("تعديل التمارين الموجودة")], [KeyboardButton("العوده لقائمة الاوامر")], [KeyboardButton("طلب المساعده من المطور او ارسال اخطاء او اقتراحات")]]
edit_main_sections = [[KeyboardButton("اضافة قسم جديد")], [KeyboardButton("تعديل قسم موجود")], [KeyboardButton("حذف قسم موجود")]]
edit_exercise = [[KeyboardButton("اضافة تمرين جديد")], [KeyboardButton("حذف تمرين موجود")]]
#keyboard buttons the second step
admin_commands_final = ReplyKeyboardMarkup(admin_commands,resize_keyboard=True, one_time_keyboard=True)
commands_final = ReplyKeyboardMarkup(commands,resize_keyboard=True, one_time_keyboard=True)
edit_main_sections_final = ReplyKeyboardMarkup(edit_main_sections,resize_keyboard=True, one_time_keyboard=True)
edit_exercise_final = ReplyKeyboardMarkup(edit_exercise,resize_keyboard=True, one_time_keyboard=True)

#important variables
json_file_name = "gym_database.json"
BASE_DIR = path.dirname(path.abspath(__file__))
json_file_path = path.join(BASE_DIR, json_file_name)
admin_id = "Admin_Id_In_Telegram"

#functions in functions
def check_request_file():
    if path.exists(json_file_path_part_2):
        return True, "Done"
    else:
        try:
            with open(json_file_path_part_2, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=4, ensure_ascii=False)
            
            return True, "Done"
        except Exception as e:
            print(f"Error: Can't create the database file. {e}")
            return False, str(e)
def read_data_base():
    with open(json_file_path , "r", encoding="utf-8") as f:
        return json.load(f)

def save_data_base(data_file):
    with open(json_file_path , "w", encoding="utf-8") as f:
        json.dump(data_file,f,indent=4,ensure_ascii=False)

def check_db():
    if path.exists(json_file_path):
        return True, "Done"
    else:
        try:
            with open(json_file_path, "w", encoding="utf-8") as f:
                json.dump({}, f, indent=4, ensure_ascii=False)
            return True, "Done"
        except Exception as e:
            print(f"Error: Can't create the database file. {e}")
            return False, str(e)

def check_user(user_id):
    data_base = read_data_base()
    if user_id in data_base:
        return True
    else:
        return False
def show_sections (user_id):
    data_base = read_data_base()
    return data_base.get(user_id, {}).get("sections", [])

def show_exercises (user_id, section):
    data_base = read_data_base()
    return data_base.get(user_id, {}).get(section, [])

def show_sections_keyboard_button(user_id):
    sections = show_sections(user_id)
    buttons = []
    for section in sections:
        buttons.append([KeyboardButton(section)])
    if buttons == []:
        return False
    else:
        return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)

def show_exercises_keyboard_button(user_id, section):
    exercises = show_exercises(user_id, section)
    buttons = []
    for exercise in exercises:
        buttons.append([KeyboardButton(exercise)])
    if buttons == []:
        return False
    else:
        return ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
def is_admen (user_id):
    if admin_id == user_id :
        return True
    else:
        return False


#main Functions part 1
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    check_request_file()
    text = update.message.text
    user_id = str(update.message.from_user.id)
    data_base_part_2_temp = read_data_base_part_2()
    user_keys = sorted([k for k in data_base_part_2_temp if k.startswith(f"{user_id}_")])
    current_key = user_keys[-1] if user_keys else None
    condition, message = check_db()
    if condition is False:
        await update.message.reply_text("حدث خطأ في انشاء قاعدة البيانات, حاول مرة اخرى. \nالخطأ: " + message)
        return
    data_base = read_data_base()
    
    data_base["admin_id"] = "2108964915"
    data_base["accepted_IDs"] = ["2108964915"]
    save_data_base(data_base)
    if user_id not in data_base["accepted_IDs"] :
        await update.message.reply_text("انت غير مشترك للاشتراك يجب التواصل مع بوت المطور https://t.me/example_bot .")
        context.user_data.clear()
        return
    if check_user(user_id) is False:
        data_base[user_id] = {}
        data_base[user_id]["sections"] = []
    if text == "/start" and context.user_data.get("user_choose") == "waiting_for_photo" :
        python_file_path = os.path.realpath(__file__)
        folder_path = os.path.dirname(python_file_path)
        images_path = os.path.join(folder_path, "tempimage", user_id)
        images = []
        if os.path.exists(images_path):
            for file in os.listdir(images_path):
                file_path = os.path.join(images_path, file)
                if file.lower().endswith((".png")):
                    images.append(file_path)
                else:
                    await update.message.reply_text("لم يتم معالجة الصوره بعد يرجى اعاده المحاولة بالضغط على.")
            images.sort()
            if images:
                images_as_group = [InputMediaPhoto(open(img, 'rb')) for img in images]
                await context.bot.send_media_group(chat_id=user_id, media=images_as_group)
                shutil.rmtree(images_path)
                context.user_data.clear()
                await update.message.reply_text("هذا هو جدولك استمتع به❤️❤️")
            else:
                await update.message.reply_text("لم يتم معالجة الصوره بعد يرجى اعاده المحاولة بالضغط على.")
        else:
            await update.message.reply_text("لم يتم معالجة الصوره بعد يرجى اعاده المحاولة بالضغط على.")


    if text == "/start" :
        context.user_data.pop("user_choose",None)
        await update.message.reply_text("مرحبا في بوت صنع جداول للتمرينات.")
        if is_admen(user_id):
            commands = [[KeyboardButton("انشاء جدول تمارين جديد")], [KeyboardButton("تعديل التمارين الموجودة")], [KeyboardButton("العوده لقائمة الاوامر")], [KeyboardButton("طلب المساعده من المطور او ارسال اخطاء او اقتراحات")],[KeyboardButton("اوامر الادمن")]]
            commands_final = ReplyKeyboardMarkup(commands,resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text("هذه هي الاوامر المتاحة:",reply_markup=commands_final)
        context.user_data.clear()
        return

    if text == "طلب المساعده من المطور او ارسال اخطاء او اقتراحات" :
        await update.message.reply_text("للتواصل مع المطور او ارسال اخطاء او اقتراحات, يرجى الضغط على الرابط التالي: https://t.me/HMM210_bot")
    
    if text == "تعديل التمارين الموجودة" or context.user_data.get("user_choose") == "edit_exercises" :
        context.user_data["user_choose"] = "edit_exercises"
        await commands_Functions_operations(update, context)
    elif text == "انشاء جدول تمارين جديد" or context.user_data.get("user_choose") == "create_new_schedule" :
        context.user_data["user_choose"] = "create_new_schedule"
        await request(update, context)
    elif text == "العوده لقائمة الاوامر" and context.user_data.get("user_choose") not in "waiting_for_photo" :
        context.user_data.pop("user_choose", None)
        if text == "العوده لقائمة الاوامر":
            context.user_data.clear()
            await update.message.reply_text("تم الرجوع لقائمة الاوامر.", reply_markup=commands_final)
    elif text == "اوامر الادمن" and is_admen(user_id) or context.user_data.get("user_choose") == "admin_commands" and is_admen(user_id) :
        context.user_data["user_choose"] = "admin_commands"
        await admin_commands(update,context)
    else:
        await update.message.reply_text("نص خاطئ :اضغط على /start للبدأ.")

async def admin_commands (update: Update, context: ContextTypes.DEFAULT_TYPE):
    data_base = read_data_base()
    admin_choose = context.user_data.get("admin_choose")
    text = str(update.message.text)
    if text == "اوامر الادمن" :
        await update.message.reply_text ("ما هي اوامرك سيدي",reply_markup=admin_commands_final)
    if text == "اضافة مستخدم جديد" :
        await update.message.reply_text ("ادخل ايدي المستخدم الذي تريد اضافته يا سيدي.")
        context.user_data["admin_choose"] = "add_user"
    if admin_choose == "add_user":
        if text in data_base["accepted_IDs"]:
            context.user_data.pop("admin_choose")
            await update.message.reply_text ("عذرا سيدي هذا الايدي موجود بالفعل")
            return
        try :
            text = int(text)
        except ValueError:
            context.user_data.pop("admin_choose")
            await update.message.reply_text ("عذرا سيدي هذا الايدي غير صالح.")
            return

        data_base["accepted_IDs"].append(str(text))
        save_data_base(data_base)
        await update.message.reply_text ("تم تنفيذ الامر")
    if text == "حذف مستخدم موجود":
        botton = [[KeyboardButton(id)] for id in data_base["accepted_IDs"]]
        botton_final = ReplyKeyboardMarkup(botton,resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text ("ادخل ايدي المستخدم الذي تريد حذفه يا سيدي.",reply_markup=botton_final)
        context.user_data["admin_choose"] = "delete_user"      
    if admin_choose == "delete_user":
        if text == admin_id:
            await update.message.reply_text ("لا يمكنني حذف هذا الحساب سيدي")
            return
        if text not in  data_base["accepted_IDs"]:
            await update.message.reply_text ("عذرا سيدي هذا الايدي غير موجود ")
            return
        try :
            text = int(text)
        except ValueError:
            context.user_data.pop("admin_choose")
            await update.message.reply_text ("عذرا سيدي هذا الايدي غير صالح.")
            return
        data_base["accepted_IDs"].remove(str(text))
        save_data_base(data_base)
        await update.message.reply_text ("تم تنفيذ الامر")

async def commands_Functions_operations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = str(update.message.text)
    user_id = str(update.message.from_user.id)
    data_base_part_2_temp = read_data_base_part_2()
    user_keys = sorted([k for k in data_base_part_2_temp if k.startswith(f"{user_id}_")])
    current_key = user_keys[-1] if user_keys else None
    data_base = read_data_base()
    operation = context.user_data.get("operation")
    user_selection = context.user_data.get("user_selection_delete")
    sections_keyboard = show_sections_keyboard_button(user_id)


    if text == "تعديل التمارين الموجودة" or operation == "edit_exercises" :
        await update.message.reply_text("اختر ما تريد تعديله:",reply_markup=edit_main_sections_final)
    
    elif text == "اضافة قسم جديد" :
        context.user_data["operation"] = "add_section"
        await update.message.reply_text("ادخل اسم القسم الجديد الذي تريد اضافته:")
    
    elif operation == "add_section" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)

        if text in show_sections(user_id) :
            context.user_data["operation"] = "add_section"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته موجود بالفعل, حاول مره اخرى ", reply_markup=sections_keyboard)
            status = False
        else: 
            status = True
        if check_user(user_id) and status is not  False :
            data_base[user_id]["sections"].append(text)
            data_base[user_id][text] = []
        elif status is not False :
            data_base[user_id] = {}
            data_base[user_id]["sections"] = []
            data_base[user_id]["sections"].append(text)
            data_base[user_id][text] = []
        if status is not False :
            save_data_base(data_base)
            context.user_data.pop("operation")
            await update.message.reply_text("تم اضافة القسم الجديد بنجاح.")
    elif text == "حذف قسم موجود" :
        context.user_data["operation"] = "delete_section"
        if show_sections_keyboard_button(user_id) not in False :
            await update.message.reply_text("اختر القسم الذي تريد حذفه:",reply_markup=show_sections_keyboard_button(user_id))
        else:
            await update.message.reply_text("لا يوجد اقسام لحذفها, حاول اضافه قسم جديد اولاً.")
            context.user_data.pop("operation")
    elif operation == "delete_section" :
        if text in show_sections(user_id) :
            data_base[user_id]["sections"].remove(text)
            data_base[user_id].pop(text, None)
            save_data_base(data_base)
            context.user_data.pop("operation")
            await update.message.reply_text("تم حذف القسم بنجاح.")
        else:
            await update.message.reply_text("القسم الذي ادخلته غير موجود حاول مره اخرى")
            text = "حذف قسم موجود"
    
    elif text == "تعديل قسم موجود":
        await update.message.reply_text("اختر نوع التعديل الذي تريده",reply_markup=edit_exercise_final)
        
    elif text == "اضافة تمرين جديد"  :
        context.user_data["operation"] = "add_exercise_place"
        if show_sections_keyboard_button(user_id) is not False :
            await update.message.reply_text("اختر القسم الذي تريد اضافه  للتمرين الجديد  فيه :",reply_markup=show_sections_keyboard_button(user_id))
        else:
            await update.message.reply_text("لا يوجد اقسام لاضافة تمرين لها, حاول اضافه قسم جديد اولاً.")
            context.user_data.pop("operation")

    elif operation == "add_exercise_place" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
 
        if text not in show_sections(user_id) :
            context.user_data.pop("user_selection_delete", None)
            context.user_data.pop("operation", None)
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود ", reply_markup=sections_keyboard)
        else:
            context.user_data["user_selection"] = text
            context.user_data["operation"] = "add_exercise_name"
            await update.message.reply_text("ادخل اسم التمرين الجديد الذي تريد اضافته:")
    
    elif operation == "add_exercise_name" :
        data_base = read_data_base()
        user_selection = context.user_data.get("user_selection")
        data_base[user_id][user_selection].append(text)
        save_data_base(data_base)
        context.user_data.pop("operation", None)
        context.user_data.pop("user_selection", None)
        await update.message.reply_text("تم اضافة التمرين الجديد .")

    elif text == "حذف تمرين موجود"  :
        context.user_data["operation"] = "add_exercise_place_delete"
        if show_sections_keyboard_button(user_id) is not False :
            await update.message.reply_text("اختر القسم الذي تريد حذف  التمرين  منه :",reply_markup=show_sections_keyboard_button(user_id))
        else:
            await update.message.reply_text("لا يوجد اقسام لحذف التمرين منها, حاول اضافه قسم جديد اولاً.")
            context.user_data.pop("operation")

    elif operation == "add_exercise_place_delete" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
 
        if text not in show_sections(user_id) :
            context.user_data["operation"] = "add_exercise_place_delete"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود ", reply_markup=sections_keyboard)
            context.user_data.pop("user_selection_delete", None)
            context.user_data.pop("operation", None)
        else:
            context.user_data["user_selection_delete"] = text
            context.user_data["operation"] = "add_exercise_name_delete"
            await update.message.reply_text("ادخل اسم التمرين الذي تريد حذفه:")
    
    elif operation == "add_exercise_name_delete" :
        if text not in show_exercises(user_id ,user_selection):
            data_base = read_data_base()
            data_base[user_id][user_selection].remove(text)
            save_data_base(data_base)
            context.user_data.pop("operation", None)
            context.user_data.pop("user_selection_delete", None)
            await update.message.reply_text("تم حذف التمرين.")

    else:
        await update.message.reply_text("نص خاطئ :اضغط على /start للبدأ.")


###########################################################################################################


#important variables part 2
json_file_name_part_2 = "requests.json"
BASE_DIR_part_2 = path.dirname(path.abspath(__file__))
json_file_path_part_2 = path.join(BASE_DIR_part_2, json_file_name_part_2)

#functions in functions part 2
        
def read_data_base_part_2():
    with open(json_file_path_part_2 , "r", encoding="utf-8") as f:
        return json.load(f)

def save_data_base_part_2(data_file):
    with open(json_file_path_part_2 , "w", encoding="utf-8") as f:
        json.dump(data_file,f,indent=4,ensure_ascii=False)
def check_end_and_del(user_id):
    data_base = read_data_base_part_2()
    keys_to_del = [k for k in data_base if k.startswith(f"{user_id}_") and data_base[k].get("end") != "end"]
    for key in keys_to_del:
        del data_base[key]
    if keys_to_del:
        save_data_base_part_2(data_base)
    return True

#main Functions part 2
async def request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = str(update.message.from_user.id)
    data_base_part_2_temp = read_data_base_part_2()
    user_keys = sorted([k for k in data_base_part_2_temp if k.startswith(f"{user_id}_")])
    current_key = user_keys[-1] if user_keys else None
    user_choose = context.user_data.get("user_choose")
    operation_part_2 = context.user_data.get("operation_part_2")
    condition, message = check_request_file()
    operation_part_3 = context.user_data.get("operation_part_3")
    if condition is False:
        await update.message.reply_text("حدث خطأ في انشاء قاعدة البيانات, حاول مرة اخرى. \nالخطأ: " + message)
        return
    data_base_part_2 = read_data_base_part_2()
    if text == "انشاء جدول تمارين جديد"  :
        check_end_and_del(user_id)
        await update.message.reply_text("ادخل اسم صاحب الجدول:")
        context.user_data["operation_part_2"] = "request_name"
    elif operation_part_2 == "request_name" :
        key = f"{user_id}_{int(time.time() * 1000)}"
        data_base_part_2[key] = {"start": "start", "user_id": user_id, "name": text}
        save_data_base_part_2(data_base_part_2)
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("استراحه")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        rest_button = ReplyKeyboardMarkup([[KeyboardButton("استراحه")]],resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text("الان ادخل قسم اول تمرين تريد اضافته في اليوم الاول:", reply_markup=sections_keyboard or rest_button)
        context.user_data["operation_part_2"] = "request_section1_day1"

    # ==================== اليوم الاول ====================

    elif operation_part_2 == "request_section1_day1" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("استراحه")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "استراحه" :
            data_base_part_2[current_key]["day1"] = ["استراحه"]
            save_data_base_part_2(data_base_part_2)
            context.user_data["operation_part_2"] = "request_section1_day2"
            await update.message.reply_text("تم حفظ اليوم الاول كاستراحه \nالان اختر قسم اول تمرين لليوم التالي:", reply_markup=sections_keyboard)
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section1_day1"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("الان ادخل التمرين الاول الذي تريد اضافته في القسم الذي اخترته في اليوم الاول:",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise1_day1"
    elif operation_part_2 == "request_exercise1_day1" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise1_day1"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets1_day1"

    elif operation_part_2 == "request_sets1_day1" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثاني")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day1"] = {"day1_exercise1":[current[0], current[1], text]}
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الثاني في اليوم الاول:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section2_day1"
    elif operation_part_2 == "request_section2_day1" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثاني")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الثاني" :
            context.user_data["operation_part_2"] = "request_section1_day2"
            await update.message.reply_text("جاري الانتقال الى اليوم الثاني ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section2_day1"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الثاني من اليوم الاول", reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise2_day1"
    elif operation_part_2 == "request_exercise2_day1" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise2_day1"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets2_day1"

    elif operation_part_2 == "request_sets2_day1" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثاني")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day1"]["day1_exercise2"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الثالث في اليوم الاول:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section3_day1"
    elif operation_part_2 == "request_section3_day1" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثاني")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الثاني" :
            context.user_data["operation_part_2"] = "request_section1_day2"
            await update.message.reply_text("جاري الانتقال الى اليوم الثاني ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section3_day1"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الثالث من اليوم الاول",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise3_day1"
    elif operation_part_2 == "request_exercise3_day1" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise3_day1"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets3_day1"

    elif operation_part_2 == "request_sets3_day1" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثاني")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day1"]["day1_exercise3"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الرابع في اليوم الاول:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section4_day1"
    elif operation_part_2 == "request_section4_day1" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثاني")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الثاني" :
            context.user_data["operation_part_2"] = "request_section1_day2"
            await update.message.reply_text("جاري الانتقال الى اليوم الثاني ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section4_day1"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الرابع من اليوم الاول",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise4_day1"
    elif operation_part_2 == "request_exercise4_day1" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise4_day1"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets4_day1"

    elif operation_part_2 == "request_sets4_day1" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثاني")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day1"]["day1_exercise4"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الخامس في اليوم الاول:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section5_day1"
    elif operation_part_2 == "request_section5_day1" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثاني")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الثاني" :
            context.user_data["operation_part_2"] = "request_section1_day2"
            await update.message.reply_text("جاري الانتقال الى اليوم الثاني ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section5_day1"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الخامس من اليوم الاول",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise5_day1"
    elif operation_part_2 == "request_exercise5_day1" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise5_day1"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets5_day1"

    elif operation_part_2 == "request_sets5_day1" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثاني")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day1"]["day1_exercise5"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين السادس في اليوم الاول:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section6_day1"
    elif operation_part_2 == "request_section6_day1" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثاني")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الثاني" :
            context.user_data["operation_part_2"] = "request_section1_day2"
            await update.message.reply_text("جاري الانتقال الى اليوم الثاني ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section6_day1"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين السادس من اليوم الاول",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise6_day1"
    elif operation_part_2 == "request_exercise6_day1" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise6_day1"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets6_day1"

    elif operation_part_2 == "request_sets6_day1" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثاني")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day1"]["day1_exercise6"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين السابع في اليوم الاول:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section7_day1"
    elif operation_part_2 == "request_section7_day1" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثاني")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الثاني" :
            context.user_data["operation_part_2"] = "request_section1_day2"
            await update.message.reply_text("جاري الانتقال الى اليوم الثاني ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section7_day1"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين السابع من اليوم الاول",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise7_day1"
    elif operation_part_2 == "request_exercise7_day1" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise7_day1"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets7_day1"

    elif operation_part_2 == "request_sets7_day1" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثاني")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day1"]["day1_exercise7"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nتم الانتهاء من اليوم الاول، الان اختر قسم اول تمرين لليوم التالي:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section1_day2"

    # ==================== اليوم الثاني ====================

    elif operation_part_2 == "request_section1_day2" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("استراحه")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "استراحه" :
            data_base_part_2[current_key]["day2"] = ["استراحه"]
            save_data_base_part_2(data_base_part_2)
            context.user_data["operation_part_2"] = "request_section1_day3"
            await update.message.reply_text("تم حفظ اليوم الثاني كاستراحه \nالان اختر قسم اول تمرين لليوم التالي:", reply_markup=sections_keyboard)
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section1_day2"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("الان ادخل التمرين الاول الذي تريد اضافته في القسم الذي اخترته في اليوم الثاني:",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise1_day2"
    elif operation_part_2 == "request_exercise1_day2" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise1_day2"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets1_day2"

    elif operation_part_2 == "request_sets1_day2" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثالث")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day2"] = {"day2_exercise1":[current[0], current[1], text]}
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الثاني في اليوم الثاني:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section2_day2"
    elif operation_part_2 == "request_section2_day2" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثالث")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الثالث" :
            context.user_data["operation_part_2"] = "request_section1_day3"
            await update.message.reply_text("جاري الانتقال الى اليوم الثالث ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section2_day2"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الثاني من اليوم الثاني",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise2_day2"
    elif operation_part_2 == "request_exercise2_day2" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise2_day2"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets2_day2"

    elif operation_part_2 == "request_sets2_day2" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثالث")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day2"]["day2_exercise2"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الثالث في اليوم الثاني:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section3_day2"
    elif operation_part_2 == "request_section3_day2" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثالث")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الثالث" :
            context.user_data["operation_part_2"] = "request_section1_day3"
            await update.message.reply_text("جاري الانتقال الى اليوم الثالث ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section3_day2"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الثالث من اليوم الثاني",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise3_day2"
    elif operation_part_2 == "request_exercise3_day2" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise3_day2"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets3_day2"

    elif operation_part_2 == "request_sets3_day2" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثالث")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day2"]["day2_exercise3"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الرابع في اليوم الثاني:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section4_day2"
    elif operation_part_2 == "request_section4_day2" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثالث")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الثالث" :
            context.user_data["operation_part_2"] = "request_section1_day3"
            await update.message.reply_text("جاري الانتقال الى اليوم الثالث ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section4_day2"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الرابع من اليوم الثاني",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise4_day2"
    elif operation_part_2 == "request_exercise4_day2" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise4_day2"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets4_day2"

    elif operation_part_2 == "request_sets4_day2" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثالث")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day2"]["day2_exercise4"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الخامس في اليوم الثاني:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section5_day2"
    elif operation_part_2 == "request_section5_day2" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثالث")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الثالث" :
            context.user_data["operation_part_2"] = "request_section1_day3"
            await update.message.reply_text("جاري الانتقال الى اليوم الثالث ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section5_day2"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الخامس من اليوم الثاني",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise5_day2"
    elif operation_part_2 == "request_exercise5_day2" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise5_day2"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets5_day2"

    elif operation_part_2 == "request_sets5_day2" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثالث")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day2"]["day2_exercise5"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين السادس في اليوم الثاني:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section6_day2"
    elif operation_part_2 == "request_section6_day2" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثالث")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الثالث" :
            context.user_data["operation_part_2"] = "request_section1_day3"
            await update.message.reply_text("جاري الانتقال الى اليوم الثالث ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section6_day2"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين السادس من اليوم الثاني",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise6_day2"
    elif operation_part_2 == "request_exercise6_day2" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise6_day2"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets6_day2"

    elif operation_part_2 == "request_sets6_day2" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثالث")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day2"]["day2_exercise6"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين السابع في اليوم الثاني:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section7_day2"
    elif operation_part_2 == "request_section7_day2" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثالث")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الثالث" :
            context.user_data["operation_part_2"] = "request_section1_day3"
            await update.message.reply_text("جاري الانتقال الى اليوم الثالث ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section7_day2"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين السابع من اليوم الثاني",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise7_day2"
    elif operation_part_2 == "request_exercise7_day2" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise7_day2"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets7_day2"

    elif operation_part_2 == "request_sets7_day2" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الثالث")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day2"]["day2_exercise7"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nتم الانتهاء من اليوم الثاني، الان اختر قسم اول تمرين لليوم التالي:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section1_day3"

    # ==================== اليوم الثالث ====================

    elif operation_part_2 == "request_section1_day3" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("استراحه")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "استراحه" :
            data_base_part_2[current_key]["day3"] = ["استراحه"]
            save_data_base_part_2(data_base_part_2)
            context.user_data["operation_part_2"] = "request_section1_day4"
            await update.message.reply_text("تم حفظ اليوم الثالث كاستراحه \nالان اختر قسم اول تمرين لليوم التالي:", reply_markup=sections_keyboard)
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section1_day3"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("الان ادخل التمرين الاول الذي تريد اضافته في القسم الذي اخترته في اليوم الثالث:",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise1_day3"
    elif operation_part_2 == "request_exercise1_day3" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise1_day3"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets1_day3"

    elif operation_part_2 == "request_sets1_day3" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الرابع")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day3"] = {"day3_exercise1":[current[0], current[1], text]}
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الثاني في اليوم الثالث:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section2_day3"
    elif operation_part_2 == "request_section2_day3" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الرابع")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الرابع" :
            context.user_data["operation_part_2"] = "request_section1_day4"
            await update.message.reply_text("جاري الانتقال الى اليوم الرابع ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section2_day3"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الثاني من اليوم الثالث",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise2_day3"
    elif operation_part_2 == "request_exercise2_day3" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise2_day3"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets2_day3"

    elif operation_part_2 == "request_sets2_day3" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الرابع")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day3"]["day3_exercise2"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الثالث في اليوم الثالث:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section3_day3"
    elif operation_part_2 == "request_section3_day3" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الرابع")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الرابع" :
            context.user_data["operation_part_2"] = "request_section1_day4"
            await update.message.reply_text("جاري الانتقال الى اليوم الرابع ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section3_day3"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الثالث من اليوم الثالث",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise3_day3"
    elif operation_part_2 == "request_exercise3_day3" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise3_day3"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets3_day3"

    elif operation_part_2 == "request_sets3_day3" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الرابع")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day3"]["day3_exercise3"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الرابع في اليوم الثالث:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section4_day3"
    elif operation_part_2 == "request_section4_day3" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الرابع")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الرابع" :
            context.user_data["operation_part_2"] = "request_section1_day4"
            await update.message.reply_text("جاري الانتقال الى اليوم الرابع ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section4_day3"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الرابع من اليوم الثالث",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise4_day3"
    elif operation_part_2 == "request_exercise4_day3" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise4_day3"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets4_day3"

    elif operation_part_2 == "request_sets4_day3" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الرابع")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day3"]["day3_exercise4"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الخامس في اليوم الثالث:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section5_day3"
    elif operation_part_2 == "request_section5_day3" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الرابع")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الرابع" :
            context.user_data["operation_part_2"] = "request_section1_day4"
            await update.message.reply_text("جاري الانتقال الى اليوم الرابع ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section5_day3"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الخامس من اليوم الثالث",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise5_day3"
    elif operation_part_2 == "request_exercise5_day3" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise5_day3"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets5_day3"

    elif operation_part_2 == "request_sets5_day3" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الرابع")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day3"]["day3_exercise5"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين السادس في اليوم الثالث:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section6_day3"
    elif operation_part_2 == "request_section6_day3" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الرابع")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الرابع" :
            context.user_data["operation_part_2"] = "request_section1_day4"
            await update.message.reply_text("جاري الانتقال الى اليوم الرابع ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section6_day3"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين السادس من اليوم الثالث",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise6_day3"
    elif operation_part_2 == "request_exercise6_day3" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise6_day3"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets6_day3"

    elif operation_part_2 == "request_sets6_day3" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الرابع")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day3"]["day3_exercise6"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين السابع في اليوم الثالث:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section7_day3"
    elif operation_part_2 == "request_section7_day3" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الرابع")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الرابع" :
            context.user_data["operation_part_2"] = "request_section1_day4"
            await update.message.reply_text("جاري الانتقال الى اليوم الرابع ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section7_day3"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين السابع من اليوم الثالث",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise7_day3"
    elif operation_part_2 == "request_exercise7_day3" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise7_day3"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets7_day3"

    elif operation_part_2 == "request_sets7_day3" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الرابع")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day3"]["day3_exercise7"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nتم الانتهاء من اليوم الثالث، الان اختر قسم اول تمرين لليوم التالي:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section1_day4"

    # ==================== اليوم الرابع ====================

    elif operation_part_2 == "request_section1_day4" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("استراحه")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "استراحه" :
            data_base_part_2[current_key]["day4"] = ["استراحه"]
            save_data_base_part_2(data_base_part_2)
            context.user_data["operation_part_2"] = "request_section1_day5"
            await update.message.reply_text("تم حفظ اليوم الرابع كاستراحه \nالان اختر قسم اول تمرين لليوم التالي:", reply_markup=sections_keyboard)
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section1_day4"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("الان ادخل التمرين الاول الذي تريد اضافته في القسم الذي اخترته في اليوم الرابع:",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise1_day4"
    elif operation_part_2 == "request_exercise1_day4" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise1_day4"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets1_day4"

    elif operation_part_2 == "request_sets1_day4" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الخامس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day4"] = {"day4_exercise1":[current[0], current[1], text]}
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الثاني في اليوم الرابع:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section2_day4"
    elif operation_part_2 == "request_section2_day4" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الخامس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الخامس" :
            context.user_data["operation_part_2"] = "request_section1_day5"
            await update.message.reply_text("جاري الانتقال الى اليوم الخامس ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section2_day4"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الثاني من اليوم الرابع",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise2_day4"
    elif operation_part_2 == "request_exercise2_day4" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise2_day4"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets2_day4"

    elif operation_part_2 == "request_sets2_day4" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الخامس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day4"]["day4_exercise2"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الثالث في اليوم الرابع:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section3_day4"
    elif operation_part_2 == "request_section3_day4" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الخامس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الخامس" :
            context.user_data["operation_part_2"] = "request_section1_day5"
            await update.message.reply_text("جاري الانتقال الى اليوم الخامس ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section3_day4"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الثالث من اليوم الرابع",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise3_day4"
    elif operation_part_2 == "request_exercise3_day4" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise3_day4"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets3_day4"

    elif operation_part_2 == "request_sets3_day4" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الخامس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day4"]["day4_exercise3"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الرابع في اليوم الرابع:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section4_day4"
    elif operation_part_2 == "request_section4_day4" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الخامس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الخامس" :
            context.user_data["operation_part_2"] = "request_section1_day5"
            await update.message.reply_text("جاري الانتقال الى اليوم الخامس ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section4_day4"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الرابع من اليوم الرابع",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise4_day4"
    elif operation_part_2 == "request_exercise4_day4" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise4_day4"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets4_day4"

    elif operation_part_2 == "request_sets4_day4" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الخامس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day4"]["day4_exercise4"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الخامس في اليوم الرابع:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section5_day4"
    elif operation_part_2 == "request_section5_day4" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الخامس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الخامس" :
            context.user_data["operation_part_2"] = "request_section1_day5"
            await update.message.reply_text("جاري الانتقال الى اليوم الخامس ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section5_day4"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الخامس من اليوم الرابع",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise5_day4"
    elif operation_part_2 == "request_exercise5_day4" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise5_day4"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets5_day4"

    elif operation_part_2 == "request_sets5_day4" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الخامس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day4"]["day4_exercise5"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين السادس في اليوم الرابع:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section6_day4"
    elif operation_part_2 == "request_section6_day4" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الخامس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الخامس" :
            context.user_data["operation_part_2"] = "request_section1_day5"
            await update.message.reply_text("جاري الانتقال الى اليوم الخامس ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section6_day4"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين السادس من اليوم الرابع",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise6_day4"
    elif operation_part_2 == "request_exercise6_day4" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise6_day4"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets6_day4"

    elif operation_part_2 == "request_sets6_day4" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الخامس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day4"]["day4_exercise6"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين السابع في اليوم الرابع:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section7_day4"
    elif operation_part_2 == "request_section7_day4" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الخامس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم الخامس" :
            context.user_data["operation_part_2"] = "request_section1_day5"
            await update.message.reply_text("جاري الانتقال الى اليوم الخامس ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section7_day4"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين السابع من اليوم الرابع",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise7_day4"
    elif operation_part_2 == "request_exercise7_day4" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise7_day4"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets7_day4"

    elif operation_part_2 == "request_sets7_day4" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم الخامس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day4"]["day4_exercise7"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nتم الانتهاء من اليوم الرابع، الان اختر قسم اول تمرين لليوم التالي:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section1_day5"

    # ==================== اليوم الخامس ====================

    elif operation_part_2 == "request_section1_day5" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("استراحه")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "استراحه" :
            data_base_part_2[current_key]["day5"] = ["استراحه"]
            save_data_base_part_2(data_base_part_2)
            context.user_data["operation_part_2"] = "request_section1_day6"
            await update.message.reply_text("تم حفظ اليوم الخامس كاستراحه \nالان اختر قسم اول تمرين لليوم التالي:", reply_markup=sections_keyboard)
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section1_day5"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("الان ادخل التمرين الاول الذي تريد اضافته في القسم الذي اخترته في اليوم الخامس:",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise1_day5"
    elif operation_part_2 == "request_exercise1_day5" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise1_day5"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets1_day5"

    elif operation_part_2 == "request_sets1_day5" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم السادس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day5"] = {"day5_exercise1":[current[0], current[1], text]}
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الثاني في اليوم الخامس:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section2_day5"
    elif operation_part_2 == "request_section2_day5" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم السادس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم السادس" :
            context.user_data["operation_part_2"] = "request_section1_day6"
            await update.message.reply_text("جاري الانتقال الى اليوم السادس ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section2_day5"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الثاني من اليوم الخامس",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise2_day5"
    elif operation_part_2 == "request_exercise2_day5" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise2_day5"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets2_day5"

    elif operation_part_2 == "request_sets2_day5" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم السادس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day5"]["day5_exercise2"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الثالث في اليوم الخامس:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section3_day5"
    elif operation_part_2 == "request_section3_day5" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم السادس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم السادس" :
            context.user_data["operation_part_2"] = "request_section1_day6"
            await update.message.reply_text("جاري الانتقال الى اليوم السادس ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section3_day5"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الثالث من اليوم الخامس",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise3_day5"
    elif operation_part_2 == "request_exercise3_day5" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise3_day5"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets3_day5"

    elif operation_part_2 == "request_sets3_day5" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم السادس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day5"]["day5_exercise3"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الرابع في اليوم الخامس:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section4_day5"
    elif operation_part_2 == "request_section4_day5" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم السادس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم السادس" :
            context.user_data["operation_part_2"] = "request_section1_day6"
            await update.message.reply_text("جاري الانتقال الى اليوم السادس ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section4_day5"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الرابع من اليوم الخامس",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise4_day5"
    elif operation_part_2 == "request_exercise4_day5" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise4_day5"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets4_day5"

    elif operation_part_2 == "request_sets4_day5" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم السادس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day5"]["day5_exercise4"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الخامس في اليوم الخامس:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section5_day5"
    elif operation_part_2 == "request_section5_day5" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم السادس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم السادس" :
            context.user_data["operation_part_2"] = "request_section1_day6"
            await update.message.reply_text("جاري الانتقال الى اليوم السادس ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section5_day5"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الخامس من اليوم الخامس",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise5_day5"
    elif operation_part_2 == "request_exercise5_day5" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise5_day5"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets5_day5"

    elif operation_part_2 == "request_sets5_day5" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم السادس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day5"]["day5_exercise5"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين السادس في اليوم الخامس:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section6_day5"
    elif operation_part_2 == "request_section6_day5" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم السادس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم السادس" :
            context.user_data["operation_part_2"] = "request_section1_day6"
            await update.message.reply_text("جاري الانتقال الى اليوم السادس ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section6_day5"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين السادس من اليوم الخامس",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise6_day5"
    elif operation_part_2 == "request_exercise6_day5" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise6_day5"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets6_day5"

    elif operation_part_2 == "request_sets6_day5" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم السادس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day5"]["day5_exercise6"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين السابع في اليوم الخامس:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section7_day5"
    elif operation_part_2 == "request_section7_day5" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم السادس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "الانتقال الى اليوم السادس" :
            context.user_data["operation_part_2"] = "request_section1_day6"
            await update.message.reply_text("جاري الانتقال الى اليوم السادس ✅")
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section7_day5"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين السابع من اليوم الخامس",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise7_day5"
    elif operation_part_2 == "request_exercise7_day5" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise7_day5"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets7_day5"

    elif operation_part_2 == "request_sets7_day5" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("الانتقال الى اليوم السادس")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day5"]["day5_exercise7"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nتم الانتهاء من اليوم الخامس، الان اختر قسم اول تمرين لليوم التالي:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section1_day6"

    # ==================== اليوم السادس ====================

    elif operation_part_2 == "request_section1_day6" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("استراحه")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "استراحه" :
            data_base_part_2[current_key]["day6"] = ["استراحه"]
            data_base_part_2[current_key]["end"] = "end"
            save_data_base_part_2(data_base_part_2)
            context.user_data.clear()
            await update.message.reply_text("تم حفظ اليوم السادس كاستراحه ", reply_markup=commands_final)
            await update.message.reply_text("تم حفظ الجدول بنجاح! 🎉 اضغط على /start لاستلام جدولك",reply_markup=commands_final)
            context.user_data["user_choose"] = "waiting_for_photo"
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section1_day6"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("الان ادخل التمرين الاول الذي تريد اضافته في القسم الذي اخترته في اليوم السادس:",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise1_day6"
    elif operation_part_2 == "request_exercise1_day6" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise1_day6"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets1_day6"

    elif operation_part_2 == "request_sets1_day6" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("انهاء الجدول")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day6"] = {"day6_exercise1":[current[0], current[1], text]}
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الثاني في اليوم السادس:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section2_day6"
    elif operation_part_2 == "request_section2_day6" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("انهاء الجدول")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "انهاء الجدول" :
            data_base_part_2[current_key]["end"] = "end"
            save_data_base_part_2(data_base_part_2)
            context.user_data.clear()
            await update.message.reply_text("تم حفظ الجدول بنجاح! 🎉 اضغط على /start لاستلام جدولك",reply_markup=commands_final)
            context.user_data["user_choose"] = "waiting_for_photo"
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section2_day6"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الثاني من اليوم السادس",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise2_day6"
    elif operation_part_2 == "request_exercise2_day6" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise2_day6"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets2_day6"

    elif operation_part_2 == "request_sets2_day6" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("انهاء الجدول")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day6"]["day6_exercise2"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الثالث في اليوم السادس:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section3_day6"
    elif operation_part_2 == "request_section3_day6" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("انهاء الجدول")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "انهاء الجدول" :
            data_base_part_2[current_key]["end"] = "end"
            save_data_base_part_2(data_base_part_2)
            context.user_data.clear()
            await update.message.reply_text("تم حفظ الجدول بنجاح! 🎉 اضغط على /start لاستلام جدولك",reply_markup=commands_final)
            context.user_data["user_choose"] = "waiting_for_photo"
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section3_day6"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الثالث من اليوم السادس",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise3_day6"
    elif operation_part_2 == "request_exercise3_day6" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise3_day6"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets3_day6"

    elif operation_part_2 == "request_sets3_day6" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("انهاء الجدول")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day6"]["day6_exercise3"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الرابع في اليوم السادس:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section4_day6"
    elif operation_part_2 == "request_section4_day6" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("انهاء الجدول")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "انهاء الجدول" :
            data_base_part_2[current_key]["end"] = "end"
            save_data_base_part_2(data_base_part_2)
            context.user_data.clear()
            await update.message.reply_text("تم حفظ الجدول بنجاح! 🎉 اضغط على /start لاستلام جدولك",reply_markup=commands_final)
            context.user_data["user_choose"] = "waiting_for_photo"
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section4_day6"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الرابع من اليوم السادس",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise4_day6"
    elif operation_part_2 == "request_exercise4_day6" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise4_day6"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets4_day6"

    elif operation_part_2 == "request_sets4_day6" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("انهاء الجدول")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day6"]["day6_exercise4"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين الخامس في اليوم السادس:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section5_day6"
    elif operation_part_2 == "request_section5_day6" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("انهاء الجدول")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "انهاء الجدول" :
            data_base_part_2[current_key]["end"] = "end"
            save_data_base_part_2(data_base_part_2)
            context.user_data.clear()
            await update.message.reply_text("تم حفظ الجدول بنجاح! 🎉 اضغط على /start لاستلام جدولك",reply_markup=commands_final)
            context.user_data["user_choose"] = "waiting_for_photo"
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section5_day6"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            context.user_data["user_choose"] = "waiting_for_photo"
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين الخامس من اليوم السادس",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise5_day6"
    elif operation_part_2 == "request_exercise5_day6" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise5_day6"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets5_day6"

    elif operation_part_2 == "request_sets5_day6" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("انهاء الجدول")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day6"]["day6_exercise5"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين السادس في اليوم السادس:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section6_day6"
    elif operation_part_2 == "request_section6_day6" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("انهاء الجدول")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "انهاء الجدول" :
            data_base_part_2[current_key]["end"] = "end"
            save_data_base_part_2(data_base_part_2)
            context.user_data.clear()
            await update.message.reply_text("تم حفظ الجدول بنجاح! 🎉 اضغط على /start لاستلام جدولك",reply_markup=commands_final)
            context.user_data["user_choose"] = "waiting_for_photo"
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section6_day6"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين السادس من اليوم السادس",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise6_day6"
    elif operation_part_2 == "request_exercise6_day6" :
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise6_day6"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets6_day6"

    elif operation_part_2 == "request_sets6_day6" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("انهاء الجدول")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day6"]["day6_exercise6"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ العدات ✅\nالان اختر قسم التمرين السابع في اليوم السادس:", reply_markup=sections_keyboard)
        context.user_data["operation_part_2"] = "request_section7_day6"
    elif operation_part_2 == "request_section7_day6" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("انهاء الجدول")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "انهاء الجدول" :
            data_base_part_2[current_key]["end"] = "end"
            save_data_base_part_2(data_base_part_2)
            context.user_data.clear()
            await update.message.reply_text("تم حفظ الجدول بنجاح! 🎉 اضغط على /start لاستلام جدولك",reply_markup=commands_final)
            context.user_data["user_choose"] = "waiting_for_photo"
            return
        if text not in show_sections(user_id) :
            context.user_data["operation_part_2"] = "request_section7_day6"
            await update.message.reply_text("حدث خطا:اسم القسم الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=sections_keyboard)
            return  
        if show_exercises(user_id, text) == [] :
            context.user_data.clear()
            await update.message.reply_text("القسم الذي اخترته لا يحتوي على تمارين, حاول اختيار قسم اخر او اضافه تمارين للقسم الذي اخترته اولاً.")
            return  
        context.user_data["operation_part_3"] = text
        await update.message.reply_text("اختيار التمرين السابع من اليوم السادس",reply_markup=show_exercises_keyboard_button(user_id, text))
        context.user_data["operation_part_2"] = "request_exercise7_day6"
    elif operation_part_2 == "request_exercise7_day6" :  # ← الشرط الأخير (رقم 86)
        if text not in show_exercises(user_id, operation_part_3) :
             context.user_data["operation_part_2"] = "request_exercise7_day6"
             await update.message.reply_text("حدث خطا:اسم التمرين الذي ادخلته غير موجود, حاول مره اخرى ", reply_markup=show_exercises_keyboard_button(user_id, operation_part_3))
             return  
        context.user_data["current_exercise"] = [operation_part_3, text]
        await update.message.reply_text("الان ادخل العدات للتمرين الذي اخترته:")
        context.user_data["operation_part_2"] = "request_sets7_day6"

    elif operation_part_2 == "request_sets7_day6" :
        sections = show_sections(user_id)
        buttons = [[KeyboardButton(s)] for s in sections]
        buttons.append([KeyboardButton("انهاء الجدول")])
        sections_keyboard = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        if text == "انهاء الجدول" :
            data_base_part_2[current_key]["end"] = "end"
            save_data_base_part_2(data_base_part_2)
            context.user_data.clear()
            await update.message.reply_text("تم حفظ الجدول بنجاح! 🎉 اضغط على /start لاستلام جدولك",reply_markup=commands_final)
            context.user_data["user_choose"] = "waiting_for_photo"
            return
        current = context.user_data.get("current_exercise")
        data_base_part_2[current_key]["day6"]["day6_exercise7"] = [current[0], current[1], text]
        save_data_base_part_2(data_base_part_2)
        await update.message.reply_text("تم حفظ الجدول بنجاح! 🎉 اضغط على /start لاستلام جدولك",reply_markup=commands_final)
        context.user_data["user_choose"] = "waiting_for_photo"    
    else :
        await update.message.reply_text("خطأ:لقد ادخال بيانات غير صحيحة, حاول مره اخرى.", reply_markup=commands_final)
        context.user_data.clear()
        return
    
#handlers
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, start))
app.add_handler(CommandHandler("start", start))

#run forever
app.run_polling()