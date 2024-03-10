import classes
from classes import AddressBook, Record


class Bot:

    def __init__(self):
        self.file_name = "AddressBook.bin"
        self.book = AddressBook()

        try:
            self.book.loading_from_file(self.file_name)
            print("Loaded from file!")
        except Exception as e:
            print(type(e).__name__, e)

    @staticmethod
    def input_error(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (TypeError, KeyError, ValueError, IndexError) as e:
                return f"Error: {e}"

        return wrapper

    def hello(self):
        return "How can I help you?"

    @input_error
    def add_contact(self, name: str, phone):
        if name not in self.book.data:
            record = Record(name)
        else:
            record = self.book.find(name)

        ph = classes.Phone(phone)
        if ph.is_valid(phone):
            record.add_phone(phone)
            self.book.add_record(record)
            return f"Contact '{name}' with phone number '{phone}' added successfully."
        else:
            return f"Wrong format"

    @input_error
    def change_phone(self, name, old_phone, new_phone):
        if name not in self.book.data:
            return "Name not found in contacts!"
        else:
            record = self.book.find(name)

            record.edit_phone(old_phone, new_phone)
            return f"Phone number for '{name}' changed to '{new_phone}'."

    @input_error
    def get_phone(self, name):
        if name not in self.book:
            return "Name not found in contacts!"
        else:
            return f"The phone number for '{name}' is {self.book[name]}."

    def show_all(self):
        if not self.book:
            return "No contacts available."

        result = "All contacts:\n"
        for name, phone in self.book.items():
            result += f"{name}: {phone}\n"
        return result

    def good_bye(self):
        try:
            self.book.save_to_file(self.file_name)
            print("The address book is saved to disk.")
        except Exception as e:
            print(type(e).__name__, e)

        return "Good bye!"

    def default_handler(self, _):
        return "Unknown command. Please try again."

    def search(self, text):
        result = set()
        for record in self.book.data.values():
            if text in record.name.value:
                result.add(record)
            for phone in record.phones:
                if text in phone.value:
                    result.add(record)

        if len(result) == 0:
            return "Contacts not found"

        return '\n'.join([str(record) for record in result])

    def delete_contact(self, name):
        if self.book.find(name):
            self.book.delete(name)
            return f"{name} contact deleted"
        else:
            return "Contacts not found"

    def my_help(self):
        return ("You can use these commands:\n"
                "hello\n"
                "add name phone\n"
                "change name old_phone new_phone\n"
                "phone name\n"
                "show all\n"
                "search \n"
                "del name \n"
                "good bye\n"
                "close\n"
                "exit\n"
                )

    commands = {
        "hello": hello,
        "add ": add_contact,
        "change ": change_phone,
        "phone ": get_phone,
        "show all": show_all,
        "good bye": good_bye,
        "search ": search,
        "del ": delete_contact,
        "close": good_bye,
        "exit": good_bye,
        "help": my_help,
    }

    @input_error
    def parse_command(self, user_input: str):
        command, args = None, []
        user_input = user_input.lower()

        for cmd in self.commands:
            if user_input.startswith(cmd):
                command = cmd
                args = user_input.replace(cmd, "").split()
                if len(args) >= 1:
                    args[0] = args[0].capitalize()  # name with a capital letter

        return command, args

    @input_error
    def command_handler(self, command, *args):
        return self.commands.get(command, self.default_handler)(self, *args)

    def run(self):
        while True:
            user_input = input("Enter command: ")

            command, args = self.parse_command(user_input)
            print("command: ", command)
            print("args: ", args)

            result = self.command_handler(command, *args)
            print(result)

            if result == "Good bye!":
                break
