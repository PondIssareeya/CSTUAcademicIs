from django.db import models
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Column, HTML, Layout, Row, Submit
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator
import re, datetime
from odf import form

# Create your models here.
# class ApplicantType(models.Model):
#     applicanttype_id = models.IntegerField()
#     applicanttype_name = models.CharField(max_length = 255)

#     def __str__(self):
#         return self.applicanttype_name

# class SubApplicantType(models.Model):
#     applicanttype = models.ForeignKey(ApplicantType, on_delete=models.CASCADE)
#     applicanttype_morespecific = models.CharField(max_length = 255)

#     def __str__(self):
#         return self.applicanttype_morespecific

class Student(models.Model):
    student_id = models.CharField(max_length = 255)
    student_name_surname = models.CharField(max_length = 255)
    level = models.CharField(max_length = 255,)
    admitacad_year = models.IntegerField()
    applicanttype_id = models.IntegerField()
    applicanttype_name = models.CharField(max_length = 255,)
    applicanttype_name_morespecific = models.CharField(max_length = 255, blank=True, null=True)
    student_highschool_study_plan = models.CharField(max_length = 50)
    student_highschool = models.CharField(max_length = 255, blank=True, null=True)
    student_highschool_gpa = models.CharField(max_length = 5, blank=True, null=True,)

    def __str__(self):
        return f'{self.level} {self.admitacad_year}'

class Course(models.Model):
    course_id = models.CharField(max_length = 20)
    curriculum = models.IntegerField()
    course_name = models.CharField(max_length = 200)
    course_description = models.CharField(max_length = 1000)
    credit = models.IntegerField()
    lecture_hours = models.IntegerField()
    lab_hours = models.IntegerField()
    selfstudy_hours = models.IntegerField()

    def __str__(self):
        return self.course_name

class Course_Sector_Curriculum(models.Model):
    sector_id = models.IntegerField()
    sector_name = models.CharField(max_length = 100)

    def __str__(self):
        return self.sector_name

class Course_Sector_Tqf(models.Model):
    tqf_no = models.IntegerField()
    tqf_name = models.CharField(max_length = 200)

    def __str__(self):
        return self.tqf_name

class Usage_Type(models.Model):
    usage_type = models.CharField(max_length = 100)
    condition = models.CharField(max_length = 100)

    def __str__(self):
        return self.usage_type

class Major_And_Track(models.Model):
    major_and_track = models.CharField(max_length = 100)

    def __str__(self):
        return self.major_and_track

class Course_Usage(models.Model):
    curriculum = models.IntegerField(default=2561)
    period = models.IntegerField(default=0)
    course_id = models.CharField(max_length = 5,default=None, null = True)
    course_name = models.CharField(max_length = 255,default=None)
    elective_or_mandatory = models.CharField(max_length = 20,)

    # course = models.ForeignKey(Course, null = True, on_delete=models.SET_NULL)
    # major_or_track = models.ForeignKey(Major_And_Track, null = True, on_delete=models.SET_NULL)
    # elective_or_mandatory = models.ForeignKey(Usage_Type, null = True, on_delete=models.SET_NULL)
    # course_sector = models.ForeignKey(Course_Sector_Curriculum, null = True, on_delete=models.SET_NULL)
    # course_tqf = models.ForeignKey(Course_Sector_Tqf, null = True, on_delete=models.SET_NULL)

class Prereq_Type(models.Model):
    description = models.CharField(max_length = 100)

class Prerequsite(models.Model):
    pre_course = models.ForeignKey(Course, related_name='course_precourse', null = True, on_delete=models.SET_NULL)
    post_course = models.ForeignKey(Course, related_name='course_postcourse', null = True, on_delete=models.SET_NULL)
    prerequsite_type = models.ForeignKey(Prereq_Type, null = True, on_delete=models.SET_NULL)
    group = models.IntegerField()

class User(models.Model):
    username = models.CharField(max_length = 100)
    is_student = models.BooleanField()
    is_teacher = models.BooleanField()
    is_staff = models.BooleanField()

class Teacher(models.Model):
    teacher_id = models.ForeignKey(User, null = True, on_delete=models.SET_NULL)
    name = models.CharField(max_length = 50)
    surname = models.CharField(max_length = 50)
    academic_position = models.CharField(max_length = 20)
    education_position = models.CharField(max_length = 20)
    education = models.CharField(max_length = 5000)
    email = models.EmailField()
    campus = models.CharField(max_length = 50)
    status = models.CharField(max_length = 50)
    works = models.CharField(max_length = 5000)

class Entrance_Info(models.Model):
    high_school_curriculum = models.CharField(max_length = 100)
    school = models.CharField(max_length = 200)
    province = models.CharField(max_length = 100)
    educated_year = models.IntegerField()
    gpax = models.FloatField()
    entrance_score = models.FloatField()
    gat = models.FloatField()
    pat1 = models.FloatField()
    pat2 = models.FloatField()
    onet_th = models.FloatField()
    onet_sci = models.FloatField()
    onet_eng = models.FloatField()
    onet_math = models.FloatField()
    onet_soc = models.FloatField()

class Curriculum(models.Model):
    curri = models.IntegerField()

class Title(models.Model):
    title = models.CharField(max_length = 50)

class Grade(models.Model):
    # grade = models.CharField(max_length = 5)
    # grade_value = models.IntegerField()
    student_id = models.CharField(max_length = 255,default=None, null = True)
    student_name_surname = models.CharField(max_length = 255,default=None, null = True)
    academic_semester = models.CharField(max_length = 1,default=None, null = True)
    academic_year = models.IntegerField(default=None, null = True)
    creditsatisfy = models.CharField(max_length = 3,default=None, null = True)
    creditpoint = models.CharField(max_length = 3,default=None, null = True)
    ix_count = models.CharField(max_length = 3,default=None, null = True)
    gradepoint = models.FloatField(default=None, null = True)
    s_gpa = models.FloatField(default=None, null = True)
    s_gpax = models.FloatField(default=None, null = True)
    s_status = models.CharField(max_length = 4,default=None, null = True)

class Enrollment(models.Model):
    # student_id =  models.CharField(max_length = 255)
    # grade = models.CharField(max_length = 5)
    # course_id = models.CharField(max_length = 10)
    # creditsatisfy = models.IntegerField(default=None)
    # semester = models.IntegerField()
    # academic_year = models.IntegerField()
    # admitacad_year = models.CharField(max_length = 4,default=None, null = True)

    student_id =  models.CharField(max_length = 255)
    admitacad_year = models.IntegerField()
    academic_year = models.IntegerField()
    semester = models.IntegerField()
    course_id = models.CharField(max_length = 10)
    creditsatisfy = models.IntegerField()
    grade = models.CharField(max_length = 5)

    def __str__(self):
        return f'{self.student_id}'

class Parent(models.Model):
    title = models.ForeignKey(Title, null = True, on_delete=models.SET_NULL)
    p_name = models.CharField(max_length = 50)
    p_surname = models.CharField(max_length = 50)
    p_relation = models.CharField(max_length = 50)
    p_phone = models.CharField(max_length = 11)
    p_income = models.FloatField()

class Applicant_Type(models.Model):
    curriculum = models.IntegerField()
    # applicant_type_id_2_digit = models.IntegerField()
    applicant_type_id = models.IntegerField()
    applicant_type_name = models.CharField(max_length = 255)
    applicant_type_specific = models.CharField(max_length = 255)

class Applicant_Plan(models.Model):
    year = models.PositiveIntegerField()
    major = models.CharField(
        max_length = 255,
        
    )
    plan = models.PositiveIntegerField()
    actual = models.PositiveIntegerField(default=0, null = True)
    t1_plan = models.PositiveIntegerField()
    t1_actual = models.PositiveIntegerField(default=0, null = True)
    t2_plan = models.PositiveIntegerField()
    t2_actual = models.PositiveIntegerField(default=0, null = True)
    t3_plan = models.PositiveIntegerField()
    t3_actual = models.PositiveIntegerField(default=0, null = True)
    t4_plan = models.PositiveIntegerField()
    t4_actual = models.PositiveIntegerField(default=0, null = True)
    t5_plan = models.PositiveIntegerField(default=0)
    t5_actual = models.PositiveIntegerField(default=0, null = True)
    all_actual = models.PositiveIntegerField(default=0, null = True)

    def __str__(self):
        return f'{self.year}'

class Data_Basic(models.Model):
    student_id =  models.CharField(max_length = 255)
    highschool_plan =  models.CharField(max_length = 20)
    admit_year = models.IntegerField()
    applicant_type = models.CharField(max_length = 255)
    major = models.CharField(max_length = 255)
    level = models.CharField(max_length = 20)
    status = models.CharField(max_length = 20)
    state = models.CharField(max_length = 20)
    grade = models.FloatField()

class Required_C(models.Model):
    student_id = models.CharField(max_length = 255)
    admitacad_year = models.IntegerField()
    academic_year = models.IntegerField()
    course_id = models.CharField(max_length = 10)
    grade = models.CharField(max_length = 5)

class Status(models.Model):
    student_id = models.CharField(max_length = 255)
    student_name_surname = models.CharField(max_length = 255)
    semester = models.IntegerField()
    academic_year = models.IntegerField()
    status = models.CharField(max_length = 20)
    grade = models.FloatField()

class State_Inactive(models.Model):
    student_id = models.CharField(max_length = 255)
    student_name_surname = models.CharField(max_length = 255)
    state_not_normal = models.CharField(max_length = 255)
    grade = models.FloatField()

class Data(models.Model):
    student_id = models.CharField(max_length = 255)
    student_name_surname = models.CharField(max_length = 255)
    highschool_plan =  models.CharField(max_length = 20)
    major = models.CharField(max_length = 255)
    applicant_type = models.CharField(max_length = 255)
    admit_year = models.IntegerField()
    level = models.IntegerField()
    academic_semester = models.CharField(max_length = 1)
    academic_year = models.IntegerField()
    grade = models.FloatField()
    status = models.CharField(max_length = 50)
    state = models.CharField(max_length = 20)

class History(models.Model):
    time = models.CharField(max_length = 30)
    name = models.CharField(max_length = 255)
    activity = models.CharField(max_length = 500)

class StudentForm(forms.ModelForm):
    class Meta:
        # ID_REGEX = RegexValidator(r'^[0-9]{10}$', 'id student 10 char')
        model = Student
        fields = ['student_id','student_name_surname','level','admitacad_year','applicanttype_id','applicanttype_name_morespecific','student_highschool_study_plan','student_highschool','student_highschool_gpa']
        # student_id_validator = RegexValidator(r'^[0-9]{10}$', "no")
        # student_id = models.CharField(validators=[student_id_validator])

        labels = {
            'student_id': 'รหัสนักศึกษา',
            'student_name_surname': 'ชื่อ-สกุล',
            'level': 'โครงการ',
            'admitacad_year': 'ปีที่เข้าศึกษา',
            'applicanttype_id': 'รหัสช่องทาง',
            'applicanttype_name': 'ช่องทาง',
            'applicanttype_name_morespecific': 'เพิ่มเติม',
            'student_highschool_study_plan': 'แผนการเรียน',
            'student_highschool': 'โรงเรียนมัธยมปลาย',
            'student_highschool_gpa' :'เกรดเฉลี่ย',
        }
        
        widgets = {
            'level' : forms.Select(
                choices = [('ปริญญาตรี โครงการปกติ','ปริญญาตรี โครงการปกติ'), ('ปริญญาตรี โครงการพิเศษ','ปริญญาตรี โครงการพิเศษ'), ('ปริญญาตรี โครงการปกติ ศูนย์ลำปาง', 'ปริญญาตรี โครงการปกติ ศูนย์ลำปาง')],
            ),
            'admitacad_year' : forms.TextInput(attrs={'value':datetime.datetime.now().year+543}),
            # 'applicanttype_id' : forms.ModelMultipleChoiceField(queryset=Applicant_Type.objects.all()),
            # forms.Select(
            #     choices = [(61,'61 : Admission ภาคปกติ'), (6801,'6801 : รับตรง ภาคปกติ'), (6561,'6561 : Admission ภาคพิเศษ'), (650901,'650901 : รับตรง ภาคพิเศษ'), (6101,'6101 : Admission ลำปาง'),
            #     (70,'70 : รับตรง ลำปาง'), (4501,'4501 : เรียนดีเมือง'), (50,'50 : ชาวไทยภูเขา'), (51,'51 : มหาดไทย'), (5201,'5201 : เรียนดีชนบท'), (53,'53 : ผู้พิการ'),
            #     (54,'54 : เรียนดีภาคกลาง'), (62,'62 : ดีเด่นการกีฬา'), (66, '66 : โครงการโอลิมปิก')],
            # ),
            # 'applicanttype_name_morespecific' : forms.Select(
            #     choices = [('โครงการของมหาวิทยาลัย','------'), ('TCAS รอบ 1','TCAS รอบ 1'), ('TCAS รอบ 2','TCAS รอบ 2'),('TCAS รอบ 3','TCAS รอบ 3'),('TCAS รอบ 4','TCAS รอบ 4'),],
            # ),
            'student_highschool_study_plan' : forms.Select(
                choices = [('วิทย์-คณิต','วิทย์-คณิต'), ('ศิลป์-คำนวณ','ศิลป์-คำนวณ')],
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        student_field = forms.RegexField(
            label=("รหัสนักศึกษา"), regex=r'^[0-9]{10}$',
            error_messages={
                'invalid': ("กรุณาใส่รหัสนักศึกษา 10 หลัก")
            }
        )
        self.fields['student_id'] = student_field

        grade_field = forms.FloatField(
            label=("เกรดเฉลี่ย"),
            validators=[MinValueValidator(0.00), MaxValueValidator(4.00)], 
            error_messages={
                'min_value': ("กรุณาใส่เกรดระหว่าง 0.00 - 4.00"),
                'max_value': ("กรุณาใส่เกรดระหว่าง 0.00 - 4.00"),
            },
            required = False
            # error_messages={'min_value' or 'max_value' or 'required' or 'invalid': ("กรุณาใส่เกรดระหว่าง 0.00 - 4.00")},
        )

        self.fields['student_highschool_gpa'] = grade_field
        # self.fields['applicanttype_id'] = forms.ModelChoiceField(queryset=Applicant_Type.objects.all())

        # self.fields['applicanttype_id'].choices = list(ApplicantType.objects.values_list('applicanttype_id', 'applicanttype_name'))
        # self.fields['applicanttype_name_morespecific'].queryset = SubApplicantType.objects.none()

        # if 'applicanttype_id' in self.data:
        #     try:
        #         app_id = int(self.data.get('applicanttype_id'))
        #         self.fields['applicanttype_name_morespecific'].queryset = SubApplicantType.objects.filter(applicanttype_id=app_id).order_by('applicanttype_morespecific')
        #     except (ValueError, TypeError):
        #         pass  # invalid input from the client; ignore and fallback to empty City queryset
        # elif self.instance.pk:
        #     self.fields['applicanttype_name_morespecific'].queryset = self.instance.ApplicantType.SubApplicantType_set.order_by('applicanttype_morespecific')

        submit = Submit('submit', 'บันทึก')
        submit.field_classes = "btn btn-outline-success mt-4 col-md-2"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('student_id', css_class = 'form-group col-md-5 mb-0'),
                Column('student_name_surname', css_class = 'form-group col-md-7 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column('level', css_class = 'form-group col-md-8 mb-0'),
                Column('admitacad_year', css_class = 'form-group col-md-4 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column('applicanttype_id', css_class = 'form-group col-md-7 mb-0'),
                # Column('applicanttype_name', css_class = 'form-group col-md-5 mb-0'),
                Column('applicanttype_name_morespecific', css_class = 'form-group col-md-5 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column('student_highschool', css_class = 'form-group col-md-6 mb-0'),
                Column('student_highschool_study_plan', css_class = 'form-group col-md-3 mb-0'),
                Column('student_highschool_gpa', css_class = 'form-group col-md-3 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column(
                    ButtonHolder(
                        submit,
                        HTML(
                            """
                            &nbsp;<button onclick="window.location.href='{{ '/academicis/createStudent' }}'" class="btn btn-outline-danger mt-4 col-md-2" type="button">ยกเลิก</button>
                            """
                    ), css_class='text-center'),
                ),
            ),
        )
    
class StudentEditForm(forms.ModelForm):
    class Meta:
        # ID_REGEX = RegexValidator(r'^[0-9]{10}$', 'id student 10 char')
        model = Student
        fields = '__all__'
        # student_id_validator = RegexValidator(r'^[0-9]{10}$', "no")
        # student_id = models.CharField(validators=[student_id_validator])

        labels = {
            'student_id': 'รหัสนักศึกษา',
            'student_name_surname': 'ชื่อ-สกุล',
            'level': 'โครงการ',
            'admitacad_year': 'ปีที่เข้าศึกษา',
            'applicanttype_id': 'รหัสช่องทาง',
            'applicanttype_name': 'ช่องทาง',
            'applicanttype_name_morespecific': 'เพิ่มเติม',
            'student_highschool_study_plan': 'แผนการเรียน',
            'student_highschool': 'โรงเรียนมัธยมปลาย',
            'student_highschool_gpa' :'เกรดเฉลี่ย',
        }
        
        widgets = {
        #     'level' : forms.Select(),
        #     'admitacad_year' : forms.TextInput(attrs={'value':datetime.datetime.now().year+543}),
        #     'applicanttype_id' : forms.Select(
        #         choices = [(61,'61 : Admission ภาคปกติ'), (6801,'6801 : รับตรง ภาคปกติ'), (6561,'6561 : Admission ภาคพิเศษ'), (650901,'650901 : รับตรง ภาคพิเศษ'), (6101,'6101 : Admission ลำปาง'),
        #         (70,'70 : รับตรง ลำปาง'), (4501,'4501 : เรียนดีเมือง'), (50,'50 : ชาวไทยภูเขา'), (51,'51 : มหาดไทย'), (5201,'5201 : เรียนดีชนบท'), (53,'53 : ผู้พิการ'),
        #         (54,'54 : เรียนดีภาคกลาง'), (62,'62 : ดีเด่นการกีฬา'), (66, '66 : โครงการโอลิมปิก')],
        #     ),
        #     'applicanttype_name_morespecific' : forms.Select(),
            'student_highschool_study_plan' : forms.Select(
                choices = [('วิทย์-คณิต','วิทย์-คณิต'), ('ศิลป์-คำนวณ','ศิลป์-คำนวณ')],
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['student_id'].widget.attrs['readonly'] = "readonly"
        self.fields['level'].widget.attrs['readonly'] = "readonly"
        self.fields['admitacad_year'].widget.attrs['readonly'] = "readonly"
        self.fields['applicanttype_id'].widget.attrs['readonly'] = "readonly"
        self.fields['applicanttype_name'].widget.attrs['readonly'] = "readonly"
        self.fields['applicanttype_name_morespecific'].widget.attrs['readonly'] = "readonly"

        grade_field = forms.FloatField(
            label=("เกรดเฉลี่ย"),
            validators=[MinValueValidator(0.00), MaxValueValidator(4.00)], 
            error_messages={
                'min_value': ("กรุณาใส่เกรดระหว่าง 0.00 - 4.00"),
                'max_value': ("กรุณาใส่เกรดระหว่าง 0.00 - 4.00"),
            },
            required = False
            # error_messages={'min_value' or 'max_value' or 'required' or 'invalid': ("กรุณาใส่เกรดระหว่าง 0.00 - 4.00")},
        )

        self.fields['student_highschool_gpa'] = grade_field



        submit = Submit('submit', 'บันทึก')
        submit.field_classes = "btn btn-outline-success mt-4 col-md-2"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('student_id', css_class = 'form-group col-md-5 mb-0'),
                Column('student_name_surname', css_class = 'form-group col-md-7 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column('level', css_class = 'form-group col-md-8 mb-0'),
                Column('admitacad_year', css_class = 'form-group col-md-4 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column('applicanttype_id', css_class = 'form-group col-md-2 mb-0'),
                Column('applicanttype_name', css_class = 'form-group col-md-6 mb-0'),
                Column('applicanttype_name_morespecific', css_class = 'form-group col-md-4 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column('student_highschool', css_class = 'form-group col-md-6 mb-0'),
                Column('student_highschool_study_plan', css_class = 'form-group col-md-3 mb-0'),
                Column('student_highschool_gpa', css_class = 'form-group col-md-3 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column(
                    ButtonHolder(
                        submit,
                        HTML(
                            """
                            &nbsp;<button onclick="window.location.href='{{ '/academicis/editStudent' }}'" class="btn btn-outline-danger mt-4 col-md-2" type="button">ยกเลิก</button>
                            """
                    ), css_class='text-center'),
                ),
            ),
        )


class EnrollmentEditForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = '__all__'
        labels = {
            'student_id': 'รหัสนักศึกษา',
            'admitacad_year': 'ปีที่เข้าศึกษา',
            'academic_year': 'ปีลงทะเบียน',
            'semester': 'เทอมลงทะเบียน',
            'course_id': 'รหัสวิชา',
            'creditsatisfy': 'เครดิตที่ได้รับ',
            'grade': 'เกรดที่ได้รับ',
        }
        widgets = {
            # 'semester' : forms.Select(choices=[(1,1),(2,2),(3,'Summer')]),
            'creditsatisfy' : forms.Select(choices=[(0,0),(1,1),(2,2),(3,3)]),
            'grade' : forms.Select(choices=[('A','A'),('B+','B+'),('B','B'),('C+','C+'),('C','C'),('D+','D+'),('D','D'),('F','F'),('W','W'),('U','U'),('S','S'),])
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # student_field = forms.RegexField(
        #     label=("รหัสนักศึกษา"), regex=r'^[0-9]{10}$',
        #     error_messages={
        #         'invalid': ("กรุณาใส่รหัสนักศึกษา 10 หลัก")
        #     }
        # )
        # self.fields['student_id'] = student_field

        self.fields['student_id'].widget.attrs['readonly'] = "readonly"
        self.fields['admitacad_year'].widget.attrs['readonly'] = "readonly"
        self.fields['academic_year'].widget.attrs['readonly'] = "readonly"
        self.fields['semester'].widget.attrs['readonly'] = "readonly"
        self.fields['course_id'].widget.attrs['readonly'] = "readonly"

        submit = Submit('submit', 'บันทึก')
        submit.field_classes = "btn btn-outline-success mt-4 col-md-2"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('student_id', css_class = 'form-group col-md-8 mb-0'),
                Column('admitacad_year', css_class = 'form-group col-md-4 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column('academic_year', css_class = 'form-group col-md-3 mb-0'),
                Column('semester', css_class = 'form-group col-md-2 mb-0'),
                Column('course_id', css_class = 'form-group col-md-3 mb-0'),
                Column('creditsatisfy', css_class = 'form-group col-md-2 mb-0'),
                Column('grade', css_class = 'form-group col-md-2 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column(
                    ButtonHolder(
                        submit,
                        HTML(
                            """
                            &nbsp;<button onclick="window.location.href='{{ '/academicis/editEnrollment' }}'" class="btn btn-outline-danger mt-4 col-md-2" type="button">ยกเลิก</button>
                            """
                    ), css_class='text-center'),
                ),
            ),
        )

class GradeEditForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = '__all__'
        labels = {
            'student_id' : 'รหัสนักศึกษา',
            'student_name_surname' : 'ชื่อ-สกุล',
            'academic_semester' : 'เทอม',
            'academic_year' : 'ปีการศึกษา',
            'creditsatisfy' : 'เครดิตที่ได้รับ',
            'creditpoint' : 'เครดิตที่ลงทะเบียน',
            'ix_count' : 'เครดิตที่ผ่านทั้งหมด',
            'gradepoint' : 'คะแนนรวม',
            's_gpa' : 'เกรดเฉลี่ยสะสม',
            's_gpax' : 'เกรดเฉลี่ย',
            's_status' : 'สถานะ',
        }
        widgets = {
            's_status' : forms.Select(choices=[("N","Normal"),("W","Warning"),("W1","Warning 1"),("W2","Warning 2"),("P","Probation")]),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        gpa_field = forms.FloatField(
            label=("เกรดเฉลี่ยสะสม"),
            validators=[MinValueValidator(0.00), MaxValueValidator(4.00)], 
            error_messages={
                'min_value': ("กรุณาใส่เกรดระหว่าง 0.00 - 4.00"),
                'max_value': ("กรุณาใส่เกรดระหว่าง 0.00 - 4.00"),
            },
        )

        self.fields['s_gpa'] = gpa_field

        gpax_field = forms.FloatField(
            label=("เกรดเฉลี่ย"),
            validators=[MinValueValidator(0.00), MaxValueValidator(4.00)], 
            error_messages={
                'min_value': ("กรุณาใส่เกรดระหว่าง 0.00 - 4.00"),
                'max_value': ("กรุณาใส่เกรดระหว่าง 0.00 - 4.00"),
            },
        )

        self.fields['s_gpax'] = gpax_field


        self.fields['student_id'].widget.attrs['readonly'] = "readonly"
        self.fields['student_name_surname'].widget.attrs['readonly'] = "readonly"
        self.fields['academic_semester'].widget.attrs['readonly'] = "readonly"
        self.fields['academic_year'].widget.attrs['readonly'] = "readonly"

        submit = Submit('submit', 'บันทึก')
        submit.field_classes = "btn btn-outline-success mt-4 col-md-2"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('student_id', css_class = 'form-group col-md-5 mb-0'),
                Column('student_name_surname', css_class = 'form-group col-md-7 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column('academic_year', css_class = 'form-group col-md-3 mb-0'),
                Column('academic_semester', css_class = 'form-group col-md-2 mb-0'),
                Column('creditsatisfy', css_class = 'form-group col-md-2 mb-0'),
                Column('creditpoint', css_class = 'form-group col-md-2 mb-0'),
                Column('ix_count', css_class = 'form-group col-md-3 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column('gradepoint', css_class = 'form-group col-md-3 mb-0'),
                Column('s_gpa', css_class = 'form-group col-md-3 mb-0'),
                Column('s_gpax', css_class = 'form-group col-md-3 mb-0'),
                Column('s_status', css_class = 'form-group col-md-3 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column(
                    ButtonHolder(
                        submit,
                        HTML(
                            """
                            &nbsp;<button onclick="window.location.href='{{ '/academicis/editGrade' }}'" class="btn btn-outline-danger mt-4 col-md-2" type="button">ยกเลิก</button>
                            """
                    ), css_class='text-center'),
                ),
            ),
        )

class StateEditForm(forms.ModelForm):
    class Meta:
        model = State_Inactive
        fields = '__all__'
        labels = {
            'student_id' : 'รหัสนักศึกษา',
            'student_name_surname' : 'ชื่อ-สกุล',
            'state_not_normal' : 'สถานะไม่ปกติ',
            'grade' : 'เกรด',
        }
        widgets = {
            'state_not_normal' : forms.Select(choices=[("ลาออก","ลาออก"),("ไม่จดทะเบียนศึกษารายวิชาภาค","ไม่จดทะเบียนศึกษารายวิชาภาค"),]),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        grade_field = forms.FloatField(
            label=("เกรดเฉลี่ย"),
            validators=[MinValueValidator(0.00), MaxValueValidator(4.00)], 
            error_messages={
                'min_value': ("กรุณาใส่เกรดระหว่าง 0.00 - 4.00"),
                'max_value': ("กรุณาใส่เกรดระหว่าง 0.00 - 4.00"),
            },
        )

        self.fields['grade'] = grade_field

        self.fields['student_id'].widget.attrs['readonly'] = "readonly"
        self.fields['student_name_surname'].widget.attrs['readonly'] = "readonly"



        submit = Submit('submit', 'บันทึก')
        submit.field_classes = "btn btn-outline-success mt-4 col-md-2"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('student_id', css_class = 'form-group col-md-5 mb-0'),
                Column('student_name_surname', css_class = 'form-group col-md-7 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column('state_not_normal', css_class = 'form-group col-md-8 mb-0'),
                Column('grade', css_class = 'form-group col-md-4 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column(
                    ButtonHolder(
                        submit,
                        HTML(
                            """
                            &nbsp;<button onclick="window.location.href='{{ '/academicis/editState' }}'" class="btn btn-outline-danger mt-4 col-md-2" type="button">ยกเลิก</button>
                            """
                    ), css_class='text-center'),
                ),
            ),
        )

class CourseUsageForm(forms.ModelForm):
    class Meta:
        model = Course_Usage
        fields = ['curriculum','course_id','course_name','elective_or_mandatory']
        # fields = '__all__'
        labels = {
            'curriculum' : 'หลักสูตรปรับปรุง พ.ศ.',
            # 'period' : 'ระยะเวลาที่ใช้',
            'course_id' : 'รหัสวิชา',
            'course_name' : 'ชื่อวิชา',
            'elective_or_mandatory' : 'ประเภทวิชา',
        }
        widgets = {
            'curriculum' : forms.Select(
                choices=[(2556,2556),(2561, 2561)]
                ),
            'elective_or_mandatory' : forms.Select(
                choices = [('วิชาบังคับร่วม','วิชาบังคับร่วม'), ('วิชาบังคับเอก','วิชาบังคับเอก'), ('วิชาเลือก','วิชาเลือก')],
            ),
            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        submit = Submit('submit', 'บันทึก')
        submit.field_classes = "btn btn-outline-success mt-4 col-md-2"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('curriculum', css_class = 'form-group col-md-3 mb-0'),
                # Column('period', css_class = 'form-group col-md-3 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column('course_id', css_class = 'form-group col-md-2 mb-0'),
                Column('course_name', css_class = 'form-group col-md-6 mb-0'),
                Column('elective_or_mandatory', css_class = 'form-group col-md-4 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column(
                    ButtonHolder(
                        submit,
                        HTML(
                            """
                            &nbsp;<button onclick="window.location.href='{{ '/academicis/createCourseUsage' }}'" class="btn btn-outline-danger mt-4 col-md-2" type="button">ยกเลิก</button>
                            """
                    ), css_class='text-center'),
                ),
            ),
        )

class CourseUsageEditForm(forms.ModelForm):
    class Meta:
        model = Course_Usage
        fields = '__all__'
        labels = {
            'curriculum' : 'หลักสูตรปรับปรุง พ.ศ.',
            'period' : 'ระยะเวลาที่ใช้',
            'course_id' : 'รหัสวิชา',
            'course_name' : 'ชื่อวิชา',
            'elective_or_mandatory' : 'ประเภทวิชา',
        }
        # widgets = {
            # 'curriculum' : forms.Select(choices=[(curri['curriculum'], curri['curriculum']) for curri in Course_Usage.objects.values('curriculum').distinct()]),
        #     'elective_or_mandatory' : forms.RadioSelect(),
            
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['curriculum'].widget.attrs['readonly'] = "readonly"
        self.fields['period'].widget.attrs['readonly'] = "readonly"
        self.fields['course_id'].widget.attrs['readonly'] = "readonly"
        self.fields['elective_or_mandatory'].widget.attrs['readonly'] = "readonly"

        submit = Submit('submit', 'บันทึก')
        submit.field_classes = "btn btn-outline-success mt-4 col-md-2"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('curriculum', css_class = 'form-group col-md-3 mb-0'),
                Column('period', css_class = 'form-group col-md-3 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column('course_id', css_class = 'form-group col-md-2 mb-0'),
                Column('course_name', css_class = 'form-group col-md-6 mb-0'),
                Column('elective_or_mandatory', css_class = 'form-group col-md-4 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column(
                    ButtonHolder(
                        submit,
                        HTML(
                            """
                            &nbsp;<button onclick="window.location.href='{{ '/academicis/editCourseUsage' }}'" class="btn btn-outline-danger mt-4 col-md-2" type="button">ยกเลิก</button>
                            """
                    ), css_class='text-center'),
                ),
            ),
        )


class PlanEditForm(forms.ModelForm):
    class Meta:
        model = Applicant_Plan
        fields = ['year', 'major', 't1_plan', 't2_plan', 't3_plan', 't4_plan', 't5_plan']
        labels = {
            'year' : 'ปีการศึกษา',
            'major' : 'โครงการ',
            't1_plan' : 'แผนรับเข้า TCAS รอบ 1',
            't2_plan' : 'แผนรับเข้า TCAS รอบ 2',
            't3_plan' : 'แผนรับเข้า TCAS รอบ 3',
            't4_plan' : 'แผนรับเข้า TCAS รอบ 4',
            't5_plan' : 'แผนรับเข้า TCAS รอบ 5',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['year'].widget.attrs['readonly'] = "readonly"
        self.fields['major'].widget.attrs['readonly'] = "readonly"

        submit = Submit('submit', 'บันทึก')
        submit.field_classes = "btn btn-outline-success mt-4 col-md-2"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('year', css_class = 'form-group col-md-4 mb-0'),
                Column('major', css_class = 'form-group col-md-8 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column('t1_plan', css_class = 'form-group col-md-3 mb-0'),
                Column('t2_plan', css_class = 'form-group col-md-3 mb-0'),
                Column('t3_plan', css_class = 'form-group col-md-3 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column('t4_plan', css_class = 'form-group col-md-3 mb-0'),
                Column('t5_plan', css_class = 'form-group col-md-3 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column(
                    ButtonHolder(
                        submit,
                        HTML(
                            """
                            &nbsp;<button onclick="window.location.href='{{ '/academicis/editPlan' }}'" class="btn btn-outline-danger mt-4 col-md-2" type="button">ยกเลิก</button>
                            """
                    ), css_class='text-center'),
                ),
            ),
        )

# class Country(models.Model):
#     name = models.CharField(max_length=40)

#     def __str__(self):
#         return self.name


# class City(models.Model):
#     applicant = models.ForeignKey(Country, on_delete=models.CASCADE)
#     name = models.CharField(max_length=40)

#     def __str__(self):
#         return self.name

class ApplicantType(models.Model):
    type_id = models.IntegerField()
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name


class SubApplicantType(models.Model):
    applicant = models.ForeignKey(ApplicantType, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Person(models.Model):
    student_id = models.CharField(max_length = 255)
    student_name_surname = models.CharField(max_length = 255)
    level = models.CharField(max_length = 255,)
    admitacad_year = models.IntegerField()
    applicanttype_id = models.IntegerField()
    applicanttype_name = models.ForeignKey(ApplicantType, on_delete=models.SET_NULL, blank=True, null=True)
    applicanttype_name_morespecific = models.ForeignKey(SubApplicantType, on_delete=models.SET_NULL, blank=True, null=True)
    student_highschool_study_plan = models.CharField(max_length = 20,)
    student_highschool = models.CharField(max_length = 255, blank=True, null=True)
    student_highschool_gpa = models.CharField(max_length = 5, blank=True, null=True,)
    # name = models.FloatField()

    def __str__(self):
        return self.name

class PersonCreationForm(forms.ModelForm):
    class Meta:
        model = Person
        # fields = '__all__'
        fields = ['student_id','student_name_surname','level','admitacad_year','applicanttype_name','applicanttype_name_morespecific','student_highschool_study_plan','student_highschool','student_highschool_gpa']
        labels = {
            'student_id': 'รหัสนักศึกษา',
            'student_name_surname': 'ชื่อ-สกุล',
            'level': 'โครงการ',
            'admitacad_year': 'ปีที่เข้าศึกษา',
            'applicanttype_id': 'รหัสช่องทาง',
            'applicanttype_name': 'ช่องทางการเข้าศึกษา',
            'applicanttype_name_morespecific': 'เพิ่มเติม',
            'student_highschool_study_plan': 'แผนการเรียน',
            'student_highschool': 'โรงเรียนมัธยมปลาย',
            'student_highschool_gpa' :'เกรดเฉลี่ย',
        }
        widgets = {
            'level' : forms.Select(
                choices = [('ปริญญาตรี โครงการปกติ','ปริญญาตรี โครงการปกติ'), ('ปริญญาตรี โครงการพิเศษ','ปริญญาตรี โครงการพิเศษ'), ('ปริญญาตรี โครงการปกติ ศูนย์ลำปาง', 'ปริญญาตรี โครงการปกติ ศูนย์ลำปาง')],
            ),
            'admitacad_year' : forms.TextInput(attrs={'value':datetime.datetime.now().year+543}),
            'student_highschool_study_plan' : forms.Select(
                choices = [('วิทย์-คณิต','วิทย์-คณิต'), ('ศิลป์-คำนวณ','ศิลป์-คำนวณ')],
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['applicanttype_name'].empty_label = None #remove first empty
        self.fields['applicanttype_name'].required = True
        self.fields['applicanttype_name_morespecific'].empty_label = None #remove first empty
        self.fields['applicanttype_name_morespecific'].queryset = SubApplicantType.objects.filter(applicant_id=1).order_by('name')

        if 'applicanttype_name' in self.data:
            try:
                applicant_id = int(self.data.get('applicanttype_name'))
                self.fields['applicanttype_name_morespecific'].queryset = SubApplicantType.objects.filter(applicant_id=applicant_id).order_by('name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['applicanttype_name_morespecific'].queryset = self.instance.applicanttype_name.applicanttype_name_morespecific_set.order_by('name')

        student_field = forms.RegexField(
            label=("รหัสนักศึกษา"), regex=r'^[0-9]{10}$',
            error_messages={
                'invalid': ("กรุณาใส่รหัสนักศึกษา 10 หลัก")
            }
        )
        self.fields['student_id'] = student_field

        grade_field = forms.FloatField(
            label=("เกรดเฉลี่ย"),
            validators=[MinValueValidator(0.00), MaxValueValidator(4.00)], 
            error_messages={
                'min_value': ("กรุณาใส่เกรดระหว่าง 0.00 - 4.00"),
                'max_value': ("กรุณาใส่เกรดระหว่าง 0.00 - 4.00"),
            },
            required = False
            # error_messages={'min_value' or 'max_value' or 'required' or 'invalid': ("กรุณาใส่เกรดระหว่าง 0.00 - 4.00")},
        )

        self.fields['student_highschool_gpa'] = grade_field
        submit = Submit('submit', 'บันทึก')
        submit.field_classes = "btn btn-outline-success mt-4 col-md-2"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('student_id', css_class = 'form-group col-md-5 mb-0'),
                Column('student_name_surname', css_class = 'form-group col-md-7 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column('level', css_class = 'form-group col-md-8 mb-0'),
                Column('admitacad_year', css_class = 'form-group col-md-4 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column('applicanttype_name', css_class = 'form-group col-md-7 mb-0'),
                Column('applicanttype_name_morespecific', css_class = 'form-group col-md-5 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column('student_highschool', css_class = 'form-group col-md-6 mb-0'),
                Column('student_highschool_study_plan', css_class = 'form-group col-md-3 mb-0'),
                Column('student_highschool_gpa', css_class = 'form-group col-md-3 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column(
                    ButtonHolder(
                        submit,
                        HTML(
                            """
                            &nbsp;<button onclick="window.location.href='{{ '/academicis/createStudent' }}'" class="btn btn-outline-danger mt-4 col-md-2" type="button">ยกเลิก</button>
                            """
                    ), css_class='text-center'),
                ),
            ),
        )


class SubApplicantTypeForm(forms.ModelForm):
    class Meta:
        model = SubApplicantType
        fields = '__all__'
        labels = {
            'applicant': 'ช่องทางการเข้าศึกษา',
            'name': 'เพิ่มเติม',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['applicant'].empty_label = None #remove first empty

        submit = Submit('submit', 'บันทึก')
        submit.field_classes = "btn btn-outline-success mt-4 col-md-2"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('applicant', css_class = 'form-group col-md-5 mb-0'),
                Column('name', css_class = 'form-group col-md-7 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column(
                    ButtonHolder(
                        submit,
                        HTML(
                            """
                            &nbsp;<button onclick="window.location.href='{{ '/academicis/createApptype' }}'" class="btn btn-outline-danger mt-4 col-md-2" type="button">ยกเลิก</button>
                            """
                    ), css_class='text-center'),
                ),
            ),
        )

class SubApplicantTypeEditForm(forms.ModelForm):
    class Meta:
        model = SubApplicantType
        fields = '__all__'
        labels = {
            'applicant': 'ช่องทางการเข้าศึกษา',
            'name': 'เพิ่มเติม',
        }
        # widgets = {
        #     'applicant': forms.TextInput(attrs={'value':"aa"})
        # }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['applicant'].empty_label = None #remove first empty
        for key, value in kwargs.items():
            print("The value of {} is {}".format(key, value))
            if key == 'initial':
                applicant = value['applicant_id']
            if key == 'data':
                applicant = value['applicant']

        self.fields['applicant'].queryset = ApplicantType.objects.filter(id=applicant)
        self.fields['applicant'].widget.attrs['readonly'] = "readonly"

        submit = Submit('submit', 'บันทึก')
        submit.field_classes = "btn btn-outline-success mt-4 col-md-2"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('applicant', css_class = 'form-group col-md-5 mb-0'),
                Column('name', css_class = 'form-group col-md-7 mb-0'),
                css_class = 'form-row'
            ),
            Row(
                Column(
                    ButtonHolder(
                        submit,
                        HTML(
                            """
                            &nbsp;<button onclick="window.location.href='{{ '/academicis/editApptype' }}'" class="btn btn-outline-danger mt-4 col-md-2" type="button">ยกเลิก</button>
                            """
                    ), css_class='text-center'),
                ),
            ),
        )