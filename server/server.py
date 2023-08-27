from flask import Flask, jsonify, abort
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def get_result():
  try:
    with open('result.json', 'r', encoding='utf-8') as fp:
      return jsonify(json.load(fp))
  except:
    abort(500)

if __name__ == "__main__":
  app.run(port=8080)
