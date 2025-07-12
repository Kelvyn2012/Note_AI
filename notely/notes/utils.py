from transformers import pipeline

_summarizer = None


def summarize_text(text):
    global _summarizer

    print("🚀 Called summarize_text()")

    if _summarizer is None:
        print("⚡ Loading lightweight T5-small model...")
        _summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")

    word_count = len(text.split())
    print(f"📝 Word count: {word_count}")

    if word_count < 30:
        print("⚠️ Too short to summarize. Returning original text.")
        return text

    try:
        input_text = "summarize: " + text[:512]  # T5 needs this prefix
        summary = _summarizer(input_text, max_length=60, min_length=20, do_sample=False)
        print("✅ Summary:", summary[0]["summary_text"])
        return summary[0]["summary_text"]
    except Exception as e:
        print("❌ Summary error:", e)
        return "Summary unavailable"
