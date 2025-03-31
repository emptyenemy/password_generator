import requests
import sys
import os
import zipfile
import shutil
import pyfiglet
from colorama import init, Fore, Style

def get_local_version():
    try:
        from version import __version__
        return __version__
    except Exception:
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

def download_latest_release(version):
    download_url = f"https://github.com/emptyenemy/password_generator/archive/refs/tags/{version}.zip"
    print(Fore.YELLOW + "Скачиваем последнюю версию проекта..." + Style.RESET_ALL)
    response = requests.get(download_url)
    if response.status_code == 200:
        with open('password_generator_latest.zip', 'wb') as f:
            f.write(response.content)
        print(Fore.GREEN + "Загрузка завершена!" + Style.RESET_ALL)
    else:
        print(Fore.RED + "Ошибка при скачивании файла!" + Style.RESET_ALL)
        sys.exit(1)

def extract_zip():
    print(Fore.YELLOW + "Распаковываем архив..." + Style.RESET_ALL)
    try:
        with zipfile.ZipFile('password_generator_latest.zip', 'r') as zip_ref:
            if zip_ref.testzip() is not None:
                print(Fore.RED + "Ошибка: повреждённый zip-архив!" + Style.RESET_ALL)
                sys.exit(1)
            zip_ref.extractall('password_generator_latest')
        print(Fore.GREEN + "Распаковка завершена!" + Style.RESET_ALL)
    except zipfile.BadZipFile:
        print(Fore.RED + "Ошибка: файл не является корректным zip-архивом!" + Style.RESET_ALL)
        sys.exit(1)

def get_extracted_folder_name(extract_path):
    entries = os.listdir(extract_path)
    for entry in entries:
        full_path = os.path.join(extract_path, entry)
        if os.path.isdir(full_path):
            return full_path
    return extract_path

def replace_old_files(source_dir):
    print(Fore.YELLOW + "Заменяем старые файлы новыми..." + Style.RESET_ALL)
    for item in os.listdir(source_dir):
        s = os.path.join(source_dir, item)
        d = os.path.join(os.getcwd(), item)
        if os.path.exists(d):
            if os.path.isdir(d):
                shutil.rmtree(d)
            else:
                os.remove(d)
        shutil.move(s, d)
    print(Fore.GREEN + "Файлы успешно заменены!" + Style.RESET_ALL)

def clean_up():
    if os.path.exists('password_generator_latest.zip'):
        os.remove('password_generator_latest.zip')
    if os.path.exists('password_generator_latest'):
        shutil.rmtree('password_generator_latest')

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
            download_latest_release(remote)
            extract_zip()
            extracted_folder = get_extracted_folder_name('password_generator_latest')
            replace_old_files(extracted_folder)
            clean_up()
            print(Fore.GREEN + "Обновление завершено! Перезапустите программу." + Style.RESET_ALL)
        else:
            print(Fore.RED + "Обновление отменено пользователем." + Style.RESET_ALL)
    else:
        print(Fore.GREEN + "У вас установлена последняя версия." + Style.RESET_ALL)

if __name__ == '__main__':
    main()
