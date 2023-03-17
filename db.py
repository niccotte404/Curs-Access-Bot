import sqlite3
import imaplib

# Запуск БД
async def open_database():
    global connect, cursor
    connect = sqlite3.connect("curs_access.db")
    cursor = connect.cursor()
    
    if connect:
        print("Databace connected OK")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS mails(
        mail TEXT PRIMARY KEY,
        curs TEXT
        )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS administration(
        user_id TEXT PRIMARY KEY,
        user_name TEXT,
        user_type TEXT
        )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS curses(
        curs TEXT,
        description TEXT, 
        url TEXT
        )""")
    
    connect.commit()
    
    
# Добавление пользователя
async def add_user(message):
    
    user_id = message.from_user.id
    username = message.from_user.username
    data = cursor.execute(f"SELECT user_id FROM administration WHERE user_id = '{user_id}'").fetchone()[0]
    print(data)
    if data is None:
        if user_id == 1468286116:
            cursor.execute("INSERT INTO administration VALUES (?, ?, ?)", (user_id, username, "админ"))
        else:
            cursor.execute("INSERT INTO administration VALUES (?, ?, ?)", (user_id, username, "юзверь"))
        connect.commit()
        

# Проверка на администратора
async def check_admin(message):
    
    user_id = message.from_user.id
    admins = cursor.execute("SELECT user_id FROM administration WHERE user_type='админ'").fetchall()
    for item in admins:
        if user_id == int(item[0]):
            return True
    return False


# Добавление администратора
async def add_curs(data):
    cursor.execute("INSERT INTO curses VALUES (?, ?, ?)", data)
    connect.commit()
    

# Выгрузка курсов
async def load_curses():
    
    curses = []
    data = cursor.execute("SELECT * FROM curses").fetchall()
    for curs in data:
        curses.append(curs[0])
    return curses



# Выгрузка курсов 2
async def load_curses_for_other():
    data = cursor.execute("SELECT * FROM curses").fetchall()
    return data


# Здесь должна быть функция обработки почты и поиска совпадений 
# async def mail_data(user_data):

#     send_to = user_data[1]
    
#     mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
#     mail.login('nickys.create@gmail.com', 'helloyolo')
#     mail.list()
#     mail.select("INBOX")
#     print("Entered to SENT OK")
    
#     res, data = mail.search(None, 'ALL')
#     print("Got email OK")
#     ids = data[0]
#     id_list = ids.split()
#     latest_email_id = id_list[-1]
    
#     res, data = mail.fetch(latest_email_id, "(RFC822)")
#     raw_email = data[0][1]
#     print(raw_email)
    
#     mail.close()
#     mail.logout()
    
#     # Возврат True/False