"""
URL configuration for osm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("home/",home,name="home"),
    path("register/",register_view,name="register"),
    path('login_view/',login_view,name="login"),
    path("logout_view/",logout_view,name="logout_view"),
    path("dashboard/",dashboard,name="dashboard"),
    path("student_dashboard/",student_dashboard,name="student_dashboard"),
    path("admin_dashboard/",admin_dashboard,name="admin_dashboard"),
    path("teacher_dashboard/",teacher_dashboard,name="teacher_dashboard"),
    #Admin panel urls
    
    path("view_students_of_all_classes/",view_students_of_all_classes,name="view_students_of_all_classes"),
    path("add_students_of_all_classes",add_students_of_all_classes,name="add_students_of_all_classes"),
    path("delete_students_of_all_classes",delete_students_of_all_classes ,name="delete_students_of_all_classes"),
    path("update_students_of_all_classes/",update_students_of_all_classes,name="update_students_of_all_classes"),
    path("view_teacher/",view_teacher,name="view_teacher"),
    path("add_teacher/",add_teacher,name="add_teacher"),
    path("delete_teacher/",delete_teacher,name="delete_teacher"),
    path("update_teacher/",update_teacher,name="update_teacher"),
    path("search_teacher/",search_teacher,name="search_teacher"),
    path("search_page_update_error/",search_page_update_error,name="search_page_update_error"),
    path("search_page_delete_error/",search_page_delete_error,name="search_page_delete_error"),
    path("search_student/",search_student,name="search_student"),
    path("manage_subjects/",view_subjects,name="manage_subjects"),
    path("add_subjects/",add_subjects,name="add_subjects"),
    path("delete_subjects/",delete_subjects,name="delete_subjects"),
    path("update_subjects/",update_subjects,name="update_subjects"),
    path("view_student_attendance/",view_student_attendance,name="view_student_attendance"),
    path("delete_student_attendance/",delete_student_attendance,name="delete_student_attendance"),
    path("view_student_leave/",view_student_leave,name="view_student_leave"),
    path("update_admin_reply_for _student_leave/",update_admin_reply_for_student_leave,name="update_admin_reply_for _student_leave"),
    path("delete_student_leave_history/",delete_student_leave_history,name="delete_student_leave_history"),
    path("view_teacher_leave/",view_teacher_leave,name="view_teacher_leave"),
    path("view_student_feedback/",view_student_feedback,name="view_student_feedback"),
    path("delete_student_feedback/",delete_student_feedback,name="delete_student_feedback"),
    path("view_teacher_feedback/",view_teacher_feedback,name="view_teacher_feedback"),
    path("reply_feedback_of_teacher_by_admin",reply_feedback_of_teacher_by_admin,name="reply_feedback_of_teacher_by_admin"),
    path("delete_reply_feedback_of_teacher/",delete_reply_feedback_of_teacher,name="delete_reply_feedback_of_teacher"),

   #url for teacher dashboard
   path("teachers_manage_all_class_attendance/",teachers_manage_all_class_attendance,name="teachers_manage_all_class_attendance"),
   path("take_all_class_student_attendance/",take_all_class_student_attendance,name="take_all_class_student_attendance"),
   path("dispaly_attendance/",dispaly_attendance,name="dispaly_attendance"),
   path("manage_all_classes_student_result/",manage_all_classes_student_result,name="manage_all_classes_student_result"),
   path("show_student_details_for_adding_mark_class1/",show_student_details_for_adding_mark_class1,name="show_student_details_for_adding_mark_class1"),
   path("add_class1_student_result/",add_class1_student_result,name="add_class1_student_result"),
   path("show_student_details_and_updating_mark_class1/",show_student_details_and_updating_mark_class1,name="show_student_details_and_updating_mark_class1"),
   path("update_class1_student_result/",update_class1_student_result,name="update_class1_student_result"),
   path("delete_class1_student_result/",delete_class1_student_result,name="delete_class1_student_result"),
   path("display_student_result_of_class1/",display_student_result_of_class1,name="display_student_result_of_class1"),
   path("show_details_of_teacher_for_leave/",show_details_of_teacher_for_leave,name="show_details_of_teacher_for_leave"),
   path( "apply_leave_by_teacher/", apply_leave_by_teacher,name="apply_leave_by_teacher"),
   path("show_status_of_teacher_leave/",show_status_of_teacher_leave,name="show_status_of_teacher_leave"),
   path("show_details_of_teacher_for_sending_feedback/",show_details_of_teacher_for_sending_feedback,name="show_details_of_teacher_for_sending_feedback"),
   path("teacher_send_feedback/",teacher_send_feedback,name="teacher_send_feedback"),
   path("teacher_see_the_reply_of_feedback/",teacher_see_the_reply_of_feedback,name="teacher_see_the_reply_of_feedback"),
   path("view_students_of_all_class_by_teacher/",view_students_of_all_class_by_teacher,name="view_students_of_all_class_by_teacher"),
   path("from_card_to_today_attendance/",from_card_to_today_attendance,name="from_card_to_today_attendance"),
   path("from_card_to_total_subjects/",from_card_to_total_subjects,name="from_card_to_total_subjects"),
   path("from_cards_to_teacher_see_his_and_others_leave/",from_cards_to_teacher_see_his_and_others_leave,name="from_cards_to_teacher_see_his_and_others_leave")


]  
