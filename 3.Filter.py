import csv

# قراءة ملف CV.csv وحفظ البيانات المطلوبة في ملف جديد
input_file = 'CS.csv'
output_file = 'filtered_CV.csv'

# فتح الملف الأصلي للقراءة
with open(input_file, mode='r', encoding='windows-1252') as infile:
    # قراءة البيانات من ملف CSV مع تحديد الفاصل الصحيح
    reader = csv.DictReader(infile, delimiter=';')  # تحديد الفاصل كـ ;
    
    # طباعة أسماء الأعمدة لتأكيد وجودها
    print("Column names in CSV:", reader.fieldnames)
    
    # قاموس لتجميع توقيتات المدربين
    tutor_schedule = {}

    for row in reader:
        tutor_name = row['TUTOR']
        aou_email = row['AOU_EMAIL']
        full_schedule = row['FullSchedule']
        
        # إذا كان المدرب موجود بالفعل، نقوم بدمج التواقيت
        if tutor_name in tutor_schedule:
            if full_schedule not in tutor_schedule[tutor_name]['FullSchedule']:
                tutor_schedule[tutor_name]['FullSchedule'].append(full_schedule)
        else:
            # إضافة المدرب الجديد إلى القاموس
            tutor_schedule[tutor_name] = {
                'AOU_EMAIL': aou_email,
                'FullSchedule': [full_schedule]  # اجعل التواقيت كقائمة
            }

    # فتح الملف الجديد للكتابة
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        # تحديد أسماء الأعمدة التي نريد الاحتفاظ بها
        fieldnames = ['TUTOR', 'AOU_EMAIL', 'FullSchedule']
        
        # كتابة البيانات المطلوبة في ملف جديد
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()  # كتابة رأس الجدول

        # كتابة البيانات المجمعة في الملف الجديد
        for tutor, details in tutor_schedule.items():
            writer.writerow({
                'TUTOR': tutor,
                'AOU_EMAIL': details['AOU_EMAIL'],
                'FullSchedule': ', '.join(details['FullSchedule'])  # دمج التواقيت في خانة واحدة
            })
            # طباعة القيم المطلوبة على الشاشة
            print("=" * 40)
            print(f"Tutor: {tutor}")
            print(f"AOU Email: {details['AOU_EMAIL']}")
            print(f"Full Schedule: {', '.join(details['FullSchedule'])}")

