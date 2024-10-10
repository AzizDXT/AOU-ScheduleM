from flask import Flask, render_template, request
import openai
import pandas as pd

app = Flask(__name__)

# Load the CSV file and sort tutors by name alphabetically
def load_tutors_data():
    df = pd.read_csv('4.filtered_CV.csv')
    # تأكد من استبدال 'Tutor Name' باسم العمود الصحيح
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
    app.run(debug=True, port=80)
