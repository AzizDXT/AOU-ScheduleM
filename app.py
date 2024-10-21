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
    # قراءة ملف Excel
    df = pd.read_excel(file_path)
    
    # حفظ الملف كـ CSV جديد في نفس مسار السكربت
    csv_file_path = os.path.join(os.getcwd(), '2.CS.CSV')  # حفظ الملف باسم 2.CS.CSV
    df.to_csv(csv_file_path, index=False, sep=';')  # حفظ كملف CSV مع الفاصل المطلوب
    return csv_file_path

def filter_data(csv_file):
    output_file = '4.filtered-Data.csv'

    # قراءة ملف CSV وحفظ البيانات المطلوبة في ملف جديد
    with open(csv_file, mode='r', encoding='windows-1252') as infile:
        reader = csv.DictReader(infile, delimiter=';')
        print("Column names in CSV:", reader.fieldnames)
        
        if 'COURSEPROGRAM' not in reader.fieldnames:
            print("Error: 'COURSEPROGRAM' column is not found in the CSV file.")
            return
        
        # قاموس لتجميع توقيتات المدربين
        tutor_schedule = {}

        for row in reader:
            # التحقق من وجود القيم المطلوبة في الصف
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

    # فتح الملف الجديد للكتابة
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
            if file.endswith('.xlsx'):  # التحقق من وجود ملف Excel
                file_path = os.path.join(drop_here_folder, file)
                csv_file = convert_excel_to_csv(file_path)  # تحويل ملف Excel إلى CSV
                filter_data(csv_file)  # تنفيذ عملية الفلترة
                print(f"Processed file: {file_path} into {csv_file}")  # عرض الملف المعالج
                os.remove(file_path)  # حذف الملف الأصلي بعد المعالجة
                break  # اخرج من الحلقة بعد معالجة الملف

        time.sleep(5)  # الانتظار لمدة 5 ثوانٍ قبل التحقق مرة أخرى

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
    tutors = load_tutors_data()
    return render_template('index.html', tutors=tutors)

@app.route('/response', methods=['GET'])
def response():
    gpt_response = request.args.get('response', 'No response received.')
    return render_template('response.html', gpt_response=gpt_response) 

if __name__ == '__main__':
    threading.Thread(target=start_monitoring, daemon=True).start()  # بدء المراقبة في خيط منفصل
    app.run(debug=True, port=5000)
