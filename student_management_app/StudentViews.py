from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import*
import datetime
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def student_home(request):
    return render(request, 'student_template/student_home_template.html')

def student_view_attendance(request):
    student = Students.objects.get(admin=request.user.id)
    course =  student.course_id.id
    subjects = Subjects.objects.filter(course_id = course)
    return render(request, "student_template/student_view_attendance_template.html", {'subjects':subjects})

@csrf_exempt
def student_view_attendance_post(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        subject_id = request.POST.get("subject")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        
        start_date_parse = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        end_date_parse = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()
        
        subject_obj = Subjects.objects.get(id = subject_id)
        user_obj = CustomUser.objects.get(id = request.user.id)
        student_obj = Students.objects.get(admin = user_obj)
        attendance = Attendance.objects.filter(attendance_date__range = (start_date_parse, end_date_parse), subject_id = subject_obj)
        attendance_reports = AttendanceReport.objects.filter(attendance_id__in=attendance, student_id = student_obj)
        
        return render(request, "student_template/student_attendance_data_template.html", {'attendance_reports':attendance_reports})

    
def student_apply_leave(request):
    student_id = Students.objects.get(admin = request.user.id)
    leave_data = LeaveReportStudent.objects.filter(student_id = student_id)
    return render(request, 'student_template/student_apply_leave_template.html', {'leave_data':leave_data})

@csrf_exempt 
def student_apply_leave_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_msg")
        student_id = Students.objects.get(admin = request.user.id)

        try:
            leave_report = LeaveReportStudent(student_id = student_id, leave_date = leave_date, leave_message = leave_msg)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))  
        except:
            messages.error(request, "Failed to Applied for Leave")
            return HttpResponseRedirect(reverse("student_apply_leave"))

def student_feedback(request):
    student_id = Students.objects.get(admin = request.user.id)
    feedback_data = FeedbackStudent.objects.filter(student_id = student_id)
    return render(request, 'student_template/student_feedback_template.html', {'feedback_data':feedback_data})

@csrf_exempt
def student_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("student_feedback_save"))
    else:
        feedback_msg = request.POST.get("feedback_msg")
        student_id = Students.objects.get(admin = request.user.id)
        try:
            feedback = FeedbackStudent(student_id = student_id, feedback = feedback_msg, feedback_reply = "")
            feedback.save()
            messages.success(request, "Successfully Sent for Leave")
            return HttpResponseRedirect(reverse("student_feedback"))  
        except:
            messages.error(request, "Failed to Send Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))