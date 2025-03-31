import requests
import subprocess
import sys
import pyfiglet
from colorama import init, Fore, Style

def get_local_version():
    try:
        from version import __version__
        return __version__
    except Exception as e:
        print(Fore.RED + "Ошибка: не удалось получить локальную версию" + Style.RESET_ALL)
        sys.exit(1)

def get_remote_version():
    url = "https://api.github.com/repos/emptyenemy/password_generator/releases/latest"
    response = requests.get(url)
    if response.status_code != 200:
        print(Fore.RED + "Ошибка при получении информации о последнем релизе" + Style.RESET_ALL)
        sys.exit(1)
    data = response.json()
    tag = data.get("tag_name", "")
    tag = tag.lstrip('v')
    return tag

def version_tuple(v):
    return tuple(map(int, v.split(".")))

def is_update_available(local, remote):
    try:
        return version_tuple(local) < version_tuple(remote)
    except Exception:
        print(Fore.RED + "Ошибка при сравнении версий" + Style.RESET_ALL)
        sys.exit(1)

def update_repo():
    try:
        subprocess.run(["git", "pull"], check=True)
        print(Fore.GREEN + "Обновление завершено успешно!" + Style.RESET_ALL)
    except subprocess.CalledProcessError:
        print(Fore.RED + "Ошибка обновления репозитория." + Style.RESET_ALL)
        sys.exit(1)

def print_banner():
    ascii_banner = pyfiglet.figlet_format("Update\nChecker")
    print(Fore.CYAN + ascii_banner + "\nby @emptyenemy\n" + Style.RESET_ALL)

def main():
    init(autoreset=True)
    print_banner()
    local = get_local_version()
    remote = get_remote_version()
    print(Fore.YELLOW + f"Локальная версия: {local}" + Style.RESET_ALL)
    print(Fore.YELLOW + f"Последняя версия: {remote}" + Style.RESET_ALL)
    if is_update_available(local, remote):
        choice = input(Fore.YELLOW + "Доступна новая версия. Обновить? (Y/N): " + Style.RESET_ALL).strip().lower()
        if choice == 'y':
            update_repo()
        else:
            print(Fore.RED + "\nОбновление отменено пользователем." + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "\nУ вас установлена последняя версия." + Style.RESET_ALL)

if __name__ == '__main__':
    main()
