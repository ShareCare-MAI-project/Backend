import openai


from app.core.config import OPEN_AI_KEY

openai.api_key = OPEN_AI_KEY


def ask_gpt(prompt, model="gpt-4o-mini"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Ошибка: {e}"


prompt = "ваш пример промпта"
answer = ask_gpt(prompt)
print("Ответ GPT:", answer)
