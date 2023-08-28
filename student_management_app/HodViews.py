from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from datetime import datetime
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.utils.datastructures import MultiValueDict
from django.views.decorators.csrf import csrf_exempt

from .forms import *

from .models import *

def admin_home(request):
    return render(request, 'hod_template/home_content.html')

def add_staff(request):
    return  render(request, 'hod_template/add_staff_template.html')

def add_staff_save(request):
    if request.method != 'POST':
        return HttpResponse("Method Not Allowed")
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        address = request.POST.get('address')
        
    try:
        user = CustomUser.objects.create_user(username = username, first_name = first_name , last_name = last_name, password = password, email = email, user_type = 2)
        user.staffs.address = address
        user.save()
        messages.success(request, "successfully added Staff")
        return HttpResponseRedirect(reverse('add_staff'))
    except:
        messages.error(request, "Failed to add Staff")
        return HttpResponseRedirect(reverse('add_staff'))
        
        
def add_course(request):
    return render(request, 'hod_template/add_course_template.html')

def add_course_save(request):
    if request.method != 'POST':
        return HttpResponse('Method Not Allowed')
    else:
        course = request.POST.get('course')
        try:
            course_model = Courses(course_name = course)
            course_model.save()
            messages.success(request, "successfully added Course")
            return HttpResponseRedirect(reverse('add_course'))
        except:
            messages.error(request, "Failed to add Course")
            return HttpResponseRedirect(reverse('add_course'))
        
def add_student(request):
    form = AddStudentForm()
    return render(request, 'hod_template/add_student_template.html',{'form':form})

def add_student_save(request):
    if request.method != 'POST':
        return HttpResponse("Method Not Allowed")
    
    else:
        form = AddStudentForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name =form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            gender = form.cleaned_data['gender']
            address = form.cleaned_data['address']
            course_id = form.cleaned_data['course']
            session_year_id = form.cleaned_data['session_year_id']
         
        
            profile_pic = request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
        
            try:
                user = CustomUser.objects.create_user(username = username, first_name = first_name , last_name = last_name, password = password, email = email, user_type = 3)
                
                user.students.address = address
                
                course_obj = Courses.objects.get(id = course_id)
                user.students.course_id = course_obj
            
                user.students.gender = gender
                session_year = SessionYearModel.objects.get(id = session_year_id)
                user.students.session_year_id = session_year
                
                user.students.profile_pic = profile_pic_url
                user.save()
                messages.success(request, "successfully added Student")
                return HttpResponseRedirect(reverse('add_student'))
                
            except:
                messages.error(request, 'Failed to add Student')
                return HttpResponseRedirect(reverse('add_student'))
        else:
            form = AddStudentForm(request.POST)
            return render(request, 'hod_template/add_student_template.html', {'form':form})
def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type = 2)
    return render(request, 'hod_template/add_subject_template.html', {'courses':courses, 'staffs':staffs})

# def add_subject_save(request):
#     if request.method != 'POST':
#         return HttpResponse('Method Not Allowed')
#     else:
#         subject_name= request.POST.get('subject')
#         course_id = request.POST.get('course')
#         course = Courses.objects.get(id = course_id) 
#         staff_id = request.POST.get('staff')
#         staff = CustomUser.objects.get(id = staff_id)
#         try:
#             subject = Subjects(subject_name=subject_name, course_id=course, staff_id = staff)
#             subject.save()
#             messages.success(request, 'Successfully Subject Added')
#             return HttpResponseRedirect('/add_subject')
#         except:
#             messages.error(request, 'Failed to add Subject')
#             return HttpResponseRedirect('/add_subject')
def add_subject_save(request):
    if request.method != 'POST':
        return HttpResponse('Method Not Allowed')
    else:
        subject_name = request.POST.get('subject_name')
       
        course_id = request.POST.get("course")
       
        staff_id = request.POST.get("staff")
      
        
        # Validate course_id and staff_id
        if not (subject_name and course_id and staff_id):
            messages.error(request, 'Failed to add Subject. Invalid data provided.')
            return HttpResponseRedirect(reverse('add_subject'))
        
        try:
            course = Courses.objects.get(id=course_id)
            staff = CustomUser.objects.get(id=staff_id)
            
            subject = Subjects(subject_name=subject_name, course_id=course, staff_id=staff)
            subject.save()
            
            messages.success(request, 'Successfully Subject Added')
            return HttpResponseRedirect(reverse('add_subject'))
        except (Courses.DoesNotExist, CustomUser.DoesNotExist):
            messages.error(request, 'Failed to add Subject. Invalid course or staff.')
            return HttpResponseRedirect(reverse('add_subject'))
        except Exception as e:
            messages.error(request, 'Failed to add Subject. Error: {}'.format(str(e)))
            return HttpResponseRedirect(reverse('add_subject'))
        
def manage_staff(request):
    staffs = Staffs.objects.all()
    return render(request, 'hod_template/manage_staff_template.html', {'staffs':staffs})

def manage_student(request):
    students = Students.objects.all()
    return render(request, 'hod_template/manage_student_template.html', {'students':students})

def manage_course(request):
    courses = Courses.objects.all()
    return render(request, 'hod_template/manage_course_template.html', {'courses':courses})

def manage_subject(request):
    subjects = Subjects.objects.all()
    return render(request, 'hod_template/manage_subject_template.html', {'subjects':subjects})

def edit_staff(request,staff_id):
    staff = Staffs.objects.get(admin = staff_id)
    return render(request, 'hod_template/edit_staff_template.html', {'staff':staff,'id':staff_id})

def edit_staff_save(request):
    if request.method != 'POST':
        return HttpResponse('Method Not Allowed')
    else:
        staff_id = request.POST.get('staff_id')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        address = request.POST.get('address')
        try:
            user = CustomUser.objects.get(id = staff_id)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.username = username
            user.save()
            
            staff_model = Staffs.objects.get(admin=staff_id)
            staff_model.address = address
            staff_model.save()
            messages.success(request, "Successfully Edited Staff")
            return HttpResponseRedirect(reverse('edit_staff',kwargs={'staff_id':staff_id}))
        except:
            messages.error(request, "Failed to Edit Staff")
            return HttpResponseRedirect(reverse('edit_staff',kwargs={'staff_id':staff_id}))
        
# Standrad Code
def edit_student(request, student_id):
    request.session['student_id']=student_id
    student = Students.objects.get(admin = student_id)
    form = EditStudentForm()
    form.fields['email'].initial = student.admin.email
    form.fields['first_name'].initial = student.admin.first_name
    form.fields['last_name'].initial = student.admin.last_name
    form.fields['username'].initial = student.admin.username
    form.fields['address'].initial = student.address
    form.fields['course'].initial = student.course_id.id
    form.fields['session_year_id'].initial = student.session_year_id.id

    form.fields['profile_pic'].initial = student.profile_pic
    return render(request, 'hod_template/edit_student_template.html', {'form':form, 'id':student_id, 'username':student.admin.username})

def edit_student_save(request):
    if request.method != 'POST':
        return HttpResponse('Method Not Allowed')
    else:
        student_id = request.session.get('student_id')
        if student_id == None:
            return HttpResponseRedirect(reverse('manage_student'))
        form = EditStudentForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            gender = form.cleaned_data['gender']
            session_year_id = form.cleaned_data['session_year_id']
         
            course_id = form.cleaned_data['course']
            if request.FILES.get('profile_pic', False):
                profile_pic = request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename = fs.save(profile_pic.name, profile_pic)
                profile_pic_url = fs.url(filename)
            else:
                profile_pic_url = None
            try:
                user = CustomUser.objects.get(id = student_id)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.save()
                
                student = Students.objects.get(admin = student_id)
                student.address = address
                session_year = SessionYearModel.objects.get(id = session_year_id)
                student.session_year_id = session_year
                
                student.gender = gender
                
                course = Courses.objects.get(id = course_id)
                student.course_id = course
                if profile_pic_url !=None :
                    student.profile_pic = profile_pic_url
                student.save()
                del request.session['student_id']
                messages.success(request, 'Successfully Edited Staff')
                return HttpResponseRedirect(reverse('edit_student',kwargs={'student_id':student_id}))
            
            except:
                messages.error(request, "Failed to Edit Staff")
                return HttpResponseRedirect(reverse('edit_student',kwargs={'student_id':student_id}))

        else:
            form = EditStudentForm(request.POST)
            student = Students.objects.get(admin = student_id)
            return render(request, 'hod_template/edit_student_template.html', {'form':form, "id":student_id, 'username':student.admin.username})

def edit_subject(request, subject_id):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type = 2)
    subject = Subjects.objects.get(id = subject_id)
    return render(request, 'hod_template/edit_subject_template.html', {"subject":subject,'staffs':staffs ,'courses':courses,"id": subject_id})

def edit_subject_save(request):
    if request.method != 'POST':
        return HttpResponse("Method Not Allowed")
    else:
        subject_name = request.POST.get('subject_name')
        subject_id = request.POST.get('subject_id')
        staff_id = request.POST.get('staff')
        course_id = request.POST.get('course')
        try:
            subject = Subjects.objects.get(id = subject_id)
            subject.subject_name = subject_name
            staff = CustomUser.objects.get(id = staff_id)
            subject.staff_id = staff
            course = Courses.objects.get(id = course_id)
            subject.course_id = course
            subject.save()
            messages.success(request, "Successfully edited Subject")
            return HttpResponseRedirect(reverse('edit_subject',kwargs={'subject_id':subject_id}))
        except:
            messages.error(request, 'Failed to edit Subject')
            return HttpResponseRedirect(reverse('edit_subject',kwargs={'subject_id':subject_id}))

def edit_course(request, course_id):
    course = Courses.objects.get(id = course_id)
    return render(request, "hod_template/edit_course_template.html", {"course":course, "id":course_id})

def edit_course_save(request):
    if request.method != 'POST':
        return HttpResponse("Method Not Allowed")
    else:
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('course')
        try:
            course = Courses.objects.get(id = course_id)
            course.course_name = course_name
            course.save()
            messages.success(request, 'Successfully edited course')
            return HttpResponseRedirect(reverse('edit_course',kwargs={'course_id':course_id}))
        except:
            messages.error(request, "Failed to edit Course")
            return HttpResponseRedirect(reverse('edit_course',kwargs={'course_id':course_id}))
        
        
def manage_session(request):
    return render(request, 'hod_template/manage_session_template.html')

def add_session_save(request):
    if request.method != 'POST':
        return HttpResponseRedirect(reverse("manage_session"))
    else:
      session_start_year = request.POST.get('session_start')
      session_end_year = request.POST.get("session_end")
      try:
          sessionyear = SessionYearModel(session_start_year = session_start_year, session_end_year = session_end_year)
          sessionyear.save()
          messages.success(request, "successfully Add Session Year")
          return HttpResponseRedirect(reverse('manage_session'))
      
      except:
          messages.error(request, 'Failed to Add Session Year')
          return HttpResponseRedirect(reverse('manage_session'))
    
@csrf_exempt  
def check_email_exist(request):
    email = request.POST.get('email')
    user_obj = CustomUser.objects.filter(email = email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
    
@csrf_exempt
def check_username_exist(request):
    username = request.POST.get('username')
    user_obj = CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)
    
def student_feedback_message(request):
    feedbacks = FeedbackStudent.objects.all()
    return render(request, 'hod_template/student_feedback_message.html', {'feedbacks':feedbacks})

def staff_feedback_message(request):
    feedbacks = FeedbackStaff.objects.all()
    return render(request, "hod_template/staff_feedback_message.html", {'feedbacks':feedbacks})

@csrf_exempt
def student_feedback_message_replied(request):
    feedback_id = request.POST.get('id')
    feedback_message = request.POST.get('message')
    try:
        feedback = FeedbackStudent.objects.get(id = feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    
    except:
        return HttpResponse("False")
    
@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id = request.POST.get('id')
    feedback_message = request.POST.get('message')
    try:
        feedback = FeedbackStaff.objects.get(id = feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")

    except:
        return HttpResponse("False")