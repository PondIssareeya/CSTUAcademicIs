# Generated by Django 3.2 on 2021-05-24 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Applicant_Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField()),
                ('major', models.CharField(max_length=255)),
                ('plan', models.PositiveIntegerField()),
                ('actual', models.PositiveIntegerField(default=0, null=True)),
                ('t1_plan', models.PositiveIntegerField()),
                ('t1_actual', models.PositiveIntegerField(default=0, null=True)),
                ('t2_plan', models.PositiveIntegerField()),
                ('t2_actual', models.PositiveIntegerField(default=0, null=True)),
                ('t3_plan', models.PositiveIntegerField()),
                ('t3_actual', models.PositiveIntegerField(default=0, null=True)),
                ('t4_plan', models.PositiveIntegerField()),
                ('t4_actual', models.PositiveIntegerField(default=0, null=True)),
                ('t5_plan', models.PositiveIntegerField(default=0)),
                ('t5_actual', models.PositiveIntegerField(default=0, null=True)),
                ('all_actual', models.PositiveIntegerField(default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Applicant_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curriculum', models.IntegerField()),
                ('applicant_type_id', models.IntegerField()),
                ('applicant_type_name', models.CharField(max_length=255)),
                ('applicant_type_specific', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ApplicantType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_id', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_id', models.CharField(max_length=20)),
                ('curriculum', models.IntegerField()),
                ('course_name', models.CharField(max_length=200)),
                ('course_description', models.CharField(max_length=1000)),
                ('credit', models.IntegerField()),
                ('lecture_hours', models.IntegerField()),
                ('lab_hours', models.IntegerField()),
                ('selfstudy_hours', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Course_Sector_Curriculum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sector_id', models.IntegerField()),
                ('sector_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Course_Sector_Tqf',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tqf_no', models.IntegerField()),
                ('tqf_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Course_Usage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curriculum', models.IntegerField(default=2561)),
                ('period', models.IntegerField(default=0)),
                ('course_id', models.CharField(default=None, max_length=5, null=True)),
                ('course_name', models.CharField(default=None, max_length=255)),
                ('elective_or_mandatory', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Curriculum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('curri', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=255)),
                ('student_name_surname', models.CharField(max_length=255)),
                ('highschool_plan', models.CharField(max_length=20)),
                ('major', models.CharField(max_length=255)),
                ('applicant_type', models.CharField(max_length=255)),
                ('admit_year', models.IntegerField()),
                ('level', models.IntegerField()),
                ('academic_semester', models.CharField(max_length=1)),
                ('academic_year', models.IntegerField()),
                ('grade', models.FloatField()),
                ('status', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Data_Basic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=255)),
                ('highschool_plan', models.CharField(max_length=20)),
                ('admit_year', models.IntegerField()),
                ('applicant_type', models.CharField(max_length=255)),
                ('major', models.CharField(max_length=255)),
                ('level', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('grade', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=255)),
                ('admitacad_year', models.IntegerField()),
                ('academic_year', models.IntegerField()),
                ('semester', models.IntegerField()),
                ('course_id', models.CharField(max_length=10)),
                ('creditsatisfy', models.IntegerField()),
                ('grade', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Entrance_Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('high_school_curriculum', models.CharField(max_length=100)),
                ('school', models.CharField(max_length=200)),
                ('province', models.CharField(max_length=100)),
                ('educated_year', models.IntegerField()),
                ('gpax', models.FloatField()),
                ('entrance_score', models.FloatField()),
                ('gat', models.FloatField()),
                ('pat1', models.FloatField()),
                ('pat2', models.FloatField()),
                ('onet_th', models.FloatField()),
                ('onet_sci', models.FloatField()),
                ('onet_eng', models.FloatField()),
                ('onet_math', models.FloatField()),
                ('onet_soc', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(default=None, max_length=255, null=True)),
                ('student_name_surname', models.CharField(default=None, max_length=255, null=True)),
                ('academic_semester', models.CharField(default=None, max_length=1, null=True)),
                ('academic_year', models.IntegerField(default=None, null=True)),
                ('creditsatisfy', models.CharField(default=None, max_length=3, null=True)),
                ('creditpoint', models.CharField(default=None, max_length=3, null=True)),
                ('ix_count', models.CharField(default=None, max_length=3, null=True)),
                ('gradepoint', models.FloatField(default=None, null=True)),
                ('s_gpa', models.FloatField(default=None, null=True)),
                ('s_gpax', models.FloatField(default=None, null=True)),
                ('s_status', models.CharField(default=None, max_length=4, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=255)),
                ('activity', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Major_And_Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('major_and_track', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Prereq_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Required_C',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=255)),
                ('admitacad_year', models.IntegerField()),
                ('academic_year', models.IntegerField()),
                ('course_id', models.CharField(max_length=10)),
                ('grade', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='State_Inactive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=255)),
                ('student_name_surname', models.CharField(max_length=255)),
                ('state_not_normal', models.CharField(max_length=255)),
                ('grade', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=255)),
                ('student_name_surname', models.CharField(max_length=255)),
                ('semester', models.IntegerField()),
                ('academic_year', models.IntegerField()),
                ('status', models.CharField(max_length=20)),
                ('grade', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=255)),
                ('student_name_surname', models.CharField(max_length=255)),
                ('level', models.CharField(max_length=255)),
                ('admitacad_year', models.IntegerField()),
                ('applicanttype_id', models.IntegerField()),
                ('applicanttype_name', models.CharField(max_length=255)),
                ('applicanttype_name_morespecific', models.CharField(blank=True, max_length=255, null=True)),
                ('student_highschool_study_plan', models.CharField(max_length=50)),
                ('student_highschool', models.CharField(blank=True, max_length=255, null=True)),
                ('student_highschool_gpa', models.CharField(blank=True, max_length=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Title',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Usage_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usage_type', models.CharField(max_length=100)),
                ('condition', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('is_student', models.BooleanField()),
                ('is_teacher', models.BooleanField()),
                ('is_staff', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('surname', models.CharField(max_length=50)),
                ('academic_position', models.CharField(max_length=20)),
                ('education_position', models.CharField(max_length=20)),
                ('education', models.CharField(max_length=5000)),
                ('email', models.EmailField(max_length=254)),
                ('campus', models.CharField(max_length=50)),
                ('status', models.CharField(max_length=50)),
                ('works', models.CharField(max_length=5000)),
                ('teacher_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='academicis_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='SubApplicantType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='academicis_app.applicanttype')),
            ],
        ),
        migrations.CreateModel(
            name='Prerequsite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.IntegerField()),
                ('post_course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='course_postcourse', to='academicis_app.course')),
                ('pre_course', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='course_precourse', to='academicis_app.course')),
                ('prerequsite_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='academicis_app.prereq_type')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=255)),
                ('student_name_surname', models.CharField(max_length=255)),
                ('level', models.CharField(max_length=255)),
                ('admitacad_year', models.IntegerField()),
                ('applicanttype_id', models.IntegerField()),
                ('student_highschool_study_plan', models.CharField(max_length=20)),
                ('student_highschool', models.CharField(blank=True, max_length=255, null=True)),
                ('student_highschool_gpa', models.CharField(blank=True, max_length=5, null=True)),
                ('applicanttype_name', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academicis_app.applicanttype')),
                ('applicanttype_name_morespecific', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='academicis_app.subapplicanttype')),
            ],
        ),
        migrations.CreateModel(
            name='Parent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_name', models.CharField(max_length=50)),
                ('p_surname', models.CharField(max_length=50)),
                ('p_relation', models.CharField(max_length=50)),
                ('p_phone', models.CharField(max_length=11)),
                ('p_income', models.FloatField()),
                ('title', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='academicis_app.title')),
            ],
        ),
    ]