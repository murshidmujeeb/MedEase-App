import google.generativeai as genai
import json
import base64
from pathlib import Path
from app.core.config import settings

# Configure Gemini
genai.configure(api_key=settings.GOOGLE_API_KEY)

VISION_PROMPT = """
You are a pharmaceutical data extraction specialist. Analyze this prescription image and extract ALL medicines, dosages, frequencies, and patient details. Return ONLY valid JSON.

RETURN THIS EXACT JSON STRUCTURE (no markdown, just raw JSON):
{
  "prescription_metadata": {
    "patient_name": "string or null",
    "patient_age": "integer or null",
    "prescriber_name": "string or null",
    "prescription_date": "YYYY-MM-DD or null",
    "overall_confidence": 0.95
  },
  "medicines": [
    {
      "generic_name": "string",
      "brand_name": "string or null",
      "strength": "string",
      "form": "string (tablet, capsule, syrup, etc)",
      "quantity_prescribed": 10,
      "frequency": "string",
      "duration": "string",
      "special_instructions": "string or null",
      "extraction_confidence": 0.95
    }
  ],
  "extraction_quality": {
    "is_readable": true,
    "missing_fields": [],
    "overall_suggestion": "string"
  }
}
"""

async def extract_medicines_from_prescription(image_path: str) -> dict:
    try:
        # Using generic alias 'gemini-flash-latest' which maps to the current stable Flash model
        # If this fails with 429, the user MUST enable billing on their Google Cloud Project.
        model = genai.GenerativeModel('gemini-flash-latest') 
        
        print(f"Processing image: {image_path}")
        
        # Load image
        if not Path(image_path).exists():
             raise FileNotFoundError(f"Image not found at {image_path}")
             
        with open(image_path, "rb") as f:
            image_data = f.read()
            
        parts = [
            {"mime_type": "image/jpeg", "data": image_data},
            {"text": VISION_PROMPT}
        ]
        
        print("Sending request to Gemini...")
        response = model.generate_content(parts)
        print(f"Gemini Raw Response: {response.text}")
        
        # Clean response text (remove markdown code blocks if any)
        text = response.text.replace("```json", "").replace("```", "").strip()
        
        return json.loads(text)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Gemini Extraction Error: {e}")
        # Return a fallback/error structure
        return {
            "prescription_metadata": {},
            "medicines": [],
            "extraction_quality": {
                "is_readable": False, 
                "error": str(e)
            }
        }
