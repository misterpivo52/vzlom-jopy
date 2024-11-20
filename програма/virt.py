import re

def extract_and_write_questions(input_file_path, output_file_path):
    questions = {}

    # Відкрити файл для читання
    with open(input_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    current_question_number = None
    current_question_text = []

    # Обробка рядків
    for line in lines:
        # Шукаємо номер питання, наприклад, "Question 14"
        match = re.match(r'Question (\d+)', line.strip())
        if match:
            # Зберегти попереднє питання, якщо воно є
            if current_question_number is not None and current_question_text:
                questions[current_question_number] = " ".join(current_question_text).strip()

            # Почати нове питання
            current_question_number = int(match.group(1))
            current_question_text = []
        elif current_question_number is not None:
            # Додавати текст до питання
            current_question_text.append(line.strip())

    # Додати останнє питання
    if current_question_number is not None and current_question_text:
        questions[current_question_number] = " ".join(current_question_text).strip()

    # Записати результати у файл
    with open(output_file_path, "w", encoding="utf-8") as output:
        for number, question in questions.items():
            output.write(f"{number}: {question}\n")


# Виклик функції
extract_and_write_questions("visible_text.txt", "extracted_questions.txt")


