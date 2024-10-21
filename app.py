import os
import time
import csv
import pandas as pd
from flask import Flask, render_template, request
import threading

app = Flask(__name__)

drop_here_folder = "Drop-here"

def ensure_drop_here_folder():
    if not os.path.exists(drop_here_folder):
        os.makedirs(drop_here_folder)

def convert_excel_to_csv(file_path):
    df = pd.read_excel(file_path)
    csv_file_path = os.path.join(os.getcwd(), '2.CS.CSV')
    df.to_csv(csv_file_path, index=False, sep=';')
    return csv_file_path

def filter_data(csv_file):
    output_file = '4.filtered-Data.csv'

    with open(csv_file, mode='r', encoding='windows-1252') as infile:
        reader = csv.DictReader(infile, delimiter=';')
        if 'COURSEPROGRAM' not in reader.fieldnames:
            print("Error: 'COURSEPROGRAM' column is not found in the CSV file.")
            return
        
        tutor_schedule = {}
        for row in reader:
            try:
                COURSEPROGRAM = row['COURSEPROGRAM']
                tutor_name = row['TUTOR']
                aou_email = row['AOU_EMAIL']
                full_schedule = row['FullSchedule']
                
                if tutor_name in tutor_schedule:
                    if full_schedule not in tutor_schedule[tutor_name]['FullSchedule']:
                        tutor_schedule[tutor_name]['FullSchedule'].append(full_schedule)
                else:
                    tutor_schedule[tutor_name] = {
                        'AOU_EMAIL': aou_email,
                        'FullSchedule': [full_schedule],
                        'COURSEPROGRAM': COURSEPROGRAM
                    }
            except KeyError as e:
                print(f"Error: Missing key {e} in row: {row}")

    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        fieldnames = ['TUTOR', 'AOU_EMAIL', 'FullSchedule', 'COURSEPROGRAM']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for tutor, details in tutor_schedule.items():
            writer.writerow({
                'TUTOR': tutor,
                'AOU_EMAIL': details['AOU_EMAIL'],
                'FullSchedule': ', '.join(details['FullSchedule']),
                'COURSEPROGRAM': details['COURSEPROGRAM']
            })

def monitor_drop_here(drop_here_folder):
    while True:
        files = os.listdir(drop_here_folder)
        for file in files:
            if file.endswith('.xlsx'):
                file_path = os.path.join(drop_here_folder, file)
                csv_file = convert_excel_to_csv(file_path)
                filter_data(csv_file)
                print(f"Processed file: {file_path} into {csv_file}")
                os.remove(file_path)
                break
        time.sleep(5)

def start_monitoring():
    ensure_drop_here_folder()
    monitor_drop_here(drop_here_folder)

def load_tutors_data():
    df = pd.read_csv('4.filtered-Data.csv')
    df.sort_values(by='TUTOR', inplace=True)
    tutors = df.to_dict(orient='records')
    return tutors

@app.route('/')
def index():
    try:
        tutors = load_tutors_data()
        return render_template('index.html', tutors=tutors)
    except Exception as e:
        return f"Error loading tutors data: {e}", 500

@app.route('/response', methods=['GET'])
def response():
    gpt_response = request.args.get('response', 'No response received.')
    return render_template('response.html', gpt_response=gpt_response)

# وظيفة التطبيق لـ WSGI
def application(environ, start_response):
    with app.request_context(environ):
        try:
            response = app.full_dispatch_request()
            start_response(f'{response.status_code} {response.status}', list(response.headers.items()))  # تحويل إلى قائمة
            return response.response
        except Exception as e:
            start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
            return [f"Internal Server Error: {str(e)}".encode()]

if __name__ == '__main__':
    threading.Thread(target=start_monitoring, daemon=True).start()
    app.run(debug=False)  # يعمل بدون تحديد المنفذ أو المضيف
