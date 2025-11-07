from flask import Flask, render_template, request, jsonify
from bytez import Bytez
import os
app = Flask(__name__)

# ✅ Bytez setup
key = os.getenv ("BYTEZ_API_KEY", "b0158cc05479f10b8e76167236616626")
sdk = Bytez(key)
model = sdk.model("openai/gpt-4o")

conversation = []

@app.route("/")
def home():
    return render_template("index.html", title="Winston AI")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "").strip()
    print("USER SAID:", user_input)

    if not user_input:
        return jsonify({"reply": "Please say something."})

    conversation.append({"role": "user", "content": user_input})

    try:
        result = model.run(conversation)
        print("DEBUG RESULT:", result)

        # ✅ Improved extraction logic
        bot_reply = None
        if hasattr(result, "output"):
            output = result.output
            if isinstance(output, dict):
                bot_reply = output.get("content") or output.get("message") or output.get("output")
            else:
                bot_reply = str(output)
        elif isinstance(result, dict):
            bot_reply = (
                result.get("output")
                or result.get("content")
                or result.get("message")
                or str(result)
            )
        else:
            bot_reply = str(result)

        if not bot_reply:
            bot_reply = "⚠️ Winston AI didn’t send a reply."

        conversation.append({"role": "assistant", "content": bot_reply})
        return jsonify({"reply": bot_reply})

    except Exception as e:
        print("⚠️ Error:", e)
        return jsonify({"reply": f"⚠️ Error: {e}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
