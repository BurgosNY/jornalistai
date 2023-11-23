from flask import Flask, render_template, jsonify, url_for, request
import json
from openai import OpenAI
from transcricao import entrevista
from dotenv import load_dotenv
import jinja_partials
load_dotenv()


app = Flask(__name__)
client = OpenAI()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/processar_pergunta', methods=['POST'])
def ask_gpt():
    pergunta = request.form.get('pergunta').strip()
    response = client.chat.completions.create(
                                              model="gpt-4-1106-preview",
                                              response_format={ "type": "json_object" },
                                              messages=[
                                                        {"role": "system", "content": "Você é um assistente solícito que responde em JSON. Sua resposta deve ser uma das duas opções: ou 'não sei' ou o 'start' e 'end' contidos na transcrição de uma entrevista."},
                                                        {"role": "user", "content": f"Utilize essa transcrição de entrevista para responder uma pergunta: {entrevista}.\nA pergunta é: {pergunta}"}])
    gpt_answer = json.loads(response.choices[0].message.content)
    gpt_answer = {'start': 0, 'end': 30}
    return render_template('componente_audio.html', start=gpt_answer['start'], end=gpt_answer['end'])

if __name__ == '__main__':
  app.run(port=8000, debug=True)