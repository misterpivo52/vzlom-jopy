from databaza import DATABASE

def complete_and_substitute(input_sentence, database):
    """
    Ищет предложение, начинающееся с введённого текста (без учета последних двух символов),
    и возвращает его с подстановкой значения, если оно есть.
    """
    # Убираем последние два символа из входного предложения для проверки
    trimmed_input = input_sentence[:-3].strip() if len(input_sentence) > 2 else input_sentence.strip()

    for sentence, value in database.items():
        if sentence.lower().startswith(trimmed_input.lower()):  # Игнорирует регистр
            # Если значение есть, добавляем его в вывод
            if value is not None:
                return f"{sentence}: {value}"
            return sentence  # Если значение None, возвращаем только предложение
    return "No matching sentence"

def process_file(input_file, output_file, database):
    """
    Обрабатывает файл построчно, добавляя к неполному предложению полное предложение и значение.
    """
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for line in infile:
            # Убираем лишние пробелы и разбиваем на номер и неполное предложение
            line = line.strip()
            if not line:
                continue  # Пропускаем пустые строки

            try:
                number, incomplete_sentence = line.split(':', 1)
                number = number.strip()
                incomplete_sentence = incomplete_sentence.strip()

                # Получаем полное предложение и значение
                result = complete_and_substitute(incomplete_sentence, database)

                # Сохраняем результат в формате: номер: полное предложение: значение
                outfile.write(f"{number}: {result}\n")
            except ValueError:
                # Если строка не соответствует формату "номер: неполное предложение"
                outfile.write(f"Error processing line: {line}\n")
if __name__ == "__main__":
    # Укажите входной и выходной файлы
    input_file = "output.txt"  # Файл с номерами и неполными предложениями
    output_file = "ou1tput.txt"  # Файл для сохранения результатов

    # Запуск обработки
    process_file(input_file, output_file, DATABASE)
