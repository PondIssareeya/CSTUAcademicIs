from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
import csv, io, os, datetime, mimetypes, pytz
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.conf import settings
from django.template import loader
# from json import dumps
from django.db.models import ObjectDoesNotExist, Q
from .models import Student, Enrollment, Applicant_Plan, Data_Basic, Data, Required_C, Course_Usage, Grade, Status, State_Inactive, History, Person, ApplicantType, SubApplicantType, User
from .models import StudentForm, EnrollmentEditForm, GradeEditForm, StateEditForm, CourseUsageForm, CourseUsageEditForm, StudentEditForm, PlanEditForm, PersonCreationForm, SubApplicantTypeForm, SubApplicantTypeEditForm
from .forms import SearchForm


# Create your views here.
# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = auth.authenticate(username=username, password=password)
#         if user is None:
#             messages.error(request, 'Username or Password invalid!')
#             return redirect('/academicis/login')
#         else:
#             auth.login(request, user)
#             return redirect('/academicis/home')
#     return render(request, 'academicis_app/page_login.html')

# def logout(request):
#     auth.logout(request)
#     return redirect('/academicis/login')

@login_required
def homepage(request):
    return render(request, 'academicis_app/page_home.html')

def basic(request):
    return render(request, 'academicis_app/page_basic.html')

def highschool_plan(request):
    return render(request, 'academicis_app/page_highschool_plan.html')

def admit_type(request):
    return render(request, 'academicis_app/page_admit_type.html')

def student_now(request):
    return render(request, 'academicis_app/page_student_now.html')

def eng_efficiency(request):
    return render(request, 'academicis_app/page_english.html')

def requiredC(request):
    return render(request, 'academicis_app/page_requiredC.html')

def pass_CS300(request):
    return render(request, 'academicis_app/page_pass300.html')

# def list_data(request):
#     return render(request, 'academicis_app/student_detail.html',{
#         'students': Student.objects.all(),
#     })

def history(request):
    return render(request, 'academicis_app/page_history.html',{'show':History.objects.all().order_by('-id')})

def download_history(request):
    history = History.objects.all().order_by('-id')

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="activity.csv"'
    response.write(u'\ufeff'.encode('utf8'))

    writer = csv.writer(response)
    writer.writerow(['date_time', 'user', 'activity'])

    for item in history:
        writer.writerow([item.time, item.name, item.activity])

    return response

def download_file(request):
    return render(request, 'academicis_app/page_download.html')

def download_student(request):    
    response = HttpResponse(content_type='text/csv') #Define an HttpResponse of type CSV
    response['Content-Disposition'] = "attachment;filename=student.csv" #Define the return information, attachment mode and file name;
    writer = csv.writer(response)  #Write response using csv module
    writer.writerow(['student_id','student_name_surname','level','admitacad_year','applicanttype_id','applicanttype_name','applicanttype_name_morespecific','student_highschool_study_plan','student_highschool','student_highschool_gpa']) #Heading line
    return response

def download_enrollment(request):    
    response = HttpResponse(content_type='text/csv') #Define an HttpResponse of type CSV
    response['Content-Disposition'] = "attachment;filename=enrollment.csv" #Define the return information, attachment mode and file name;
    writer = csv.writer(response)  #Write response using csv module
    writer.writerow(['student_id','admitacad_year','academic_year','semester','course_id','creditsatisfy','grade']) #Heading line
    return response

def download_grade(request):    
    response = HttpResponse(content_type='text/csv') #Define an HttpResponse of type CSV
    response['Content-Disposition'] = "attachment;filename=grade.csv" #Define the return information, attachment mode and file name;
    writer = csv.writer(response)  #Write response using csv module
    writer.writerow(['student_id','student_name_surname','academic_semester','academic_year','creditsatisfy','creditpoint', 'ix_count', 'gradepoint', 's_gpa', 's_gpax', 'status']) #Heading line
    return response

def download_status(request):    
    response = HttpResponse(content_type='text/csv') #Define an HttpResponse of type CSV
    response['Content-Disposition'] = "attachment;filename=status.csv" #Define the return information, attachment mode and file name;
    writer = csv.writer(response)  #Write response using csv module
    writer.writerow(['student_id','student_name_surname','semester','academic_year','status','grade']) #Heading line
    return response

def download_state(request):    
    response = HttpResponse(content_type='text/csv') #Define an HttpResponse of type CSV
    response['Content-Disposition'] = "attachment;filename=state.csv" #Define the return information, attachment mode and file name;
    writer = csv.writer(response)  #Write response using csv module
    writer.writerow(['student_id','student_name_surname','state_not_normal','grade']) #Heading line
    return response

def download_course(request):    
    response = HttpResponse(content_type='text/csv') #Define an HttpResponse of type CSV
    response['Content-Disposition'] = "attachment;filename=course.csv" #Define the return information, attachment mode and file name;
    writer = csv.writer(response)  #Write response using csv module
    writer.writerow(['curriculum', 'period', 'course_id', 'course_name', 'elective_or_mandatory']) #Heading line
    return response

def download_appType(request):    
    response = HttpResponse(content_type='text/csv') #Define an HttpResponse of type CSV
    response['Content-Disposition'] = "attachment;filename=applicant_type.csv" #Define the return information, attachment mode and file name;
    writer = csv.writer(response)  #Write response using csv module
    writer.writerow(['type_id', 'name']) #Heading line
    return response

def download_plan(request):    
    response = HttpResponse(content_type='text/csv') #Define an HttpResponse of type CSV
    response['Content-Disposition'] = "attachment;filename=plan.csv" #Define the return information, attachment mode and file name;
    writer = csv.writer(response)  #Write response using csv module
    writer.writerow(['year', 'major', 't1_plan', 't2_plan', 't3_plan', 't4_plan', 't5_plan']) #Heading line
    return response

def upload_file(request):
    if request.method == "GET":
        return render(request, 'academicis_app/page_upload.html')
    if 'file' in request.FILES:
        csv_file = request.FILES['file']
        data = []
        temp = []
        item = -1 #not count head
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'กรุณาเลือกไฟล์สกุล csv เท่านั้น')
            return redirect('/academicis/uploadfile')
        data_set = csv_file.read().decode('utf-8')
        io_string = io.StringIO(data_set)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            data.append(column)
            item += 1
        messages.success(request, 'Data ' + str(item) + ' rows')
        return render(request, 'academicis_app/page_upload.html',{'data': data_set, 'file': csv_file, 'show':data})
    else:
        messages.error(request, "กรุณาเลือกไฟล์")
        return redirect('/academicis/uploadfile')

def check_data(request):
    if request.method == "POST":
        choice = request.POST.get("choice", None)
        files = request.POST.get("fileDB", None)
        btn = request.POST.get("btn", None)
        if 'cancel' in btn:
            return redirect('/academicis/uploadfile')
        else:
            io_string = io.StringIO(files)
            data_head= []
            temp = next(io_string)
            header = temp.split(",")
            for x in header:
                data_head.append(x)
            if 'student' in choice:
                if ((data_head[0] == "\ufeffstudent_id" or data_head[0] == "student_id") and data_head[1] == "student_name_surname" and data_head[2] == "level" and data_head[3] == "admitacad_year" and data_head[4] == "applicanttype_id" and
                    data_head[5] == "applicanttype_name" and data_head[6] == "applicanttype_name_morespecific" and data_head[7] == "student_highschool_study_plan" and data_head[8] == "student_highschool" and data_head[9] == "student_highschool_gpa\r\n"):
                    return data_student(request, files)
                else:
                    messages.error(request, "ข้อมูลไม่ถูกต้อง") 
                    return redirect('/academicis/uploadfile')
            elif 'enrollment' in choice:
                if ((data_head[0] == "\ufeffstudent_id" or data_head[0] == "student_id") and data_head[1] == "admitacad_year" and data_head[2] == "academic_year" and data_head[3] == "semester" and 
                    data_head[4] == "course_id" and data_head[5] == "creditsatisfy" and data_head[6] == "grade\r\n"):
                    return data_enrollment(request, files)
                else:
                    messages.error(request, "ข้อมูลไม่ถูกต้อง") 
                    return redirect('/academicis/uploadfile')
            elif 'grade' in choice:
                if ((data_head[0] == "\ufeffstudent_id" or data_head[0] == "student_id") and data_head[1] == "student_name_surname" and data_head[2] == "academic_semester" and data_head[3] == "academic_year" and data_head[4] == "creditsatisfy" and 
                    data_head[5] == "creditpoint" and data_head[6] == "ix_count" and data_head[7] == "gradepoint" and data_head[8] == "s_gpa" and data_head[9] == "s_gpax" and data_head[10] == "s_status\r\n"):
                    return data_grade(request, files)
                else:
                    messages.error(request, "ข้อมูลไม่ถูกต้อง") 
                    return redirect('/academicis/uploadfile')
            elif 'state' in choice:
                if ((data_head[0] == "\ufeffstudent_id" or data_head[0] == "student_id") and data_head[1] == "student_name_surname" and data_head[2] == "state_not_normal" and data_head[3] == "grade\r\n"):
                    return data_state(request, files)
                else:
                    messages.error(request, "ข้อมูลไม่ถูกต้อง") 
                    return redirect('/academicis/uploadfile')
            elif 'course' in choice:
                if ((data_head[0] == "\ufeffcurriculum" or data_head[0] == "curriculum") and data_head[1] == "period" and data_head[2] == "course_id" and data_head[3] == "course_name" and data_head[4] == "elective_or_mandatory\r\n"):
                    return data_course(request, files)
                else:
                    messages.error(request, "ข้อมูลไม่ถูกต้อง") 
                    return redirect('/academicis/uploadfile')
            elif 'appType' in choice:
                if ((data_head[0] == "\ufefftype_id" or data_head[0] == "type_id") and data_head[1] == "name\r\n"):
                    return data_appType(request, files)
                else:
                    messages.error(request, "ข้อมูลไม่ถูกต้อง") 
                    return redirect('/academicis/uploadfile')
            elif 'plan' in choice:
                if ((data_head[0] == "\ufeffyear" or data_head[0] == "year") and data_head[1] == "major" and data_head[2] == "t1_plan" and data_head[3] == "t2_plan" and 
                    data_head[4] == "t3_plan" and data_head[5] == "t4_plan" and data_head[6] == "t5_plan\r\n"):
                    return data_plan(request, files)
                else:
                    messages.error(request, "ข้อมูลไม่ถูกต้อง") 
                    return redirect('/academicis/uploadfile')

def confirm_file(request):
    if request.method == "POST":
        name = request.POST.get("tableDB", None)
        if 'Student' in name:
            return confirm_uploadStudent(request)
        elif 'Enrollment' in name:
            return confirm_uploadEnrollment(request)
        elif 'Grade' in name:
            return confirm_uploadGrade(request)
        elif 'State' in name:
            return confirm_uploadState(request)
        elif 'Course' in name:
            return confirm_uploadCourse(request)
        elif 'Applicant Type' in name:
            return confirm_uploadAppType(request)
        elif 'Plan' in name:
            return confirm_uploadPlan(request)

def data_student(request, file):
    data = Student.objects.all()
    if request.method == "GET":
        return render(request, 'academicis_app/page_showData.html')
    io_string = io.StringIO(file)
    next(io_string)
    list_data = [] #only ID student
    new_data = [] #data new
    old_data = [] #student on database
    update_data = [] #data update
    head = ["รหัสนักศึกษา","ชื่อ-สกุล","โครงการ","ปีที่เข้าศึกษา","รหัส","ช่องทางเข้าศึกษา","รายละเอียดช่องทาง","แผนการเรียนมัธยม","โรงเรียนมัธยม","เกรดมัธยม"]
    for x in data:
        list_data.append(x.student_id)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        new_data.append(column)
        for x in list_data:
            if column[0] == x:
                old = Student.objects.get(student_id=x)
                list_old = [old.student_id,old.student_name_surname,old.level,old.admitacad_year,old.applicanttype_id,old.applicanttype_name,old.applicanttype_name_morespecific,old.student_highschool_study_plan,old.student_highschool,old.student_highschool_gpa]
                old_data.append(list_old)
                update_data.append(column)
                new_data.remove(column)
                break

    return render(request, 'academicis_app/page_showData.html',{'new': new_data, 'up': len(update_data),'files':file, 'header':head, 'data':zip(old_data,update_data), 'nameTable': "Student"})

def confirm_uploadStudent(request):
    if request.method == 'POST':
        data = request.POST.getlist('check')
        choice = request.POST.get("choice", None)
        files = request.POST.get("fileDB", None)
    item = 0
    if 'confirm' in choice:

        io_string = io.StringIO(files)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            for x in data:
                if column[2] == "ปริญญาตรี โครงการปกติ" or column[2] == "ปริญญาตรี โครงการพิเศษ" or column[2] == "ปริญญาตรี โครงการปกติ ศูนย์ลำปาง":
                    pass
                else:
                    messages.error(request, "นักศึกษารหัส " + column[0] + " ชื่อโครงการไม่ถูกต้อง") 
                    return redirect('/academicis/uploadfile')
                if column[7] in (None, ""):
                    column[7] = "วิทย์-คณิต"

                if column[0] == eval(x)[0]:
                    _, created = Student.objects.update_or_create(
                        student_id = column[0],
                        defaults = {
                        'student_name_surname' : column[1],
                        'level' : column[2],
                        'admitacad_year' : column[3],
                        'applicanttype_id' : column[4],
                        'applicanttype_name' : column[5],
                        'applicanttype_name_morespecific' : column[6], 
                        'student_highschool_study_plan' : column[7],
                        'student_highschool' : column[8],
                        'student_highschool_gpa' : column[9],}
                    )
                    item += 1
        messages.success(request, "อัพโหลดไฟล์เข้าตาราง \"Student\" สำเร็จ " + str(item) + " รายการ")
        process_basic()
        process_plan()
        student_Inactive()
        tz = pytz.timezone('Asia/Bangkok')
        date = datetime.datetime.now(tz=tz)
        History.objects.create(time=date.strftime("%d/%m/") + str(date.year+543) + " " + date.strftime("%H:%M"), name=request.user.username, activity="อัพโหลดไฟล์ข้อมูลนักศึกษา")
        # process_data()
    elif 'cancel' in choice:
        return redirect('/academicis/uploadfile')
    return render(request, 'academicis_app/page_uploadfinished.html')

def data_enrollment(request, file):
    data = Enrollment.objects.all()
    if request.method == "GET":
        return render(request, 'academicis_app/page_showData.html')
    io_string = io.StringIO(file)
    next(io_string)
    list_data = [] #only ID student
    new_data = [] #data new
    old_data = [] #student on database
    update_data = [] #data update
    head = head = ["รหัสนักศึกษา","ปีที่เข้าศึกษา", "ปีลงทะเบียนเรียน", "เทอมลงทะเบียน", "รหัสวิชา", "เครดิตที่ได้รับ", "เกรดที่ได้รับ"]
    for x in data:
        list_course = [x.student_id, x.academic_year, x.semester, x.course_id]
        list_data.append(list_course)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        new_data.append(column)
        for x in list_data:
            if column[0] == x[0] and column[2] == str(x[1]) and column[3] == str(x[2]) and column[4] == x[3]:
                old = Enrollment.objects.get(student_id=x[0], academic_year=x[1], semester=x[2], course_id=x[3])
                list_old = [old.student_id,old.admitacad_year,old.academic_year,old.semester,old.course_id,old.creditsatisfy,old.grade]
                old_data.append(list_old)
                update_data.append(column)
                new_data.remove(column)
                break

    return render(request, 'academicis_app/page_showData.html',{'new': new_data, 'up': len(update_data),'files':file, 'header':head, 'data':zip(old_data,update_data), 'nameTable': "Enrollment"})

def confirm_uploadEnrollment(request):
    if request.method == 'POST':
        data = request.POST.getlist('check')
        choice = request.POST.get("choice", None)
        files = request.POST.get("fileDB", None)
    item = 0
    if 'confirm' in choice:
        io_string = io.StringIO(files)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            for x in data:
                if column[6] == "A" or column[6] == "B+" or column[6] == "B" or column[6] == "C+" or column[6] == "C" or column[6] == "D+" or column[6] == "D" or column[6] == "F" or column[6] == "W" or column[6] == "U" or column[6] == "S" or column[6] == "S#" or column[6] == "U#":
                    pass
                else:
                    messages.error(request, "นักศึกษารหัส " + column[0] + " เกรดวิชา " + column[4] + " ไม่ถูกต้อง") 
                    return redirect('/academicis/uploadfile')

                if column[0] == eval(x)[0] and column[2] == eval(x)[2] and column[3] == eval(x)[3] and column[4] == eval(x)[4]:
                    _, created = Enrollment.objects.update_or_create(
                        student_id = column[0],
                        admitacad_year = column[1],
                        academic_year = column[2],
                        semester = column[3],
                        course_id = column[4],
                        defaults = {
                            'creditsatisfy' : column[5],
                            'grade' : column[6],
                        }
                    )
                    item += 1
        messages.success(request, "อัพโหลดไฟล์เข้าตาราง \"Enrollment\" สำเร็จ " + str(item) + " รายการ")
        # process_basic(request)
        process_requiredC(data)
        tz = pytz.timezone('Asia/Bangkok')
        date = datetime.datetime.now(tz=tz)
        History.objects.create(time=date.strftime("%d/%m/") + str(date.year+543) + " " + date.strftime("%H:%M"), name=request.user.username, activity="อัพโหลดไฟล์การลงทะเบียนเรียน และผลการศึกษาแต่ละรายวิชา")
    elif 'cancel' in choice:
        return redirect('/academicis/uploadfile')
    return render(request, 'academicis_app/page_uploadfinished.html')

def data_grade(request, file):
    data = Grade.objects.all()
    if request.method == "GET":
        return render(request, 'academicis_app/page_showData.html')
    io_string = io.StringIO(file)
    next(io_string)
    list_data = [] #only ID student
    new_data = [] #data new
    old_data = [] #student on database
    update_data = [] #data update
    head = ["รหัสนักศึกษา","ชื่อ-สกุล","เทอม","ปีการศึกษา","เครดิตที่ได้รับ", "เครดิตที่ลงทะเบียน", "เครดิตที่ผ่านทั้งหมด", "คะแนนรวม", "เกรดเฉลี่ยรวม", "เกรดเฉลี่ย", "สถานะ"]
    for x in data:
        list_status = [x.student_id, x.academic_semester, x.academic_year]
        list_data.append(list_status)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        new_data.append(column)
        for x in list_data:
            if column[0] == x[0] and column[2] == str(x[1]) and column[3] == str(x[2]):
                old = Grade.objects.get(student_id=x[0], academic_semester=x[1], academic_year=x[2])
                list_old = [old.student_id,old.student_name_surname,old.academic_semester,old.academic_year,old.creditsatisfy,old.creditpoint,old.ix_count,old.gradepoint,old.s_gpa,old.s_gpax,old.s_status]
                old_data.append(list_old)
                update_data.append(column)
                new_data.remove(column)
                break

    return render(request, 'academicis_app/page_showData.html',{'new': new_data, 'up': len(update_data),'files':file, 'header':head, 'data':zip(old_data,update_data), 'nameTable': "Grade"})

def confirm_uploadGrade(request):
    if request.method == 'POST':
        data = request.POST.getlist('check')
        choice = request.POST.get("choice", None)
        files = request.POST.get("fileDB", None)
    item = 0
    if 'confirm' in choice:
        io_string = io.StringIO(files)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            for x in data:
                if column[10] == "N" or column[10] == "W" or column[10] == "W1" or column[10] == "W2" or column[10] == "P" or column[10] == "A":
                    pass
                else:
                    messages.error(request, "นักศึกษารหัส " + column[0] + " สถานะไม่ถูกต้อง") 
                    return redirect('/academicis/uploadfile')

                if column[0] == eval(x)[0] and column[2] == eval(x)[2] and column[3] == eval(x)[3]:
                    _, created = Grade.objects.update_or_create(
                        student_id = column[0],
                        academic_semester = column[2],
                        academic_year = column[3],
                        defaults = {
                        'student_name_surname' : column[1],
                        'creditsatisfy' : column[4],
                        'creditpoint' : column[5],
                        'ix_count' : column[6],
                        'gradepoint' : column[7],
                        's_gpa' : column[8],
                        's_gpax' : column[9],
                        's_status' : column[10],
                        }
                    )
                    item += 1
        messages.success(request, "อัพโหลดไฟล์เข้าตาราง \"Grade\" สำเร็จ " + str(item) + " รายการ")
        process_data(files)
        tz = pytz.timezone('Asia/Bangkok')
        date = datetime.datetime.now(tz=tz)
        History.objects.create(time=date.strftime("%d/%m/") + str(date.year+543) + " " + date.strftime("%H:%M"), name=request.user.username, activity="อัพโหลดไฟล์ข้อมูล GPA ของนักศึกษา")
    elif 'cancel' in choice:
        return redirect('/academicis/uploadfile')
    return render(request, 'academicis_app/page_uploadfinished.html')

# def data_status(request, file):
#     data = Status.objects.all()
#     if request.method == "GET":
#         return render(request, 'academicis_app/page_showData.html')
#     io_string = io.StringIO(file)
#     next(io_string)
#     list_data = [] #only ID student
#     new_data = [] #data new
#     old_data = [] #student on database
#     update_data = [] #data update
#     head = ["รหัสนักศึกษา","ชื่อ-สกุล","เทอม","ปีการศึกษา","สถานะ","เกรด"]
#     for x in data:
#         list_status = [x.student_id, x.semester, x.academic_year]
#         list_data.append(list_status)
#     for column in csv.reader(io_string, delimiter=',', quotechar="|"):
#         new_data.append(column)
#         for x in list_data:
#             if column[0] == x[0] and column[2] == str(x[1]) and column[3] == str(x[2]):
#                 old = Status.objects.get(student_id=x[0], semester=x[1], academic_year=x[2])
#                 list_old = [old.student_id,old.student_name_surname,old.semester,old.academic_year,old.status,old.grade]
#                 old_data.append(list_old)
#                 update_data.append(column)
#                 new_data.remove(column)
#                 break

#     return render(request, 'academicis_app/page_showData.html',{'new': new_data, 'up': len(update_data),'files':file, 'header':head, 'data':zip(old_data,update_data), 'nameTable': "Status"})

# def confirm_uploadStatus(request):
#     if request.method == 'POST':
#         data = request.POST.getlist('check')
#         choice = request.POST.get("choice", None)
#         files = request.POST.get("fileDB", None)
#     item = 0
#     if 'confirm' in choice:
#         io_string = io.StringIO(files)
#         next(io_string)
#         for column in csv.reader(io_string, delimiter=',', quotechar="|"):
#             for x in data:
#                 if column[0] == eval(x)[0] and column[2] == eval(x)[2] and column[3] == eval(x)[3]:
#                     _, created = Status.objects.update_or_create(
#                         student_id = column[0],
#                         semester = column[2],
#                         academic_year = column[3],
#                         defaults = {
#                         'student_name_surname' : column[1],
#                         'status' : column[4],
#                         'grade' : column[5],
#                         }
#                     )
#                     item += 1
#         messages.success(request, "อัพโหลดไฟล์เข้าตาราง \"Status\" สำเร็จ " + str(item) + " รายการ")
#     elif 'cancel' in choice:
#         return redirect('/academicis/uploadfile')
#     return render(request, 'academicis_app/page_uploadfinished.html')

def data_state(request, file):
    data = State_Inactive.objects.all()
    if request.method == "GET":
        return render(request, 'academicis_app/page_showData.html')
    io_string = io.StringIO(file)
    next(io_string)
    list_data = [] #only ID student
    new_data = [] #data new
    old_data = [] #student on database
    update_data = [] #data update
    head = ["รหัสนักศึกษา","ชื่อ-สกุล","สถานภาพทางการศึกษา","เกรด"]
    for x in data:
        list_data.append(x.student_id)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        new_data.append(column)
        for x in list_data:
            if column[0] == x:
                old = State_Inactive.objects.get(student_id=x)
                list_old = [old.student_id,old.student_name_surname,old.state_not_normal,old.grade]
                old_data.append(list_old)
                update_data.append(column)
                new_data.remove(column)
                break

    return render(request, 'academicis_app/page_showData.html',{'new': new_data, 'up': len(update_data),'files':file, 'header':head, 'data':zip(old_data,update_data), 'nameTable': "State"})

def confirm_uploadState(request):
    if request.method == 'POST':
        data = request.POST.getlist('check')
        choice = request.POST.get("choice", None)
        files = request.POST.get("fileDB", None)
    item = 0
    if 'confirm' in choice:
        io_string = io.StringIO(files)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            for x in data:
                if column[0] == eval(x)[0]:
                    _, created = State_Inactive.objects.update_or_create(
                        student_id = column[0],
                        defaults = {
                        'student_name_surname' : column[1],
                        'state_not_normal' : column[2],
                        'grade' : column[3],
                        }
                    )
                    item += 1
        messages.success(request, "อัพโหลดไฟล์เข้าตาราง \"State\" สำเร็จ " + str(item) + " รายการ")
        student_Inactive()
        tz = pytz.timezone('Asia/Bangkok')
        date = datetime.datetime.now(tz=tz)
        History.objects.create(time=date.strftime("%d/%m/") + str(date.year+543) + " " + date.strftime("%H:%M"), name=request.user.username, activity="อัพโหลดไฟล์นักศึกษาสถานะไม่ปกติ")
    elif 'cancel' in choice:
        return redirect('/academicis/uploadfile')
    return render(request, 'academicis_app/page_uploadfinished.html')

def data_course(request, file):
    data = Course_Usage.objects.all()
    if request.method == "GET":
        return render(request, 'academicis_app/page_showData.html')
    io_string = io.StringIO(file)
    next(io_string)
    list_data = [] #only ID student
    new_data = [] #data new
    old_data = [] #student on database
    update_data = [] #data update
    head = ["หลักสูตรปรับปรุง พ.ศ.","ระยะเวลาที่ใช้","รหัสวิชา","ชื่อวิชา","ประเภทวิชา"]
    for x in data:
        list_status = [x.curriculum, x.course_id]
        list_data.append(list_status)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        new_data.append(column)
        for x in list_data:
            if column[0] == str(x[0]) and column[2] == x[1]:
                old = Course_Usage.objects.get(curriculum=x[0], course_id=x[1])
                list_old = [old.curriculum,old.period,old.course_id,old.course_name,old.elective_or_mandatory]
                old_data.append(list_old)
                update_data.append(column)
                new_data.remove(column)
                break

    return render(request, 'academicis_app/page_showData.html',{'new': new_data, 'up': len(update_data),'files':file, 'header':head, 'data':zip(old_data,update_data), 'nameTable': "Course"})

def confirm_uploadCourse(request):
    if request.method == 'POST':
        data = request.POST.getlist('check')
        choice = request.POST.get("choice", None)
        files = request.POST.get("fileDB", None)
    item = 0
    if 'confirm' in choice:
        io_string = io.StringIO(files)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            for x in data:
                if column[4] == "วิชาบังคับ C" or column[4] == "วิชาเลือก" or column[4] == "วิชาบังคับร่วม" or column[4] == "วิชาบังคับเอก":
                    pass
                else:
                    messages.error(request, "หลักสูตรปรับปรง พ.ศ. " + column[0] + " รหัสวิชา " + column[2] + " ประเภทวิชาไม่ถูกต้อง") 
                    return redirect('/academicis/uploadfile')

                if column[0] == eval(x)[0] and column[2] == eval(x)[2]:
                    _, created = Course_Usage.objects.update_or_create(
                        curriculum = column[0],
                        period = column[1],
                        course_id = column[2],
                        defaults = {
                        'course_name' : column[3],
                        'elective_or_mandatory' : column[4],
                        }
                    )
                    item += 1
        messages.success(request, "อัพโหลดไฟล์เข้าตาราง \"Course\" สำเร็จ " + str(item) + " รายการ")
        create_requiredC()
        tz = pytz.timezone('Asia/Bangkok')
        date = datetime.datetime.now(tz=tz)
        History.objects.create(time=date.strftime("%d/%m/") + str(date.year+543) + " " + date.strftime("%H:%M"), name=request.user.username, activity="อัพโหลดไฟล์รายวิชา")
    elif 'cancel' in choice:
        return redirect('/academicis/uploadfile')
    return render(request, 'academicis_app/page_uploadfinished.html')

def data_appType(request, file):
    data = ApplicantType.objects.all()
    if request.method == "GET":
        return render(request, 'academicis_app/page_showData.html')
    io_string = io.StringIO(file)
    next(io_string)
    list_data = [] #only ID student
    new_data = [] #data new
    old_data = [] #student on database
    update_data = [] #data update
    head = ["รหัสช่องทางการเข้าศึกษา","ชื่อช่องทางการเข้าศึกษา"]
    for x in data:
        list_status = [x.type_id]
        list_data.append(list_status)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        new_data.append(column)
        for x in list_data:
            if column[0] == str(x[0]):
                old = ApplicantType.objects.get(type_id=x[0])
                list_old = [old.type_id,old.name]
                old_data.append(list_old)
                update_data.append(column)
                new_data.remove(column)
                break

    return render(request, 'academicis_app/page_showData.html',{'new': new_data, 'up': len(update_data),'files':file, 'header':head, 'data':zip(old_data,update_data), 'nameTable': "Applicant Type"})

def confirm_uploadAppType(request):
    if request.method == 'POST':
        data = request.POST.getlist('check')
        choice = request.POST.get("choice", None)
        files = request.POST.get("fileDB", None)
    item = 0
    if 'confirm' in choice:
        io_string = io.StringIO(files)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            for x in data:

                if column[0] == eval(x)[0] and column[1] == eval(x)[1]:
                    _, created = ApplicantType.objects.update_or_create(
                        type_id = column[0],
                        defaults = {
                        'name' : column[1],
                        }
                    )
                    item += 1
        messages.success(request, "อัพโหลดไฟล์เข้าตาราง \"Applicant Type\" สำเร็จ " + str(item) + " รายการ")
        tz = pytz.timezone('Asia/Bangkok')
        date = datetime.datetime.now(tz=tz)
        History.objects.create(time=date.strftime("%d/%m/") + str(date.year+543) + " " + date.strftime("%H:%M"), name=request.user.username, activity="อัพโหลดไฟล์รายชื่อช่องทางการเข้าศึกษา")
    elif 'cancel' in choice:
        return redirect('/academicis/uploadfile')
    return render(request, 'academicis_app/page_uploadfinished.html')

def data_plan(request, file):
    data = Applicant_Plan.objects.all()
    if request.method == "GET":
        return render(request, 'academicis_app/page_showData.html')
    io_string = io.StringIO(file)
    next(io_string)
    list_data = [] #only ID student
    new_data = [] #data new
    old_data = [] #student on database
    update_data = [] #data update
    head = ["ปีการศึกษา","โครงการ","แผนรับ TCAS รอบ 1","แผนรับ TCAS รอบ 2","แผนรับ TCAS รอบ 3","แผนรับ TCAS รอบ 4","แผนรับ TCAS รอบ 5"]
    for x in data:
        list_status = [x.year, x.major]
        list_data.append(list_status)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        new_data.append(column)
        for x in list_data:
            if column[0] == str(x[0]) and column[1] == x[1]:
                old = Applicant_Plan.objects.get(year=x[0], major=x[1])
                list_old = [old.year,old.major,old.t1_plan,old.t2_plan,old.t3_plan,old.t5_plan]
                old_data.append(list_old)
                update_data.append(column)
                new_data.remove(column)
                break

    return render(request, 'academicis_app/page_showData.html',{'new': new_data, 'up': len(update_data),'files':file, 'header':head, 'data':zip(old_data,update_data), 'nameTable': "Plan"})

def confirm_uploadPlan(request):
    if request.method == 'POST':
        data = request.POST.getlist('check')
        choice = request.POST.get("choice", None)
        files = request.POST.get("fileDB", None)
    item = 0
    if 'confirm' in choice:
        io_string = io.StringIO(files)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            for x in data:
                if column[0] == eval(x)[0] and column[1] == eval(x)[1]:
                    if column[1] == "CSTU-Reg\xa0RS":
                        column[1] = "CSTU-Reg RS"
                    elif column[1] == "CSTU-Spe\xa0RS":
                        column[1] = "CSTU-Spe RS"
                    elif column[1] == "CSTU-Reg\xa0LP":
                        column[1] = "CSTU-Reg LP"

                    tcas = int(column[2]) + int(column[3]) + int(column[4]) + int(column[5]) + int(column[6])

                    _, created = Applicant_Plan.objects.update_or_create(
                        year = column[0],
                        major = column[1],
                        defaults = {
                        'plan' : tcas,
                        't1_plan' : column[2],
                        't2_plan' : column[3],
                        't3_plan' : column[4],
                        't4_plan' : column[5],
                        't5_plan' : column[6],
                        }
                    )
                    item += 1
        messages.success(request, "อัพโหลดไฟล์เข้าตาราง \"Plan\" สำเร็จ " + str(item) + " รายการ")
        process_plan()
        tz = pytz.timezone('Asia/Bangkok')
        date = datetime.datetime.now(tz=tz)
        History.objects.create(time=date.strftime("%d/%m/") + str(date.year+543) + " " + date.strftime("%H:%M"), name=request.user.username, activity="อัพโหลดไฟล์แผนการรับเข้านักศึกษา")
    elif 'cancel' in choice:
        return redirect('/academicis/uploadfile')
    return render(request, 'academicis_app/page_uploadfinished.html')

def create_student(request):
    if request.method == "POST":
        form = PersonCreationForm(request.POST)
            
        if form.is_valid():
            type_id = 0
            data = Student.objects.all()

            for x in data:
                if form.cleaned_data.get('student_id') == x.student_id:
                    messages.error(request, "มีข้อมูลแล้ว")
                    return redirect('/academicis/createStudent')
            
            obj = ApplicantType.objects.get(name=str(form.cleaned_data.get('applicanttype_name')))
            if form.cleaned_data.get('level') == "ปริญญาตรี โครงการปกติ" and (obj.type_id == 65 or obj.type_id == 6561 or obj.type_id == 650901 or obj.type_id == 6101 or obj.type_id == 70):
                messages.error(request, "ช่องทางการเข้าศึกษาผิดพลาด")
                return redirect('/academicis/createStudent')
            elif form.cleaned_data.get('level') == "ปริญญาตรี โครงการพิเศษ" and (obj.type_id == 61 or obj.type_id == 68 or obj.type_id == 6801 or obj.type_id == 6101 or obj.type_id == 70):
                messages.error(request, "ช่องทางการเข้าศึกษาผิดพลาด")
                return redirect('/academicis/createStudent')
            elif form.cleaned_data.get('level') == "ปริญญาตรี โครงการปกติ ศูนย์ลำปาง" and (obj.type_id == 61 or obj.type_id == 68 or obj.type_id == 6801 or obj.type_id == 65 or obj.type_id == 6561 or obj.type_id == 650901):
                messages.error(request, "ช่องทางการเข้าศึกษาผิดพลาด")
                return redirect('/academicis/createStudent')

            temp = form.cleaned_data.get('student_id')[0:2]
            y = 2500
            y = y + int(temp)
            # print(y)
            if int(form.cleaned_data.get('admitacad_year')) != y:
                messages.error(request, "ปีที่เข้าศึกษาผิดพลาด")
                return redirect('/academicis/createStudent')

            Student.objects.create(
                student_id = form.cleaned_data.get('student_id'),
                student_name_surname = form.cleaned_data.get('student_name_surname'),
                level = form.cleaned_data.get('level'),
                admitacad_year = form.cleaned_data.get('admitacad_year'),
                applicanttype_id = obj.type_id,
                applicanttype_name = form.cleaned_data.get('applicanttype_name'),
                applicanttype_name_morespecific = form.cleaned_data.get('applicanttype_name_morespecific'),
                student_highschool_study_plan = form.cleaned_data.get('student_highschool_study_plan'),
                student_highschool = form.cleaned_data.get('student_highschool'),
                student_highschool_gpa = form.cleaned_data.get('student_highschool_gpa')
            )
            process_basic()
            process_plan()
            tz = pytz.timezone('Asia/Bangkok')
            date = datetime.datetime.now(tz=tz)
            History.objects.create(time=date.strftime("%d/%m/") + str(date.year+543) + " " + date.strftime("%H:%M"), name=request.user.username, activity="เพิ่มข้อมูลนักศึกษา รหัส "+ form.cleaned_data.get('student_id'))
    else:
        form = PersonCreationForm()
    
    return render(request, 'academicis_app/page_createStudent.html', {'form': form})

def create_courseUsage(request):
    if request.method == "POST":
        form = CourseUsageForm(request.POST)
        if form.is_valid():
            data = Course_Usage.objects.all()
            period = 0
            for x in data:
                if form.cleaned_data.get('curriculum') == x.curriculum and form.cleaned_data.get('course_id') == x.course_id:
                    messages.error(request, "มีข้อมูลแล้ว")
                    return redirect('/academicis/createCourseUsage')
                if form.cleaned_data.get('curriculum') == x.curriculum:
                    period = x.period
                    break

            form.save()
            Course_Usage.objects.filter(curriculum=form.cleaned_data.get('curriculum'),course_id=form.cleaned_data.get('course_id')).update(period=period)
            tz = pytz.timezone('Asia/Bangkok')
            date = datetime.datetime.now(tz=tz)
            History.objects.create(time=date.strftime("%d/%m/") + str(date.year+543) + " " + date.strftime("%H:%M"), name=request.user.username, activity="เพิ่มข้อมูลรายวิชา หลักสูตรปรับปรุง พ.ศ. "+ str(form.cleaned_data.get('curriculum')) + " รหัสวิชา " + form.cleaned_data.get('course_id'))
    else:
        form = CourseUsageForm()
    
    return render(request, 'academicis_app/page_createCourseUsage.html', {'form': form})    

def create_appType(request):
    if request.method == "POST":
        form = SubApplicantTypeForm(request.POST)
        if form.is_valid():
            form.save()
            tz = pytz.timezone('Asia/Bangkok')
            date = datetime.datetime.now(tz=tz)
            History.objects.create(time=date.strftime("%d/%m/") + str(date.year+543) + " " + date.strftime("%H:%M"), name=request.user.username, activity="เพิ่มข้อมูลช่องทางการเข้าศึกษาของ \""+ str(form.cleaned_data.get('applicant')) + "\" : " + form.cleaned_data.get('name'))
    else:
        form = SubApplicantTypeForm()
    return render(request, 'academicis_app/page_createSubAppType.html', {'form': form})

def search_student(request):
    if request.method == "POST":
        kw = request.POST.get('name', '')
        form = SearchForm(request.POST, initial={'name':kw})
    else:
        kw = request.GET.get('name', '')
        form = SearchForm(initial={'name':kw})

    data = Student.objects.filter(Q(student_id__contains=kw) | Q(student_name_surname__contains=kw))
    return render(request, 'academicis_app/page_editStudent.html', {'form':form, 'data':data})

def update_student(request, id):
    if request.method == "POST":
        row = Student.objects.get(id=id)
        form = StudentEditForm(instance=row, data = request.POST)

        if form.is_valid(): 
            form.save()
            edit_name = form.cleaned_data.get('student_name_surname')
            try:
                Grade.objects.filter(student_id = form.cleaned_data.get('student_id')).update(student_name_surname = edit_name,)
                State_Inactive.objects.filter(student_id = form.cleaned_data.get('student_id')).update(student_name_surname = edit_name,)
                Data.objects.filter(student_id = form.cleaned_data.get('student_id')).update(student_name_surname = edit_name,)
                tz = pytz.timezone('Asia/Bangkok')
                date = datetime.datetime.now(tz=tz)
                History.objects.create(time=date.strftime("%d/%m/") + str(date.year+543) + " " + date.strftime("%H:%M"), name=request.user.username, activity="แก้ไขข้อมูลนักศึกษา รหัส "+ form.cleaned_data.get('student_id'))
            except ObjectDoesNotExist: 
                pass
            
    else:
        row = Student.objects.filter(id=id).values()
        form = StudentEditForm(initial=row[0])
    return render(request, 'academicis_app/page_updateData.html', {'form':form, 'type': "student"})

def search_enrollment(request):
    if request.method == "POST":
        kw = request.POST.get('id_stu', '')
        form = SearchForm(request.POST, initial={'id_stu':kw})
    else:
        kw = request.GET.get('id_stu', '')
        form = SearchForm(initial={'id_stu':kw})

    data = Enrollment.objects.filter(Q(student_id__contains=kw))
    return render(request, 'academicis_app/page_editEnrollment.html', {'form':form, 'data':data})

def update_enrollment(request, id):
    if request.method == "POST":
        row = Enrollment.objects.get(id=id)
        form = EnrollmentEditForm(instance=row, data = request.POST)

        if form.is_valid():
            form.save()
            course = Course_Usage.objects.all()
            create_requiredC()
            x = 0
            while (x < len(course)):
                if form.cleaned_data.get('course_id') == course[x].course_id and course[x].elective_or_mandatory == 'วิชาบังคับ C' and (form.cleaned_data.get('grade') == "D+" or form.cleaned_data.get('grade') == "D" or form.cleaned_data.get('grade') == "F" or form.cleaned_data.get('grade') == "W"):
                    Required_C.objects.update_or_create(student_id = form.cleaned_data.get('student_id'), admitacad_year = form.cleaned_data.get('admitacad_year'), course_id = form.cleaned_data.get('course_id'), defaults={'academic_year' : form.cleaned_data.get('academic_year'), 'grade' : form.cleaned_data.get('grade')},)
                    break
                elif form.cleaned_data.get('course_id') == course[x].course_id and course[x].elective_or_mandatory == 'วิชาบังคับ C' and (form.cleaned_data.get('grade') == "A" or form.cleaned_data.get('grade') == "B+" or form.cleaned_data.get('grade') == "B" or form.cleaned_data.get('grade') == "C+" or form.cleaned_data.get('grade') == "C"):
                    Required_C.objects.filter(student_id = form.cleaned_data.get('student_id'), course_id = form.cleaned_data.get('course_id')).delete()
                    break
                elif form.cleaned_data.get('course_id') == "CS300" and (form.cleaned_data.get('grade') == "U" or form.cleaned_data.get('grade') == "W"):
                    Required_C.objects.update_or_create(student_id = form.cleaned_data.get('student_id'), admitacad_year = form.cleaned_data.get('admitacad_year'), course_id = form.cleaned_data.get('course_id'), defaults={'academic_year' : form.cleaned_data.get('academic_year'), 'grade' : form.cleaned_data.get('grade')},)
                    break
                elif form.cleaned_data.get('course_id') == "CS300" and (form.cleaned_data.get('grade') == "S"):
                    Required_C.objects.filter(student_id = form.cleaned_data.get('student_id'), course_id = form.cleaned_data.get('course_id')).delete()
                    break
                x += 1

            tz = pytz.timezone('Asia/Bangkok')
            date = datetime.datetime.now(tz=tz)
            History.objects.create(time=date.strftime("%d/%m/") + str(date.year+543) + " " + date.strftime("%H:%M"), name=request.user.username, activity="แก้ไขข้อมูลการลงทะเบียน & ผลการศึกษาของนักศึกษา รหัส "+ form.cleaned_data.get('student_id'))
    else:
        row = Enrollment.objects.filter(id=id).values()
        form = EnrollmentEditForm(initial=row[0])
    return render(request, 'academicis_app/page_updateData.html', {'form':form, 'type': "enrollment"})

def search_grade(request):
    if request.method == "POST":
        kw = request.POST.get('name', '')
        form = SearchForm(request.POST, initial={'name':kw})
    else:
        kw = request.GET.get('name', '')
        form = SearchForm(initial={'name':kw})

    data = Grade.objects.filter(Q(student_id__contains=kw) | Q(student_name_surname__contains=kw))
    return render(request, 'academicis_app/page_editGrade.html', {'form':form, 'data':data})

def update_grade(request, id):
    if request.method == "POST":
        row = Grade.objects.get(id=id)
        form = GradeEditForm(instance=row, data = request.POST)

        if form.is_valid():
            form.save()
            Data.objects.filter(student_id = form.cleaned_data.get('student_id'), academic_semester = form.cleaned_data.get('academic_semester'), academic_year = form.cleaned_data.get('academic_year')).update(grade = form.cleaned_data.get('s_gpax'), status = form.cleaned_data.get('s_status'))
            tz = pytz.timezone('Asia/Bangkok')
            date = datetime.datetime.now(tz=tz)
            History.objects.create(time=date.strftime("%d/%m/") + str(date.year+543) + " " + date.strftime("%H:%M"), name=request.user.username, activity="แก้ไขข้อมูล GPA ของนักศึกษา รหัส "+ form.cleaned_data.get('student_id'))
    else:
        row = Grade.objects.filter(id=id).values()
        form = GradeEditForm(initial=row[0])
    return render(request, 'academicis_app/page_updateData.html', {'form':form, 'type': "grade"})

def search_state(request):
    if request.method == "POST":
        kw = request.POST.get('name', '')
        form = SearchForm(request.POST, initial={'name':kw})
    else:
        kw = request.GET.get('name', '')
        form = SearchForm(initial={'name':kw})

    data = State_Inactive.objects.filter(Q(student_id__contains=kw) | Q(student_name_surname__contains=kw))
    return render(request, 'academicis_app/page_editState.html', {'form':form, 'data':data})

def update_state(request, id):
    if request.method == "POST":
        row = State_Inactive.objects.get(id=id)
        form = StateEditForm(instance=row, data = request.POST)

        if form.is_valid():
            form.save()
            Data.objects.filter(student_id = form.cleaned_data.get('student_id')).update(grade= form.cleaned_data.get('grade'), status= form.cleaned_data.get('state_not_normal'), state= "Inactive")
            tz = pytz.timezone('Asia/Bangkok')
            date = datetime.datetime.now(tz=tz)
            History.objects.create(time=date.strftime("%d/%m/") + str(date.year+543) + " " + date.strftime("%H:%M"), name=request.user.username, activity="แก้ไขข้อมูลสถานะไม่ปกติของนักศึกษา รหัส "+ form.cleaned_data.get('student_id'))
    else:
        row = State_Inactive.objects.filter(id=id).values()
        form = StateEditForm(initial=row[0])
    return render(request, 'academicis_app/page_updateData.html', {'form':form, 'type': "state"})

def search_courseUsage(request):
    if request.method == "POST":
        kw = request.POST.get('curri', '')
        form = SearchForm(request.POST, initial={'curri':kw})
    else:
        kw = request.GET.get('curri', '')
        form = SearchForm(initial={'curri':kw})

    data = Course_Usage.objects.filter(Q(curriculum__contains=kw)).order_by('curriculum')
    return render(request, 'academicis_app/page_editCourseUsage.html', {'form':form, 'data':data})

def update_courseUsage(request, id):
    if request.method == "POST":
        row = Course_Usage.objects.get(id=id)
        form = CourseUsageEditForm(instance=row, data = request.POST)

        if form.is_valid():
            form.save()
            create_requiredC()
            tz = pytz.timezone('Asia/Bangkok')
            date = datetime.datetime.now(tz=tz)
            History.objects.create(time=date.strftime("%d/%m/") + str(date.year+543) + " " + date.strftime("%H:%M"), name=request.user.username, activity="แก้ไขข้อมูลรายวิชา หลักสูตรปรับปรุง พ.ศ. "+ str(form.cleaned_data.get('curriculum')) + " รหัสวิชา " + form.cleaned_data.get('course_id'))
    else:
        row = Course_Usage.objects.filter(id=id).values()
        form = CourseUsageEditForm(initial=row[0])
    return render(request, 'academicis_app/page_updateData.html', {'form':form, 'type': "course"})

def search_appType(request):
    if request.method == "POST":
        kw = request.POST.get('app_type', '')
        form = SearchForm(request.POST, initial={'app_type':kw})
    else:
        kw = request.GET.get('app_type', '')
        form = SearchForm(initial={'app_type':kw})
    data = SubApplicantType.objects.filter(Q(applicant__name__contains=kw)).order_by('applicant')
    return render(request, 'academicis_app/page_editSubApptype.html', {'form':form, 'data':data})

def update_appType(request, id):
    
    if request.method == "POST":
        row = SubApplicantType.objects.get(id=id)
        form = SubApplicantTypeEditForm(instance=row, data = request.POST)
        
        if form.is_valid():
            form.save()
            tz = pytz.timezone('Asia/Bangkok')
            date = datetime.datetime.now(tz=tz)
            History.objects.create(time=date.strftime("%d/%m/") + str(date.year+543) + " " + date.strftime("%H:%M"), name=request.user.username, activity="แก้ไขข้อมูลช่องทางการรับเข้าของ "+ str(form.cleaned_data.get('applicant')))
            
    else:
        row = SubApplicantType.objects.filter(id=id).values()
        form = SubApplicantTypeEditForm(initial=row[0])
    return render(request, 'academicis_app/page_updateData.html', {'form':form, 'type': "appType"})

def search_plan(request):
    if request.method == "POST":
        kw = request.POST.get('year', '')
        form = SearchForm(request.POST, initial={'year':kw})
    else:
        kw = request.GET.get('year', '')
        form = SearchForm(initial={'year':kw})
    data = Applicant_Plan.objects.filter(Q(year__contains=kw)).order_by('year')
    return render(request, 'academicis_app/page_editPlan.html', {'form':form, 'data':data})

def update_plan(request, id):
    if request.method == "POST":
        row = Applicant_Plan.objects.get(id=id)
        form = PlanEditForm(instance=row, data = request.POST)

        if form.is_valid():
            form.save()
            edit_plan = int(form.cleaned_data.get('t1_plan')) + int(form.cleaned_data.get('t2_plan')) + int(form.cleaned_data.get('t3_plan')) + int(form.cleaned_data.get('t4_plan') + int(form.cleaned_data.get('t5_plan')))
            # obj = Applicant_Plan.objects.get(id=id)
            # obj.plan = edit_plan
            # obj.save()
            Applicant_Plan.objects.filter(id=id).update(plan=edit_plan)
            tz = pytz.timezone('Asia/Bangkok')
            date = datetime.datetime.now(tz=tz)
            History.objects.create(time=date.strftime("%d/%m/") + str(date.year+543) + " " + date.strftime("%H:%M"), name=request.user.username, activity="แก้ไขข้อมูลแผนการรับเข้านักศึกษา ปีการศึกษา "+ str(form.cleaned_data.get('year')) + " หลักสูตร " + form.cleaned_data.get('major'))
            
    else:
        row = Applicant_Plan.objects.filter(id=id).values()
        form = PlanEditForm(initial=row[0])
    return render(request, 'academicis_app/page_updateData.html', {'form':form, 'type': "plan"})

def process_plan():
    
    data = Student.objects.all()
    x = 0
    count = 0
    tcas_count = 0
    t1_count = 0
    t2_count = 0
    t3_count = 0
    t4_count = 0
    t5_count = 0

    while(x < len(data)):


        ad_type = data[x].applicanttype_name_morespecific
        ad_year = int(data[x].admitacad_year)

        # Applicant_Plan.objects.filter(year = ad_year, major="CSTU-Reg RS").update(actual = tcas_count, t1_actual = t1_count, t2_actual = t2_count, t3_actual = t3_count, t4_actual = t4_count, all_actual = count)
        # Applicant_Plan.objects.filter(year = ad_year, major="CSTU-Spe RS").update(actual = tcas_count, t1_actual = t1_count, t2_actual = t2_count, t3_actual = t3_count, t4_actual = t4_count, all_actual = count)
        # Applicant_Plan.objects.filter(year = ad_year, major="CSTU-Reg LP").update(actual = tcas_count, t1_actual = t1_count, t2_actual = t2_count, t3_actual = t3_count, t4_actual = t4_count, all_actual = count)

        if (data[x].level == "ปริญญาตรี โครงการปกติ"):
            count = Student.objects.filter(admitacad_year = data[x].admitacad_year,  level = "ปริญญาตรี โครงการปกติ").count()
            tcas_count += Student.objects.filter(admitacad_year = data[x].admitacad_year, applicanttype_id = "61").count()
            tcas_count += Student.objects.filter(admitacad_year = data[x].admitacad_year, applicanttype_id = "6801").count()

            if (ad_type == "TCAS รอบ 1" or ad_type == "Tcas รอบ 1"):
                t1_count =  Student.objects.filter(admitacad_year = data[x].admitacad_year, level = "ปริญญาตรี โครงการปกติ", applicanttype_name_morespecific = ad_type).count()
                Applicant_Plan.objects.filter(year = ad_year, major="CSTU-Reg RS").update(actual = tcas_count, t1_actual = t1_count, all_actual = count)
            elif (ad_type == "TCAS รอบ 2" or ad_type == "Tcas รอบ 2"):
                t2_count =  Student.objects.filter(admitacad_year = data[x].admitacad_year, level = "ปริญญาตรี โครงการปกติ", applicanttype_name_morespecific = ad_type).count()
                Applicant_Plan.objects.filter(year = ad_year, major="CSTU-Reg RS").update(actual = tcas_count, t2_actual = t2_count, all_actual = count)
            elif (ad_type == "TCAS รอบ 3" or ad_type == "Tcas รอบ 3"):
                t3_count =  Student.objects.filter(admitacad_year = data[x].admitacad_year, level = "ปริญญาตรี โครงการปกติ", applicanttype_name_morespecific = ad_type).count()
                Applicant_Plan.objects.filter(year = ad_year, major="CSTU-Reg RS").update(actual = tcas_count, t3_actual = t3_count, all_actual = count)
            elif (ad_type == "TCAS รอบ 4" or ad_type == "Tcas รอบ 4"):
                t4_count =  Student.objects.filter(admitacad_year = data[x].admitacad_year, level = "ปริญญาตรี โครงการปกติ", applicanttype_name_morespecific = ad_type).count()
                Applicant_Plan.objects.filter(year = ad_year, major="CSTU-Reg RS").update(actual = tcas_count, t4_actual = t4_count, all_actual = count)
            elif (ad_type == "TCAS รอบ 5" or ad_type == "Tcas รอบ 5"):
                t5_count =  Student.objects.filter(admitacad_year = data[x].admitacad_year, level = "ปริญญาตรี โครงการปกติ", applicanttype_name_morespecific = ad_type).count()
                Applicant_Plan.objects.filter(year = ad_year, major="CSTU-Reg RS").update(actual = tcas_count, t5_actual = t5_count, all_actual = count)
            else:
                Applicant_Plan.objects.filter(year = ad_year, major="CSTU-Reg RS").update(all_actual = count)
            
        elif (data[x].level == "ปริญญาตรี โครงการพิเศษ"):
            count = Student.objects.filter(admitacad_year = data[x].admitacad_year,  level = "ปริญญาตรี โครงการพิเศษ").count()
            tcas_count += Student.objects.filter(admitacad_year = data[x].admitacad_year, applicanttype_id = "650901").count()
            tcas_count += Student.objects.filter(admitacad_year = data[x].admitacad_year, applicanttype_id = "6561").count()
            if (ad_type == "TCAS รอบ 1" or ad_type == "Tcas รอบ 1"):
                t1_count =  Student.objects.filter(admitacad_year = data[x].admitacad_year, level = "ปริญญาตรี โครงการพิเศษ", applicanttype_name_morespecific = ad_type).count()
                Applicant_Plan.objects.filter(year = ad_year, major="CSTU-Spe RS").update(actual = tcas_count, t1_actual = t1_count, all_actual = count)
            elif (ad_type == "TCAS รอบ 2" or ad_type == "Tcas รอบ 2"):
                t2_count =  Student.objects.filter(admitacad_year = data[x].admitacad_year, level = "ปริญญาตรี โครงการพิเศษ", applicanttype_name_morespecific = ad_type).count()
                Applicant_Plan.objects.filter(year = ad_year, major="CSTU-Spe RS").update(actual = tcas_count, t2_actual = t2_count, all_actual = count)
            elif (ad_type == "TCAS รอบ 3" or ad_type == "Tcas รอบ 3"):
                t3_count =  Student.objects.filter(admitacad_year = data[x].admitacad_year, level = "ปริญญาตรี โครงการพิเศษ", applicanttype_name_morespecific = ad_type).count()
                Applicant_Plan.objects.filter(year = ad_year, major="CSTU-Spe RS").update(actual = tcas_count, t3_actual = t3_count, all_actual = count)
            elif (ad_type == "TCAS รอบ 4" or ad_type == "Tcas รอบ 4"):
                t4_count =  Student.objects.filter(admitacad_year = data[x].admitacad_year, level = "ปริญญาตรี โครงการพิเศษ", applicanttype_name_morespecific = ad_type).count()
                Applicant_Plan.objects.filter(year = ad_year, major="CSTU-Spe RS").update(actual = tcas_count, t4_actual = t4_count, all_actual = count)
            elif (ad_type == "TCAS รอบ 5" or ad_type == "Tcas รอบ 5"):
                t5_count =  Student.objects.filter(admitacad_year = data[x].admitacad_year, level = "ปริญญาตรี โครงการพิเศษ", applicanttype_name_morespecific = ad_type).count()
                Applicant_Plan.objects.filter(year = ad_year, major="CSTU-Spe RS").update(actual = tcas_count, t5_actual = t5_count, all_actual = count)
            else:
                Applicant_Plan.objects.filter(year = ad_year, major="CSTU-Spe RS").update(all_actual = count)

        elif (data[x].level == "ปริญญาตรี โครงการปกติ ศูนย์ลำปาง"):
            count = Student.objects.filter(admitacad_year = data[x].admitacad_year,  level = "ปริญญาตรี โครงการปกติ ศูนย์ลำปาง").count()
            tcas_count += Student.objects.filter(admitacad_year = data[x].admitacad_year, applicanttype_id = "6101").count()
            tcas_count += Student.objects.filter(admitacad_year = data[x].admitacad_year, applicanttype_id = "70").count()
            
            if (ad_type == "TCAS รอบ 1" or ad_type == "Tcas รอบ 1"):
                t1_count =  Student.objects.filter(admitacad_year = data[x].admitacad_year, level = "ปริญญาตรี โครงการปกติ ศูนย์ลำปาง", applicanttype_name_morespecific = ad_type).count()
                Applicant_Plan.objects.filter(year = ad_year, major="CSTU-Reg LP").update(actual = tcas_count, t1_actual = t1_count, all_actual = count)
            elif (ad_type == "TCAS รอบ 2" or ad_type == "Tcas รอบ 2"):
                t2_count =  Student.objects.filter(admitacad_year = data[x].admitacad_year, level = "ปริญญาตรี โครงการปกติ ศูนย์ลำปาง", applicanttype_name_morespecific = ad_type).count()
                Applicant_Plan.objects.filter(year = ad_year, major="CSTU-Reg LP").update(actual = tcas_count, t2_actual = t2_count, all_actual = count)
            elif (ad_type == "TCAS รอบ 3" or ad_type == "Tcas รอบ 3"):
                t3_count =  Student.objects.filter(admitacad_year = data[x].admitacad_year, level = "ปริญญาตรี โครงการปกติ ศูนย์ลำปาง", applicanttype_name_morespecific = ad_type).count()
                Applicant_Plan.objects.filter(year = ad_year, major="CSTU-Reg LP").update(actual = tcas_count, t3_actual = t3_count, all_actual = count)
            elif (ad_type == "TCAS รอบ 4" or ad_type == "Tcas รอบ 4"):
                t4_count =  Student.objects.filter(admitacad_year = data[x].admitacad_year, level = "ปริญญาตรี โครงการปกติ ศูนย์ลำปาง", applicanttype_name_morespecific = ad_type).count()
                Applicant_Plan.objects.filter(year = ad_year, major="CSTU-Reg LP").update(actual = tcas_count, t4_actual = t4_count, all_actual = count)
            elif (ad_type == "TCAS รอบ 5" or ad_type == "Tcas รอบ 5"):
                t5_count =  Student.objects.filter(admitacad_year = data[x].admitacad_year, level = "ปริญญาตรี โครงการปกติ ศูนย์ลำปาง", applicanttype_name_morespecific = ad_type).count()
                Applicant_Plan.objects.filter(year = ad_year, major="CSTU-Reg LP").update(actual = tcas_count, t5_actual = t5_count, all_actual = count)
            else:
                Applicant_Plan.objects.filter(year = ad_year, major="CSTU-Reg LP").update(all_actual = count)


        tcas_count = 0
        x += 1

def process_requiredC(data):
    # data = Enrollment data
    
    course = Course_Usage.objects.all()

    for x in data:
        y = 0
        while (y < len(course)):
            if int(eval(x)[1]) >= course[y].curriculum and int(eval(x)[1]) <= course[y].curriculum + course[y].period - 1:
            # if course[y].curriculum == 2561:
            #     if int(eval(x)[1]) >= 2561:
                if (eval(x)[4] == course[y].course_id and course[y].elective_or_mandatory == 'วิชาบังคับ C' and (eval(x)[6] == "D+" or eval(x)[6] == "D" or eval(x)[6] == "F" or eval(x)[6] == "W")):
                    Required_C.objects.update_or_create(student_id = eval(x)[0], admitacad_year = eval(x)[1], course_id = eval(x)[4], defaults={'academic_year' : eval(x)[2], 'grade' : eval(x)[6]},)
                    break
                elif (eval(x)[4] == course[y].course_id and course[y].elective_or_mandatory == 'วิชาบังคับ C' and (eval(x)[6] == "A" or eval(x)[6] == "B+" or eval(x)[6] == "B" or eval(x)[6] == "C+" or eval(x)[6] == "C")):
                    Required_C.objects.filter(student_id = eval(x)[0], course_id = eval(x)[4]).delete()
                    break

            if (eval(x)[4] == "CS300" and (eval(x)[6] == "U" or eval(x)[6] == "W")):
                Required_C.objects.update_or_create(student_id = eval(x)[0], admitacad_year = eval(x)[1], course_id = eval(x)[4], defaults={'academic_year' : eval(x)[2], 'grade' : eval(x)[6]},)
                break
            else:
                Required_C.objects.filter(student_id = eval(x)[0], course_id = eval(x)[4]).delete()
                break

            if (datetime.datetime.now().year + 543 - int(eval(x)[1]) > 8):
                Required_C.objects.filter(student_id = eval(x)[0]).delete()
            y += 1


def process_basic():
    student = Student.objects.all()
    x = 0
    level = 1
    ad_type = "Admission"
    school_plan = "วิทย์-คณิต"
    major = "CSTU-Reg RS"
    date = datetime.datetime.now()

    while x < len(student):
        school_plan = student[x].student_highschool_study_plan

        if (student[x].admitacad_year < 2561):
            ad_type = "สอบเข้าแบบเก่า"
        else:
            if (student[x].applicanttype_name_morespecific == "TCAS รอบ 1" or student[x].applicanttype_name_morespecific == "TCAS รอบ 2" or student[x].applicanttype_name_morespecific == "TCAS รอบ 3" or student[x].applicanttype_name_morespecific == "TCAS รอบ 4"):
                ad_type = student[x].applicanttype_name_morespecific
            else:
                ad_type = "โครงการอื่นๆ"

        if (date.month >= 7):
            level = (date.year + 543) - student[x].admitacad_year + 1
        else:
            level = (date.year + 543) - student[x].admitacad_year
                
        if (student[x].level == "ปริญญาตรี โครงการปกติ ศูนย์ลำปาง"):
            major = "CSTU-Reg LP"
        elif (student[x].level == "ปริญญาตรี โครงการปกติ"):
            major = "CSTU-Reg RS"
        elif (student[x].level == "ปริญญาตรี โครงการพิเศษ"):
            major = "CSTU-Spe RS"

        if student[x].admitacad_year >= 2561:
            Data.objects.update_or_create(student_id = student[x].student_id, academic_semester =  "1", academic_year = student[x].admitacad_year, defaults={'student_name_surname' : student[x].student_name_surname, 'highschool_plan' : school_plan, 'major' : major, 'applicant_type' : ad_type, 'admit_year': student[x].admitacad_year, 'level' : level, 'grade' : 0.00, 'status' : "Normal", 'state' : "Active"})
            
        x += 1

def process_data(data):
    student = Data.objects.all()
    # grade = Grade.objects.all()
    # x = 0
    student_Inactive()


    io_string = io.StringIO(data)
    next(io_string)
    for column in csv.reader(io_string, delimiter=',', quotechar="|"):
        x = 0
        while (x < len(student)):
            if student[x].student_id == column[0]:
                Data.objects.update_or_create(student_id = student[x].student_id, academic_semester =  column[2], academic_year = column[3], defaults={'student_name_surname' : student[x].student_name_surname, 'highschool_plan' : student[x].highschool_plan, 'major' : student[x].major, 'applicant_type' : student[x].applicant_type, 'admit_year': student[x].admit_year, 'level' : student[x].level, 'grade' : column[8], 'status' : column[10], 'state' : "Active"})
            
            x += 1

    # while x < len(grade):
    #     y = 0
    #     while y < len(student):
    #         if student[y].student_id == grade[x].student_id:
    #             Data.objects.update_or_create(student_id = student[y].student_id, academic_semester =  grade[x].academic_semester, academic_year = grade[x].academic_year, defaults={'student_name_surname' : student[y].student_name_surname, 'highschool_plan' : student[y].highschool_plan, 'major' : student[y].major, 'applicant_type' : student[y].applicant_type, 'admit_year': student[y].admit_year, 'level' : student[y].level, 'grade' : grade[x].s_gpax, 'status' : grade[x].s_status, 'state' : "Active"})
    #         y += 1
        
    #     x += 1

def student_Inactive():
    student = Data.objects.all()
    inactive = State_Inactive.objects.all()
    x = 0
    while x < len(student):
        y = 0
        
        while (y < len(inactive)):
            if (student[x].student_id == inactive[y].student_id):
                Data.objects.filter(student_id = student[x].student_id).update(student_name_surname = student[x].student_name_surname, highschool_plan= student[x].highschool_plan, major= student[x].major, applicant_type= student[x].applicant_type, admit_year= student[x].admit_year, level= student[x].level, academic_semester=  student[x].academic_semester, academic_year= student[x].academic_year, grade= inactive[y].grade, status= inactive[y].state_not_normal, state= "Inactive")
            y += 1
        
        x += 1

def create_requiredC():
    data = Enrollment.objects.all()
    x = 0
    course = Course_Usage.objects.all()
    while (x < len(data)):
        y = 0
        while (y < len(course)):
            if data[x].admitacad_year >= course[y].curriculum and data[x].admitacad_year <= course[y].curriculum + course[y].period - 1:
                if (data[x].course_id == course[y].course_id and course[y].elective_or_mandatory == 'วิชาบังคับ C' and (data[x].grade == "D+" or data[x].grade == "D" or data[x].grade == "F" or data[x].grade == "W")):
                    Required_C.objects.update_or_create(student_id = data[x].student_id, admitacad_year = data[x].admitacad_year, course_id = data[x].course_id, defaults={'academic_year' : data[x].academic_year, 'grade' : data[x].grade},)
                    break
                elif (data[x].course_id == course[y].course_id and course[y].elective_or_mandatory == 'วิชาบังคับ C' and (data[x].grade == "A" or data[x].grade == "B+" or data[x].grade == "B" or data[x].grade == "C+" or data[x].grade == "C")):
                    Required_C.objects.filter(student_id = data[x].student_id, course_id = data[x].course_id).delete()
                    break
                elif (data[x].course_id == course[y].course_id and course[y].elective_or_mandatory == 'วิชาเลือก'):
                    Required_C.objects.filter(student_id = data[x].student_id, course_id = data[x].course_id).delete()
                    break

            if (data[x].course_id == "CS300" and (data[x].grade == "U" or data[x].grade == "W")):
                Required_C.objects.update_or_create(student_id = data[x].student_id, admitacad_year = data[x].admitacad_year, course_id = data[x].course_id, defaults={'academic_year' : data[x].academic_year, 'grade' : data[x].grade},)
                break
            else:
                Required_C.objects.filter(student_id = data[x].student_id, course_id = data[x].course_id).delete()
                break

            if ((datetime.datetime.now().year + 543) - data[x].admitacad_year > 8):
                Required_C.objects.filter(student_id = data[x].student_id).delete()
            y += 1
        
        x += 1






# AJAX
def load_subapptype(request):
    applicanttype_id = request.GET.get('applicanttype_id')
    subapptype = SubApplicantType.objects.filter(applicant_id=applicanttype_id).all()
    return render(request, 'academicis_app/dropdown_list_options.html', {'subapptype': subapptype})
