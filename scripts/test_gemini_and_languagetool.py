import os
import sys
import json

backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend"))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.core.config import settings

def test_llm_and_languagetool():
    print("=" * 80)
    print("TASK 6: LLM (GEMINI) AND LANGUAGETOOL VERIFICATION")
    print("=" * 80)

    # 1. Gemini
    gemini_key = settings.GEMINI_API_KEY
    if gemini_key and gemini_key.strip():
        redacted_key = f"{gemini_key[:4]}...{gemini_key[-4:]}" if len(gemini_key) > 8 else "***"
        print(f"[Gemini] GEMINI_API_KEY detected: {redacted_key}")
        try:
            from google import genai
            client = genai.Client(api_key=gemini_key)
            prompt = "Evaluate the following interview response: 'I optimized database query response times by 40% using Redis caching and compound indexes in PostgreSQL.' Provide 1 sentence of constructive feedback in JSON: {\"feedback\": \"...\"}"
            print("[Gemini] Sending real request to Google Gemini 2.5 Flash...")
            resp = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            print("[Gemini] Real Response Received (redacted format):")
            print(f"Status: Success (chars: {len(resp.text)})")
            print(f"Sample response content: {resp.text.strip()[:200]}")
        except Exception as e:
            print(f"[Gemini] Request failed: {e}")
    else:
        print("[Gemini] GEMINI_API_KEY is not set in environment.")
        print("[Gemini] Fallback Behavior Matrix when key is missing:")
        print("  1. Resume Analysis   -> pdfplumber + Heuristic Regex Matcher (extracts education, skills, projects, certifications)")
        print("  2. Question Gen      -> Curated Question Bank from SQLite/PostgreSQL by Job Role, Category, Difficulty")
        print("  3. Follow-ups        -> Curated Contextual Probing Follow-ups mapped by question topic")
        print("  4. Content Eval      -> STAR Rubric & Keyword Matcher (evaluates Situation, Task, Action, Result & keyword hits)")
        print("  5. Feedback Gen      -> Comprehensive Rubric Synthesizer & Dynamic Learning Resource Mapper")

    print("\n" + "-" * 80)

    # 2. LanguageTool
    lt_url = getattr(settings, "LANGUAGETOOL_URL", "http://localhost:8010/v2/check")
    public_lt_url = "https://api.languagetool.org/v2/check"
    print(f"[LanguageTool] Configured Self-Hosted URL: {lt_url}")
    print(f"[LanguageTool] Public API Fallback: {public_lt_url}")

    import requests
    sample_text = "I has completed my degree and we is working on microservices."

    # Try configured self-hosted
    self_hosted_ok = False
    try:
        r = requests.post(lt_url, data={"text": sample_text, "language": "en-US"}, timeout=1.0)
        if r.status_code == 200:
            self_hosted_ok = True
            data = r.json()
            print(f"[LanguageTool] Self-hosted service ACTIVE. Found {len(data.get('matches', []))} grammatical issues.")
    except Exception:
        print("[LanguageTool] Self-hosted service is currently offline (available when started via docker-compose profile 'with-languagetool').")

    # Try public API
    public_ok = False
    try:
        r = requests.post(public_lt_url, data={"text": sample_text, "language": "en-US"}, timeout=3.0)
        if r.status_code == 200:
            public_ok = True
            data = r.json()
            matches = data.get("matches", [])
            print(f"[LanguageTool] Public API reachable. Found {len(matches)} issues.")
            for m in matches[:2]:
                print(f"  - Message: {m.get('message')} (offset: {m.get('offset')})")
    except Exception as e:
        print(f"[LanguageTool] Public API check failed or rate-limited: {e}")

    # Fallback explanation
    print("[LanguageTool] Fallback Behavior when LanguageTool is offline:")
    print("  - Uses app.ai.grammar_analyzer with regex patterns for subject-verb agreement, double comparatives, prepositions.")
    print("  - Computes Flesch-Kincaid Reading Ease readability score and Type-Token Ratio vocabulary score locally.")

    print("=" * 80)

if __name__ == "__main__":
    test_llm_and_languagetool()
