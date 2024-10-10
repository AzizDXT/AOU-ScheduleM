import csv
import random

# فتح الملف وقراءة البيانات باستخدام ترميز مختلف مثل 'ISO-8859-1'
with open('CS.csv', encoding='ISO-8859-1') as csvfile:
    csv_reader = csv.DictReader(csvfile, delimiter=';')

    # رقم ترتيبي يبدأ من 1
    order_number = 1

    # عرض البيانات لكل شخص
    for row in csv_reader:
        # توليد معرف بالشكل 400-XX حيث XX رقم عشوائي من خانتين
        unique_id = f"{random.randint(10, 99)}"
        print(f"ID: {order_number}--{unique_id}")

        # عرض البيانات
        print(f"Tutor: {row['TUTOR']}")
        print(f"AOU Email: {row['AOU_EMAIL']}")
        print(f"Full Schedule: {row['FullSchedule']}")
        print("="*40)

        # زيادة الرقم الترتيبي
        order_number += 1
