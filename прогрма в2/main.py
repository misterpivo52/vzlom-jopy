import time
import threading
import keyboard  # Для отслеживания клавиш
from chrome import main_loop
from databaza import DATABASE
from Questionnc import extract_first_sentence
from compilator import process_file
from virt import extract_and_write_questions
from maikamf import mainx

def execute_sequence():
    """Выполняет цепочку операций с заданными задержками."""
    try:
        y = "visible_text.txt"
        fds = "extracted_questions.txt"
        dfgdgf = "output.txt"
        zro = "ou1tput.txt"

        print("Запуск extract_and_write_questions через 10 секунд...")
        time.sleep(10)
        extract_and_write_questions(y, fds)
        print("extract_and_write_questions выполнена.")

        print("Запуск extract_first_sentence через 3 секунды...")
        time.sleep(3)
        extract_first_sentence(fds, dfgdgf)
        print("extract_first_sentence выполнена.")

        print("Запуск process_file через 3 секунды...")
        time.sleep(3)
        process_file(dfgdgf, zro, DATABASE)
        print("process_file выполнена.")

        print("Запуск mainx через 3 секунды...")
        time.sleep(3)
        mainx(zro)
        print("mainx выполнена.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def listen_for_hotkey():
    """Отслеживает горячую клавишу Ctrl + Alt + A и запускает цепочку функций."""
    print("Ожидаю нажатия Ctrl + Alt + A...")
    while True:
        if keyboard.is_pressed("]"):
            print("Комбинация Ctrl + Alt + A нажата. Запуск цепочки функций.")
            threading.Thread(target=execute_sequence, daemon=True).start()
            # Ждём, чтобы избежать множественных срабатываний на одном нажатии
            time.sleep(1)

def main():
    # Запуск потока для отслеживания горячих клавиш
    hotkey_thread = threading.Thread(target=listen_for_hotkey, daemon=True)
    hotkey_thread.start()
    main_loop()
    # Основной цикл программы
    while True:
        time.sleep(1)  # Поддерживает основной поток активным

if __name__ == "__main__":
    main()

