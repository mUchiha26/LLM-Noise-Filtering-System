import requests
import subprocess

class LLMClassifier:
    def __init__(self, mode="local", model_name="llama3"):
        """
        mode: "local" or "api"
        model_name: depends on backend
        """
        self.mode = mode
        self.model_name = model_name

    def classify(self, text):
        """
        Main entry point: returns True (relevant) or False (noise)
        """
        prompt = self._build_prompt(text)

        if self.mode == "local":
            response = self._call_local_llm(prompt)
        elif self.mode == "api":
            response = self._call_api_llm(prompt)
        else:
            raise ValueError("Invalid mode")

        return self._parse_response(response)

    # -------------------------
    # Prompt Engineering Layer
    # -------------------------
    def _build_prompt(self, text):
        return f"""
You are a cybersecurity expert.

Task: Determine if the following text contains relevant cybersecurity knowledge.

Answer ONLY with "YES" or "NO".

Text:
{text}
"""

    # -------------------------
    # Local LLM (Ollama)
    # -------------------------
    def _call_local_llm(self, prompt):
        try:
            result = subprocess.run(
                ["ollama", "run", self.model_name],
                input=prompt,
                text=True,
                capture_output=True
            )
            return result.stdout.strip()
        except Exception as e:
            print(f"[ERROR - LOCAL LLM] {e}")
            return ""

    # -------------------------
    # API LLM (OpenAI / others)
    # -------------------------
    def _call_api_llm(self, prompt):
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"

            headers = {
                "Authorization": "Bearer API_KEY_HERE",  # change here
                "Content-Type": "application/json"
            }

            data = {
                "model": "openai/gpt-5.4",  # change here
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0
            }

            response = requests.post(url, headers=headers, json=data)
            #print(response.status_code, response.text)

            if response.status_code != 200:
                print("[API ERROR]", response.text)
                return ""

            return response.json()["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[ERROR - API LLM] {e}")
            return ""


    # -------------------------
    # Output Parsing (CRITICAL)
    # -------------------------
    def _parse_response(self, response):
        response = response.strip().lower()

        if "yes" in response:
            return True
        elif "no" in response:
            return False
        else:
            return False  # default safe fallback
