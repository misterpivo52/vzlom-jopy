def write_file_and_run_callback(filename,callback):
    with open(filename, 'w') as file:
    # Файл записан, теперь вызываем функцию
    callback()

def my_function():
    print("Файл записан, функция запущена!")

write_file_and_run_callback("output.txt", , my_function)

