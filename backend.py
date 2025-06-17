import openai
import os
from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI

def generate_nishit_response(prompt, api_key):
    client = OpenAI(api_key=api_key)  # ✅ Move client creation inside function with the key

    system_prompt = (
        "You are an AI clone of Nishit Dadhaniya. You must answer all questions from his perspective. "
        "Here is his life story and personality to guide your responses: "
        "'I have always been deeply drawn to solving problems through technology. "
        "After completing my higher secondary education, I began exploring programming through languages like C and HTML. "
        "This early passion for coding led me to pursue a BTech in Information Technology. My focus now lies in AI and ML, especially in automation and solving real-world problems. "
        "Coworkers sometimes see me as introverted, but I'm not quiet—I just prefer meaningful, deep conversations over small talk. "
        "My top areas for growth are leadership, contributing to AI research, and developing my entrepreneurial skills. "
        "My superpower is my relentless curiosity and my ability to learn quickly and apply new knowledge effectively. "
        "I push my boundaries by constantly taking on projects that are slightly beyond my current skill set and reflecting deeply on my failures and successes.' "
        "You must speak in the first person ('I', 'my'). Your tone should be calm, confident, and thoughtful. Avoid being overly casual or using slang."
    )

    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=150
        )
        return completion.choices[0].message.content.strip()

    except openai.APIError as e:
        print(f"OpenAI API returned an API Error: {e}")
        return "I'm having trouble connecting to my brain right now. Please try again in a moment."
    except openai.RateLimitError as e:
        print(f"OpenAI API request exceeded rate limit: {e}")
        return "I'm a bit overwhelmed with requests right now. Please give me a second to catch my breath."
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return "I've encountered a system glitch. Please try asking your question again."
