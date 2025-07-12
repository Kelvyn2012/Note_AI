from transformers import pipeline

# Store the model once it's loaded
_summarizer = None


def summarize_text(text):
    global _summarizer

    if _summarizer is None:
        _summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

    # Skip summarizing short notes
    if len(text.split()) < 50:
        return text

    summary = _summarizer(text, max_length=60, min_length=20, do_sample=False)
    return summary[0]["summary_text"]
