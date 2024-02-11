from classes import AddressBook


class Bot:

    def __init__(self):
        self.file_name = "AddressBook.bin"
        self.book = AddressBook()

        try:
            self.book.loading_from_file(self.file_name)
        except Exception as e:
            print(type(e).__name__, e)

    @staticmethod
    def input_error(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except (TypeError, KeyError, ValueError, IndexError) as e:
                print(f"Error: {e}")
                return None

        return wrapper

    def hello(self, data):
        return "How can I help you?"

    @input_error
    def add_contact(self, data, name, phone):
        data[name] = phone
        return f"Contact '{name}' with phone number '{phone}' added successfully."

    @input_error
    def change_phone(self, data, name, phone):
        data[name] = phone
        return f"Phone number for '{name}' changed to '{phone}'."

    @input_error
    def get_phone(self, data, name):
        return f"The phone number for '{name}' is {data[name]}."

    def show_all(self, data):
        if not data:
            return "No contacts available."

        result = "All contacts:\n"
        for name, phone in data.items():
            result += f"{name}: {phone}\n"
        return result

    def good_bye(self, data):
        try:
            self.book.save_to_file(self.file_name)
            print("The address book is saved to disk.")
        except Exception as e:
            print(type(e).__name__, e)

        return "Good bye!"

    def default_handler(self, data):
        return "Unknown command. Please try again."

    commands = {
        "hello": hello,
        "add": add_contact,
        "change": change_phone,
        "phone": get_phone,
        "show all": show_all,
        "good bye": good_bye,
        "close": good_bye,
        "exit": good_bye,
    }

    @input_error
    def parse_command(self, user_input):
        command, args = None, []

        for cmd in self.commands:
            if user_input.startswith(cmd):
                command = cmd
                args = user_input.replace(cmd, "").split()

        return command, args

    @input_error
    def curry_command_handler(self, data):
        def command_handler(command, *args):
            return self.commands.get(command, self.default_handler)(self, data, *args)

        return command_handler

    def run(self):
        data = {}
        handle_command = self.curry_command_handler(data)

        while True:
            user_input = input("Enter command: ")

            command, args = self.parse_command(user_input)
            print("command: ", command, type(command))
            print("args: ", args)

            result = handle_command(command, *args)
            print(result)

            if result == "Good bye!":
                break

    # if __name__ == "__main__":
    #     main()
