from flask import Flask, request, jsonify

app=Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    return jsonify('Durian Flask')

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)