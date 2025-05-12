# backend/chatgpt_helper.py
import os, json, openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_day_plan(tasks):
    task_text = "\n".join(
        f"- {t['title']}" for t in tasks if not t.get("completed")
    )

    prompt = (
        "Разбей следующие задачи на утро/день/вечер.\n"
        "Верни результат строго в JSON: "
        "[{timeRange:'Утро',tasks:[...]}, ...]\n\n"
        f"{task_text}"
    )

    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return json.loads(res["choices"][0]["message"]["content"])
    except Exception as e:
        print("generate_day_plan:", e)
        return []


def suggest_tasks(description):
    prompt = (
        f"Разбей цель «{description}» на 3-5 конкретных задач.\n"
        "Ответ дай списком, без нумерации."
    )

    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        lines = res["choices"][0]["message"]["content"].splitlines()
        return [l.lstrip("-•1234567890. ").strip() for l in lines if l.strip()]
    except Exception as e:
        print("suggest_tasks:", e)
        return []
