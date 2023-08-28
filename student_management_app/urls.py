from django.urls import path

from student_management_app import HodViews, StaffViews, StudentViews
from . import views
urlpatterns = [
    path('', views.shwoDemoPage, name = 'demo'),
    path('showLogin/', views.ShowLoginPage, name = 'show_login'),
    path('doLogin', views.doLoginPage, name = 'do_login'),
    path('logout', views.LogoutUser, name = 'logout'),
    path('get_user_details', views.GetUserDetails, name = 'get_user_details'),
    path('admin_home', HodViews.admin_home, name = "admin_home"),
    path('add_staff', HodViews.add_staff, name = "add_staff"),
    path('add_staff_save', HodViews.add_staff_save, name = "add_staff_save"),        
    path('add_course', HodViews.add_course, name = "add_course"),
    path('add_course_save', HodViews.add_course_save, name = "add_course_save"),
    path('add_student', HodViews.add_student, name = "add_student"),
    path('add_student_save', HodViews.add_student_save, name = "add_student_save"),
    path('add_subject', HodViews.add_subject, name = "add_subject"),
    path('add_subject_save', HodViews.add_subject_save, name = "add_subject_save"),
    path('manage_staff', HodViews.manage_staff, name = "manage_staff"),
    path('manage_student', HodViews.manage_student, name = "manage_student"),
    path('manage_course', HodViews.manage_course, name = "manage_course"),
    path('manage_subject', HodViews.manage_subject, name = "manage_subject"),
    path('edit_staff/<str:staff_id>', HodViews.edit_staff, name = "edit_staff"),
    path('edit_staff_save', HodViews.edit_staff_save, name = "edit_staff_save"),
    path('edit_student/<str:student_id>',HodViews.edit_student, name = "edit_student"),
    path('edit_student_save', HodViews.edit_student_save, name = "edit_student_save"),
    path('edit_subject/<str:subject_id>',HodViews.edit_subject, name = "edit_subject"),
    path('edit_subject_save', HodViews.edit_subject_save, name = "edit_subject_save"),
    path('edit_course/<str:course_id>',HodViews.edit_course, name = "edit_course"),
    path('edit_course_save', HodViews.edit_course_save, name = "edit_course_save"),
    path('manage_session', HodViews.manage_session, name = "manage_session"),
    path('add_session_save', HodViews.add_session_save, name = "add_session_save"),
    path('check_email_exist', HodViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist', HodViews.check_username_exist, name="check_username_exist"),
    path('student_feedback_message', HodViews.student_feedback_message, name="student_feedback_message"),
    path('student_feedback_message_replied', HodViews.student_feedback_message_replied, name="student_feedback_message_replied"),
    path('staff_feedback_message', HodViews.staff_feedback_message, name="staff_feedback_message"),
    path('staff_feedback_message_replied', HodViews.staff_feedback_message_replied, name="staff_feedback_message_replied"),
    
    # Staff Url Path
    
    path('staff_home', StaffViews.staff_home, name = "staff_home"),
    path('staff_take_attendance', StaffViews.staff_take_attendance, name = "staff_take_attendance"),
    path('staff_update_attendance', StaffViews.staff_update_attendance, name = "staff_update_attendance"),
    path('get_students', StaffViews.get_students, name = "get_students"),
    path('get_attendance_dates', StaffViews.get_attendance_dates, name = "get_attendance_dates"),
    path('get_attendance_student', StaffViews.get_attendance_student, name = "get_attendance_student"),
    path('save_attendance_data', StaffViews.save_attendance_data, name = "save_attendance_data"),
    path('save_update_attendance_data', StaffViews.save_update_attendance_data, name = "save_update_attendance_data"),
    path('staff_apply_leave', StaffViews.staff_apply_leave, name = "staff_apply_leave"),
    path('staff_apply_leave_save', StaffViews.staff_apply_leave_save, name = "staff_apply_leave_save"),
    path('staff_feedback', StaffViews.staff_feedback, name = "staff_feedback"),
    path('staff_feedback_save', StaffViews.staff_feedback_save, name = "staff_feedback_save"),
    
    
    # Student Url Path
    path('student_home', StudentViews.student_home, name = "student_home"),
    path('student_view_attendance', StudentViews.student_view_attendance, name = "student_view_attendance"),
    path('student_view_attendance_post', StudentViews.student_view_attendance_post, name = "student_view_attendance_post"),
    path('student_apply_leave', StudentViews.student_apply_leave, name = "student_apply_leave"),
    path('student_apply_leave_save', StudentViews.student_apply_leave_save, name = "student_apply_leave_save"),
    path('student_feedback', StudentViews.student_feedback, name = "student_feedback"),
    path('student_feedback_save', StudentViews.student_feedback_save, name = "student_feedback_save"),

]   