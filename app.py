from flask import Flask, request, jsonify
import requests
import json
import datetime

app = Flask(__name__)

def fetch_page(zone_code, year, month=None):
    base_url = "https://www.e-solat.gov.my/index.php?r=esolatApi/takwimsolat&period=duration&zone="
    url = f"{base_url}{zone_code}"
    
    # Prepare POST data
    dates = get_duration_date(month, year)
    postdata = {
        'datestart': dates['start'],
        'dateend': dates['end']
    }
    
    # Fetch the page content
    try:
        response = requests.post(url, data=postdata, verify=False)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.RequestException as e:
        return {'error': str(e)}, 500
    
    result = response.json()
    
    arr_data = {'data': []}
    if 'prayerTime' in result and len(result['prayerTime']) > 0:
        for waktu in result['prayerTime']:
            arr_data['data'].append({
                'hijri': waktu['hijri'],
                'date': datetime.datetime.strptime(waktu['date'], '%d-%b-%Y').strftime('%Y-%m-%d'),
                'day': waktu['day'],
                'imsak': convert_time(waktu['imsak']),
                'subuh': convert_time(waktu['fajr']),
                'syuruk': convert_time(waktu['syuruk']),
                'zohor': convert_time(waktu['dhuhr']),
                'asar': convert_time(waktu['asr']),
                'maghrib': convert_time(waktu['maghrib']),
                'isyak': convert_time(waktu['isha']),
            })
    
    arr_data['httpstatus'] = response.status_code
    return arr_data, response.status_code

def get_duration_date(month, year):
    if month:
        month = str(month).zfill(2)
        start_date = f"{year}-{month}-01"
        end_date = f"{year}-{month}-{(datetime.datetime(year, int(month), 1) + datetime.timedelta(days=31)).replace(day=1) - datetime.timedelta(days=1):%d}"
    else:
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
    
    return {'start': start_date, 'end': end_date}

def convert_time(time_str):
    # Replace separator and convert to 12h format
    print(time_str)
    time_str = time_str.replace(".", ":")
    time_obj = datetime.datetime.strptime(time_str, "%H:%M:%S")
    return time_obj.strftime('%I:%M %p')

def proj_info(arr_data):
    arr_data['info'] = {
        'creator': "Muhammad Haziq bin Abdul Hamid",
        'date_updated': "28/08/2024"
    }
    return arr_data

@app.route('/apiv2', methods=['GET'])
def api_v2():
    zone_code = request.args.get('z')
    year = request.args.get('y')
    month = request.args.get('m', None)
    day = request.args.get('d', None)

    if not zone_code or not year:
        return jsonify({
            'error': 'Missing required parameters. Zone and Year required.'
        }), 400

    try:
        year = int(year)
        if month:
            month = int(month)
            if month < 1 or month > 12:
                return jsonify({'error': 'Month must be between 1 and 12.'}), 400
        if month:
            arr_data, status_code = fetch_page(zone_code, year, month)
        else:
            arr_data = {i: fetch_page(zone_code, year, i) for i in range(1, 13)}
            status_code = 200
        
        return jsonify(proj_info(arr_data)), status_code
    except ValueError:
        return jsonify({'error': 'Invalid value insert into (Year - 4 digit) and (month - Range 1 - 12)'}), 400

if __name__ == "__main__":
    app.run(debug=True)
