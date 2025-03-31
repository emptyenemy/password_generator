import requests
import subprocess
import sys

def get_local_version():
    try:
        from version import __version__
        return __version__
    except Exception as e:
        print("Ошибка: не удалось получить локальную версию")
        sys.exit(1)

def get_remote_version():
    url = "https://api.github.com/repos/emptyenemy/password_generator/releases/latest"
    response = requests.get(url)
    if response.status_code != 200:
        print("Ошибка при получении информации о последнем релизе")
        sys.exit(1)
    data = response.json()
    tag = data.get("tag_name", "")
    tag = tag.lstrip('v')  # Удаляем только ведущие 'v', если они есть
    return tag

def version_tuple(v):
    return tuple(map(int, v.split(".")))

def is_update_available(local, remote):
    try:
        return version_tuple(local) < version_tuple(remote)
    except Exception:
        print("Ошибка при сравнении версий")
        sys.exit(1)

def update_repo():
    try:
        subprocess.run(["git", "pull"], check=True)
        print("Обновление завершено успешно!")
    except subprocess.CalledProcessError:
        print("Ошибка обновления репозитория.")
        sys.exit(1)

def main():
    local = get_local_version()
    remote = get_remote_version()
    print(f"Локальная версия: {local}")
    print(f"Последняя версия: {remote}")
    if is_update_available(local, remote):
        choice = input("Доступна новая версия. Обновить? (Y/N): ").strip().lower()
        if choice == 'y':
            update_repo()
        else:
            print("Обновление отменено пользователем.")
    else:
        print("У вас установлена последняя версия.")

if __name__ == '__main__':
    main()
