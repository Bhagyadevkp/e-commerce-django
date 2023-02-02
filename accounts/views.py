import datetime
import email
from django.contrib.auth.decorators import login_required
# import view as view
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.validators import validate_email
from django.utils import timezone


from merchboxapp.models import additems, catelog, merchshop
from shopcart.models import buy, cartitems
from .utils import token_generator
from django.contrib import messages
from django.core.mail import send_mail, EmailMessage
from django.forms import ModelForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render,redirect
from  django.contrib.auth.models import User,auth

from django.template import RequestContext
from django.urls import reverse
from django.views import View

from django.apps import apps
# from merchboxapp.forms import carForm


from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site


def register(request):
    if request.method=='POST':

        user_name = request.POST['user_name']
        # phonenumber= request.POST['phonenumber']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']
        # if password1==password2:
        if User.objects.filter(username=user_name).exists():
                messages.error(request,"username_taken")
                return  render(request,'register.html')
        elif User.objects.filter(email=email).exists():
                messages.error(request,"email_taken")
                return  render(request,'register.html')
        elif len(password1)<6:
                messages.error(request,"password too short")
                return  render(request,'register.html')

        elif password1 == password2:
                user=User.objects.create_user(username=user_name,email=email,password=password1)

                # user.set_password(password1)
                # user.is_active=False
                user.is_active = False
                user.save()


                uidb64=urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link=reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})
                email_subject = 'activate your account'
                activate_url='http://'+domain+link
                email_body='hi'+user.username+\
                            ',username:'+user.username+\
                           ',please verify your account\n'+ activate_url
                print("user created")
                email=EmailMessage(
                        email_subject,
                        email_body,
                        'salmansaalu10@gmail.com',
                        [email],

                    )

                email.send(fail_silently=False,)
                # send_mail(
                #     email_subject,
                #     email_body,
                #     'salmansaalu10@gmail.com',
                #     ['salmanpp05@gmail.com'],
                #     fail_silently=False,
                # )
                messages.success(request,'Check your mail for account verification')
                return redirect('register')
        else:
            print("password not match")
            messages.error(request, "password not match")
            return redirect('register')
    #     return redirect('/')
    # else:
    else:
        return render(request,'register.html')

class verificationView(View):
    def get(self,request,uidb64,token):
        print('good')
        try:
            id=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=id)

            if user.is_active:
                return redirect('loginned')
            # if not account_activation_token.check_token(user,token):
            #     return  redirect('login'+'?message='+'user already activated')

            user.is_active=True
            user.save()

            messages.success(request,'account activated succesfuly')
            return redirect('loginned')
        except Exception as e:
            pass
        return redirect('loginned')

class loginView(View):
    def get(self,request):
        # return redirect('loginned')
        return render(request,"login.html")
    def post(self,request):
        username=request.POST['user_name']
        password=request.POST['password']

        if username and password:
            user=auth.authenticate(username=username,password=password)
            if user:
                if user.is_active:
                    auth.login(request,user)
                    return redirect('/')
                messages.error(request,'account is not active please check ur mail')
                return render(request,'login.html')
            messages.error(request, 'invalid details,try again')
            return render(request, 'login.html')
        messages.error(request, 'please fill fields')
        return render(request, 'login.html')

#
#
# def requestpassword(request):
#     if request.method=='POST':
#                 print('work')
#                 email = request.POST['email']
#                 context={
#                 'values':request.POST
#         }
#
#                 # if not validate_email(email):
#                 #     messages.error(request,'please supply a valid email')
#                 #     return render(request, "reset-password.html")
#                 user=User.objects.filter(email=email)
#                 current_site=get_current_site(request)
#                 if user.exists():
#                     email_contents = {
#                         'user': user[0],
#                         'domain':current_site.domain,
#                         'uidb64': urlsafe_base64_encode(force_bytes(user[0].pk)),
#                         'token': PasswordResetTokenGenerator().make_token(user[0])
#
#                     }
#                     # uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
#
#                     link = reverse('resetuserpassword', kwargs={'uidb64': email_contents['uidb64'], 'token': email_contents['token']})
#                     email_subject = 'password reset instructions'
#                     reset_url = 'http://' + current_site.domain + link
#                     email_body = 'hi' + user.username + \
#                                  ',username:' + user.username + \
#                                  ',please click to reset password\n' +reset_url
#                     print("user created")
#                     email = EmailMessage(
#                         email_subject,
#                         email_body,
#                         'salmansaalu10@gmail.com',
#                         [email],
#
#                     )
#
#                     email.send(fail_silently=False, )
#
#                 messages.success(request,'we have send u email to reset password')
#
#                 return render(request,"reset-password.html")
#
#     return render(request,"reset-password.html")
# # class RequestPasswordResetEmail(View):
# #
#     def get(self,request):
# #
# #
#         return render(request,"reset-password.html")
#
# def postpassword(request):
# class RequestPasswordResetEmail(View):

# def post(request):
#     if request.method=='POST':
#         print('work')
#         email=request.POST['email']

        # context={
        #     'values':request.POST
        # }
#
#         # if not validate_email(email):
#         #     messages.error(request,'please supply a valid email')
#         #     return render(request, "reset-password.html")
#         user=User.objects.filter(email=email)
#         current_site=get_current_site(request)
#         if user.exists():
#             email_contents = {
#                 'user': user[0],
#                 'domain':current_site.domain,
#                 'uidb64': urlsafe_base64_encode(force_bytes(user[0].pk)),
#                 'token': PasswordResetTokenGenerator().make_token(user[0])
#
#             }
#             # uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
#
#             link = reverse('resetuserpassword', kwargs={'uidb64': email_contents['uidb64'], 'token': email_contents['token']})
#             email_subject = 'password reset instructions'
#             reset_url = 'http://' + current_site.domain + link
#             email_body = 'hi' + user.username + \
#                          ',username:' + user.username + \
#                          ',please click to reset password\n' +reset_url
#             print("user created")
#             email = EmailMessage(
#                 email_subject,
#                 email_body,
#                 'salmansaalu10@gmail.com',
#                 [email],
#
#             )
#
#             email.send(fail_silently=False, )
#
#         messages.success(request,'we have send u email to reset password')
#
#         return render(request,"reset-password.html")

# class CompletePasswordReset(view):
#
#
#     def get(self,request,uidb64,token):
#         return render(request,'set-new-password.html')
#
#     def post(self,request,uidb64,token):
#         return render(request,'set-new-password.html')

# def login(request):
#
#     if request.method=='POST':
#         user_name=request.POST['user_name']
#         password=request.POST['password']
#         user=auth.authenticate(username=user_name,password=password)
#         if user is not None:
#             auth.login(request,user)
#             return redirect('/')
#
#         else:
#             messages.info(request,'invalid details')
#             return redirect('login')
#
#     else:
#         return  render(request,"login.html")

def logout(request):
    auth.logout(request)
    return  redirect('/')





# def merchant(request):
#     if request.user.is_authenticated:
#         # return render(request, "merchant.html")
#
#         return render(request, "merchant.html")
#     elif request.method == 'POST':
#
#          user_name = request.POST['user_name']
#          password = request.POST['password']
#          user = auth.authenticate(username=user_name, password=password)
#          if user is not None:
#              auth.login(request, user)
#              return redirect('merchant')
#
#
#          else:
#
#              messages.info(request, 'invalid details,try again')
#              return redirect('merchant')
#
#
#     else:
#         return render(request, "login2.html")







@login_required(login_url='loginned')

def profile(request):

            # v.delete()


    if merchshop.objects.filter(user=request.user.id).exists():
            viewshop=merchshop.objects.filter(user_id=request.user.id).order_by('-dateadded')
            s = request.user

            a = buy.objects.filter(username=s).order_by('-dateadded')
            b = additems.objects.all()

            ss = request.user.username
            if buy.objects.filter(sellinguser=ss).exists():
                n=buy.objects.filter(sellinguser=ss).order_by('-dateadded')
                p = additems.objects.all()
                vv=0
                return render(request, "profile.html", {'viewshop': viewshop, 'a': a, 'b': b,'n':n,  'p': p, 'vv': vv})
            # n = merchshop.objects.filter(user=ss).order_by('-dateadded')

            # for i in n:
            #     if buy.objects.filter(shopname=i.shopname).exists():
            #
            #         k = merchshop.objects.filter(user=ss).order_by('-dateadded')
            #
            #         p = additems.objects.all()
            #         v = buy.objects.all().order_by('-dateadded')
                    # for i in v:
                    #     print(i.dateadded)
                    # vv=0
                    # return render(request, "profile.html",
                    #               {'viewshop': viewshop, 'a': a, 'b': b, 'k': k, 'v': v, 'p': p, 'vv': vv})

            vv = 1
            return render(request, "profile.html",{'viewshop': viewshop, 'a': a, 'b': b, 'vv': vv})
    s = request.user
    if buy.objects.filter(username=s).exists():
        # print('koo')
        a = buy.objects.filter(username=s).order_by('-dateadded')
        b = additems.objects.all()

        # ss = request.user.id
        # n = merchshop.objects.filter(user=ss).order_by('-dateadded')
        #
        # for i in n:
        #     if buy.objects.filter(shopname=i.shopname).exists():
        #         k = merchshop.objects.filter(user=ss).order_by('-dateadded')
        #
        #         p = additems.objects.all()
        #         v = buy.objects.all().order_by('-dateadded')
        #         vv = 0
        #         return render('profile.html',{'a': a, 'b': b, 'k': k, 'v': v, 'p': p, 'vv': vv})

        vv=1
        return render(request, 'profile.html', {'a': a, 'b': b,'vv':vv})


    else:

        vv = 1
        return render(request,'profile.html',{ 'vv': vv})

            # return render(request, "profile.html",{'ap':addedprod})
@login_required(login_url='loginned')

def detailshop(request,shopname):
    # print('working')
    viewshop = merchshop.objects.filter(user_id=request.user.id).order_by('-dateadded')

    a=merchshop.objects.get(shopname=shopname)
    if a.user.id == request.user.id:

    # print(request.user.id)
        addedprod = additems.objects.filter(title=shopname)
        shop=merchshop.objects.get(shopname=shopname)
        return render(request,'detailshop.html',{'ap':addedprod,'shop':shop,'viewshop':viewshop})
    else:
        return redirect('profile')



    # carview = vehicle.objects.filter(user_id=request.user.id)
    # wholesaleview= wholesale.objects.filter(user_id=request.user.id)
    # # image=car.objects.filter(image=car.image)
    # # carview = car.objects.filter(id=request.user.id)
    # return render(request, "profile.html", {'carview': carview,'wholesaleview':wholesaleview})


def update(request,id):



    if request.method=="POST":


            productview =additems.objects.get(id=id)
            f = catelog.objects.get(name=request.POST['category'])
            productview.category = catelog.objects.get(id=f.id)
            # print(productview.category)
            productview.name = request.POST['name']
            productview.subcategory = request.POST['subcategory']
            # productview.slug = productview.name

            # productview.title = request.POST['title']
            # productview.flag=request.POST['flag']
            productview.desc = request.POST['desc']
            price = request.POST['price']
            productview.price=int(price)
            productview.offerprice=request.POST['offerprice']
            if request.POST['offerprice']:
                if request.POST['offerprice'] == 0:
                    productview.offerprice = 0
                else:    
                    c = request.POST['offerprice']
                    f = int(c)
    
                    productview.offerprice = f
            else:
                productview.offerprice = 0

            if productview.offerprice > productview.price :
                messages.success(request, "offer price should be less than price")
                print('1st')
                return render(request, 'update.html')
            if productview.offerprice < 0:
                messages.success(request, "offer price should be above 0")
                print('second')
                return render(request, 'update.html')
            if productview.price <= 0:
                messages.success(request, "offer price should be above 0")
                print('third')
                return render(request, 'update.html')
            w = request.POST['stock']
            productview.stock=int(w)
            # print(productview.stock)
            productview.image1 = request.FILES['image1']
            productview.image2 = request.FILES.get('image2', False)
            productview.image3 = request.FILES.get('image3', False)
            productview.image4 = request.FILES.get('image4', False)

            # user = User.objects.get(pk=request.user.id)

            # addinfo = products(slug=productview.slug, name=productview.name, image1=productview.image1, image2=productview.image2, image3=productview.image3, image4=productview.image4,
            #                    category=productview.category, title=productview.title, desc=productview.desc, location=productview.location, price=productview.price, city=productview.city,
            #                    dealer=productview.dealer, phonenumber=productview.phonenumber, user=user)
            productview.save()
            w=merchshop.objects.get(shopname=productview.title)
            w.productavailability=1;
            w.save()
            # s=additems.objects.get(id=)
            messages.success(request, "submitted successfully")

            return redirect('profile')
#     else:
#         form=carForm(instance=carview)
#     form = productForm()
    updateproduct=additems.objects.get(id=id)
    return render(request, "update.html",{'updateproduct':updateproduct})

def delete(request,id):
            # print('delete')
    # if request.method=="POST":

            wholesaleview = additems.objects.get(id=id)
            if buy.objects.filter(productid=wholesaleview.prod_id).exists():
                p=buy.objects.filter(productid=wholesaleview.prod_id)
                for i in p:


                    if i.delivery == 'no':

                        messages.success(request,'u cannot delete this item since order has already placed for this product..u can delete this product after delivering it')
                        return redirect('profile')
            e=wholesaleview.prod_id
            wholesaleview.delete()
            if cartitems.objects.filter(productid=e).exists():
                h=cartitems.objects.filter(productid=e)
                h.delete()
            if buy.objects.filter(productid=e).exists():
                g=buy.objects.filter(productid=e)
                for u in g:
                    u.delete()


            return redirect('profile')







def stock_finished(request,id):
        addedprod = additems.objects.get(id=id)

        addedprod.stock=0
        addedprod.save()

        # addedprods = additems.objects.filter(title=shopname)
        return  redirect('profile')
        # return render(request, 'detailshop.html')

def ext_date(request, id):
            addedprod = additems.objects.get(id=id)
            # addedprod.flag = 2
            print('ki')
            # print(addedprod.expdate)
            addedprod.expdate=timezone.now()+datetime.timedelta(days=10)
            addedprod.flag=1
            addedprod.save()

            ww=merchshop.objects.get(shopname=addedprod.title)
            ww.productavailability=1
            ww.save()
            # addedprod.save()

            # addedprod = additems.objects.filter(title=shopname)
            return redirect('profile')


def edit_shop(request,id):
    if request.method=='POST':
        shop=merchshop.objects.get(id=id)
        c=shop.shopname
        shop.shopname=request.POST['shopname']

        change=additems.objects.filter(title=c)
        for i in change:
            i.title=shop.shopname
            i.save()

        shop.location=request.POST['location']
        shop.city=request.POST['city']
        shop.phonenumber=request.POST['phonenumber']
        shop.shopimage1 = request.FILES.get('shopimage1', False)
        shop.shopimage2 = request.FILES.get('shopimage2', False)
        shop.shopimage3 = request.FILES.get('shopimage3', False)
        shop.shopimage4 = request.FILES.get('shopimage4', False)
        shop.save()

        return redirect('profile')
    editshop = merchshop.objects.get(id=id)
    return render(request, "editshop.html", {'editshop': editshop})

def delete_shop(request,id):

        s=merchshop.objects.get(id=id)
        v=additems.objects.filter(title=s.shopname)
        for i in v:
            wholesaleview = additems.objects.get(id=i.id)
            if buy.objects.filter(productid=wholesaleview.prod_id).exists():
                p = buy.objects.filter(productid=wholesaleview.prod_id)
                for j in p:
                    if j.delivery == 'no':

                        messages.success(request,'u cannot delete this shop since order has already placed for the  products in this shop..u can delete this shop after delivering it')
                        return redirect('profile')
            # i.delete()
            # print(i)
        # print(s)
        # s.delete()
        # print('good')
        for k in v:
            e=k.prod_id
            print(k)
            k.delete()
            if cartitems.objects.filter(productid=e).exists():
                h=cartitems.objects.get(productid=e)
                h.delete()
            if buy.objects.filter(productid=e).exists():
                g=buy.objects.filter(productid=e)
                print('work')
                for u in g:
                    # print(u.productname)
                    u.delete()
        s.delete()

        return redirect('profile')






            # e=wholesaleview.prod_id
            # wholesaleview.delete()
            # g=buy.objects.get(productid=e)
            # g.delete()



import uuid
def forgetpassword(request):
    try:
        if request.method=='POST':
            username=request.POST.get('username')

            if not User.objects.filter(username=username).first():
                messages.success(request,'no user found with this username')
                return redirect('forgetpassword')

            user_obj=User.objects.get(username=username)
            # token = str(uuid.uuid4())
            uidb64 = urlsafe_base64_encode(force_bytes(user_obj.pk))
            domain = get_current_site(request).domain
            link = reverse('changepassword', kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user_obj)})

            # send_forget_password_email(user_obj,token)
            email_subject = 'yor forget password link'
            # activate_url = 'http://127.0.0.1:8000/changepassword/' + token
            activate_url = 'http://' + domain + link
            email_body = 'hi' + user_obj.username + \
                         ',username:' + user_obj.username + \
                         ',click on link to reset your password\n' + activate_url

            # emailnew=user_obj.email

            email = EmailMessage(
                email_subject,
                email_body,
                'salmansaalu10@gmail.com',
                [user_obj.email],)

            email.send(fail_silently=False, )
            # message = 'hi ,click on link to reset your password http://127.0.0.1:8000/changepassword/'+token
            # email_from = settings.EMAIL_HOST_USER
            # recipient_list = user_obj.email
            # send_mail(subject, message, email_from, recipient_list)
            messages.success(request, 'an email is send')
            return render(request, 'forgetpassword.html')
    except:
        return redirect('/')



    return render(request,'forgetpassword.html')

# def changepassword(request,token,uidb64):
#     print('good')
#     id = force_text(urlsafe_base64_decode(uidb64))
#     user = User.objects.get(pk=id)
#     return render(request,'changepassword.html')
class changepassword(View):
    def get(self,request,uidb64,token):
        print('good')
        try:
            id=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=id)


            return render(request,'changepassword.html')

        except Exception as e:
            pass
        return render(request,'changepassword.html')

    def post(self,request,uidb64,token):
        id = force_text(urlsafe_base64_decode(uidb64))
        print('newgood')
        password=request.POST.get('password')
        confirm_password=request.POST.get('passwordnew')
        user = User.objects.get(pk=id)

        if user is None:
            messages.success(request,'no user found')
            return render(request,'changepassword.html')

        if password!=confirm_password:
            messages.success(request, 'retype ur password')
            return render(request, 'changepassword.html')

        user.set_password(password)
        user.save()
        return redirect('loginned')


def pendingdelivery(request,id):
    c=buy.objects.get(id=id)
    c.delivery='yes'
    c.save()
    k=c.username
    user_obj=User.objects.get(username=k)


    email_subject = 'product delivering  successful'

    email_body = 'hi' + user_obj.username + \
                 ',username:' + user_obj.username + \
                 ',product delivered ...'+\
                 'NOTE:if u havent recieved the product contact the shopowner \n'



    email = EmailMessage(
        email_subject,
        email_body,
        'salmansaalu10@gmail.com',
        [user_obj.email], )

    email.send(fail_silently=False, )
    return redirect('profile')



