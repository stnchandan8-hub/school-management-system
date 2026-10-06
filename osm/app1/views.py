from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from django.db.models import Q,Count
from django.utils import timezone
from django.contrib.auth.models import User,Group
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib import messages
from app1.models import *
from datetime import date


# Create your views here.
def home(request):
    response=render(request,"homepage.html")
    return response
def register_view(request):
    if request.method=="POST":
        
        
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        confirm_password=request.POST.get("confirm_password")
        group_id=request.POST.get("group_id")
        #validation
        
        if password!= confirm_password:
            return render(request,"homepage.html",context={"password":"password does not match"})
            
        if User.objects.filter(username=username).exists():
            messages.error(request,message="username already exists")
            response=redirect("register")
            return response
        else:
            user=User.objects.create_user(username=username,email=email,password=password)
            user.save()
            
            group=Group.objects.get(id=group_id)
            user.groups.add(group)
            user.save()
            response=render(request,"homepage.html")
            return response
    else:
        return render(request,"homepage.html")

def login_view(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user=authenticate(request,username=username,password=password)
        if user!=None:
            login(request,user)
            response=redirect("dashboard")
            return response
        else:
            messages.error(request,message="invalid username and password")
            response=redirect("login")
            return response
    else:
        return redirect("home")
@login_required
def dashboard(request):
    user = request.user
    if user.groups.filter(name="Admin").exists():
        return redirect("admin_dashboard")
    elif user.groups.filter(name="Teachers").exists():
        return redirect("teacher_dashboard")
    elif user.groups.filter(name="Students").exists():
        return redirect("student_dashboard")
    else:
       return HttpResponse("Group not Found")
    
def admin_dashboard(request):
    today=timezone.localdate()
    attendance = (
        student_check_indivisually_absent_present_taken_by_teacher.objects.filter(date=today).values("srollno__cname").annotate(
            present=Count("id", filter=Q(status="Present")),
            absent=Count("id", filter=Q(status="Absent"))
        )
    )
    print(list(attendance))
    labels = []
    present_data = []
    absent_data = []

    for item in attendance:
        labels.append(item["srollno__cname"])
        present_data.append(item["present"])
        absent_data.append(item["absent"])
    users=User.objects.all()
    total_student=students_of_all_classes.objects.all().count()
    total_subjects=subject.objects.all().count()
    total_teachers=teacher.objects.all().count()
    response=render(request,"adminpage.html",context={"users":users,"total_student":total_student,"total_subjects":total_subjects,"total_teachers":total_teachers,"labels": labels,
        "present_data": present_data,
        "absent_data": absent_data})
    return response
def  teacher_dashboard(request):
    total_leave=leave_for_teachers.objects.all().count()
    total_student=students_of_all_classes.objects.all().count()
    total_subjects=subject.objects.all().count()
    total_present=student_check_indivisually_absent_present_taken_by_teacher.objects.filter(date=date.today(),status="Present").count()
    total_absent=student_check_indivisually_absent_present_taken_by_teacher.objects.filter(date=date.today(),status="Absent").count()
    total_attendance=student_check_indivisually_absent_present_taken_by_teacher.objects.filter(date=date.today()).count()
    response=render(request,"teacher_dashboard.html",context={"total_leave":total_leave,"total_present": total_present, "total_absent":total_absent,"total_attendance":total_attendance,"total_student":total_student,"total_subjects":total_subjects})
    return response

def student_dashboard(request):
    response=render(request,"student_dashboard.html")
    return response
#logout session
def logout_view(request):
    logout(request)
    return redirect("home")



#views for admin(teachers)
def add_teacher(request):
    if request.method=="POST":
      tid=request.POST.get("tid")
      username=request.POST.get("username")
      t_1st_name=request.POST.get("t_1st_name")
      t_last_name=request.POST.get("t_last_name")
      age=request.POST.get("age")
      qualification=request.POST.get("qualification")
      address=request.POST.get("address")
      contactno=request.POST.get("contactno")
      gerder=request.POST.get("gender") 
      user_name=User.objects.get(username=username)

      if  teacher.objects.filter(tid=tid).exists():
         messages.error(request,"The given teacher id is already exist")
         return redirect("view_teacher")  
      if  teacher.objects.filter(contactno=contactno).exists(): 
                messages.error(request,"The given phone number is already registered with a user")
                return redirect("view_teacher")
      if   teacher.objects.filter(user=user_name).exists():
              messages.error(request," This user is already exist")
              return redirect("view_teacher")
      else:
        
        user_added_or_not.objects.create(user=user_name,add_or_pending=True)
        teacher.objects.create(tid=tid,user=user_name,t_1st_name=t_1st_name,t_last_name=t_last_name,age=age,qualification=qualification,address=address,contactno=contactno,gender=gerder)  
        messages.success(request,"Teacher data is added successfully")
        return redirect("view_teacher")
    else:

        response=render(request,"add_teacher.html")
        return response
def view_teacher(request):
    qs=teacher.objects.all()
    response=render(request,"manage_teacher.html",context={"qs":qs})
    return response


def delete_teacher(request):
    if request.method == "POST":
      try:
         td1= request.POST.get("tid")
         td=teacher.objects.get(tid=td1)
         td.delete()
         messages.success(request,"Teacher deleted successfully")
         return redirect("view_teacher")
      except teacher.DoesNotExist:
          messages.error(request,"Invalid Teacher id")
          return redirect("view_teacher")
    else:
      return redirect("view_teacher")
    

        

def update_teacher(request):
        if request.method=="POST":
            tid1=request.POST.get("tid")
            t_1st_name=request.POST.get("t_1st_name")
            t_last_name=request.POST.get("t_last_name")
            age=request.POST.get("age")
            qualification=request.POST.get("qualification")
            address=request.POST.get("address")
            contactno=request.POST.get("contactno")
            gender=request.POST.get("gender")
            email_of_teacher=request.POST.get("email_of_teacher") 
            if not teacher.objects.filter(email_of_teacher=email_of_teacher).exists():
              pass
            else:
               messages.error(request,"The given email address is already register with a user")
            if not teacher.objects.filter(contactno=contactno).exists():
              pass
            else:
               messages.error(request,"The given phone number is already register with a user")
            

            try:
                #update Teacher by teacher id
                tu1=teacher.objects.get(tid=tid1)
                #update only field which are filled
                if t_1st_name:
                  tu1.t_1st_name=t_1st_name
                if t_last_name:
                  tu1.t_last_name=t_last_name
                if age:
                  tu1.age=age
                if qualification:
                  tu1.qualification=qualification
                if address:
                  tu1.address=address
                if contactno:
                  tu1.contactno=contactno
                if gender:
                  tu1.gender=gender
                if email_of_teacher:
                  tu1.email_of_teacher=email_of_teacher
                #save update records of teacher
                tu1.save()
                messages.success(request,"Teacher record updated successfully")
                return redirect("view_teacher")
            except teacher.DoesNotExist:
                messages.error(request,"Given Teacher Id not found")
                return redirect("view_teacher")
        else:
            return redirect("view_teacher")
        
def search_teacher(request):
   result=None
   if request.method=="POST":
      q= request.POST.get('q')
      if (q>="a" and q<="z") or  (q>="A" and q<="Z"):
        messages.error(request,"Teacher id must be a number")
        return redirect("view_teacher")
      if q and teacher.objects.filter(tid=q).exists():
          result = teacher.objects.filter(tid=q)
          response=render(request, 'search_teacher.html', {'tq': result})
          return response
      else:
             messages.error(request,"Invalid teacher id")
             return redirect("view_teacher")

   else:
        response=render(request,"manage_teacher.html")
        return response
def view_teacher_feedback(request):
   qs=feedback_teacher.objects.all()
   response=render(request,"view_teacher_feedback.html",context={'qs':qs})
   return response 
def reply_feedback_of_teacher_by_admin(request,fid):
   feedback=feedback_teacher.objects.get(fid)
   if request.method=="POST":
      feedback.reply=request.POST.get('reply')
      feedback.save()
def delete_reply_feedback_of_teacher(request):
    if request.method=="POST":
       tid=request.POST.get("tid")
       if feedback_teacher.objects.filter(tid=tid).exists():
         fid=feedback_teacher.objects.get("tid")
         fid.delete()
       else:
          messages.error(request,"Invalid teacher id")
          return redirect("view_teacher_feedback")
       


        
    
#view for admin(student)
#all views for manage student classwise(add,view,delete,update)
#manage students for class1

def add_students_of_all_classes(request):
    if request.method=="POST":
     rollno=request.POST.get("rollno")
     username=request.POST.get("username")
     s1stname=request.POST.get("s1stname")
     slstname=request.POST.get("slstname")
     cname=request.POST.get("cname")
     gender=request.POST.get("gender")
     address=request.POST.get("address")
     contact_no=request.POST.get("contact_no")
     age=request.POST.get("age")
     father_1stname=request.POST.get("father_1stname")
     father_lstname=request.POST.get("father_lstname")
     user_name=User.objects.get(username=username)
     if students_of_all_classes.objects.filter(user=user_name).exists():
        messages.error(request,"Student already exists for this user")
        return redirect("view_students_of_all_classes")
        
     if  students_of_all_classes.objects.filter(rollno=rollno).exists():
       messages.error(request, "Roll number already exists")
       return redirect("view_students_of_all_classes")
     user_added_or_not.objects.get_or_create(user=user_name)
     students_of_all_classes.objects.create(user=user_name,rollno=rollno,s1stname=s1stname,slstname=slstname,cname=cname,gender=gender,address=address,contact_no=contact_no,age=age,father_1stname=father_1stname,father_lstname=father_lstname)
     messages.success(request,"student is added successfully")
     return redirect("view_students_of_all_classes")
     
     
        
    else:
          response=render(request,"add_student.html")
          return response
def view_students_of_all_classes(request):
    vs=students_of_all_classes.objects.all()
    response=render(request,"manage_student_of_all_classes.html",context={"vs":vs})
    return response
def update_students_of_all_classes(request):
    
    if request.method=="POST":
            rollno=request.POST.get("rollno")
            s1stname=request.POST.get("s1stname")
            slstname=request.POST.get("slstname")
            cname=request.POST.get("cname")
            gender=request.POST.get("gender")
            address=request.POST.get("address")
            contact_no=request.POST.get("contact_no")
            age=request.POST.get("age")
            father_1stname=request.POST.get("father_1stname")
            father_lstname=request.POST.get("father_lstname")
            

            try:
                #update Teacher by student id
                su=students_of_all_classes.objects.get(rollno=rollno)
                #update only field which are filled
                if s1stname:
                  su.s1stname=s1stname
                if slstname:
                  su.slstname=slstname
                if cname:
                  su.cname=cname
                if gender:
                  su.gender=gender
                if address:
                  su.address=address
                if contact_no:
                  su.contact_no=contact_no
               
                if age:
                  su.age=age
                if father_1stname:
                    su.father_1stname=father_1stname
                if father_lstname:
                    su.father_lstname=father_lstname
                #save update records of students
                su.save()
                messages.success(request,"students record updated successfully")
                return redirect("view_students_of_all_classes")
                
            except students_of_all_classes.DoesNotExist:
                messages.error(request,"Given student Id is not found")
                return redirect("view_students_of_all_classes")
            
    
def delete_students_of_all_classes(request):
    
    if request.method=="POST":
        try:
         rollno=request.POST.get('rollno')
         sd=students_of_all_classes.objects.get(rollno=rollno)
         sd.delete()
         messages.success(request,"Student is deleted successfully")
         return redirect("view_students_of_all_classes")
        except students_of_all_classes.DoesNotExist:
            messages.error(request,"Invalid Student Id")
            return redirect("view_students_of_all_classes")
def search_student(request):
   result=None
   if request.method=="POST":
      q= request.POST.get('q')
      if (q>="a" and q<="z") or  (q>="A" and q<="Z"):
        messages.error(request,"Student id must be a number")
        return redirect("view_students_of_all_classes")
      if q and students_of_all_classes.objects.filter(rollno=q).exists():
          result = students_of_all_classes.objects.filter(rollno=q)
          response=render(request, 'search_student.html', {'vs': result})
          return response
      else:
             messages.error(request,"Invalid student id")
             return redirect("view_students_of_all_classes")

   else:
        response=render(request,"search_student.html")
        return response
   
def search_page_delete_error(request):
    if request.method=="POST":
        try:
         rollno=request.POST.get('rollno')
         if (rollno>="a" and rollno<="z") or (rollno>="A" and rollno<="Z"):
          messages.error(request,"Student id Must contain numeric value in delete form")
          return redirect("search_student")
         else:
          sd=students_of_all_classes.objects.get(rollno=rollno)
          sd.delete()
          messages.success(request,"Student is deleted successfully")
          return redirect("search_student")
        except students_of_all_classes.DoesNotExist:
            messages.error(request,"Invalid Student Id")
            return redirect("search_student")
def search_page_update_error(request):
    if request.method=="POST":
            rollno=request.POST.get("rollno")
            if (rollno>="a" and rollno<="z") or (rollno>="A" and rollno<="Z"):
                   messages.error(request,"Student id Must be a number in update form")
                   return redirect("search_student")
            s1stname=request.POST.get("s1stname")
            slstname=request.POST.get("slstname")
            cname=request.POST.get("cname")
            gender=request.POST.get("gender")
            address=request.POST.get("address")
            contact_no=request.POST.get("contact_no")
            email=request.POST.get("email")
            age=request.POST.get("age")
            father_1stname=request.POST.get("father_1stname")
            father_lstname=request.POST.get("father_lstname")
            

            try:
                #update Teacher by student id
                su=students_of_all_classes.objects.get(rollno=rollno)
                
                #update only field which are filled
                if s1stname:
                  su.s1stname=s1stname
                if slstname:
                  su.slstname=slstname
                if cname:
                  su.cname=cname
                if gender:
                  su.gender=gender
                if address:
                  su.address=address
                if contact_no:
                  su.contact_no=contact_no
                if email:
                  su.email=email
                if age:
                  su.age=age
                if father_1stname:
                    su.father_1stname=father_1stname
                if father_lstname:
                    su.father_lstname=father_lstname
                #save update records of students
                su.save()
                messages.success(request,"students record updated successfully")
                return redirect("search_student")
                
            except students_of_all_classes.DoesNotExist:
                messages.error("Given student Id not found")
            return redirect("search_student")
            
    
#for subjests
def add_subjects(request):
    if request.method=="POST":
        sub_id=request.POST.get("sub_id")
        sub_name=request.POST.get("sub_name")
        if sub_name=="" or sub_id=="":
           messages.error(request,"Both subject id and subject name is required")
           return redirect("manage_subjects")
        sub=subject(sub_id=sub_id,sub_name=sub_name)
        sub.save()
        messages.success(request,"Subject has been added successfuly")
        return redirect("manage_subjects")
    else:
        messages.error(request,"Subject id is already exists")
        return redirect("manage_subjects")
def view_subjects(request):
        qs=subject.objects.all()
        response=render(request,"manage_subjects.html",context={"qs":qs})
        return response
   



def delete_subjects(request):
    if request.method=="POST":
        sub_id=request.POST.get("sub_id")
        if sub_id=="":
           messages.error(request,"To delete subject, subject id is required")
           return redirect("manage_subjects")
        try:
         sd=subject.objects.filter(sub_id=sub_id)
         sd.delete()
         messages.success(request,"Subject is deleted")
         return redirect("manage_subjects")
        except:
           messages.error(request,"Invalid Subject id")
           return redirect("manage_subjects")
    else:
         qs=subject.objects.all()
         response=render(request,"manage_subjects.html",context={'qs':qs})
         return response
    
def update_subjects(request):
     if request.method=="POST":
        sub_id=request.POST.get("sub_id")
        sub_name=request.POST.get("sub_name")
        if sub_id=="" or sub_name=="":
           messages.error(request,"Each field is required for updation")
           return redirect("manage_subjects")
        try:
          sd=subject.objects.get(sub_id=sub_id)
      
          sd.sub_name=sub_name
          sd.save()
          messages.success(request,"subject Name updated successfully")
          return redirect("manage_subjects")
        except:
             messages.error(request,"Invalid teacher id")
            
             return redirect("manage_subjects")

     else:
          qs=subject.objects.all()
          response=render(request,"manage_subjects.html",{"qs":qs})
          return response
         










#admin views(attendance)
def view_student_attendance(request):
    vas=student_check_indivisually_absent_present_taken_by_teacher.objects.all()
    response=render(request,"view_student_attendance.html",context={"vas":vas})
    return response
def delete_student_attendance(request):
    if request.method=="POST":
        rollno=request.POST.get('rollno')
        if rollno=="":
            messages.success(request,"Student rollno is required")
            return redirect("view_student_attendance")
           
        if student_check_indivisually_absent_present_taken_by_teacher.objects.filter(srollno=rollno).exists():
         qs=student_check_indivisually_absent_present_taken_by_teacher.objects.filter(srollno=rollno)
         qs.delete()
         messages.success(request,"Student's attendance is successfully deleted")
      
         return redirect("view_student_attendance")
        else:
           messages.error(request,"Invalid student rollno")
           return redirect("view_student_attendance")
#student leave views
def view_student_leave(request):
    vsl=leave_for_students.objects.all()
    response=render(request,"view_student_leave.html",context={"vsl":vsl})
    return response
def student_apply_leave(request):
    if request.method=="POST":
        rollno_id=request.POST.get('rollno_id')
        sname=request.POST.get('sname')
        ph_no=request.POST.get(ph_no)
        leave_reason=request.POST.get("leave_reason")
        date_of_apply=request.POST.get("date_of_apply")
        accept1_or_reject=request.POST.get('accept1_or_reject')
        leave=leave_for_students(rollno_id=rollno_id,sname=sname,ph_no=ph_no,leave_reason=leave_reason,date_of_apply=date_of_apply,accept1_or_reject=accept1_or_reject)
        leave.save()
    else:
        response=render(request,"student_apply_leave.html")
        return response
def update_admin_reply_for_student_leave(request):
    if request.method=="POST":
        
        date_of_apply=request.POST.get("date_of_apply")
        accept1_or_reject=request.POST.get('accept1_or_reject')
        try:
            leave1=leave_for_students.objects.filter(date_of_apply=date_of_apply)
            #update status using model instance
            if date_of_apply:
                leave1.date_of_apply=date_of_apply
            if date_of_apply:
                leave1.accept1_or_reject=accept1_or_reject
                leave1.save()
        except:
            message_fail="Invalid Date"
            response=render(request,"view_student_leave.html",context={'message_fail':message_fail})
            return response
def delete_student_leave_history(request):
    if request.method=="POST":
        date_of_apply=request.POST.get("date_of_apply")
        leave1=leave_for_students.objects.filter(date_of_apply=date_of_apply)
        leave1.delete()
        response=render(request,"view_student_leave.html")
        return response
#teacher leave views
def view_teacher_leave(request):
    vtl=leave_for_teachers.objects.all()
    response=render(request,"view_teacher_leave.html",context={"vtl":vtl})
    return response
#student check attendance indivisually


def view_attendance_teacher(request):
    sat=attendance_teacher.objects.all()
    response=render(request,"view_attendance_teacher.html",context={"vas":sat})
    return response
#view student feedback
def view_student_feedback(request):
    vsf=feedback_student.objects.all()
    response=render(request,"view_student_feedback.html",context={"vas":vsf})
    return response
def delete_student_feedback(request):
    
    if request.method=="POST":
        try:
         qs=request.POST.get("semail")
         dsf=feedback_student.objects.get(semail=qs)
         dsf.delete()
         messages.success(request,"Student feedback is deleted successfully")
         return redirect("view_student_feedback")
        except:
            messages.error(request,"Invalid Email ID")
            return redirect("view_student_feedback")

    else:
        response=render(request,"view_student_feedback.html")
        return response
def view_teacher_feedback(request):
    vtf=feedback_teacher.objects.all()
    response=render(request,"view_teacher_feedback.html",context={"vtf":vtf})
    return response
@permission_required('app1.delete_student')
def delete_teacher_feedback(request,semail):
    dtf=get_object_or_404(feedback_student,semail=semail)
    if request.method=="POST":
        dtf.delete()
        return redirect("view_student_feedback")
    else:
        response=render(request,"view_student_feedback.html",context={"dtf":dtf})
        return response

#views for teacher dashboard
#teacher take attendance
def teachers_manage_all_class_attendance(request):
   response=render(request,"classwise_attendance_taken.html")
   return response

def take_all_class_student_attendance(request):
   
    if request.method=="GET":
     cname=request.GET.get("cname")
     print(cname)
     students=students_of_all_classes.objects.filter(cname=cname)
     response=render(request,"take_class1_attendance_sheet.html",context={'students':students,'cname':cname})
     return response
     
    
    elif request.method == "POST":
        cname = request.POST.get("cname")
        students = students_of_all_classes.objects.filter(cname=cname)
        
        for student in students:
            current_status = request.POST.get(f"status_{student.rollno}")

            if not current_status:
                messages.error(request, "Please fill current status of each student")

                return render(
                    request,
                    "take_class1_attendance_sheet.html",
                    {"students": students}
                )
            if not student_check_indivisually_absent_present_taken_by_teacher.objects.filter(srollno=student,date=date.today()).exists():
            
               student_check_indivisually_absent_present_taken_by_teacher.objects.create(srollno=student,status=current_status )
               
            else:
               messages.error(request,f"Students of class {cname} attendance records are already added")
               return render(request,"take_class1_attendance_sheet.html",context={"students":students,"cname":cname})
        messages.success(request,f"Students of class {cname} attendance records are successfully added")
        return render(request,"take_class1_attendance_sheet.html",context={"students":students,"cname":cname})           
    
        
def dispaly_attendance(request):
    qs=student_check_indivisually_absent_present_taken_by_teacher.objects.all()
    response=render(request,"display_attendance.html",context={"qs":qs})
    return response


#manage student result of class1
def manage_all_classes_student_result(request):
   response=render(request,"manage_all_classes_student_result.html")
   return response
def show_student_details_for_adding_mark_class1(request):
   
   if request.method=="POST":
      rollno=request.POST.get("rollno")
      if students_of_all_classes.objects.filter(rollno=rollno).exists():
         qs=students_of_all_classes.objects.get(rollno=rollno)
         if not  result_of_all_classes_annual.objects.filter(rollno=qs).exists():
          pass
         else:
            messages.error(request,"This student mark  is already added")
         if qs.cname=="one":
            
            response=render(request,"manage_all_classes_student_result.html",context={"qs":qs,"c1":"*"})
            return response
        
         elif qs.cname=="two":
            response=render(request,"manage_all_classes_student_result.html",context={"qs":qs,"c2":"*"})
            return response
         elif qs.cname=="three":
            response=render(request,"manage_all_classes_student_result.html",context={"qs":qs,"c3":"*"})
            return response
         elif qs.cname=="four":
            response=render(request,"manage_all_classes_student_result.html",context={"qs":qs,"c4":"*"})
            return response
         elif qs.cname=="five":
            response=render(request,"manage_all_classes_student_result.html",context={"qs":qs,"c5":"*"})
            return response
         elif qs.cname=="six":
            response=render(request,"manage_all_classes_student_result.html",context={"qs":qs,"c6":"*"})
            return response
         elif qs.cname=="seven":
            response=render(request,"manage_all_classes_student_result.html",context={"qs":qs,"c7":"*"})
            return response
         elif qs.cname=="eight":
            response=render(request,"manage_all_classes_student_result.html",context={"qs":qs,"c8":"*"})
            return response
         elif qs.cname=="nine":
            response=render(request,"manage_all_classes_student_result.html",context={"qs":qs,"c9":"*"})
            return response
         elif qs.cname=="ten":
            response=render(request,"manage_all_classes_student_result.html",context={"qs":qs,"c10":"*"})
            return response
         else:
            messages.error(request,"You entered invalid rollno")
            response=render(request,"manage_all_classes_student_result.html")
            return response

         
      else:
         messages.error(request,"You entered invalid rollno")
         response=render(request,"manage_all_classes_student_result.html")
         return response
         
      
   else:
      response=render(request,"manage_all_classes_student_result.html")
      return response
      
     


def show_student_details_and_updating_mark_class1(request):
    if request.method == "POST":

        rollno = request.POST.get("rollno")
        
        if not rollno:
            messages.error(request, "Please enter roll number")
            return render(request, "manage_all_classes_student_result.html")

        if not students_of_all_classes.objects.filter(rollno=rollno).exists():
            messages.error(request, "Entered Student rollno  not found")
            return render(request, "manage_all_classes_student_result.html")
        if not result_of_all_classes_annual.objects.filter(rollno=rollno).exists():
            messages.error(request, "Entered Student rollno  not found")
            return render(request, "manage_all_classes_student_result.html")
        qs=students_of_all_classes.objects.get(rollno=rollno)


        if qs.cname=="one":

            qs1 = result_of_all_classes_annual.objects.get(rollno=rollno)
            return render(request,"manage_all_classes_student_result.html",context={"qs1": qs1,"c1":"*"})
        elif qs.cname=="two":
           qs1 = result_of_all_classes_annual.objects.get(rollno=rollno)
           return render(request,"manage_all_classes_student_result.html",context={"qs1": qs1,"c2":"*"})
        elif qs.cname=="three":
           qs1 = result_of_all_classes_annual.objects.get(rollno=rollno)
           return render(request,"manage_all_classes_student_result.html",context={"qs1": qs1,"c3":"*"})
        elif qs.cname=="four":
           qs1 = result_of_all_classes_annual.objects.get(rollno=rollno)
           return render(request,"manage_all_classes_student_result.html",context={"qs1": qs1,"c4":"*"})
        elif qs.cname=="five":
           qs1 = result_of_all_classes_annual.objects.get(rollno=rollno)
           return render(request,"manage_all_classes_student_result.html",context={"qs1": qs1,"c5":"*"})
        elif qs.cname=="six":
           qs1 = result_of_all_classes_annual.objects.get(rollno=rollno)
           return render(request,"manage_all_classes_student_result.html",context={"qs1": qs1,"c6":"*"})
        elif qs.cname=="seven":
           qs1 = result_of_all_classes_annual.objects.get(rollno=rollno)
           return render(request,"manage_all_classes_student_result.html",context={"qs1": qs1,"c7":"*"})
        elif qs.cname=="eight":
           qs1 = result_of_all_classes_annual.objects.get(rollno=rollno)
           return render(request,"manage_all_classes_student_result.html",context={"qs1": qs1,"c8":"*"})
        elif qs.cname=="nine":
           qs1 = result_of_all_classes_annual.objects.get(rollno=rollno)
           return render(request,"manage_all_classes_student_result.html",context={"qs1": qs1,"c9":"*"})
        elif qs.cname=="ten":
           qs1 = result_of_all_classes_annual.objects.get(rollno=rollno)
           return render(request,"manage_all_classes_student_result.html",context={"qs1": qs1,"c10":"*"})
                 
    return render(request, "manage_all_classes_student_result.html")
   
   
def add_class1_student_result(request):
    
    if  request.method=="POST":
        rollno=request.POST.get("rollno","").strip()
        cname=request.POST.get("cname","").strip()
        seesion_year=request.POST.get("seesion_year","").strip()
        math=request.POST.get("math","").strip()
        drawing= request.POST.get("drawing","").strip()
        project=request.POST.get("project","").strip()
        english=request.POST.get("english","").strip()
        rime=request.POST.get("rime","").strip()
        science=request.POST.get("science","").strip()
        hindi=request.POST.get("hindi","").strip()
        life_science=request.POST.get("life_science","").strip()
        physical_science=request.POST.get("physical_science","").strip()
        Algebra_math=request.POST.get("Algebra_math","").strip()
        history=request.POST.get("history","").strip()
        geometry_math=request.POST.get("geometry_math","").strip()
        geography=request.POST.get("geography","").strip()
        Polity=request.POST.get("Polity","").strip()
        exam_name=request.POST.get("exam_name")
        if students_of_all_classes.objects.filter(rollno=rollno).exists():
           qs=students_of_all_classes.objects.get(rollno=rollno)
           if qs.cname=="one":
              if seesion_year:
               pass
              if exam_name:
                pass
           
              if math:
               if int(math)>=1 and int(math)<=100 :
                  pass
               else:
                 messages.error(request,"Fill required field between(1 to 100)")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
              else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
              if drawing:
                   if int(drawing)>=1 and int(drawing)<=100:
                    pass
         
                   else:
                        messages.error(request,"Fill required field between(1 to 100)")
                        response=render(request,"manage_all_classes_student_result.html")
                        return response
         
              else:
               messages.error(request,"Fill required field between(1 to 100)")
               response=render(request,"manage_all_classes_student_result.html")
               return response
           
              if project:
                 if int(project)>=1 and int(project)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
           
              if english:
               if int(english)>=1 and int(english)<=100:
                pass
               else:
                 messages.error(request,"Fill required field between(1 to 100)")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
              else:
               messages.error(request,"Fill required field between(1 to 100)")
               response=render(request,"manage_all_classes_student_result.html")
               return response
           
        
              if rime:
               if int(rime)>=1 and int(rime)<=100:
                pass
               else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                messages.error(request,"Fill required field between(1 to 100)")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              if history or geography or science or Polity or Algebra_math   or life_science or physical_science or geometry_math:
                 messages.error(request,"You filled unwanted fields")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              if result_of_all_classes_annual.objects.filter(rollno=qs).exists():
                messages.error(request,"This student mark is already added")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              else:
        
               result_of_all_classes_annual.objects.create(rollno=qs,cname=cname,seesion_year=seesion_year,exam_name=exam_name,rime=rime,english=english,project=project,drawing=drawing,math=math,hindi=hindi)
               messages.success(request,"Student mark added successfully")
               response=render(request,"manage_all_classes_student_result.html")
              return response
           #for class-2
           if qs.cname=="two":
              if seesion_year:
               pass
              if exam_name:
                pass
           
              if math:
               if int(math)>=1 and int(math)<=100 :
                  pass
               else:
                 messages.error(request,"Fill required field between(1 to 100)")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
              else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
              if drawing:
                   if int(drawing)>=1 and int(drawing)<=100:
                    pass
         
                   else:
                        messages.error(request,"Fill required field between(1 to 100)")
                        response=render(request,"manage_all_classes_student_result.html")
                        return response
         
              else:
               messages.error(request,"Fill required field between(1 to 100)")
               response=render(request,"manage_all_classes_student_result.html")
               return response
           
              if project:
                 if int(project)>=1 and int(project)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
           
              if english:
               if int(english)>=1 and int(english)<=100:
                pass
               else:
                 messages.error(request,"Fill required field between(1 to 100)")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
              else:
               messages.error(request,"Fill required field between(1 to 100)")
               response=render(request,"manage_all_classes_student_result.html")
               return response
           
        
              if rime:
               if int(rime)>=1 and int(rime)<=100:
                pass
               else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                messages.error(request,"Fill required field between(1 to 100)")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              if history or geography or science or Polity or Algebra_math   or life_science or physical_science or geometry_math:
                 messages.error(request,"You filled unwanted fields")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              if result_of_all_classes_annual.objects.filter(rollno=qs).exists():
                messages.error(request,"This student mark is already added")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              else:
        
               result_of_all_classes_annual.objects.create(rollno=qs,cname=cname,seesion_year=seesion_year,exam_name=exam_name,rime=rime,english=english,project=project,drawing=drawing,math=math,hindi=hindi)
               messages.success(request,"Student mark added successfully")
               response=render(request,"manage_all_classes_student_result.html")
              return response 
           #for class-3
           if qs.cname=="three":
              if seesion_year:
               pass
              if exam_name:
                pass
           
              if math:
               if int(math)>=1 and int(math)<=100 :
                  pass
               else:
                 messages.error(request,"Fill required field between(1 to 100)")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
              else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
              
           
              if project:
                 if int(project)>=1 and int(project)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
           
              if english:
               if int(english)>=1 and int(english)<=100:
                pass
               else:
                 messages.error(request,"Fill required field between(1 to 100)")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
              else:
               messages.error(request,"Fill required field between(1 to 100)")
               response=render(request,"manage_all_classes_student_result.html")
               return response
           
        
              if rime:
               if int(rime)>=1 and int(rime)<=100:
                pass
               else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                messages.error(request,"Fill required field between(1 to 100)")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              if science:
               if int(science)>=1 and int(science)<=100:
                pass
               else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                messages.error(request,"Fill required field between(1 to 100)")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              
              if history or geography or drawing  or Polity or Algebra_math   or life_science or physical_science or geometry_math:
                 messages.error(request,"You filled unwanted fields")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              if result_of_all_classes_annual.objects.filter(rollno=qs).exists():
                messages.error(request,"This student mark is already added")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              else:
        
               result_of_all_classes_annual.objects.create(rollno=qs,cname=cname,science=science,seesion_year=seesion_year,exam_name=exam_name,rime=rime,english=english,project=project,math=math,hindi=hindi)
               messages.success(request,"Student mark added successfully")
               response=render(request,"manage_all_classes_student_result.html")
              return response
            #for class4
           if qs.cname=="four":
              if seesion_year:
               pass
              if exam_name:
                pass
           
              if math:
               if int(math)>=1 and int(math)<=100 :
                  pass
               else:
                 messages.error(request,"Fill required field between(1 to 100)")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
              else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
              
           
              if project:
                 if int(project)>=1 and int(project)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
           
              if english:
               if int(english)>=1 and int(english)<=100:
                pass
               else:
                 messages.error(request,"Fill required field between(1 to 100)")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
              else:
               messages.error(request,"Fill required field between(1 to 100)")
               response=render(request,"manage_all_classes_student_result.html")
               return response
           
        
              
              if science:
               if int(science)>=1 and int(science)<=100:
                pass
               else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                messages.error(request,"Fill required field between(1 to 100)")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              if hindi:
               if int(hindi)>=1 and int(hindi)<=100:
                pass
               else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                messages.error(request,"Fill required field between(1 to 100)")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              if history or geography  or drawing or Polity or Algebra_math   or life_science or physical_science or geometry_math or rime:
                 messages.error(request,"You filled unwanted fields")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              if result_of_all_classes_annual.objects.filter(rollno=qs).exists():
                messages.error(request,"This student mark is already added")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              else:
        
               result_of_all_classes_annual.objects.create(rollno=qs,cname=cname,science=science,seesion_year=seesion_year,exam_name=exam_name,english=english,project=project,math=math,hindi=hindi)
               messages.success(request,"Student mark added successfully")
               response=render(request,"manage_all_classes_student_result.html")
              return response
           
            #class five
           if qs.cname=="five":
              if seesion_year:
               pass
              if exam_name:
                pass
           
              if math:
               if int(math)>=1 and int(math)<=100 :
                  pass
               else:
                 messages.error(request,"Fill required field between(1 to 100)")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
              else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
              
           
              if project:
                 if int(project)>=1 and int(project)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
           
              if english:
               if int(english)>=1 and int(english)<=100:
                pass
               else:
                 messages.error(request,"Fill required field between(1 to 100)")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
              else:
               messages.error(request,"Fill required field between(1 to 100)")
               response=render(request,"manage_all_classes_student_result.html")
               return response
              if hindi:
               if int(hindi)>=1 and int(hindi)<=100:
                pass
               else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                messages.error(request,"Fill required field between(1 to 100)")
                response=render(request,"manage_all_classes_student_result.html")
                return response
        
              
              if science:
               if int(science)>=1 and int(science)<=100:
                pass
               else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                messages.error(request,"Fill required field between(1 to 100)")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              if history or geography  or drawing or Polity or Algebra_math   or life_science or physical_science or geometry_math:
                 messages.error(request,"You filled unwanted fields")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              if result_of_all_classes_annual.objects.filter(rollno=qs).exists():
                messages.error(request,"This student mark is already added")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              else:
        
               result_of_all_classes_annual.objects.create(rollno=qs,cname=cname,science=science,seesion_year=seesion_year,exam_name=exam_name,english=english,project=project,math=math,hindi=hindi)
               messages.success(request,"Student mark added successfully")
               response=render(request,"manage_all_classes_student_result.html")
              return response
           #for class 6
           if qs.cname=="six":
              if seesion_year:
               pass
              if exam_name:
                pass
           
              if math:
               if int(math)>=1 and int(math)<=100 :
                  pass
               else:
                 messages.error(request,"Fill required field between(1 to 100)")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
              else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
              
           
              if project:
                 if int(project)>=1 and int(project)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
           
              if english:
               if int(english)>=1 and int(english)<=100:
                pass
               else:
                 messages.error(request,"Fill required field between(1 to 100)")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
              else:
               messages.error(request,"Fill required field between(1 to 100)")
               response=render(request,"manage_all_classes_student_result.html")
               return response
           
        
              if history:
               if int(history)>=1 and int(history)<=100:
                pass
               else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                messages.error(request,"Fill required field between(1 to 100)")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              if geography:
               if int(geography)>=1 and int(geography)<=100:
                pass
               else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                messages.error(request,"Fill required field between(1 to 100)")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              if science:
               if int(science)>=1 and int(science)<=100:
                pass
               else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                messages.error(request,"Fill required field between(1 to 100)")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              if rime  or drawing or Polity or Algebra_math   or life_science or physical_science or geometry_math:
                 messages.error(request,"You filled unwanted fields")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              if result_of_all_classes_annual.objects.filter(rollno=qs).exists():
                messages.error(request,"This student mark is already added")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              else:
        
               result_of_all_classes_annual.objects.create(rollno=qs,cname=cname,science=science,seesion_year=seesion_year,exam_name=exam_name,history=history,geography=geography,english=english,project=project,math=math,hindi=hindi)
               messages.success(request,"Student mark added successfully")
               response=render(request,"manage_all_classes_student_result.html")
              return response
            #class7
           if qs.cname=="seven":
              if seesion_year:
               pass
              if exam_name:
                pass
           
              if math:
               if int(math)>=1 and int(math)<=100 :
                  pass
               else:
                 messages.error(request,"Fill required field between(1 to 100)")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
              else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
              
           
              if project:
                 if int(project)>=1 and int(project)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
           
              if english:
               if int(english)>=1 and int(english)<=100:
                pass
               else:
                 messages.error(request,"Fill required field between(1 to 100)")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
              else:
               messages.error(request,"Fill required field between(1 to 100)")
               response=render(request,"manage_all_classes_student_result.html")
               return response
           
        
              if history:
               if int(history)>=1 and int(history)<=100:
                pass
               else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                messages.error(request,"Fill required field between(1 to 100)")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              if geography:
               if int(geography)>=1 and int(geography)<=100:
                pass
               else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                messages.error(request,"Fill required field between(1 to 100)")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              if science:
               if int(science)>=1 and int(science)<=100:
                pass
               else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                messages.error(request,"Fill required field between(1 to 100)")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              if rime  or drawing or Polity or Algebra_math   or life_science or physical_science or geometry_math:
                 messages.error(request,"You filled unwanted fields")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              if result_of_all_classes_annual.objects.filter(rollno=qs).exists():
                messages.error(request,"This student mark is already added")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              else:
        
               result_of_all_classes_annual.objects.create(rollno=qs,cname=cname,science=science,seesion_year=seesion_year,exam_name=exam_name,history=history,geography=geography,english=english,project=project,math=math,hindi=hindi)
               messages.success(request,"Student mark added successfully")
               response=render(request,"manage_all_classes_student_result.html")
              return response
            #for class 8
           if qs.cname=="eight":
              if seesion_year:
               pass
              if exam_name:
                pass
              
           
              if project:
                 if int(project)>=1 and int(project)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              if life_science:
                 if int(life_science)>=1 and int(life_science)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              
              
              if Algebra_math:
                 if int(Algebra_math)>=1 and int(Algebra_math)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              if Polity:
                 if int(Polity)>=1 and int(Polity)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              if geometry_math:
                 if int(geometry_math)>=1 and int(geometry_math)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              if physical_science:
                 if int(physical_science)>=1 and int(physical_science)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
           
              if english:
               if int(english)>=1 and int(english)<=100:
                pass
               else:
                 messages.error(request,"Fill required field between(1 to 100)")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
              else:
               messages.error(request,"Fill required field between(1 to 100)")
               response=render(request,"manage_all_classes_student_result.html")
               return response
           
        
              if history:
               if int(history)>=1 and int(history)<=100:
                pass
               else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                messages.error(request,"Fill required field between(1 to 100)")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              if geography:
               if int(geography)>=1 and int(geography)<=100:
                pass
               else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                messages.error(request,"Fill required field between(1 to 100)")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              
              if rime or science or drawing or math :
                 messages.error(request,"You filled unwanted fields")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              if result_of_all_classes_annual.objects.filter(rollno=qs).exists():
                messages.error(request,"This student mark is already added")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              else:
        
               result_of_all_classes_annual.objects.create(rollno=qs,cname=cname,seesion_year=seesion_year,exam_name=exam_name,life_science=life_science,physical_science=physical_science,geometry_math=geometry_math,Polity=Polity,history=history,geography=geography,english=english,project=project,Algebra_math=Algebra_math,hindi=hindi)
               messages.success(request,"Student mark added successfully")
               response=render(request,"manage_all_classes_student_result.html")
              return response
           #for claas9
           if qs.cname=="nine":
              if seesion_year:
               pass
              if exam_name:
                pass
              if project:
                 if int(project)>=1 and int(project)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              if life_science:
                 if int(life_science)>=1 and int(life_science)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              
              
              if Algebra_math:
                 if int(Algebra_math)>=1 and int(Algebra_math)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              if Polity:
                 if int(Polity)>=1 and int(Polity)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              if geometry_math:
                 if int(geometry_math)>=1 and int(geometry_math)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              if physical_science:
                 if int(physical_science)>=1 and int(physical_science)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
           
              if english:
               if int(english)>=1 and int(english)<=100:
                pass
               else:
                 messages.error(request,"Fill required field between(1 to 100)")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
              else:
               messages.error(request,"Fill required field between(1 to 100)")
               response=render(request,"manage_all_classes_student_result.html")
               return response
           
        
              if history:
               if int(history)>=1 and int(history)<=100:
                pass
               else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                messages.error(request,"Fill required field between(1 to 100)")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              if geography:
               if int(geography)>=1 and int(geography)<=100:
                pass
               else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                messages.error(request,"Fill required field between(1 to 100)")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              
              if rime or science or drawing or math :
                 messages.error(request,"You filled unwanted fields")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              if result_of_all_classes_annual.objects.filter(rollno=qs).exists():
                messages.error(request,"This student mark is already added")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              else:
        
               result_of_all_classes_annual.objects.create(rollno=qs,seesion_year=seesion_year,cname=cname,exam_name=exam_name,life_science=life_science,physical_science=physical_science,geometry_math=geometry_math,Polity=Polity,history=history,geography=geography,english=english,project=project,Algebra_math=Algebra_math,hindi=hindi)
               messages.success(request,"Student mark added successfully")
               response=render(request,"manage_all_classes_student_result.html")
              return response
            #for class10
           if qs.cname=="ten":
              if seesion_year:
               pass
              if exam_name:
                pass
              if project:
                 if int(project)>=1 and int(project)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              if life_science:
                 if int(life_science)>=1 and int(life_science)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              
              
              if Algebra_math:
                 if int(Algebra_math)>=1 and int(Algebra_math)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              if Polity:
                 if int(Polity)>=1 and int(Polity)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              if geometry_math:
                 if int(geometry_math)>=1 and int(geometry_math)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              if physical_science:
                 if int(physical_science)>=1 and int(physical_science)<=100:
                   pass
                 else:
                  messages.error(request,"Fill required field between(1 to 100) ")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                 messages.error(request,"Fill required field between(1 to 100) ")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
           
              if english:
               if int(english)>=1 and int(english)<=100:
                pass
               else:
                 messages.error(request,"Fill required field between(1 to 100)")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
         
              else:
               messages.error(request,"Fill required field between(1 to 100)")
               response=render(request,"manage_all_classes_student_result.html")
               return response
           
        
              if history:
               if int(history)>=1 and int(history)<=100:
                pass
               else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                messages.error(request,"Fill required field between(1 to 100)")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              if geography:
               if int(geography)>=1 and int(geography)<=100:
                pass
               else:
                  messages.error(request,"Fill required field between(1 to 100)")
                  response=render(request,"manage_all_classes_student_result.html")
                  return response
         
              else:
                messages.error(request,"Fill required field between(1 to 100)")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              
         
              
              if rime or science or drawing or math :
                 messages.error(request,"You filled unwanted fields")
                 response=render(request,"manage_all_classes_student_result.html")
                 return response
              if result_of_all_classes_annual.objects.filter(rollno=qs).exists():
                messages.error(request,"This student mark is already added")
                response=render(request,"manage_all_classes_student_result.html")
                return response
              else:
        
               result_of_all_classes_annual.objects.create(rollno=qs,cname=cname,seesion_year=seesion_year,exam_name=exam_name,life_science=life_science,physical_science=physical_science,geometry_math=geometry_math,Polity=Polity,history=history,geography=geography,english=english,project=project,Algebra_math=Algebra_math,hindi=hindi)
               messages.success(request,"Student mark added successfully")
               response=render(request,"manage_all_classes_student_result.html")
              return response
           
            
              
              
        else:
           messages.error(request,"invalid student rollno")
           response=render(request,"manage_all_classes_student_result.html")
           return response

        
    else:
      qs=students_of_all_classes.objects.all()
      response=render(request,"manage_all_classes_student_result.html",context={"qs":qs})
      return response 
     
def update_class1_student_result(request):
   if request.method=="POST":
      rollno=request.POST.get("rollno","").strip()
      math=request.POST.get("math","").strip()
      english=request.POST.get("english","").strip()
      rime=request.POST.get("rime","").strip()
      drawing=request.POST.get("drawing","").strip()
      project=request.POST.get("project","").strip()
      science=request.POST.get("science","").strip()
      hindi=request.POST.get("hindi","").strip()
      life_science=request.POST.get("life_science","").strip()
      physical_science=request.POST.get("physical_science","").strip()
      Algebra_math=request.POST.get("Algebra_math","").strip()
      history=request.POST.get("history","").strip()
      geometry_math=request.POST.get("geometry_math","").strip()
      geography=request.POST.get("geography","").strip()
      Polity=request.POST.get("Polity","").strip()
      qs3=result_of_all_classes_annual.objects.get(rollno=rollno)
      if qs3.rollno.cname=="one":
         if life_science or physical_science or Polity or Algebra_math or geometry_math or geography or history or science:
            messages.error(request,"You filled unwanted field")
            response=render(request,"manage_all_classes_student_result.html",context={"qs3":qs3})
            return response 
         else:
            
            qs3.project=project
            qs3.math=math
            qs3.drawing=drawing
            qs3.english=english
            qs3.hindi=hindi
            qs3.rime=rime
            qs3.save()
      if qs3.rollno.cname=="two":
         if life_science or physical_science or Polity or Algebra_math or geometry_math or geography or history or science:
            messages.error(request,"You filled unwanted field")
            response=render(request,"manage_all_classes_student_result.html",context={"qs3":qs3})
            return response 
         else:
            qs3.project=project
            qs3.math=math
            qs3.drawing=drawing
            qs3.english=english
            qs3.hindi=hindi
            qs3.rime=rime
            qs3.save()
      if qs3.rollno.cname=="three":
         if life_science or physical_science or drawing or Polity or Algebra_math or geometry_math or geography or history :
            messages.error(request,"You filled unwanted field")
            response=render(request,"manage_all_classes_student_result.html",context={"qs3":qs3})
            return response 
         else:
            qs3.project=project
            qs3.math=math
            qs3.science=science
            qs3.english=english
            qs3.hindi=hindi
            qs3.rime=rime
            qs3.save()
      if qs3.rollno.cname=="four":
         if life_science or physical_science or drawing or Polity or Algebra_math or geometry_math or geography or history :
            messages.error(request,"You filled unwanted field")
            response=render(request,"manage_all_classes_student_result.html",context={"qs3":qs3})
            return response 
         else:
            qs3.project=project
            qs3.math=math
            qs3.science=science
            qs3.english=english
            qs3.hindi=hindi
            qs3.rime=rime
            qs3.save()
      if qs3.rollno.cname=="five":
         if life_science or rime or  physical_science or Polity or Algebra_math or geometry_math or geography or history :
            messages.error(request,"You filled unwanted field")
            response=render(request,"manage_all_classes_student_result.html",context={"qs3":qs3})
            return response 
         else:
            qs3.project=project
            qs3.math=math
            qs3.science=science
            qs3.english=english
            qs3.hindi=hindi
            qs3.rime=rime
            qs3.save()
      if qs3.rollno.cname=="six":
         if life_science or physical_science or Polity or Algebra_math or geometry_math or rime or drawing :
            messages.error(request,"You filled unwanted field")
            response=render(request,"manage_all_classes_student_result.html",context={"qs3":qs3})
            return response 
         else:
            qs3.project=project
            qs3.math=math
            qs3.science=science
            qs3.history=history
            qs3.geography=geography
            qs3.english=english
            qs3.hindi=hindi
            qs3.save()
      if qs3.rollno.cname=="seven":
         if life_science or physical_science or Polity or Algebra_math or geometry_math or rime or drawing :
            messages.error(request,"You filled unwanted field")
            response=render(request,"manage_all_classes_student_result.html",context={"qs3":qs3})
            return response 
         else:
            qs3.project=project
            qs3.math=math
            qs3.science=science
            qs3.history=history
            qs3.geography=geography
            qs3.english=english
            qs3.hindi=hindi
            qs3.save()
      if qs3.rollno.cname=="eight":
         if science or math or rime or drawing :
            messages.error(request,"You filled unwanted field")
            response=render(request,"manage_all_classes_student_result.html",context={"qs3":qs3})
            return response 
         else:
            qs3.project=project
            qs3.Algebra_math=Algebra_math
            qs3.geometry_math=geometry_math
            qs3.physical_science=physical_science
            qs3.life_science=life_science
            qs3.Polity=Polity
            qs3.history=history
            qs3.geography=geography
            qs3.english=english
            qs3.hindi=hindi
            qs3.save()
      if qs3.rollno.cname=="nine":
         if science or math or rime or drawing :
            messages.error(request,"You filled unwanted field")
            response=render(request,"manage_all_classes_student_result.html",context={"qs3":qs3})
            return response 
         else:
            qs3.project=project
            qs3.Algebra_math=Algebra_math
            qs3.geometry_math=geometry_math
            qs3.physical_science=physical_science
            qs3.life_science=life_science
            qs3.Polity=Polity
            qs3.history=history
            qs3.geography=geography
            qs3.english=english
            qs3.hindi=hindi
            qs3.save()
      if qs3.rollno.cname=="ten":
         if science or math or rime or drawing :
            messages.error(request,"You filled unwanted field")
            response=render(request,"manage_all_classes_student_result.html",context={"qs3":qs3})
            return response 
         else:
            qs3.project=project
            qs3.Algebra_math=Algebra_math
            qs3.geometry_math=geometry_math
            qs3.physical_science=physical_science
            qs3.life_science=life_science
            qs3.Polity=Polity
            qs3.history=history
            qs3.geography=geography
            qs3.english=english
            qs3.hindi=hindi
            qs3.save()
      
      
     
         
      
      messages.success(request,"Student mark updated")
      response=render(request,"manage_all_classes_student_result.html")
      return response 
   else:
        response=render(request,"manage_all_classes_student_result.html")
        return response 
def delete_class1_student_result(request):
   if request.method=="POST":
    try:
      rollno=request.POST.get("rollno")
      qs=result_of_all_classes_annual.objects.get(rollno=rollno)
      qs.delete()
      messages.success(request,"Student mark deleted successfully")
      response=render(request,"manage_all_classes_student_result.html")
      return response
    except:
      messages.success(request,"invalid rollno")
      response=render(request,"manage_all_classes_student_result.html")
      return response
def display_student_result_of_class1(request):
    stud=result_of_all_classes_annual.objects.all()
    response=render(request,"display_student_result_of_class1.html",context={"stud":stud})
    return response
#apply for teacher leave
def show_details_of_teacher_for_leave(request):
   if request.method=="POST":
     tid=request.POST.get("tid")
     if teacher.objects.filter(tid=tid).exists():
        tqs=teacher.objects.get(tid=tid)
     else:
        messages.error(request,"Invalid teacher id")
        response=render(request,"form_for_teacher_leave.html")
        return response
   response=render(request,"form_for_teacher_leave.html",context={"tqs":tqs})
   return response
def apply_leave_by_teacher(request):
   if request.method=="POST":
      tid_id=request.POST.get("tid")
      leave_reason=request.POST.get("leave_reason")
      date1_of_apply=request.POST.get("date1_of_apply")
      
      if tid_id:
         pass
      else:
         messages.error(request,"Teacher id must require")
         response=render(request,"form_for_teacher_leave.html")
         return response
      if leave_reason:
         pass
      else:
         messages.error(request,"You must provide valid a reason ")
         response=render(request,"form_for_teacher_leave.html")
         return response
      if date1_of_apply:
         pass
      else:
         messages.error(request,"You should provide a date ")
         response=render(request,"form_for_teacher_leave.html")
         return response
      print(leave_reason)
      print(date1_of_apply)
      print(tid_id)
      teachers=teacher.objects.get(tid=tid_id)
      leave_for_teachers.objects.create(leave_reason=leave_reason,date1_of_apply=date1_of_apply,tid=teachers)
      messages.success(request,"Teacher applied leave successfully")
      response=render(request,"form_for_teacher_leave.html")
      return response
      
   else:
      response=render(request,"form_for_teacher_leave.html")
      return response
def show_status_of_teacher_leave(request):
   if request.method=="POST":
    tid=request.POST.get("tid")
   if teacher.objects.filter(tid=tid).exists():
        pass
   else:
        messages.error(request,"Invalid Teacher Id")
        response=render(request,"form_for_teacher_leave.html")
        return response
   stud=leave_for_teachers.objects.filter(tid=tid)
   response=render(request,"check_teacher_leave_status.html",context={"stud":stud})
   return response
# views for Teacher send feedback 
#show teacher details for sending feedback
def show_details_of_teacher_for_sending_feedback(request):
   if request.method=="POST":
     tid=request.POST.get("tid")
     if teacher.objects.filter(tid=tid).exists():
        tqs=teacher.objects.get(tid=tid)
     else:
        messages.error(request,"Invalid teacher id")
        response=render(request,"teacher_send_feedback.html")
        return response
   response=render(request,"teacher_send_feedback.html",context={"tqs":tqs})
   return response
#teacher send feedback
def teacher_send_feedback(request):
   if request.method=="POST":
      tid_id=request.POST.get("tid")
      ttext=request.POST.get("ttext")
      if teacher.objects.filter(tid=tid_id).exists():
         pass
         
      else:
         messages.error(request,"Invalid teacher id")
         response=render(request,"teacher_send_feedback.html")
         return response

      if tid_id:
         pass
      else:
         messages.error(request,"Teacher id must require")
         response=render(request,"teacher_send_feedback.html")
         return response
      if ttext:
         pass
      else:
         messages.error(request,"You must provide some texts")
         response=render(request,"teacher_send_feedback.html")
         return response
      
      feedback_teacher.objects.create(ttext=ttext,tid_id=tid_id)
      messages.success(request,"Your feedback has been successfully recorded!")
      response=render(request,"teacher_send_feedback.html")
      return response
      
   else:
      response=render(request,"teacher_send_feedback.html")
      return response
def teacher_see_the_reply_of_feedback(request):
   if request.method=="POST":
    tid=request.POST.get("tid")
   if teacher.objects.filter(tid=tid).exists():
        pass
   
   else:
        messages.error(request,"Invalid Teacher Id")
        response=render(request,"teacher_send_feedback.html")
        return response
   stud=feedback_teacher.objects.filter(tid=tid)
   response=render(request,"teacher_see_reply_of _feedback.html",context={"stud":stud})
   return response  
#teacher view all students  
def view_students_of_all_class_by_teacher(request):
   vs=students_of_all_classes.objects.all()
   response=render(request,"view_students_of_all_class_by_teacher.html",context={"vs":vs})
   return response   
def from_card_to_today_attendance(request):
   qs=student_check_indivisually_absent_present_taken_by_teacher.objects.filter(date=date.today())
   response=render(request,"from_card_to_today_attendance.html",context={"qs":qs})
   return response
def from_card_to_total_subjects(request):
   subjects=subject.objects.all()
   response=render(request,"from_card_to_total_subjects.html",context={"subjects":subjects})
   return response
def from_cards_to_teacher_see_his_and_others_leave(request):
    teacher_leave=leave_for_teachers.objects.all()
    response=render(request,"from_cards_to_teacher_see_his_and_others_leave.html",context={"teacher_leave":teacher_leave})
    return response


   
   



    
      





       
   
       

      

           
   
   
   
      












    


   


    



    
        

