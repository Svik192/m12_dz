from classes import AddressBook


class Bot:

    def __init__(self):
        self.file_name = "AddressBook.json"
        self.book = AddressBook()
        self.data = {}

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
        if name in self.data:
            return "This name is already in the contact list!"
        else:
            self.data[name] = phone
            return f"Contact '{name}' with phone number '{phone}' added successfully."

    @input_error
    def change_phone(self, name, phone):
        if name not in self.data:
            return "Name not found in contacts!"
        else:
            self.data[name] = phone
            return f"Phone number for '{name}' changed to '{phone}'."

    @input_error
    def get_phone(self, name):
        if name not in self.data:
            return "Name not found in contacts!"
        else:
            return f"The phone number for '{name}' is {self.data[name]}."

    def show_all(self):
        if not self.data:
            return "No contacts available."

        result = "All contacts:\n"
        for name, phone in self.data.items():
            result += f"{name}: {phone}\n"
        return result

    def good_bye(self):
        try:
            self.book.save_to_file(self.file_name)
            print("The address book is saved to disk.")
        except Exception as e:
            print(type(e).__name__, e)

        return "Good bye!"

    def default_handler(self):
        return "Unknown command. Please try again."

    def my_help(self):
        return ("You can use these commands:\n"
                "hello\n"
                "add name phone\n"
                "change name phone\n"
                "phone name\n"
                "show all\n"
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

    if __name__ == "__main__":
        run()
