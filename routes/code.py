import json

from flask import Blueprint, jsonify, request
from ollama import chat

codescan_bp = Blueprint("codescan", __name__, url_prefix="/api")

@codescan_bp.route("/codescan", methods=["POST"])
def codescan():
    code = request.json.get("code")
    if not code:
        return jsonify({"error": "No code provided"}), 400
    
    try:
        # Create a prompt that asks for structured output
        prompt = f"""Analyze this code for security vulnerabilities and return the results in the following JSON format:
        [
            {{
                "severity": "high|medium|low",
                "description": "Detailed description of the vulnerability",
                "line": line_number
            }}
        ]
        
        Only include actual vulnerabilities. If no vulnerabilities are found, return an empty array. Do not return any other text or markdown formatting, only return the json array.
        Here's the code to analyze:

        {code}
        """
        
        response = chat(model="llama3.2", messages=[{
            "role": "user",
            "content": prompt
        }])

        # Parse the response content to extract the JSON
        content = response['message']['content']
        # Find the JSON array in the response (it might be wrapped in markdown code blocks)
        start_idx = content.find('[')
        end_idx = content.rfind(']') + 1
        if start_idx == -1 or end_idx == 0:
            return jsonify({"error": "Invalid response format from AI model"}), 500
            
        json_str = content[start_idx:end_idx]
        vulnerabilities = json.loads(json_str)
        
        return jsonify({"vulnerabilities": vulnerabilities})
    
    except Exception as e:
        print(e)
        print(content)
        return jsonify({"error": str(e)}), 500

