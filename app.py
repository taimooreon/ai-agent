from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
from dotenv import load_dotenv
import openai
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)

@app.route("/voice", methods=['POST'])
def voice():
    """Entry point: Twilio calls this when someone calls your Twilio number."""
    resp = VoiceResponse()
    gather = Gather(input='speech', action='/gpt-response', speechTimeout='auto', language='en-US')
    gather.say("Hello, I am your AI assistant. Please ask your question after the beep.")
    resp.append(gather)
    resp.redirect('/voice')  # if no input
    return Response(str(resp), mimetype='text/xml')


@app.route("/gpt-response", methods=['POST'])
def gpt_response():
    """Called after user speaks."""
    user_input = request.form.get('SpeechResult')
    print(f"User said: {user_input}")

    if not user_input:
        response = VoiceResponse()
        response.say("Sorry, I didn't catch that.")
        return Response(str(response), mimetype='text/xml')

    # GPT response
    openai_response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a friendly AI assistant answering phone calls."},
            {"role": "user", "content": user_input}
        ]
    )

    reply = openai_response.choices[0].message.content

    # Respond via voice
    response = VoiceResponse()
    response.say(reply)
    return Response(str(response), mimetype='text/xml')


if __name__ == "__main__":
    app.run(port=5000)
