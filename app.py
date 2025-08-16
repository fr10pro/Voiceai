from flask import Flask, render_template_string, request, jsonify
from groq import Groq

# Your Groq API key
API_KEY = "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"

# Init Flask + Groq client
app = Flask(__name__)
client = Groq(api_key=API_KEY)

# Simple HTML template
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
  <title>AI Chat (Groq)</title>
  <style>
    body { font-family: Arial, sans-serif; margin: 20px; background: #f4f4f9; }
    #chat { width: 100%; max-width: 600px; margin: auto; }
    .msg { padding: 10px; border-radius: 8px; margin: 5px; }
    .user { background: #0084ff; color: white; text-align: right; }
    .bot { background: #e5e5ea; color: black; text-align: left; }
    input { width: 80%; padding: 10px; border-radius: 8px; border: 1px solid #ccc; }
    button { padding: 10px; border: none; border-radius: 8px; background: #0084ff; color: white; }
  </style>
</head>
<body>
  <div id="chat"></div>
  <div style="text-align:center; margin-top:20px;">
    <input id="msg" placeholder="Type a message..." />
    <button onclick="send()">Send</button>
  </div>

<script>
async function send() {
  let input = document.getElementById("msg");
  let userMsg = input.value;
  if (!userMsg) return;

  // Show user message
  document.getElementById("chat").innerHTML += 
      `<div class='msg user'>${userMsg}</div>`;
  input.value = "";

  // Send to backend
  let res = await fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: userMsg })
  });

  let data = await res.json();

  // Show AI reply
  document.getElementById("chat").innerHTML += 
      `<div class='msg bot'>${data.reply}</div>`;
}
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_PAGE)

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")

    response = client.chat.completions.create(
        messages=[{"role": "user", "content": user_msg}],
        model="llama3-8b-8192"
    )

    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
