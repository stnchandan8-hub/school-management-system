from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class students_of_all_classes(models.Model):
    rollno=models.BigIntegerField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    s1stname=models.CharField(max_length=50)
    slstname=models.CharField(max_length=60)
    cname=models.CharField(max_length=20)
    gender=models.CharField(max_length=10)
    address=models.TextField(max_length=100)
    contact_no=models.CharField(max_length=10,unique=True)
    age=models.CharField(max_length=10)
    father_1stname=models.CharField(max_length=30)
    father_lstname=models.CharField(max_length=30)
class user_added_or_not(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    add_or_pending=models.BooleanField(default=False)    

class teacher(models.Model):
    tid=models.BigIntegerField(primary_key=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    t_1st_name=models.CharField(max_length=50)
    t_last_name=models.CharField(max_length=50)
    age=models.CharField(max_length=10)
    qualification=models.TextField(max_length=100)
    address=models.TextField(max_length=100)
    contactno=models.CharField(max_length=10,unique=True)
    gender=models.CharField(max_length=20)
class notice_table_for_student(models.Model):
    date=models.DateTimeField()
    text=models.TextField(max_length=1000)
class notice_table_for_teacher(models.Model):
    date=models.DateTimeField()
    text1=models.TextField(max_length=1000)
class result_of_all_classes_annual(models.Model):
    
    rollno=models.ForeignKey(students_of_all_classes, on_delete=models.CASCADE)
    cname=models.CharField(max_length=20,null=True)
    seesion_year=models.CharField(max_length=20,default="2026")
    exam_name=models.CharField(max_length=20,default="Annual")
    math=models.BigIntegerField(max_length=20,null=True,blank=True)
    science=models.BigIntegerField(max_length=20,null=True,blank=True)
    Algebra_math=models.BigIntegerField(max_length=20,null=True,blank=True)
    geometry_math=models.BigIntegerField(max_length=20,null=True,blank=True)
    hindi=models.BigIntegerField(max_length=20,null=True,blank=True)
    life_science=models.CharField(max_length=50,null=True,blank=True)
    physical_science=models.CharField(max_length=30,null=True,blank=True)
    history=models.CharField(max_length=30,null=True,blank=True)
    geography=models.CharField(max_length=30,null=True,blank=True)
    Polity=models.CharField(max_length=40,null=True,blank=True)
    drawing=models.BigIntegerField(max_length=20,null=True,blank=True)
    rime=models.BigIntegerField(max_length=20,null=True,blank=True)
    project=models.BigIntegerField(max_length=20,null=True,blank=True)
    english=models.BigIntegerField(max_length=20,null=True,blank=True)

#result model for half_yearly result

class contact(models.Model):
    contact_id=models.BigAutoField(primary_key=True)
    name=models.CharField(max_length=50)
    ph_no=models.CharField(max_length=20)
    email=models.CharField(max_length=20)
    issue=models.CharField(max_length=20)
class aboutpage(models.Model):
    aboutpage_id=models.BigAutoField(primary_key=True)
    school_name=models.CharField(max_length=50)
    estb=models.DateField()
    location=models.TextField(max_length=500)
    total_student=models.CharField(max_length=10)
    total_faculty=models.CharField(max_length=10)
    imp_text=models.TextField(max_length=500)



#period table for student
class period_table_for_student(models.Model):
    class_name=models.CharField(max_length=50)
    period_1=models.CharField(max_length=50)
    period_2=models.CharField(max_length=50)
    period_3=models.CharField(max_length=50)
    period_4=models.CharField(max_length=50)
    period_5=models.CharField(max_length=50)
    period_6=models.CharField(max_length=50)
    period_7=models.CharField(max_length=50)
    period_8=models.CharField(max_length=50)
    period_9=models.CharField(max_length=50)
#period table for teacher
class period_table_for_teacher(models.Model):
    pid_t=models.BigAutoField(primary_key=True)
    tname=models.CharField(max_length=50)
    subject=models.CharField(max_length=20)
    time=models.TextField(max_length=50)
    session_year=models.TextField(max_length=20)
#get information about monitor of each class
class monitors(models.Model):
    mid=models.BigAutoField(primary_key=True)
    cname=models.CharField(max_length=50)
    monitor_name=models.CharField(max_length=50)

class attendance_teacher(models.Model):
    at_id=models.BigAutoField(primary_key=True)
    tid=models.ForeignKey(teacher, on_delete=models.CASCADE)
    date=models.DateField()
    tname=models.CharField(max_length=50)
    seesion_year=models.CharField(max_length=30)
#student can check indivisually its present and absent monthwise by choose their respective classes
class student_check_indivisually_absent_present_taken_by_teacher(models.Model):
    
    srollno=models.ForeignKey(students_of_all_classes, on_delete=models.CASCADE)
    status=models.CharField(max_length=20,default="Pending")
    date=models.DateField(auto_now_add=True)
    


#teacher can check indivisually its present and  absent monthwise
class teacher_check_indivisually_absent_present(models.Model):
    tci=models.BigAutoField(primary_key=True)
    at_id=models.ForeignKey(attendance_teacher, on_delete=models.CASCADE)
    tname=models.CharField(max_length=50)
    total_absent=models.CharField(max_length=20)
    total_present=models.CharField(max_length=20)
    month=models.CharField(max_length=20)
    
#Apply leave for  indivisual student
class leave_for_students(models.Model):
    sname=models.CharField(max_length=20)
    leave_reason=models.TextField(max_length=500)
    ph_no=models.BigIntegerField(max_length=20,primary_key=True)
    date_of_apply=models.DateTimeField()
    accept1_or_reject=models.CharField(max_length=20,null=True,default="pending")
#Apply leave for  indivisual teacher
class leave_for_teachers(models.Model):
    tid=models.ForeignKey(teacher, on_delete=models.CASCADE)
    leave_reason=models.TextField(max_length=500)
    date1_of_apply=models.DateTimeField()
    accept_or_reject=models.CharField(max_length=20,null=True,default="Pending")
#feedback table
class feedback_student(models.Model):
    sname=models.CharField(max_length=50)
    stext=models.TextField(max_length=500)
    semail=models.EmailField(primary_key=True)
    
class feedback_teacher(models.Model):
    tid=models.ForeignKey(teacher, on_delete=models.CASCADE)
    ttext=models.TextField(max_length=500)
    date=models.DateField(auto_now_add=True)
    reply=models.CharField(max_length=30,null=True)
   
class subject(models.Model):
    sub_id=models.BigIntegerField(max_length=10,primary_key=True)
    sub_name=models.CharField(max_length=50)
    

