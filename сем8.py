import json


def load():
    with open('BD.json', 'r', encoding='utf-8') as file:
        bd_local = json.load(file)
    return bd_local


def save(data):
    with open('BD.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(data, ensure_ascii=False))
    print("БД успешно сохранена.")


def findContact(con, data_contacts):
    try:
        return data_contacts[con]
    except KeyError:
        return 'Не нашли такого человека в Ваших контактах...'
    

def appendContact(name, birthday, email):
    phones = []
    num_of_phones = int(input('Сколько номеров у контакта?'))
    while num_of_phones != 0:
        try:
            number = input("Введите номер - ")
            phones.append(number)
        except ValueError:
            print("Вы ввели не цифру...")
        num_of_phones -= 1
    new_dict = {'phone': phones, 'birthday': f'{birthday}', 'email': f'{email}'}
    contacts[name] = new_dict
    save(contacts)


def delite_con(name, data):
    data.pop(name)
    save(data)

    

contacts = {'Маша': {'phone': ['89524578854', '7454787458'], 'birthday': '17.11.2001', 'email': 'blabla@gmail.com'},
            'Миша': {'phone': ['88955225554', '7548752458'], 'birthday': '17.11.2001', 'email': 'blablamisa@gmail.com'}}


while True:
    command = input('1 - найти контакт, 2 - добавить контакт, 3 - вывести все данные, 4 - удалить контакт, exit - завершить программу\n')
    if command == '1':
        data_con = input("Введите имя контакта \n")
        data_contacts = load()
        print(findContact(data_con, data_contacts))
    elif command == '2':
        name_new_contact = input('Введите данные о контакте\n имя - ')
        birthday_new_contact = input('день рождения - ')
        email_new_contact = input('почту - ')
        appendContact(name_new_contact, birthday_new_contact, email_new_contact)
    elif command == '3':
        data_bd = load()
        print(data_bd)
    elif command == '4':
        del_name = input("Введите имя контакта, который хотите удалить - ")
        data_bd = load()
        delite_con(del_name, data_bd)
    elif command == 'exit':
        print("Программа завершена! Всего хорошего!")
        break
    else:
        print('Вы ввели несуществующую команду...')


for i in contacts:
    for v in contacts[i]:
        print(contacts[i][v])


