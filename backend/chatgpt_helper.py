import os
import json
import openai

# Читаем ключ из переменных окружения (.env или Render Secrets)
openai.api_key = os.getenv("OPENAI_API_KEY")


from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": prompt}],
)
text = response.choices[0].message.content


def generate_day_plan(tasks: list[dict]) -> list[dict]:
    """
    Составляет «умный» план дня: разбивает активные задачи
    на утро / день / вечер и возвращает список словарей:
    [
      {"timeRange": "Утро 9:00 – 12:00", "tasks": ["Задача 1", "Задача 2"]},
      ...
    ]
    """
    # Формируем текст для модели: только невыполненные задачи
    task_text = "\n".join(
        f"- {t['title']} (до {t.get('dueDate') or 'без срока'})"
        for t in tasks
        if not t.get("completed")
    )

    prompt = (
        "Разбей следующие задачи на три временных блока (утро, день, вечер) "
        "учитывая приоритет по срокам. Верни результат строго в JSON-формате: "
        "[{timeRange: 'Утро 9:00-12:00', tasks: [...]}, …]\n\n"
        f"{task_text}"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        plan_json = response.choices[0].message.content.strip()

        # Пробуем распарсить; если модель добавила лишний текст —
        # ищем первую/последнюю скобку, берём подстроку
        if not plan_json.startswith("["):
            plan_json = plan_json[plan_json.find("[") :]
        if not plan_json.endswith("]"):
            plan_json = plan_json[: plan_json.rfind("]") + 1]

        return json.loads(plan_json)
    except Exception as exc:
        print("generate_day_plan error:", exc)
        return []


def suggest_tasks(description: str) -> list[str]:
    """
    Разбивает цель/идею, введённую пользователем, на 3-5 конкретных подзадач.
    Возвращает список строк (задач).
    """
    prompt = (
        "Пользователь сформулировал цель:\n"
        f"\"{description}\"\n\n"
        "Разбей эту цель на 3-5 конкретных задач. "
        "Ответ верни списком через перевод строки, без нумерации и лишних символов."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        lines = response.choices[0].message.content.splitlines()
        # Фильтруем пустые строки и маркеры ("- ", "• ", "1. " etc.)
        clean = [l.lstrip("-•0123456789. ").strip() for l in lines if l.strip()]
        return clean
    except Exception as exc:
        print("suggest_tasks error:", exc)
        return []
