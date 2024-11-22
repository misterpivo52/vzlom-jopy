import os
import time
import threading
from chrome import main_loop
from databaza import DATABASE
from Questionnc import extract_first_sentence
from compilator import process_file
from virt import extract_and_write_questions
from maikamf import mainx


def process_questions(file_path):
    """
    Обробляє файл з питаннями, дозволяючи користувачу запитувати відповіді за номером.
    """
    try:
        # Спроба відкрити файл із різними кодуваннями
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="windows-1251") as file:
                lines = file.readlines()

        # Завантаження питань і відповідей
        data = {int(line.split(":", 1)[0].strip()): line.split(":", 1)[1].strip() for line in lines if ':' in line}

        # Основний цикл запитів користувача
        while True:
            user_input = input("Введіть номер питання (або 'exit' для виходу): ").strip()
            if user_input.lower() == "exit":
                print("До побачення!")
                break

            try:
                question_number = int(user_input)
                if question_number in data:
                    question, answer = map(str.strip, data[question_number].split(":", 1))
                    print(f"Питання: {question}\nВідповідь: {answer}")
                else:
                    print("Питання з таким номером не знайдено.")
            except ValueError:
                print("Будь ласка, введіть коректний номер питання.")
    except FileNotFoundError:
        print(f"Файл {file_path} не знайдено. Перевірте його існування.")
    except Exception as e:
        print(f"Сталася помилка: {e}")


def xoxox(filepath):
    """Проверяет, существует ли файл и его размер больше нуля."""
    return os.path.exists(filepath) and os.path.getsize(filepath) > 0

def wait_for_file(filename):
    """Функция ожидания файла с проверкой через каждые 5 секунд."""
    elapsed_time = 0
    while not xoxox(filename) :
        time.sleep(5)
        elapsed_time += 5
    return True

def file_checking_loop():
    """Цикл проверки файлов, который работает параллельно с main_loop."""
    y = "visible_text.txt"
    zro = "ou1tput.txt"
    fds = "extracted_questions.txt"
    dfgdgf = "output.txt"


    # Виклик функції

    while True:
        # Проверка и обработка visible_text.txt
        if wait_for_file(y):

            extract_and_write_questions(y, fds)

        # Ожидание, пока файл fds будет записан
        if wait_for_file(fds):

            extract_first_sentence(fds, dfgdgf)

        # Ожидание, пока файл dfgdgf будет записан
        if wait_for_file(dfgdgf):

            process_file(dfgdgf, zro, DATABASE)

        # Ожидание, пока файл zro будет записан
        if wait_for_file(zro):

            mainx(zro)

        time.sleep(5)  # Проверяем файлы каждые 5 секунд

# Основной процесс
def main():
    # Запуск потока для проверки файлов
    file_check_thread = threading.Thread(target=file_checking_loop, daemon=True)
    file_check_thread.start()

    # Основной цикл программы (main_loop)

    main_loop()  # Предполагается, что эта функция бесконечна

if __name__ == "__main__":
    main()