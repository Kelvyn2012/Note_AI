import os

_summarizer = None
_model_available = None


def summarize_text(text):
    """
    Generate a summary of the provided text using T5 model.
    Falls back to truncated text if model is unavailable (e.g., low memory environments).
    """
    global _summarizer, _model_available

    # Check if we've already determined model availability
    if _model_available is False:
        return _create_fallback_summary(text)

    # Try to load and use the model
    if _summarizer is None:
        try:
            print("⚡ Loading lightweight T5-small model...")
            from transformers import pipeline
            _summarizer = pipeline("summarization", model="t5-small", tokenizer="t5-small")
            _model_available = True
            print("✅ Model loaded successfully")
        except Exception as e:
            print(f"⚠️ Could not load AI model (likely memory constraint): {e}")
            print("📝 Using fallback summarization")
            _model_available = False
            return _create_fallback_summary(text)

    word_count = len(text.split())
    print(f"📝 Word count: {word_count}")

    # For very short text, return as-is
    if word_count < 30:
        print("⚠️ Too short to summarize. Returning original text.")
        return text[:200] + ("..." if len(text) > 200 else "")

    # Try AI summarization
    try:
        input_text = "summarize: " + text[:512]
        summary = _summarizer(input_text, max_length=60, min_length=20, do_sample=False)
        result = summary[0]["summary_text"]
        print(f"✅ AI Summary: {result[:50]}...")
        return result
    except Exception as e:
        print(f"❌ Summary error: {e}")
        return _create_fallback_summary(text)


def _create_fallback_summary(text):
    """
    Create a simple summary by taking the first few sentences.
    Used when AI model is unavailable.
    """
    # Take first 200 characters as a simple summary
    summary = text[:200].strip()

    # Try to end at a sentence boundary
    for delimiter in ['. ', '! ', '? ']:
        last_sentence = summary.rfind(delimiter)
        if last_sentence > 50:  # Ensure we have at least 50 chars
            summary = summary[:last_sentence + 1]
            break

    # Add ellipsis if text was truncated
    if len(text) > len(summary):
        summary += "..."

    return summary
