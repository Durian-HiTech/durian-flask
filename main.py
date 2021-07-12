from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return jsonify('Durian Here')


@app.route('/test_question', methods=['POST'])
def receive_question():
    question_content = request.form.get('question_content')
    res = {
        'question_content': question_content
    }
    return jsonify(res)


# 返回航班列表 (无状态)
def get_flight_info(d, a, date):
    url = "https://flights.ctrip.com/itinerary/api/12808/products"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0",
        "Referer": "https://flights.ctrip.com/itinerary/oneway/bjs-sha?date=" + date,
        "Content-Type": "application/json"
    }
    request_payload = {
        "flightWay": "Oneway",
        "classType": "ALL",
        "hasChild": False,
        "hasBaby": False,
        "searchIndex": 1,
        "airportParams": [
            {"dcity": d, "acity": a, "date": date}
        ]
    }

    response = requests.post(url, data=json.dumps(
        request_payload), headers=headers).text

    routeList = json.loads(response).get('data').get('routeList')

    flights = []

    for route in routeList:
        # 判断是否有信息，有时候没有会报错
        if len(route.get('legs')) == 1:
            legs = route.get('legs')
            flight = legs[0].get('flight')
            # 提取想要的信息
            airline_name = flight.get('airlineName')
            flight_number = flight.get('flightNumber')
            departure_date = flight.get('departureDate')
            arrival_date = flight.get('arrivalDate')
            departure_city_name = flight.get(
                'departureAirportInfo').get('cityName')
            departure_airport_name = flight.get(
                'departureAirportInfo').get('airportName')
            arrival_city_name = flight.get(
                'arrivalAirportInfo').get('cityName')
            arrival_airport_name = flight.get(
                'arrivalAirportInfo').get('airportName')

            single_flight = {
                'airline_name': airline_name,
                'flight_number': flight_number,
                'departure_date': departure_date,
                'arrival_date': arrival_date,
                'departure_city_name': departure_city_name,
                'departure_airport_name': departure_airport_name,
                'arrival_city_name': arrival_city_name,
                'arrival_airport_name': arrival_airport_name
            }

            flights.append(single_flight)

    return flights


def get_flight_info_by_code(code, date=datetime.now().strftime('%Y-%m-%d')):
    from bs4 import BeautifulSoup
    url = f'http://www.umetrip.com/mskyweb/fs/fc.do?flightNo={code}&date={date}&channel='
    fail_num = 0
    while True:
        if fail_num == 1:
            return '暂无'
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        state = soup.find(attrs={'class': 'state'})
        if state is not None:
            condition = state.text.strip()[:2]
            return condition
        fail_num += 1


@app.route('/api/v1/flight_info_online', methods=['POST'])
def flight():
    departure_city = request.form.get('departure_city')
    arrival_city = request.form.get('arrival_city')
    date = request.form.get('date')
    print(departure_city, arrival_city, date)
    flights = get_flight_info(departure_city, arrival_city, date)
    # print(flights)
    for f in flights:
        code = f['flight_number']
        state = get_flight_info_by_code(code, date)
        f['state'] = state
        # print(state)
    return jsonify(flights)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
    # date = '2021-07-14'
    # flights = get_flight_info('BJS','SHA', date)
    # code = flights[0]['flight_number']
    # state=get_flight_info_by_code(code, date)
    # flights[0]['state']=state
    # print(flights[0])
