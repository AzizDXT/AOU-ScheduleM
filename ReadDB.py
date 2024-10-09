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
        print(f"Center: {row['CENTER']}")
        print(f"AOU Email: {row['AOU_EMAIL']}")
        print(f"Course Program: {row['COURSEPROGRAM']}")
        print(f"Course: {row['COURSE']}")
        print(f"Main Course Name: {row['MAIN_COURSE_NAME_L']}")
        print(f"Number of Credits: {row['NB_OF_CREDITS']}")
        print(f"Full Schedule: {row['FullSchedule']}")
        print(f"Days (Arabic): {row['Days_Ar']}")
        print(f"Days (English): {row['Days_En']}")
        print(f"Frequency: {row['Frequency']}")
        print(f"Start Time: {row['START_TIME']}")
        print(f"End Time: {row['END_TIME']}")
        print(f"Start On Week: {row['START_ON_WEEK_OF']}")
        print(f"End Date: {row['END_DATE']}")
        print(f"Academic Year: {row['ACADEMIC_YEAR']}")
        print(f"Semester: {row['ACADEMIC_SEM']}")
        print("="*40)

        # زيادة الرقم الترتيبي
        order_number += 1
