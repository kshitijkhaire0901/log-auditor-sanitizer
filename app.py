from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv
import os 

#Step 1: Securely load the API key from the environment variables. 
load_dotenv()  # This takes env variables from .env.

app = Flask(__name__)

# Step 2: Initialize the Gemini API CLient with the API Key.
# Note: Ensure that the GEMINI_API_KEY is set in your environment variables.
try: 
    ai_client = genai.Client()
    print("AI Gateway Initialization successful.")
except Exception as e:
    print(f"Warning AI Gateway Initialization failed. Check your API key.  Details: {e}")
    ai_client = None

def analyze_error_with_ai(raw_error_text):
    """Encapsulates the raw system error log into a high-context prompt for an LLM insight."""
    if not ai_client:
        return "AI Client initialization failed. Please ensure your .env file contains a valid GEMINI_API_KEY."

    prompt = f"""
    You are an expert enterprise systems architect troubleshooting production server logs. 
    Analyze this raw error line:
    "{raw_error_text}"
    
    Provide a crisp, professional 1-sentence explanation of the root cause, followed by exactly 2 tactical troubleshooting bullet points for an IT technician. Keep it clean and to the point.
    """
    try:
        # Utilizing the lightning-fast, production-standard gemini-2.5-flash model
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return response.text
    except Exception as err:
        return f"AI Diagnosis Gateway unavailable. Execution Error: {str(err)}"

@app.route("/", methods=["GET", "POST"])
def upload_and_parse():
    parsed_errors = []
    summary = {"total_lines": 0, "errors_found": 0}
    
    if request.method == "POST" and "log_file" in request.files:
        file = request.files["log_file"]
        if file.filename != "":
            # Memory-efficient string extraction directly from the incoming web buffer stream
            lines = file.stream.read().decode("utf-8").splitlines()
            summary["total_lines"] = len(lines)
            
            # Smart Cache: Deduplication dictionary to prevent redundant, expensive API billing calls
            seen_errors = {}
            
            for idx, line in enumerate(lines, 1):
                clean_line = line.strip()
                # Operational pipeline filter looking for target log alert patterns
                if "CRITICAL" in clean_line or "ERROR" in clean_line:
                    
                    # Deduplication Strategy implementation
                    if clean_line not in seen_errors:
                        # Call the AI model only once for a completely unique error message
                        seen_errors[clean_line] = analyze_error_with_ai(clean_line)
                    
                    parsed_errors.append({
                        "line_num": idx,
                        "content": clean_line,
                        "ai_insight": seen_errors[clean_line] # Fetch directly from memory cache
                    })
            
            summary["errors_found"] = len(parsed_errors)
            
    return render_template("index.html", errors=parsed_errors, summary=summary)

if __name__ == "__main__":
    # Standard development sandbox execution settings
    app.run(debug=True, port=8080)