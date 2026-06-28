import json
import re
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Optional

from google.generativeai.client import configure
from google.generativeai.generative_models import GenerativeModel
from google.generativeai.types import GenerationConfig
from dotenv import load_dotenv

load_dotenv()  # reads GEMINI_API_KEY from .env file

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True) # type: ignore


class MultilingualCAPAgent:
    """
    Converts a CAP v1.2 XML alert into multilingual JSON messages.

    Input  : CAP XML string  (from upstream Alert Agent)
    Output : dict with metadata + messages in each language

    Usage (standalone):
        agent  = MultilingualCAPAgent()
        result = agent.translate(cap_xml_string)

    Usage (inside a pipeline):
        from multilingual_agent import MultilingualCAPAgent
        agent  = MultilingualCAPAgent(languages={"en": "English", "hi": "Hindi"})
        result = agent.translate(cap_xml)
    """

    # Default languages — override in __init__ as needed
    DEFAULT_LANGUAGES = {
        "en": "English",
        "hi": "Hindi (हिन्दी)",
        "ta": "Tamil (தமிழ்)",
    }

    def __init__(
        self,
        api_key: str = None, # type: ignore
        languages: dict = None, # type: ignore
        use_gemini: bool = True,
    ):
        """
        Args:
            api_key  : Gemini API key. If None, reads from GEMINI_API_KEY env var.
            languages : Dict of {lang_code: lang_name}. Uses DEFAULT_LANGUAGES if None.
            use_gemini: If False, builds local fallback output without an API call.
        """
        self.languages  = languages or self.DEFAULT_LANGUAGES
        self.use_gemini = use_gemini
        self.model: Optional[GenerativeModel] = None

        if self.use_gemini:
            key = api_key or os.getenv("GEMINI_API_KEY")
            if not key:
                raise ValueError(
                    "No API key found. Either pass api_key= or set GEMINI_API_KEY in .env"
                )
            configure(api_key=key)
            self.model = GenerativeModel("gemini-2.5-flash-lite")

    def translate(self, cap_xml: str) -> dict:
        """
        Main entry point.

        Args:
            cap_xml : Raw CAP XML string from upstream agent

        Returns:
            dict with keys:
              - alert_id, event, severity, area, sent, ...
              - parameters : dict of sensor/resource values
              - messages   : {lang_code: {headline, description, instruction, sms}}
        """
        print(f"\n{'─'*55}")
        print("  MultilingualCAPAgent starting...")

        parsed       = self._parse_cap_xml(cap_xml)
        if not self.use_gemini:
            print("  Gemini disabled; using local fallback output.")
            translations = self._fallback_translations(parsed)
        else:
            try:
                translations = self._call_gemini(parsed)
            except Exception as exc:
                print(f"  Gemini call failed: {exc}")
                raise
        output       = self._build_output(parsed, translations)

        print(f"Done — {len(output['messages'])} languages generated")
        print(f"{'─'*55}\n")
        return output
    
    def _parse_cap_xml(self, xml_string: str) -> dict:
        """Extract metadata + translatable fields from CAP XML."""

        # Strip CAP namespace so ElementTree works simply
        xml_clean = re.sub(r'\s*xmlns="[^"]+"', "", xml_string.strip())
        root      = ET.fromstring(xml_clean)
        info      = root.find("info")

        if info is None:
            raise ValueError("CAP XML has no <info> block")

        # Helper: get text from root-level tag
        def r(tag):
            el = root.find(tag)
            return el.text.strip() if el is not None and el.text else ""

        # Helper: get text from <info> tag
        def i(tag):
            el = info.find(tag)
            return el.text.strip() if el is not None and el.text else ""

        # Extract <parameter> blocks
        params = {}
        for p in info.findall("parameter"):
            name = p.findtext("valueName", "").strip()
            val  = p.findtext("value", "").strip()
            if name:
                params[name] = val

        # Extract area description
        area    = ""
        area_el = info.find("area")
        if area_el is not None:
            area = area_el.findtext("areaDesc", "").strip()

        return {
            # Metadata (not translated)
            "alert_id":    r("identifier"),
            "sender":      r("sender"),
            "sent":        r("sent"),
            "status":      r("status"),
            "msg_type":    r("msgType"),
            "scope":       r("scope"),
            "area":        area,
            "event":       i("event"),
            "urgency":     i("urgency"),
            "severity":    i("severity"),
            "certainty":   i("certainty"),
            "onset":       i("onset"),
            "expires":     i("expires"),
            "parameters":  params,
            # Fields to translate
            "headline":    i("headline"),
            "description": " ".join(i("description").split()),
            "instruction": " ".join(i("instruction").split()),
        }

    def _call_gemini(self, parsed: dict) -> dict:
        """Send one prompt to Gemini and get all translations back."""

        lang_list  = "\n".join(
            f"  - {code}: {name}" for code, name in self.languages.items()
        )
        params_str = "\n".join(
            f"    {k}: {v}" for k, v in parsed["parameters"].items()
        )

        prompt = f"""You are an official emergency alert translator for the
National Disaster Management Authority (NDMA) of India.

Translate the CAP alert fields below into ALL listed languages in ONE response.
Use native scripts only (Devanagari, Gurmukhi, Tamil script etc.) — NOT romanised text.

=== ALERT DATA ===
Event       : {parsed['event']}
Severity    : {parsed['severity']}
Urgency     : {parsed['urgency']}
Certainty   : {parsed['certainty']}
Area        : {parsed['area']}
Headline    : {parsed['headline']}
Description : {parsed['description']}
Instruction : {parsed['instruction']}
Parameters  :
{params_str}

=== TARGET LANGUAGES ===
{lang_list}

=== STRICT RULES ===
1. Preserve ALL numbers, phone numbers, shelter names, and locations exactly
2. Urgent and official tone throughout
3. Do NOT shorten or summarise
4. SMS field: max 160 characters, must include area name + key action
5. Return ONLY valid JSON — no markdown, no code fences, no extra text

=== EXACT JSON FORMAT ===
{{
  "messages": {{
    "<lang_code>": {{
      "headline":    "<translated>",
      "description": "<translated with all key stats>",
      "instruction": "<translated>",
      "sms":         "<max 160 chars>"
    }}
  }}
}}"""

        print(f"Sending to Gemini ({len(self.languages)} languages in 1 call)...")

        if self.model is None:
            raise RuntimeError("Gemini model is not initialized")

        response = self.model.generate_content(
            prompt,
            generation_config=GenerationConfig(
                temperature=0.2,
                max_output_tokens=8192,
            ),
            request_options={"timeout": 30},
        )

        raw = response.text.strip()
        raw = re.sub(r"^```(?:json)?\n?", "", raw)
        raw = re.sub(r"\n?```$", "", raw).strip()

        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            raise ValueError(f"Gemini returned invalid JSON: {e}\n\nRaw:\n{raw}")

    def _fallback_translations(self, parsed: dict) -> dict:
        """Build output from parsed CAP fields when Gemini is unavailable."""
        messages = {}

        for code, name in self.languages.items():
            note = "" if code == "en" else f"[{name} translation unavailable] "
            instruction = f"{note}{parsed['instruction']}"
            sms = f"{parsed['area']}: {parsed['event']} warning. Evacuate immediately. Call 112."

            messages[code] = {
                "headline": f"{note}{parsed['headline']}",
                "description": f"{note}{parsed['description']}",
                "instruction": instruction,
                "sms": sms[:160],
            }

        return {"messages": messages}


    def _build_output(self, parsed: dict, translations: dict) -> dict:
        """Merge CAP metadata with Gemini translations into final output."""
        return {
            "agent":        "MultilingualCAPAgent",
            "version":      "1.0",
            "generated_at": datetime.utcnow().isoformat() + "Z",
            # CAP metadata (unchanged)
            "alert_id":    parsed["alert_id"],
            "event":       parsed["event"],
            "severity":    parsed["severity"],
            "urgency":     parsed["urgency"],
            "certainty":   parsed["certainty"],
            "area":        parsed["area"],
            "sender":      parsed["sender"],
            "sent":        parsed["sent"],
            "parameters":  parsed["parameters"],
            # Translated messages
            "messages": translations.get("messages", translations),
        }
