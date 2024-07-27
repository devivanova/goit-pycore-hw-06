from collections import UserDict
import re


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        self.value = self.validate(value)

    def validate(self, value):
        if re.match(r'^\d{10}$', value):
            return value
        else:
            raise ValueError("Phone number must be 10 digits")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return True
        return False

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = Phone(new_phone).value
                return True
        return False

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones = ', '.join(p.value for p in self.phones)
        return f"Contact name: {self.name.value}, phones: {phones}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return True
        return False


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Invalid command. Please provide correct arguments."
    return inner


@input_error
def add_contact(args, contacts):
    if len(args) != 2:
        raise ValueError("Invalid command. Usage: add [name] [phone]")
    name, phone = args
    record = contacts.find(name)
    if record:
        record.add_phone(phone)
    else:
        record = Record(name)
        record.add_phone(phone)
        contacts.add_record(record)
    return "Contact added."


@input_error
def change_contact(args, contacts):
    if len(args) != 2:
        raise ValueError("Invalid command. Usage: change [name] [new_phone]")
    name, new_phone = args
    record = contacts.find(name)
    if record:
        if record.edit_phone(record.phones[0].value, new_phone):
            return "Contact updated."
        else:
            return "Phone number not found."
    else:
        raise KeyError("Contact not found.")


@input_error
def show_phone(args, contacts):
    if len(args) != 1:
        raise ValueError("Invalid command. Usage: phone [name]")
    name = args[0]
    record = contacts.find(name)
    if record:
        return ', '.join(phone.value for phone in record.phones)
    else:
        raise KeyError("Contact not found.")


@input_error
def show_all(contacts):
    if not contacts.data:
        return "No contacts found."
    return "\n".join([str(record) for record in contacts.data.values()])


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, args


def main():
    contacts = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, contacts))
        elif command == "change":
            print(change_contact(args, contacts))
        elif command == "phone":
            print(show_phone(args, contacts))
        elif command == "all":
            print(show_all(contacts))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
