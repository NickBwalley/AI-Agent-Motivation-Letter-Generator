import openai
from openai import OpenAI

def generate(context, api_key):
    try:
        client = OpenAI(api_key=api_key)
        prompt = f"""You are an expert career coach. Based on the following context, write a professional motivation letter:
        
{context}

Your output should be a complete, personalized motivation letter."""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        return response.choices[0].message.content, None
    except Exception as e:
        return None, f"[OpenAI API Error: {e}]"
