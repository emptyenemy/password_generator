import string
import random
from colorama import init, Fore, Style

def generate_password(length, groups, charset):
    password_chars = [random.choice(group) for group in groups]
    password_chars += [random.choice(charset) for _ in range(length - len(groups))]
    random.shuffle(password_chars)
    return ''.join(password_chars)

def main():
    init(autoreset=True)
    print(Fore.CYAN + "\nГенератор паролей\n")
    while True:
        try:
            length = int(input(Fore.YELLOW + "Введите количество символов для пароля: " + Style.RESET_ALL))
            if length <= 0:
                print(Fore.RED + "\nКоличество символов должно быть положительным. Попробуйте снова.\n" + Style.RESET_ALL)
                continue
            break
        except ValueError:
            print(Fore.RED + "\nПожалуйста, введите корректное число.\n" + Style.RESET_ALL)
    print(Fore.CYAN + "\nВыберите пресет для пароля:")
    print("1: Только строчные латинские буквы")
    print("2: Строчные и заглавные латинские буквы")
    print("3: Строчные, заглавные латинские буквы и цифры")
    print("4: Строчные, заглавные буквы, цифры и спецсимволы\n" + Style.RESET_ALL)
    while True:
        preset = input(Fore.YELLOW + "Введите номер пресета: " + Style.RESET_ALL).strip()
        if preset == "1":
            groups = [string.ascii_lowercase]
            charset = string.ascii_lowercase
            break
        elif preset == "2":
            groups = [string.ascii_lowercase, string.ascii_uppercase]
            charset = string.ascii_lowercase + string.ascii_uppercase
            break
        elif preset == "3":
            groups = [string.ascii_lowercase, string.ascii_uppercase, string.digits]
            charset = string.ascii_lowercase + string.ascii_uppercase + string.digits
            break
        elif preset == "4":
            groups = [string.ascii_lowercase, string.ascii_uppercase, string.digits, string.punctuation]
            charset = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
            break
        else:
            print(Fore.RED + "\nНеверный выбор. Попробуйте снова.\n" + Style.RESET_ALL)
    if length < len(groups):
        print(Fore.RED + "\nДлина пароля должна быть не меньше количества групп (" + str(len(groups)) + ").\n" + Style.RESET_ALL)
        return
    password = generate_password(length, groups, charset)
    print(Fore.GREEN + "\nСгенерированный пароль: " + Fore.WHITE + password + "\n" + Style.RESET_ALL)

if __name__ == '__main__':
    main()
