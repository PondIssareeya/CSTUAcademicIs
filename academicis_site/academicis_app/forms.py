from django import forms

class SearchForm(forms.Form):
    name = forms.CharField(label="รหัส/ชื่อนักศึกษา", required = True)
    id_stu = forms.CharField(label="รหัสนักศึกษา", required = True)
    curri = forms.IntegerField(label="หลักสูตรปรับปรุง พ.ศ.", required = True, min_value=0)
    app_type = forms.CharField(label="ช่องทางการรับเข้ารอบ", required = True)
    year = forms.IntegerField(label="ปีการศึกษา", required = True, min_value=0)

# class StudentForm(forms.Form):
#     student_id = forms.CharField(label = 'รหัสนักศึกษา', required = True),
#     student_name_surname = forms.CharField(label = 'ชื่อ-สกุล', required = True),
#     level = forms.CharField(label = 'โครงการ', required = True),
#     admitacad_year = forms.IntegerField(label = 'ปีที่เข้าศึกษา', required = True),
#     applicanttype_id = forms.IntegerField(label = 'รหัสช่องทางที่เข้าศึกษา', required = True),
#     applicanttype_name = forms.CharField(label = 'ช่องทางที่เข้าศึกษา', required = True),
#     applicanttype_name_morespecific = forms.CharField(label = 'เพิ่มเติม', required = True) ,
#     student_highschool_study_plan = forms.CharField(label = 'แผนการเรียนมัธยมปลาย', required = True),
#     student_highschool = forms.CharField(label = 'โรงเรียนมัธยมปลาย', required = True) ,
#     student_highschool_gpa = forms.FloatField(label = 'เกรดเฉลี่ยระดับมัธยมปลาย', required = True),