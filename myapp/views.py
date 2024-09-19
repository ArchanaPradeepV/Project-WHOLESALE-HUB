import smtplib
from email.mime.text import MIMEText

from django.core.files.storage import FileSystemStorage
from django.shortcuts import render,HttpResponse,redirect
from myapp.models import *
from datetime import datetime
# Create your views here.
def login(request):
    return render(request,'loginindex.html')

def landing_page(request):
    return render(request, 'mainhome.html')

def about(request):
    return render(request, 'about.html')
def contact(request):
    return render(request, 'contact.html')
def manage_category(request):
    ob=category_tb.objects.all()
    return render(request,'Admin/mancat.html',{'val':ob})
def add_category(request):
    return render(request,'Admin/addcat.html')
def addcat(request):
    cat=request.POST['textfield']
    des=request.POST['textfield2']
    ob=category_tb()
    ob.Category=cat
    ob.Description=des
    ob.save()
    return redirect('/manage_category')
def edtcat(request,id):
    request.session['cid']=id
    ob=category_tb.objects.get(id=id)
    return render(request,'Admin/edtcat.html',{'val':ob})
def updtcat(request):
    cat=request.POST['textfield']
    des=request.POST['textfield2']
    ob=category_tb.objects.get(id=request.session['cid'])
    ob.Category=cat
    ob.Description=des
    ob.save()
    return HttpResponse('''<script>alert('success');window.location='/manage_category'</script>''')

def dltcat(request,id):
    a=category_tb.objects.get(id=id)
    a.delete()
    return redirect('/manage_category')



def login_post(request):
    username = request.POST['textfield']
    password = request.POST['textfield2']
    login_check = login_tb.objects.filter(Username=username,Password=password)
    if login_check.exists():
        login_function = login_tb.objects.get(Username=username,Password=password)
        request.session['lid'] = login_function.id

        if login_function.Type == "admin":
            return HttpResponse('''<script>window.location='admin_home'</script>''')
        elif login_function.Type == "staff":
            return HttpResponse('''<script>window.location='staff_home'</script>''')
        elif login_function.Type == "user":
            return HttpResponse('''<script>window.location='retailer_home'</script>''')
        else:
            return redirect('/login?error=invalid')
    else:
        return redirect('/login?error=invalid')


def admin_home(request):
    return render(request, 'Admin/index1.html')
def staff_home(request):
    return render(request, 'Staff/index1.html')
def retailer_home(request):
    return render(request,'Retailer/index1.html')
def admin_manage_staff(request):
    staff = staff_tb.objects.all()
    return render (request, 'Admin/admin_manage_staffs.html',{'staff':staff})

def add_staff(request):
    return render(request, 'Admin/add_staff.html')

def register(request):
    return render(request,'register.html')

def user_reg(request):
    Name = request.POST['name']
    Place = request.POST['place']
    PhoneNo = request.POST['phone']
    Email = request.POST['email']
    Image = request.FILES['image']
    Username = request.POST['username']
    Password = request.POST['password']

    user_login = login_tb()
    user_login.Username = Username
    user_login.Password = Password
    user_login.Type = 'pending'
    user_login.save()

    fs = FileSystemStorage()
    date = datetime.now().strftime("%Y-%m-%d") + ".jpg"
    path = fs.save(date, Image)

    user_profile = retailer_tb()
    user_profile.Loginid = user_login
    user_profile.Name = Name
    user_profile.Place = Place
    user_profile.PhoneNo = PhoneNo
    user_profile.Email = Email
    user_profile.Image = path
    user_profile.save()
    return redirect('/register')





def add_staff_post(request):
    Name = request.POST['name']
    Place = request.POST['place']
    PhoneNo = request.POST['phone']
    Email = request.POST['email']
    Image = request.FILES['image']
    Username = request.POST['username']
    Password = request.POST['password']

    staff_login = login_tb()

    staff_login.Username = Username
    staff_login.Password = Password
    staff_login.Type = 'staff'
    staff_login.save()

    fs = FileSystemStorage()
    date = datetime.now().strftime("%Y-%m-%d") +  ".jpg"
    path =fs.save(date, Image)

    staff_profile = staff_tb()
    staff_profile.Loginid = staff_login
    staff_profile.Name = Name
    staff_profile.Place = Place
    staff_profile.PhoneNo = PhoneNo
    staff_profile.Email = Email
    staff_profile.Image = path
    staff_profile.save()
    return redirect('/admin_manage_staff')


def edit_staff(request,id):
    staff = staff_tb.objects.get(id=id)
    login = login_tb.objects.get(id=staff.Loginid.id)
    return render(request, 'Admin/edit_staff.html',{'staff':staff,'login':login})

def edit_staff_post(request):
    id = request.POST['id']
    Name = request.POST['name']
    Place = request.POST['place']
    PhoneNo = request.POST['phone']
    Email = request.POST['email']
    Username = request.POST['username']
    Password = request.POST['password']

    profile = staff_tb.objects.get(id=id)

    login = profile.Loginid
    login.Username = Username
    login.Password = Password
    login.save()

    profile.Name = Name
    profile.Place = Place
    profile.PhoneNo = PhoneNo
    profile.Email = Email

    if 'image' in request.FILES:
        profile.Image = request.FILES['image']
    profile.save()
    return redirect('/admin_manage_staff')



def forgot_password(request):
    return render(request,"forpass.html")

def forgot_password_post(request):
    un=request.POST['textfield']
    try:
        ob=staff_tb.objects.get(Email=un)
        try:
            gmail = smtplib.SMTP('smtp.gmail.com', 587)
            gmail.ehlo()
            gmail.starttls()
            gmail.login('archanavadakkedath002@gmail.com', 'wtor ghcu pajm knfi')
            print("login=======")
        except Exception as e:
            print("Couldn't setup email!!" + str(e))
        msg = MIMEText("Your password is : " + str(ob.Loginid.Password))
        print(msg)
        msg['Subject'] = 'Wholesale Hub'
        msg['To'] = un
        msg['From'] = 'archanavadakkedath002@gmail.com'
        print("ok====")
        try:
            gmail.send_message(msg)
            return HttpResponse('''<script>alert("check your mail");window.location="/login"</script>''')
        except Exception as e:
            return HttpResponse('''<script>alert("Network error");window.location="/forgot_password"</script>''')
    except:
        return HttpResponse('''<script>alert("Invalid Username");window.location="/forgot_password"</script>''')

def popup(request):
    name=request.POST['textfield']
    staff = staff_tb.objects.filter(Name__icontains=name)
    return render (request, 'Admin/admin_manage_staffs.html',{'staff':staff})

def verify(request):
    ob=retailer_tb.objects.all()
    return render(request,'Admin/adminverifyretailers.html',{"val":ob})

def sretailers(request):
    name=request.POST['textfield']
    ob = retailer_tb.objects.filter(Name__istartswith=name)
    return render(request, 'Admin/adminverifyretailers.html', {"val": ob})


def acceptretailer(request,id):
    ob=login_tb.objects.get(id=id)
    ob.Type='user'
    ob.save()
    return HttpResponse('''<script>window.location="/verify"</script>''')
def rejectretailer(request,id):
    ob = login_tb.objects.get(id=id)
    ob.Type = 'Rejected'
    ob.save()
    return HttpResponse('''<script>window.location="/verify"</script>''')
def viewretailers(request):
    return render(request,'Retailer/viewretailers')