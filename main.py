from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return jsonify('Durian Here')

@app.route('/api/v1/flight_info_online', methods=['POST'])
def flight():
    departure_city = request.form.get('departure_city')
    arrival_city = request.form.get('arrival_city')
    date = request.form.get('date')
    # print(departure_city, arrival_city, date)
    # flights = get_flight_info(departure_city, arrival_city, date)
    # # print(flights)
    # for f in flights:
    #     code = f['flight_number']
    #     state = get_flight_info_by_code(code, date)
    #     f['state'] = state
    #     # print(state)
    subprocess.check_output(['python','flight_spider.py',departure_city,arrival_city,date])
    with open('flight_res.json','r') as res:
        return jsonify(json.load(res))


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
    # date = '2021-07-14'
    # flights = get_flight_info('BJS','SHA', date)
    # code = flights[0]['flight_number']
    # state=get_flight_info_by_code(code, date)
    # flights[0]['state']=state
    # print(flights[0])
