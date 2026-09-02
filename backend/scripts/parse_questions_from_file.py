import sys
import re
import argparse
from pathlib import Path

# Добавляем путь к проекту для импорта наших модулей
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.database import SessionLocal
from app.crud.question import create_question
from app.schemas.question import QuestionCreate

# Путь к локальному файлу относительно корня проекта (папка backend)
FILE_PATH = "scripts/Python_Developer_Questions.md"


def parse_questions_from_md(content: str):
    """
    Парсит .md файл и извлекает вопросы и ответы.

    Структура:
    ## N. Вопрос
    [текст ответа... (может отсутствовать)]
    <div align="right">...</div>
    ## N+1. Следующий вопрос
    """
    questions = []

    # Разбиваем по заголовкам ##
    parts = re.split(r'^## (\d+)\.\s*', content, flags=re.MULTILINE)

    for i in range(1, len(parts), 2):
        number = int(parts[i].strip())
        question_and_answer = parts[i + 1].strip() if i + 1 < len(parts) else ""

        # Разделяем вопрос и ответ
        lines = question_and_answer.split('\n')

        if lines:
            # Первая строка - это вопрос
            question_text = lines[0].strip()

            # Остальные строки - ответ (если есть)
            answer_lines = lines[1:] if len(lines) > 1 else []

            # Объединяем ответ и убираем HTML-теги
            full_answer = '\n'.join(answer_lines).strip()
            full_answer = re.sub(r'<div align="right">.*?</div>', '', full_answer, flags=re.DOTALL)
            full_answer = re.sub(r'\n+', '\n', full_answer).strip()

            # ✅ Если ответ пустой, ставим понятную заглушку
            if not full_answer:
                full_answer = "Ответ отсутствует в файле"

            questions.append({
                "id": number,
                "question": question_text,
                "answer": full_answer
            })

    return questions


def seed_questions(tag: str = None, category: str = None, difficulty: str = "medium"):
    """
    Главная функция для загрузки и сохранения вопросов в БД.

    Args:
        tag: Тег для всех вопросов (например, 'Python')
        category: Категория для всех вопросов (например, 'Основы')
        difficulty: Сложность (easy, medium, hard)
    """
    db = SessionLocal()

    try:
        base_dir = Path(__file__).parent.parent  # папка backend
        file_path = base_dir / FILE_PATH

        if not file_path.exists():
            print(f"❌ Файл не найден: {file_path}")
            print("   Проверьте путь в переменной FILE_PATH.")
            return

        print(f"📖 Чтение файла: {file_path}...")
        with open(file_path, 'r', encoding='utf-8') as f:
            file_content = f.read()
        print("✅ Файл успешно загружен.")

        print("🔍 Парсинг вопросов...")
        questions_data = parse_questions_from_md(file_content)
        print(f"✅ Найдено {len(questions_data)} вопросов.")

        if not questions_data:
            print("⚠️ Вопросы не найдены. Проверьте структуру файла.")
            return

        print(f"💾 Сохранение вопросов в базу данных...")
        print(f"   📌 Тег: {tag or 'Не указан'}")
        print(f"   📂 Категория: {category or 'Не указана'}")
        print(f"   📊 Сложность: {difficulty}")
        print()

        created_count = 0
        empty_answers = 0

        for q_data in questions_data:
            question_text = q_data["question"][:500]
            answer_text = q_data["answer"][:1000]

            # Считаем пустые ответы
            if not answer_text or answer_text == "Ответ отсутствует в файле":
                empty_answers += 1

            question_create = QuestionCreate(
                question=question_text,
                answer=answer_text,
                difficulty=difficulty,
                tag=tag,
                category=category
            )
            try:
                create_question(question_create, db)
                created_count += 1
                print(f"   ✓ Вопрос #{q_data['id']} создан.")
            except Exception as e:
                print(f"   ⚠️ Ошибка при создании вопроса #{q_data['id']}: {e}")
                db.rollback()

        db.commit()
        print(f"\n🎉 Успешно сохранено {created_count} вопросов!")
        print(f"📝 Из них с пустыми ответами: {empty_answers}")
        print(f"📌 Тег: {tag or 'Не указан'}")
        print(f"📂 Категория: {category or 'Не указана'}")

    except Exception as e:
        print(f"❌ Непредвиденная ошибка: {e}")
        db.rollback()
    finally:
        db.close()


def main():
    """Парсинг аргументов командной строки"""
    parser = argparse.ArgumentParser(
        description="Загрузка вопросов из Markdown файла в базу данных",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python scripts/seed_questions.py --tag Python --category "Основы"
  python scripts/seed_questions.py --tag Python --category "ООП" --difficulty hard
  python scripts/seed_questions.py --tag "SQL" --category "DDL"
  python scripts/seed_questions.py --tag "Web" --difficulty easy
        """
    )

    parser.add_argument(
        '--tag',
        type=str,
        help='Тег для всех вопросов (например: Python, SQL, Web)'
    )

    parser.add_argument(
        '--category',
        type=str,
        help='Категория для всех вопросов (например: Основы, ООП, DDL)'
    )

    parser.add_argument(
        '--difficulty',
        type=str,
        choices=['easy', 'medium', 'hard'],
        default='medium',
        help='Сложность вопросов (по умолчанию: medium)'
    )

    parser.add_argument(
        '--file',
        type=str,
        help='Путь к файлу с вопросами (переопределяет FILE_PATH)'
    )

    # Парсим аргументы
    args = parser.parse_args()

    # Если указан файл, меняем путь
    if args.file:
        global FILE_PATH
        FILE_PATH = args.file

    print("=" * 60)
    print("🚀 Загрузка вопросов из Markdown файла")
    print("=" * 60)

    # Запускаем загрузку
    seed_questions(
        tag=args.tag,
        category=args.category,
        difficulty=args.difficulty
    )


if __name__ == "__main__":
    main()
