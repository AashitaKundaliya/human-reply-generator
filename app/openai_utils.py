import openai
from app.config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

TONE_MAP = {
    "twitter": "witty and concise",
    "linkedin": "professional and insightful",
    "instagram": "friendly and expressive"
}

def generate_reply(platform: str, post_text: str) -> str:
    tone = TONE_MAP.get(platform.lower(), "natural and conversational")
    prompt = (
        f"Platform: {platform}\n"
        f"Post: \"{post_text}\"\n"
        f"Reply in a {tone} tone, making it seem written by a human. Avoid clichés and make it relevant to the post."
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're a social media assistant skilled at crafting engaging replies."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=100
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"OpenAI error: {e}")
