import openai
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

openai.api_key = "f79a3d8e7b7d42c6aee107040bf27c9f"

def get_lyrics_from_gpt(song_title, artist_name):
    prompt = f"Напиши текст песни под названием '{song_title}' исполнителя '{artist_name}'."
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  
            prompt=prompt,
            max_tokens=300,  
            n=1,  
            stop=None,  
            temperature=0.7
        )

        
        lyrics = response.choices[0].text.strip()
        return lyrics
    except Exception as e:
        return f"Ошибка при получении текста песни: {str(e)}"

@app.route("/get_lyrics", methods=["POST"])
def fetch_lyrics():
    data = request.json
    song_title = data.get("song_title")
    artist_name = data.get("artist_name")

    if not song_title or not artist_name:
        return jsonify({"error": "Необходимо указать название песни и исполнителя."}), 400

    lyrics = get_lyrics_from_gpt(song_title, artist_name)
    
    if lyrics.startswith("Ошибка"):
        return jsonify({"error": lyrics}), 500
    else:
        return jsonify({"lyrics": lyrics})

if __name__ == "__main__":
    app.run(debug=True)
