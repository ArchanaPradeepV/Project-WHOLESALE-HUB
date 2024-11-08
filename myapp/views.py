import smtplib
from email.mime.text import MIMEText
from datetime import  timedelta

from django.contrib import messages
from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from django.db.models import Q
from django.http.response import JsonResponse
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
    return HttpResponse('''<script>window.location='/manage_category'</script>''')

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
    paginator = Paginator(staff, 3)  # Show 10 posts per page

    page_number = request.GET.get('page')  # Get the current page number from the URL
    page_obj = paginator.get_page(page_number)  # Get the posts for that page

    return render (request, 'Admin/admin_manage_staffs.html',{'page_obj':page_obj})

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
    user_login.Type = 'user'
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

    messages.success(request, "Registration successful! Redirecting to login page...")
    return render(request, 'register.html', {'redirect_to_login': True})


def add_staff_post(request):
    Name = request.POST['name']
    Place = request.POST['place']
    PhoneNo = request.POST['phone']
    Email = request.POST['email']
    Image = request.FILES['image']
    Username = request.POST['username']
    Password = request.POST['password']

    aa=login_tb.objects.filter(Username=Username)
    if aa.exists():
        return HttpResponse('''
                                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/sweetalert2@10">
                                <script src="https://cdn.jsdelivr.net/npm/sweetalert2@10"></script>
                                <script>
                                    document.addEventListener("DOMContentLoaded", function() {
                                        Swal.fire({
                                            icon: 'Already Taken',
                                            title: '',
                                            text: '',
                                            confirmButtonText: '',
                                            reverseButtons: true
                                        }).then((result) => {
                                            if (result.isConfirmed) {
                                                window.location='/admin_manage_staff';
                                            }
                                        });
                                    });
                                </script>
                            ''')
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

from django.http import HttpResponse
from django.shortcuts import redirect
from .models import login_tb, staff_tb



def edit_staff_post(request):
    # Get form data
    id = request.POST['id']
    Name = request.POST['name']
    Place = request.POST['place']
    PhoneNo = request.POST['phone']
    Email = request.POST['email']
    Status = request.POST['status']

    # Get the staff profile
    profile = staff_tb.objects.get(id=id)

    # Update staff profile details
    profile.Name = Name
    profile.Place = Place
    profile.PhoneNo = PhoneNo
    profile.Email = Email
    profile.Status = Status

    # If an image is uploaded, update the profile image
    if 'image' in request.FILES:
        profile.Image = request.FILES['image']

    # Save the updated profile information
    profile.save()

    # Redirect to the staff management page after successful update
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
    return render (request, 'Admin/admin_manage_staffs.html',{'page_obj':staff})

def verify(request):
    ob=retailer_tb.objects.all()
    paginator = Paginator(ob, 3)  # Show 10 posts per page

    page_number = request.GET.get('page')  # Get the current page number from the URL
    page_obj = paginator.get_page(page_number)  # Get the posts for that page
    return render(request,'Admin/adminverifyretailers.html',{'page_obj':page_obj})

def sretailers(request):
    name=request.POST['textfield']
    ob = retailer_tb.objects.filter(Name__istartswith=name)
    return render(request, 'Admin/adminverifyretailers.html', {"page_obj": ob})


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

def staff_view_product(request):

    ob=product_tb.objects.all().order_by("-id")

    paginator = Paginator(ob, 3)  # Show 10 posts per page

    page_number = request.GET.get('page')  # Get the current page number from the URL
    page_obj = paginator.get_page(page_number)  # Get the posts for that page

    # return render(request, 'post_list.html', {'page_obj': page_obj})
    return render(request,'Staff/staff_manage_products.html',{'page_obj': page_obj})


def staff_view_product_search(request):
    n = request.POST['textfield']
    c = request.POST['clr']
    if n!="" and c!="":
        ob = product_tb.objects.filter( Name__icontains=n,Colour__istartswith=c)

        # ob1 = product_tb.objects.filter( Q(Colour__istartswith=c))
        # ob=ob.union(ob1)
        # # ob = product_tb.objects.filter(Q(Colour__istartswith=c))

        paginator = Paginator(ob, 3)  # Show 10 posts per page

        page_number = request.GET.get('page')  # Get the current page number from the URL
        page_obj = paginator.get_page(page_number)  # Get the posts for that page

        # return render(request, 'post_list.html', {'page_obj': page_obj})
        return render(request, 'Staff/staff_manage_products.html', {'page_obj': page_obj})
    if n!="":
        ob = product_tb.objects.filter(Q(Name__icontains=n))
        paginator = Paginator(ob, 3)  # Show 10 posts per page

        page_number = request.GET.get('page')  # Get the current page number from the URL
        page_obj = paginator.get_page(page_number)  # Get the posts for that page

        # return render(request, 'post_list.html', {'page_obj': page_obj})
        return render(request, 'Staff/staff_manage_products.html', {'page_obj': page_obj})
    else:
        ob = product_tb.objects.filter(Q(Colour__istartswith=c))
        paginator = Paginator(ob, 3)  # Show 10 posts per page

        page_number = request.GET.get('page')  # Get the current page number from the URL
        page_obj = paginator.get_page(page_number)  # Get the posts for that page

        # return render(request, 'post_list.html', {'page_obj': page_obj})
        return render(request, 'Staff/staff_manage_products.html', {'page_obj': page_obj})




def admin_view_product_search(request):
    n = request.POST['textfield']
    c = request.POST['clr']
    if n!="" and c!="":
        ob = product_tb.objects.filter( Name__icontains=n,Colour__istartswith=c)

        # ob1 = product_tb.objects.filter( Q(Colour__istartswith=c))
        # ob=ob.union(ob1)
        # # ob = product_tb.objects.filter(Q(Colour__istartswith=c))

        paginator = Paginator(ob, 3)  # Show 10 posts per page

        page_number = request.GET.get('page')  # Get the current page number from the URL
        page_obj = paginator.get_page(page_number)  # Get the posts for that page

        # return render(request, 'post_list.html', {'page_obj': page_obj})
        return render(request, 'admin/staff_manage_products.html', {'page_obj': page_obj})
    if n!="":
        ob = product_tb.objects.filter(Q(Name__icontains=n))
        paginator = Paginator(ob, 3)  # Show 10 posts per page

        page_number = request.GET.get('page')  # Get the current page number from the URL
        page_obj = paginator.get_page(page_number)  # Get the posts for that page

        # return render(request, 'post_list.html', {'page_obj': page_obj})
        return render(request, 'admin/staff_manage_products.html', {'page_obj': page_obj})
    else:
        ob = product_tb.objects.filter(Q(Colour__istartswith=c))
        paginator = Paginator(ob, 3)  # Show 10 posts per page

        page_number = request.GET.get('page')  # Get the current page number from the URL
        page_obj = paginator.get_page(page_number)  # Get the posts for that page

        # return render(request, 'post_list.html', {'page_obj': page_obj})
        return render(request, 'admin/staff_manage_products.html', {'page_obj': page_obj})



def staff_add_product(request):
    ob = category_tb.objects.all()
    return render(request, 'Staff/add_product.html', {"val": ob})


def add_product_post(request):
    Name = request.POST['name']
    Description = request.POST['description']
    Price = request.POST['price']
    Stock = request.POST['stock']
    Image = request.FILES['image']
    Colour=request.POST['colour']
    fs=FileSystemStorage()
    fn=fs.save(Image.name,Image)
    Categoryid_id = request.POST['cat']

    prdt=product_tb()
    prdt.Name = Name
    prdt.Description = Description
    prdt.Price = Price
    prdt.Image = fn
    prdt.Stock = Stock
    prdt.Colour = Colour
    prdt.Categoryid = category_tb.objects.get(id=Categoryid_id)
    prdt.save()
    return HttpResponse('''<script>window.location='/staff_view_product'</script>''')

def edit_product_link(request,id):
    ob=product_tb.objects.get(id=id)
    request.session['pid']=id
    ob1=category_tb.objects.all()
    return render(request,"Staff/edit_product.html",{"val":ob,"c":ob1})


def edit_product_post(request):
    id=request.session['pid']
    ob=product_tb.objects.get(id=id)
    Name = request.POST['name']
    Description = request.POST['description']
    Price = request.POST['price']
    Stock = request.POST['stock']
    Colour = request.POST['colour']

    Categoryid_id = request.POST['cat']
    #
    prdt = product_tb.objects.get(id=id)
    prdt.Name = Name
    prdt.Description = Description
    prdt.Price = Price
    if 'image' in request.FILES:
        Image = request.FILES['image']
        fs = FileSystemStorage()
        fn = fs.save(Image.name, Image)
        prdt.Image = fn
    prdt.Stock = Stock
    prdt.Colour = Colour
    prdt.Categoryid = category_tb.objects.get(id=Categoryid_id)
    prdt.save()
    return redirect("/staff_view_product")


def Staff_view_return_pr(request):
    ob = return_tb.objects.all()
    return render(request, 'Staff/staff_view_return_.html', {"page_obj": ob})

def add_product(request):
    return render(request,'add_product')


def checkemail(request):


    username  = request.GET['email']
    print(username)
    data = {
        'is_taken': retailer_tb.objects.filter(Email__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message']="A user with this email already exists."
    else:
        data = {
            'is_taken': staff_tb.objects.filter(Email__iexact=username).exists()
        }
    if data['is_taken']:
        data['error_message'] = "A user with this email already exists."
        # return HttpResponse("A user with this username already exists.")
    return JsonResponse(data)


def checkusername(request):

    username  = request.GET['email']
    print(username)
    data = {
        'is_taken': login_tb.objects.filter(Username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message']="A user with this Username already exists."

        # return HttpResponse("A user with this username already exists.")
    return JsonResponse(data)

def orderproduct(request):
    ob=product_tb.objects.all()
    return render(request,'Retailer/viewprdt.html',{"page_obj":ob})



def user_view_product_search(request):
    n = request.POST['textfield']
    c = request.POST['clr']
    if n!="" and c!="":
        ob = product_tb.objects.filter( Name__icontains=n,Colour__istartswith=c)

        # ob1 = product_tb.objects.filter( Q(Colour__istartswith=c))
        # ob=ob.union(ob1)
        # # ob = product_tb.objects.filter(Q(Colour__istartswith=c))

        paginator = Paginator(ob, 3)  # Show 10 posts per page

        page_number = request.GET.get('page')  # Get the current page number from the URL
        page_obj = paginator.get_page(page_number)  # Get the posts for that page

        # return render(request, 'post_list.html', {'page_obj': page_obj})
        return render(request, 'Retailer/viewprdt.html', {'page_obj': page_obj})
    if n!="":
        ob = product_tb.objects.filter(Q(Name__icontains=n))
        paginator = Paginator(ob, 3)  # Show 10 posts per page

        page_number = request.GET.get('page')  # Get the current page number from the URL
        page_obj = paginator.get_page(page_number)  # Get the posts for that page

        # return render(request, 'post_list.html', {'page_obj': page_obj})
        return render(request, 'Retailer/viewprdt.html', {'page_obj': page_obj})
    else:
        ob = product_tb.objects.filter(Q(Colour__istartswith=c))
        paginator = Paginator(ob, 3)  # Show 10 posts per page

        page_number = request.GET.get('page')  # Get the current page number from the URL
        page_obj = paginator.get_page(page_number)  # Get the posts for that page

        # return render(request, 'post_list.html', {'page_obj': page_obj})
        return render(request, 'Retailer/viewprdt.html', {'page_obj': page_obj})




def admin_view_product(request):
    ob = product_tb.objects.all().order_by("-id")

    paginator = Paginator(ob, 3)  # Show 10 posts per page

    page_number = request.GET.get('page')  # Get the current page number from the URL
    page_obj = paginator.get_page(page_number)  # Get the posts for that page

    # return render(request, 'post_list.html', {'page_obj': page_obj})
    return render(request, 'admin/staff_manage_products.html', {'page_obj': page_obj})


def add_to_cart(request,id):
    request.session['pid']=id
    ob=product_tb.objects.filter(id=id)
    return render(request,'Retailer/addtocart.html',{"page_obj":ob})



def add_to_cart_post(request):
    btn=request.POST['submit']
    if btn == 'Buy Now':
            print(request.session['pid'],"kiiiiiiiiiiiiiiiiiii")
            qty=request.POST['qty']
            qq=product_tb.objects.get(id=request.session['pid'])
            tt = int(qq.Price)* int(qty)
            stock = int(qq.Stock)
            print(stock,qty,"jjjjjjjjjjjjjjjjjjjjjj")
            nstk = int(stock) - int(qty)
            if stock >= int(qty):
                up=product_tb.objects.get(id=request.session['pid'])
                up.Stock=nstk
                up.save()
                qt=order_tb()
                qt.Date=datetime.today()
                qt.Retailerid=retailer_tb.objects.get(Loginid__id=request.session['lid'])
                qt.Status='ORDER'
                qt.Amount=tt
                qt.save()
                qty1=orderdetails_tb()
                qty1.Quantity=qty
                qty1.Productid=product_tb.objects.get(id=request.session['pid'])
                qty1.Orderid=qt
                qty1.Price=tt
                qty1.save()
                request.session['rid'] = qt.id
                request.session['pay_amount'] = qt.Amount
                return HttpResponse('''<script>window.location='/user_pay_proceed1'</script>''')
            else:
                return HttpResponse('''<script>window.location='/orderproduct'</script>''')
    else:

        qty=request.POST['qty']
        qq=product_tb.objects.get(id=request.session['pid'])
        tt = int(qq.Price)* int(qty)
        stock = int(qq.Stock)
        print(stock,qty,"jjjjjjjjjjjjjjjjjjjjjj")
        nstk = int(stock) - int(qty)
        if stock >= int(qty):
            up=product_tb.objects.get(id=request.session['pid'])
            up.Stock=nstk
            up.save()
            q=order_tb.objects.filter(Retailerid__Loginid__id=request.session['lid'],Status='cart')
            if len(q)==0:
                qt=order_tb()
                qt.Date = datetime.today()
                qt.Retailerid = retailer_tb.objects.get(Loginid__id=request.session['lid'])
                qt.Status = 'cart'
                qt.Amount = tt
                qt.save()
                qty1 = orderdetails_tb()
                qty1.Quantity = qty
                qty1.Productid = product_tb.objects.get(id=request.session['pid'])
                qty1.Orderid = qt
                qty1.Price = tt
                qty1.save()

                return HttpResponse('''<script>window.location='/orderproduct'</script>''')
            else:
                total = int(q[0].Amount) + int(tt)
                qt=order_tb.objects.get(id=q[0].id)
                qt.Amount=total
                qt.save()
                qty1=orderdetails_tb.objects.filter(Productid__id=request.session['pid'],Orderid__id=q[0].id)
                if len(qty1)==0:
                    qqt=orderdetails_tb()
                    qqt.Orderid=q[0]
                    qqt.Productid=product_tb.objects.get(id=request.session['pid'])
                    qqt.Quantity=qty
                    qqt.Price = tt
                    qqt.save()
                else:
                    j=orderdetails_tb.objects.get(id=qty1[0].id)
                    quty=int(qty1[0].Quantity) + int(qty)
                    kk=int(qty1[0].Productid.Price)+int(quty)
                    j.Quantity=quty
                    j.Price = kk
                    j.save()
                return HttpResponse('''<script>window.location='/orderproduct'</script>''')
        else:
            return HttpResponse('''<script>window.location='/orderproduct'</script>''')

def user_pay_proceed1(request):
    id=request.session['rid']
    amt=request.session['pay_amount']
    amt = round(float(amt), 2)
    # request.session['pay_amount'] = amt
    client = razorpay.Client(auth=("rzp_test_edrzdb8Gbx5U5M", "XgwjnFvJQNG6cS7Q13aHKDJj"))
    print(client)
    payment = client.order.create(
        {'amount': str(amt * 10).split(".")[0], 'currency': "INR", 'payment_capture': '1'})
    res = retailer_tb.objects.get(Loginid__id=request.session['lid'])

    # ob=order_tb.objects.get(id=request.session['rid'])
    # ob.status='paid'
    # ob.save()
    return render(request, 'Retailer/UserPayProceed.html',
                  {'p': payment, 'val': res, "lid": request.session['lid'], "id": request.session['rid']})


#
# def add_to_cart_post(request):
#     id=request.session['pid']
#     qty=request.POST['qty']
#     obp=product_tb.objects.get(id=id)
#     if obp.Stock >=int(qty):
#         ob=order_tb.objects.filter(Retailerid__Loginid__id=request.session['lid'],Status='cart')
#         if len(ob)==0:
#             ob=order_tb()
#             ob.Retailerid=retailer_tb.objects.get(Loginid__id=request.session['lid'])
#             ob.Amount=0
#             ob.Date=datetime.today()
#             ob.Status='cart'
#             ob.save()
#         else:
#             ob=ob[0]
#         obb=orderdetails_tb.objects.filter(Productid__id=id,Orderid=ob.id)
#         obp.Stock-=int(qty)
#         obp.save()
#         if len(obb)>0:
#             obb=obb[0]
#             obb.Quantity+=int(qty)
#             obb.Price+=int(qty)*obp.Price
#             obb.save()
#         else:
#             obb = orderdetails_tb()
#             obb.Orderid=ob
#             obb.Productid=obp
#             obb.Quantity = int(qty)
#             obb.Price = int(qty) * obp.Price
#             obb.Status='pending'
#             obb.save()
#         ob.Amount+=int(qty) * obp.Price
#         ob.save()
#
#     return redirect("/orderproduct")


def block(request,id):
    a = login_tb.objects.filter(id=id).update(Type = 'Blocked')
    c=staff_tb.objects.filter(Loginid_id=id).update(Status='Blocked')
    return redirect('/admin_manage_staff')



def unblock(request,id):
    a = login_tb.objects.filter(id=id).update(Type = 'staff')
    c=staff_tb.objects.filter(Loginid_id=id).update(Status='Approved')
    return redirect('/admin_manage_staff')


def deletecart(request,id):

    obpp = orderdetails_tb.objects.get(id=id)


    ob = order_tb.objects.get(id=obpp.Orderid.id)
    obp=product_tb.objects.get(id=obpp.Productid.id)

    obp.Stock += int(obpp.Quantity)
    obp.save()
    qty=int(obpp.Quantity)

    ob.Amount -= int(qty) * obp.Price
    ob.save()
    obpp.delete()
    return redirect("/cart")


from datetime import datetime
from django.shortcuts import render


def cart(request):
    cart = orderdetails_tb.objects.filter(Orderid__Status='cart',
                                        Orderid__Retailerid__Loginid__id=request.session['lid'])
    tp = 0
    for item in cart:
        item.st = item.Quantity * item.Productid.Price
        tp += item.st
    if cart.exists():
        kk1 = cart[0].Orderid.id
        kk = cart[0].Orderid
        print(kk,"jjjjjjj")
        cd = datetime.today().date()
        od = kk.Date
        pp = od + timedelta(days=14)
        print(cd, od,pp, "hhhhhhhhhhh")
        if cd > pp:
            ll=order_tb.objects.get(id=kk1)
            ll.delete()
        else:
            print("Order is still valid.")

    else:
        cd = None
        od = None
        print(cd, od, "hhhhhhhhhhh")
    return render(request, "Retailer/cart.html", {"cart": cart, "tp": tp, "cd": cd, "od": od})


import  razorpay

def user_pay_proceed(request,id,amt):
    request.session['rid'] = id

    amt=round(float(amt), 2)
    request.session['pay_amount'] = amt
    client = razorpay.Client(auth=("rzp_test_edrzdb8Gbx5U5M", "XgwjnFvJQNG6cS7Q13aHKDJj"))
    print(client)
    payment = client.order.create({'amount': str(amt*10).split(".")[0], 'currency': "INR", 'payment_capture': '1'})
    res=retailer_tb.objects.get(Loginid__id=request.session['lid'])


    # ob=order_tb.objects.get(id=request.session['rid'])
    # ob.status='paid'
    # ob.save()
    return render(request,'Retailer/UserPayProceed.html',{'p':payment,'val':res,"lid":request.session['lid'],"id":request.session['rid']})


def on_payment_success(request):
    print(request.GET)
    request.session['rid'] = request.GET['id']
    request.session['lid'] = request.GET['lid']

    event = str(request.body);
    print(event)
    if 'payment_failed' in event:
        ob = order_tb.objects.get(id=request.GET['id'])
        ob.Status = 'payment failed'
        ob.save()
        ob1 = payment_tb()
        ob1.Orderid = ob
        ob1.Date = datetime.today()
        ob1.Status = 'payment failed'
        ob1.save()

        obs=orderdetails_tb.objects.filter(Orderid__id=request.session['rid'])
        for i in obs:
            obp=product_tb.objects.get(id=i.Productid.id)
            obp.Stock+=int(i.Quantity)
            obp.save()
        return redirect('/retailer_home')
    else:
        # var = auth.authenticate(username='admin', password='admin')
        # if var is not None:
        #     auth.login(request, var)
        # amt = request.session['pay_amount']
        ob=order_tb.objects.get(id=request.GET['id'])
        ob.Status='paid'
        ob.save()
        ob1=payment_tb()
        ob1.Orderid=ob
        ob1.Date = datetime.today()
        ob1.Status ='paid'
        ob1.save()

        return redirect('/retailer_home')


def on_payment_failure(request):
    request.session['rid'] = request.GET.get('id')
    request.session['lid'] = request.GET.get('lid')

    event = request.body;
    print("event.event")

    # if (event.event === 'payment.failed') {
    ob = order_tb.objects.get(id=request.session['rid'])
    ob.Status = 'unsuccessful'
    ob.save()

    ob1 = payment_tb()
    ob1.Orderid = ob
    ob1.Date = datetime.today()
    ob1.Status = 'unsuccessful'
    ob1.save()

    return HttpResponse('kjdhckjsehfdkj')
    return redirect('/payment_failed')


def view_order(request):
    ob=order_tb.objects.exclude(Status='cart')
    paginator = Paginator(ob, 5)  # Show 10 posts per page

    page_number = request.GET.get('page')  # Get the current page number from the URL
    page_obj = paginator.get_page(page_number)
    return render(request,"Staff/staff_order.html",{"page_obj":page_obj})
def view_more_order(request,id):
    cart = orderdetails_tb.objects.filter(Orderid__id=id    )
    tp = 0
    for i in cart:
        st = i.Quantity * i.Productid.Price
        i.st = st
        tp += i.Quantity * i.Productid.Price
    return render(request, "Staff/cart.html", {"cart": cart, "tp": tp})

def view_order1(request):
    ob=order_tb.objects.exclude(Status='cart')

    paginator = Paginator(ob, 5)  # Show 10 posts per page

    page_number = request.GET.get('page')  # Get the current page number from the URL
    page_obj = paginator.get_page(page_number)  # Get the posts for that page

    return render(request,"Admin/admin_order.html",{"page_obj":page_obj})
def view_more_order1(request,id):
    cart = orderdetails_tb.objects.filter(Orderid__id=id    )
    tp = 0
    for i in cart:
        st = i.Quantity * i.Productid.Price
        i.st = st
        tp += i.Quantity * i.Productid.Price
    return render(request, "Admin/cart.html", {"cart": cart, "tp": tp})
def Admin_view_return_products(request):
    ob=return_tb.objects.all()
    return render(request,'Admin/View_return_products.html',{"page_obj":ob})


def Admin_accept_retun_product(request,id):
    ob=return_tb.objects.get(id=id)
    ob.Status="accepted"
    ob.save()

    oobj=ob.Orderid
    oobj.Status='return'
    oobj.save()

    pob=oobj.Productid
    pob.Stock+=int(oobj.Quantity)
    pob.save()

    return Admin_view_return_products(request)
def Admin_reject_retun_product(request,id):
    ob=return_tb.objects.filter(id=id).update(Status="rejected")
    return Admin_view_return_products(request)
def profile(request):
    ob = retailer_tb.objects.get(Loginid__id=request.session['lid'])
    return render(request, 'Retailer/profile.html', {'val': ob})

def myorder(request):

    ob = order_tb.objects.exclude(Status='cart').filter(Retailerid__Loginid__id=request.session['lid'])
    paginator = Paginator(ob, 5)  # Show 10 posts per page

    page_number = request.GET.get('page')  # Get the current page number from the URL
    page_obj = paginator.get_page(page_number)
    return render(request, "Retailer/view_ordes.html", {"page_obj": page_obj})

def view_myorder_more(request, id):
    cart = orderdetails_tb.objects.filter(Orderid__id=id)
    tp = 0
    for i in cart:
        st = i.Quantity * i.Productid.Price
        i.st = st
        tp += i.Quantity * i.Productid.Price
    return render(request, "Retailer/view_order_more.html", {"cart": cart, "tp": tp})


def Return_product(request, id):
    request.session['odid']=id
    return render(request, "Retailer/retuen.html")
def return_product_post(request):
    ob=orderdetails_tb.objects.get(id=request.session['odid'])
    ob.Status='Return request'
    ob.save()

    ob1=return_tb()
    ob1.Orderid=ob
    ob1.Date = datetime.today()
    ob1.Status = 'pending'
    ob1.Reason=request.POST['t']
    ob1.save()



    return redirect("/myorder")
def edit_profile(request):
    ob = retailer_tb.objects.get(Loginid__id=request.session['lid'])
    return render(request, 'Retailer/edit_profile.html', {'val': ob})

def edit_profile_post(request):
    try:
        Name = request.POST['name']
        Place = request.POST['place']
        PhoneNo = request.POST['phone']
        Email = request.POST['email']
        profile = retailer_tb.objects.get(Loginid__id=request.session['lid'])
        profile.Name=Name
        profile.Place=Place
        profile.PhoneNo=PhoneNo
        profile.Email=Email
        Image = request.FILES['image']
        fs = FileSystemStorage()
        fp = fs.save(Image.name,Image)
        profile.Image = fp
        profile.save()
    except:
        Name = request.POST['name']
        Place = request.POST['place']
        PhoneNo = request.POST['phone']
        Email = request.POST['email']
        profile = retailer_tb.objects.get(Loginid__id=request.session['lid'])
        profile.Name = Name
        profile.Place = Place
        profile.PhoneNo = PhoneNo
        profile.Email = Email
        profile.save()
    return redirect('/profile')
def Retailer_view_retuen_info(request):
    ob = return_tb.objects.filter(Orderid__Orderid__Retailerid__Loginid=request.session["lid"])
    return render(request, 'Retailer/Retailer_view_returninfo.html', {"page_obj": ob})






