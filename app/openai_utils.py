from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

# Tone map for each platform
TONE_MAP = {
    "twitter": "witty and concise",
    "linkedin": "professional and insightful",
    "instagram": "friendly and expressive"
}

# Load small model and tokenizer (CPU-friendly)
tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
model = AutoModelForCausalLM.from_pretrained("distilgpt2")

# Create generation pipeline
generator = pipeline("text-generation", model=model, tokenizer=tokenizer)

def generate_reply(platform: str, post_text: str) -> str:
    tone = TONE_MAP.get(platform.lower(), "natural")
    prompt = f"Write a {tone} human-like reply to the following post:\n\"{post_text}\""

    result = generator(prompt, max_new_tokens=60, temperature=0.8, do_sample=True)
    generated_text = result[0]["generated_text"]

    # Strip out the prompt and keep only the reply
    return generated_text.replace(prompt, "").strip()
