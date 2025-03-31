import requests
import subprocess
import sys
import os
import zipfile
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

def download_latest_release():
    url = "https://github.com/emptyenemy/password_generator/archive/refs/tags/v1.0.6.zip"  # Поменяйте на актуальный URL для последнего релиза
    print(Fore.YELLOW + "Скачиваем последнюю версию проекта..." + Style.RESET_ALL)
    response = requests.get(url)
    with open('password_generator_latest.zip', 'wb') as f:
        f.write(response.content)
    print(Fore.GREEN + "Загрузка завершена!" + Style.RESET_ALL)

def extract_zip():
    print(Fore.YELLOW + "Распаковываем архив..." + Style.RESET_ALL)
    with zipfile.ZipFile('password_generator_latest.zip', 'r') as zip_ref:
        zip_ref.extractall('password_generator_latest')
    print(Fore.GREEN + "Распаковка завершена!" + Style.RESET_ALL)

def replace_old_files():
    print(Fore.YELLOW + "Заменяем старые файлы новыми..." + Style.RESET_ALL)
    for root, dirs, files in os.walk('password_generator_latest/password_generator-1.0.6'):  # Замените на актуальный путь после распаковки
        for file in files:
            old_file_path = os.path.join(root, file)
            new_file_path = os.path.join(os.getcwd(), file)

            if os.path.exists(new_file_path):
                os.remove(new_file_path)

            os.rename(old_file_path, new_file_path)
    print(Fore.GREEN + "Файлы успешно заменены!" + Style.RESET_ALL)

def print_banner():
    ascii_banner = pyfiglet.figlet_format("Update Checker")
    print(Fore.CYAN + ascii_banner + "by @emptyenemy\n" + Style.RESET_ALL)

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
            download_latest_release()
            extract_zip()
            replace_old_files()
            print(Fore.GREEN + "Обновление завершено!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Обновление отменено пользователем." + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "У вас установлена последняя версия." + Style.RESET_ALL)

if __name__ == '__main__':
    main()
