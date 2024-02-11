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
