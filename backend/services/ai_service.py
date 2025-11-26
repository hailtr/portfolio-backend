import os
import json
import logging
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

logger = logging.getLogger(__name__)

class AIProjectGenerator:
    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            logger.error("CRITICAL: GEMINI_API_KEY not found in env variables")
            raise ValueError("GEMINI_API_KEY is missing")
        
        try:
            genai.configure(api_key=api_key)
            
            self.generation_config = {
                "temperature": 0.7,
                "top_p": 0.95,
                "top_k": 64,
                "max_output_tokens": 8192, 
                "response_mime_type": "application/json", 
            }
            
            self.safety_settings = {
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            }

            
            self.model = genai.GenerativeModel(
                model_name='gemini-2.0-flash',
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini AI: {str(e)}")
            raise e

    def analyze_github_repo(self, repo_context, repo_url="", model_name="gemini-2.0-flash"):
        """
        Analyze GitHub content and generate portfolio data
        """
        
        # Use the requested model or fallback to default
        current_model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )
        
        prompt = f"""
        You are an expert technical portfolio curator specializing in Data Engineering and Backend Development. 
        Analyze this GitHub repository content.
        Base Repository URL: {repo_url} (Use this to construct absolute URLs for media if needed).

        Repo Content (Truncated if too large):
        {repo_context[:30000]} 

        Generate a strict JSON object with the following structure:

        {{
            "title": "Project Name (Professional and descriptive, NOT generic)",
            "subtitle": "A catchy, impressive tagline (max 60 chars)",
            "category": "project", 
            "tags": ["Tech1", "Tech2", "Tech3", "Tech4", "Tech5"],
            "urls": [
                {{"type": "github", "url": "{repo_url}", "label": "Source Code"}},
                {{"type": "demo", "url": "URL_FOUND_IN_README_OR_NULL", "label": "Live Demo"}}
            ],
            "media": {{
                "gif_url": "Absolute URL of the first animated GIF found. If relative, prepend raw.githubusercontent path. If none, null.",
                "image_url": "Absolute URL of the most representative image. If relative, prepend raw.githubusercontent path. If none, null."
            }},
            "translations": {{
                "en": {{
                    "summary": "A concise, punchy 2-sentence summary (max 200 chars). Focus on the 'what' and 'why'.",
                    "description": "HTML content. Create a compelling Data Engineering narrative. Focus on the problem solved, the data pipeline architecture, and the impact. Use <h3> for section headers (e.g., 'The Challenge', 'The Solution', 'Key Features'). Use <ul>/<li> for lists. Do NOT start with 'General vision'. Do NOT list the tech stack here (use the 'tags' field for that). Do NOT use markdown."
                }},
                "es": {{
                    "summary": "Un resumen conciso y contundente de 2 oraciones (máx. 200 caracteres). Enfócate en el 'qué' y el 'por qué'.",
                    "description": "Contenido HTML. Crea una narrativa de Ingeniería de Datos convincente. Enfócate en el problema resuelto, la arquitectura del pipeline de datos y el impacto. Usa <h3> para encabezados (ej. 'El Desafío', 'La Solución', 'Características Clave'). Usa <ul>/<li> para listas. NO empieces con 'Visión general'. NO listes el stack tecnológico aquí (usa el campo 'tags' para eso). NO uses markdown."
                }}
            }},
            "diagram": "mermaid code for a sequence or architecture diagram. Start with 'graph TD' or 'sequenceDiagram'. Keep it simple."
        }}
        """
        
        try:
            response = current_model.generate_content(prompt)
            text = response.text
            
            # Clean up potential markdown formatting
            if text.startswith("```json"):
                text = text.replace("```json", "").replace("```", "")
            elif text.startswith("```"):
                text = text.replace("```", "")
            
            return json.loads(text.strip())
            
        except Exception as e:
            logger.error(f"AI Generation failed: {str(e)}")
            raise e
