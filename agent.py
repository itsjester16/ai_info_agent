pythonimport os
import requests
import json

# Fetch secret keys hidden in GitHub
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
DISCORD_URL = os.environ.get("DISCORD_WEBHOOK_URL")

# Define what you want your agent to research today
# Feel free to edit this prompt directly on GitHub later!
RESEARCH_TOPIC = "The latest advancements in AI agents, LLMs, and open-source AI models over the past 24 hours."

def search_and_summarize():
    url = f"https://googleapis.com{GEMINI_KEY}"
    
    headers = {"Content-Type": "application/json"}
    
    # Payload configuring Gemini 2.0 Flash to use Google Search Grounding
    data = {
        "contents": [{
            "parts": [{
                "text": f"Search the live web and write a clean, well-formatted daily briefing about: {RESEARCH_TOPIC}. Use clean markdown bullet points, bold key terms, and always provide brief context for why the news matters. Keep the summary comprehensive but readable."
            }]
        }],
        "tools": [{"googleSearch": {}}]  # This enables the free Google search function
    }
    
    response = requests.post(url, headers=headers, json=data)
    result = response.json()
    
    # Extract the text answer from Gemini's complex response JSON structure
    try:
        summary_text = result['candidates'][0]['content']['parts'][0]['text']
        return summary_text
    except Exception as e:
        print("Error parsing Gemini response:", result)
        return "Failed to generate daily report due to an API formatting issue."

def send_to_discord(text):
    # Discord limits single webhook messages to 2000 characters.
    # This loop safely cuts long reports into smaller blocks.
    chunks = [text[i:i+1900] for i in range(0, len(text), 1900)]
    
    for chunk in chunks:
        payload = {"content": chunk}
        requests.post(DISCORD_URL, json=payload)

if __name__ == "__main__":
    print("Agent starting research loop...")
    report = search_and_summarize()
    print("Research complete. Pushing to Discord...")
    send_to_discord(report)
    print("Done!")
