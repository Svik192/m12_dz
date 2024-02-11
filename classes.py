from collections import UserDict
from datetime import datetime, timedelta
import pickle


# import json


class Field:
    def __init__(self, value):
        if self.is_valid(value):
            self.__value = value
        else:
            raise ValueError("Invalid value")

    def is_valid(self, value):
        return True

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        if self.is_valid(value):
            self.__value = value
        else:
            raise ValueError("Invalid value")

    def __str__(self):
        return str(self.__value)


class Name(Field):
    pass


class Birthday(Field):

    def is_valid(self, str_birthday):
        if str_birthday is None:
            return True
        try:
            datetime.strptime(str_birthday, '%Y-%m-%d').date()
            return True
        except ValueError:
            return False


class Phone(Field):

    def is_valid(self, value):
        return len(value) == 10 and value.isdigit()


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        try:
            self.phones.remove(self.find_phone(phone))
        except ValueError:
            raise ValueError("Phone not found")

        return phone

    def edit_phone(self, old_phone, new_phone):

        if self.find_phone(old_phone) is None:
            raise ValueError("Phone number does not exist")

        self.remove_phone(old_phone)
        self.add_phone(new_phone)

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def days_to_birthday(self):

        if self.birthday.value is None:
            return None
        else:
            current_date = datetime.today().date()
            bd = datetime.strptime(self.birthday.value, '%Y-%m-%d').date()

            birthday_this_year = datetime(year=current_date.year, month=bd.month, day=bd.day).date()
            difference = birthday_this_year - current_date
            if difference < timedelta(days=0):
                birthday_this_year = datetime(year=current_date.year + 1, month=bd.month, day=bd.day).date()
                difference = birthday_this_year - current_date

            return difference.days

    def __str__(self):
        if self.birthday.value is None:
            return (f"Contact name: {self.name.value}, "
                    f"phones: {'; '.join(str(p) for p in self.phones)} ")
        else:
            return (f"Contact name: {self.name.value}, "
                    f"phones: {'; '.join(str(p) for p in self.phones)}, "
                    f"birthday: {self.birthday}")


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        record = self.data.get(name, None)
        return record

        # return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, portion_size=2):
        records = list(self.data.values())
        i = 0
        while i < len(records):
            portion = records[i:i + portion_size]
            yield portion
            i += portion_size

    # def save_to_file(self, file_name: str):
    #     with open(file_name, "w") as file:
    #         json.dump(self.data, file)
    #
    # def loading_from_file(self, file_name: str):
    #     self.data = {}
    #     with open(file_name, "r") as file:
    #         self.data = json.load(file)

    def save_to_file(self, file_name: str):
        with open(file_name, "wb") as file:
            pickle.dump(self.data, file)

    def loading_from_file(self, file_name: str):
        self.data = {}
        with open(file_name, "rb") as file:
            self.data = pickle.load(file)


if __name__ == "__main__":

    # Створення нової адресної книги
    book = AddressBook()

    try:
        book.loading_from_file("AddressBook.bin")
    except Exception as e:
        print(type(e).__name__, e)

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print("-++-")
        print(record)

    print("---" * 50)

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")

    # Додавання запису John до адресної книги
    book.add_record(john_record)

    # Створення та додавання нового запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")

    # Створення та додавання нового запису для Jane
    jack_record = Record("Jack")
    jack_record.add_phone("1234554321")
    jack_record.birthday.value = "1992-05-05"
    book.add_record(jack_record)

    # Додавання дня народження для запису Jane та John
    jane_record.birthday.value = "1992-03-03"

    # john_record.birthday = "1990-011-15"

    # Додавання запису Jane до адресної книги
    book.add_record(jane_record)

    # Виведення в консоль днів до дня народження Jane та John
    print(jane_record.days_to_birthday())
    print(john_record.days_to_birthday())

    # Виведення всіх записів у книзі
    for name, record in book.data.items():
        print("-++-")
        print(record)

    print("---" * 10)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    print(john)

    john.edit_phone("1234567890", "1112223333")

    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    print("---" * 20)
    found_phone = john.find_phone("5555555555")
    # found_phone = john.find_phone("1234567890")
    print(f"{john.name}: {found_phone}")  # Виведення: 5555555555

    print("+" * 70)
    for portion in book.iterator():
        print(type(portion))
        print(portion)

        for item in portion:
            print(item)

        print("-" * 40)

    # Видалення запису Jane
    book.delete("Jane")

    # Збереження книги в файл
    try:
        book.save_to_file("AddressBook.bin")
        print("The address book is saved to disk.")
    except Exception as e:
        print(type(e).__name__, e)

    # # Видалення запису Jane
    # book.delete("Jane")
