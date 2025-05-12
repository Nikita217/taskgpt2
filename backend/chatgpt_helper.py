        import os, json, openai

        openai.api_key = os.getenv('OPENAI_API_KEY')

        def generate_day_plan(tasks):
            task_text = "\n".join([f"- {t['title']}" for t in tasks if not t['completed']])
            prompt = "Разбей задачи по утро/день/вечер:
"+task_text +"\nJSON format"
            try:
                res = openai.ChatCompletion.create(model='gpt-3.5-turbo',
                    messages=[{'role':'user','content':prompt}],temperature=0.7)
                return json.loads(res['choices'][0]['message']['content'])
            except Exception as e:
                print(e)
                return []

        def suggest_tasks(prompt):
            prompt = f"Разбей цель '{prompt}' на 3-5 задач."
            try:
                res = openai.ChatCompletion.create(model='gpt-3.5-turbo',
                    messages=[{'role':'user','content':prompt}],temperature=0.5)
                lines = res['choices'][0]['message']['content'].split('\n')
                return [l.strip(' -') for l in lines if l.strip()]
            except Exception as e:
                print(e)
                return []
