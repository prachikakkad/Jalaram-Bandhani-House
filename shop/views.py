from math import ceil
from django.shortcuts import redirect, render, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Product, Message, Order, Order_Update, Review
import json
import math
import random
import smtplib
from email.message import EmailMessage
import imghdr

# Create your views here.


def Home(request):
    """Shows Home Page To The User."""
    return render(request, "Home.html")

def Contact(request):
    """Shows Contact Page To The User."""
    return render(request, "Contact.html")

def Contacting(request):
    """Saves The Contact Message Into Database."""
    if request.method == "POST":
        Email = request.user.email
        phone = "+91" + request.POST['phone']
        username = request.user.username
        msg = request.POST['msg']
        data = Message(Email=Email, Phone=phone, Username=username, Query=msg)
        data.save()
        messages.success(request, "I have received Your Message ! I will Reach Out to you via Email or Call As Soon As Possible !")
        return render(request, 'Home.html')

def About(request):
    """Shows About Page To The User."""
    return render(request, "About.html")

def Login(request):
    """Shows Login Page To The User."""
    return render(request, "Login.html")

def Log_In(request):
    """Allows The User To Login Through The Login Form."""
    if request.method == 'POST':
        username = request.POST['loginusername']
        password = request.POST['loginpass']

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user} !")
            return redirect('/')
            
        else:
            messages.error(request, "Invalid Credentials ! Please Try Again !")
            return redirect('/login')

    return HttpResponse('404 - Not Found')

def Signup(request):
    """Shows Signup Page To The User."""
    return render(request, "Signup.html")

def Create_User(request):
    """Creates A New User Through Sign Up Form."""
    if request.method == 'POST':
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        username = request.POST['username']

        if not username.isalnum():
            messages.error(request, "Username can only contain Letters and Numbers !")
            return redirect('signup') 
        else:
            user = User.objects.create_user(username, email, pass1)
            user.first_name = fname
            user.last_name = lname
            user.save()
            messages.success(request, "Account Created Successfully ! You May Login Now !")
            return redirect('login')
    else:
        return HttpResponse('404 - Not Found')

def Log_Out(request):
    """Allows The User To Log Out."""
    logout(request)
    messages.success(request, "Logged Out Successfully !")
    return redirect('signup')

def Profile(request):
    """Shows Profile Page To The User."""
    return render(request, "Profile.html")

def Shop_Home(request):
    """Shows Shopping Page To The User."""
    allProds=[]
    catprods= Product.objects.values('Category', 'id')
    cats= {item["Category"] for item in catprods}
    for cat in cats:
        prod=Product.objects.filter(Category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])

    params={'allProds':allProds }
    return render(request,"Shop_Home.html", params)

def Product_View(request, myid):
    """Shows Product Page To The User."""
    product = Product.objects.filter(id=myid)
    reviews = Review.objects.filter(Product=myid)
    return render(request, 'Product_View.html', {'product': product[0], 'reviews': reviews})

def Checkout(request):
    """Shows Checkout Page To The User."""
    return render(request, "Checkout.html")

def Tracker(request):
    """Shows Tracker Page To The User And Handles Backend Of The Tracker Page."""
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        var = True
        try:
            order = Order.objects.filter(order_id = orderId, Email=email)
            if len(order) > 0:
                update = Order_Update.objects.filter(Order_Id=orderId)
                updates = []

                for item in update:
                    updates.append({'text' : item.Update})
                    response = json.dumps({'status':'success', "updates":updates, 'json':order[0].Json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse("No Items Found !")
        except Exception as e:
            return HttpResponse("No Items Found !")
    return render(request, "Tracker.html")

def SearchMatch(query, item):
    """Handles Item Searching."""
    if query in item.Product_Name.lower() or query in item.Description.lower() or query in item.Category.lower() or query in item.Product_Name or query in item.Description or query in item.Category:
        return True
    else:
        return False

def Search(request):
    """Shows Search Result Page To The User."""
    query = request.GET.get('search', '')
    allProds=[]
    catprods= Product.objects.values('Category', 'id') 
    cats= {item["Category"] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(Category=cat)
        prod = [item for item in prodtemp if SearchMatch(query, item)]
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params={'allProds':allProds, 'msg' : ''}
    if len(allProds) == 0 or len(query) < 4:
        messages.info(request, 'Please Enter Relevant Search Query !')
    return render(request,"Shop_Home.html", params)

def review(request):
    if request.method == "POST":
        user = request.user
        prod_id = request.POST.get('product_id', '')
        prod = Product.objects.get(id=prod_id)
        review_text = request.POST.get('review_text', '')
        rating = request.POST.get('rate', '')
        data = Review(User=user, Product=prod, Review=review_text, Rating=rating)
        data.save()
        return redirect(f'/shop/product-{prod_id}')

def Get_OTP(request):
    """Sends OTP To The User's Email Address."""
    digits="0123456789"
    global list_digits
    list_digits = []
    OTP = ""
    for i in range(5):
        OTP += digits[math.floor(random.random()*10)]
    for x in OTP:
        list_digits.append(x)
        print(list_digits)
    global msg 
    msg = OTP + " is your OTP for verifying your account for Jalaram Bandhani House."
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("jalarambandhanihouse@gmail.com", "pzcfghwqwdpdwqvl")
    emailid = request.user.email
    s.sendmail("", emailid, msg)

def New_Order():
    message = "New Order Has Been Placed !"
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login("jalarambandhanihouse@gmail.com", "pzcfghwqwdpdwqvl")
    s.sendmail("", "thakkarmeena917@gmail.com", message)
    
def Verify(request):
    Get_OTP(request)
    return render(request, "OTP_Verification.html")

def Place_Order():
    """Places The Order Successfully."""
    global thank
    thank = True

    global items, email, fname, lname, username, address_1, address_2, state, city, zip_code, phone, items_json, amount

    place_order = Order(Items=items, Email=email, First_name=fname, Last_name=lname, Username=username, Address_1=address_1, Address_2=address_2, State=state, City=city, Zip_Code=zip_code, Phone=phone, Json=items_json, Amount=amount)
    place_order.save()
    global id
    id = place_order.order_id
    update = Order_Update(Order_Id=place_order.order_id, Update="The Order Has Been Placed !")
    update.save()

def Paying_Options(request):
    """Takes All The Details Of Place Order Form As Input."""
    if request.method == "POST":
        global items
        items = request.POST.get('itemsjson', '')
        global items_json
        items_json = request.POST.get('itemjson', '')
        global email
        email = request.user.email
        global fname 
        fname = request.user.first_name
        global lname 
        lname = request.user.last_name
        global username
        username = request.user.username
        global address_1
        address_1 = request.POST.get('address_1', '')
        global address_2 
        address_2 = request.POST.get('address_2', '')
        global state
        state = request.POST.get('state', '')
        global city
        city = request.POST.get('city', '')
        global zip_code
        zip_code = request.POST.get('zip_code', '')
        global phone
        phone = "+91" + request.POST.get('phone', '')
        global amount
        amount = request.POST.get('amount', '')

        amount = int(amount)
        if state == "Maharashtra":
            messages.info(request, f"As you are from {state} , You will have to pay Rs. 60 as a delivery charge extra.")
            amount = amount + 60
        else:
            messages.info(request, f"As you are from {state} , You will have to pay Rs. 100 as a delivery charge extra.")
            amount = amount + 100
        return render(request, "Paying_Options.html")
    return HttpResponse( "404 Not Found !")

def Payment_Proceed(request):
    """Takes Paying Option As Input."""
    if request.method == "POST":
        global value
        value = request.POST.get('paying-options', '')
        global string
        if value == "advance":
            string = "Pay In Advance"
            return redirect('/verify')
        elif value == "half":
            string = "Half In Advance and Half On Delivery"
            return redirect('/verify')
    return HttpResponse('404 - Not Found')

def Verifying(request):
    """Verifies The User Account And Sends QR Code To Them If Successfully Verified."""
    if request.method == 'POST':
        txt1 = request.POST['txt1']
        txt2 = request.POST['txt2']
        txt3 = request.POST['txt3']
        txt4 = request.POST['txt4']
        txt5 = request.POST['txt5']

        if txt1 == list_digits[0] and txt2 == list_digits[1] and txt3 == list_digits[2] and txt4 == list_digits[3] and txt5 == list_digits[4]:
            messages.success(request, "Verification Successful !")

            sender = "prachi412007@gmail.com"
            emailid = request.user.email
            
            new_msg = EmailMessage()
            new_msg['Subject'] = "Payment Info"
            new_msg['From'] = sender
            new_msg['To'] = emailid

            msg = f"Option Chosen For Payment : {string}\nTotal Amount To Be Paid : {amount}\nPay According To The Payment Option Selected !\n If You have selected Pay In Advance, Pay The Amount : {amount}\n If You have selected Half in Advance And Half On Delivery, Pay The Amount : {amount/2}\n In Case Of Any Error or Mistake In The Amount Paid By You , The Owner Will Contact You !"
            new_msg.set_content(msg)

            with open('shop/qr_code.jpeg', 'rb') as f:
                image_data = f.read()
                image_type = imghdr.what(f.name)
                image_name = f.name

            s = smtplib.SMTP('smtp.gmail.com', 587)
            s.starttls()
            s.login(sender, "kmztdeipmhodtitz")

            new_msg.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)

            s.send_message(new_msg)
            New_Order()
            Place_Order()
            return render(request , "Thank_You.html" , {'thank': thank, 'id': id, 'value' : string})
        else:
            messages.error(request, "Invalid Verification Code ! Try Again !")
            
    return HttpResponse("404 - Not Found !")

def Thank_You(request):
    """Shows Thank You Page With Order Id To The User."""
    return render(request, "Thank_You.html", {'id' : id, 'value': string})

