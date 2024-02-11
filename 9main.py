def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (TypeError, KeyError, ValueError, IndexError) as e:
            return f"Error: {e}"

    return wrapper


def hello(data):
    return "How can I help you?"


@input_error
def add_contact(data, name: str, phone):
    if name in data:
        return "This name is already in the contact list!"
    else:
        data[name] = phone
        return f"Contact '{name}' with phone number '{phone}' added successfully."


@input_error
def change_phone(data, name, phone):
    if name not in data:
        return "Name not found in contacts!"
    else:
        data[name] = phone
        return f"Phone number for '{name}' changed to '{phone}'."


@input_error
def get_phone(data, name):
    if name not in data:
        return "Name not found in contacts!"
    else:
        return f"The phone number for '{name}' is {data[name]}."


def show_all(data):
    if not data:
        return "No contacts available."

    result = "All contacts:\n"
    for name, phone in data.items():
        result += f"{name}: {phone}\n"
    return result


def good_bye(data):
    return "Good bye!"


def default_handler(data):
    return "Unknown command. Please try again."


def my_help(data):
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
def parse_command(user_input: str):
    command, args = None, []
    user_input = user_input.lower()

    for cmd in commands:
        if user_input.startswith(cmd):
            command = cmd
            args = user_input.replace(cmd, "").split()
            if len(args) >= 1:
                args[0] = args[0].capitalize()  # name with a capital letter

    return command, args


@input_error
def curry_command_handler(data):
    def command_handler(command, *args):
        return commands.get(command, default_handler)(data, *args)

    return command_handler


def main():
    data = {}
    handle_command = curry_command_handler(data)

    while True:
        user_input = input("Enter command: ")

        command, args = parse_command(user_input)
        print("command: ", command)
        print("args: ", args)

        result = handle_command(command, *args)
        print(result)

        if result == "Good bye!":
            break


if __name__ == "__main__":
    main()
