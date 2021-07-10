from flask import Flask, request, jsonify

app=Flask(__name__)

@app.route('/',methods=['GET'])
def index():
    return jsonify('Durian Here')

@app.route('/test_question',methods=['POST'])
def receive_question():
    question_content=request.form.get('question_content')
    res={
        'question_content': question_content
    }
    return jsonify(res)
    
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)