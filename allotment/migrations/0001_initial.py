# Generated by Django 2.1.1 on 2018-09-16 06:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Departments',
            },
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dateOfExam', models.DateField(default=django.utils.timezone.now)),
                ('noOfStudents', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Exam',
                'verbose_name_plural': 'Exams',
            },
        ),
        migrations.CreateModel(
            name='GarbageTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('nickName', models.CharField(max_length=25)),
            ],
            options={
                'verbose_name': 'Shift',
                'verbose_name_plural': 'Shifts',
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('dateofJoining', models.DateField(default=django.utils.timezone.now)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='allotment.Department')),
            ],
            options={
                'verbose_name': 'Staff',
                'verbose_name_plural': 'Staffs',
            },
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shortname', models.CharField(help_text='Enter a short name for timetable, this name is not displayed in the report', max_length=20)),
                ('longName', models.CharField(help_text='Enter the TimeTable name which is printed in the final reports', max_length=200)),
                ('oneStaffPer_Students', models.IntegerField(verbose_name='Number of students for which one is required, this is used to calculate the no of staffs required for an examination')),
            ],
            options={
                'verbose_name': 'TimeTable',
                'verbose_name_plural': 'TimeTables',
            },
        ),
        migrations.AddField(
            model_name='exam',
            name='staffs',
            field=models.ManyToManyField(blank=True, help_text='Select staffs for the exam', to='allotment.Staff'),
        ),
        migrations.AddField(
            model_name='exam',
            name='timetable_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='allotment.TimeTable'),
        ),
        migrations.AddField(
            model_name='department',
            name='shift',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='allotment.Shift'),
        ),
    ]
