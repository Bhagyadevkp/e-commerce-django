from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect


# Create your views here.
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from accounts.utils import token_generator
from shopcart.models import cart, cartitems, buy
from merchboxapp.models import additems, merchshop, catelog, subcatelog


def cartdetails(request):
    if request.user.is_authenticated:

        # s=cart.objects.all()
        # for i in s:
            # if request.user.id==s.cart_id:
            if cart.objects.filter(cart_id=request.user.id).exists():
                # print(request.user.id)
                c=cartitems.objects.filter(cart=request.user.id).order_by('-dateadded')
                if cartitems.objects.filter(cart=request.user.id).exists():
                    for n in c:
                        if  n.quantity == 0:
                            # print('goood')
                            n.delete()
                f=cartitems.objects.filter(cart=request.user.id).count()
                ff=0
                for i in c:
                    ff=i.quantity+ff

                # for i in c:
                #     a=additems.objects.filter(name=i)
                #     print(a)
                # print(a)
                # print(c)
                for i in c:
                    # print(i.productid)
                    j = additems.objects.get(prod_id=i.productid)
                    if i.quantity > j.stock:
                        i.quantity=j.stock
                        if j.offerprice:
                            o=int(j.offerprice)*int(j.stock)
                        else:
                            o=int(i.price)*int(j.stock)
                        i.price=o
                        i.save()


                a=additems.objects.all()
                b=cart.objects.get(cart_id=request.user.id)
                # v=b.cart_id
                v=0



                for i in c:
                    v=i.price + v
                d = catelog.objects.all()
                e = subcatelog.objects.all()
                return render(request, 'cart.html',{'c':c,'a':a,'v':v,'d':d,'e':e,'f':f,'ff':ff})

        # c = cart.objects.filter(cart_id=request.user.id)
            else:
                cart_id=request.user.id
                date_added=timezone.now()
                c=cart(cart_id=cart_id,date_added=date_added)
                c.save()
                return render(request,'cart.html')


        # merchshop.objects.filter(user_id=request.user.id)
        # if request.user.id==
        # print(request.user.id)


    else:


        # return render(request,'index.html')
        return redirect('loginned')

#
def cartitemsadded(request,id,shopname):
    # print('working')
    # print(id)
    if request.user.id:
        s=additems.objects.get(prod_id=id)
        just = merchshop.objects.get(shopname=shopname)

        detailprodct = additems.objects.filter(title=just.shopname, flag=1, stock__gt=0)
        a = cartitems.objects.filter(cart=request.user.id).order_by('-dateadded')
        # if cartitems.objects.filter(productid=s.prod_id,cart=request.user.id).exists():
        #     # l = [p.productid for p in a]
        # #     # print(l)
        # #     return render(request, 'detailprod.html', {'detailprodct': detailprodct, 'a': a,'l':l})
        #      return redirect(request.META['HTTP_REFERER'])

        # return redirect('/')
        # print(s)


        cart=request.user.id
        # print(request.user.id)
        cartproduct=s.name
        productid=s.prod_id
        available=1
        quantity=1
        k = additems.objects.get(prod_id=id)
        if k.offerprice >0:
            price=k.offerprice
        else:
            price=k.price
        # print(cart,cartproduct,productid,available,quantity,price)
        crt=cartitems(cart=cart,cartproduct=cartproduct,productid=productid,available=available,quantity=quantity,price=price)
        crt.save()

        # l = [p.productid for p in a]
        e=s
        # return render(request, 'singleproductdetail.html', {'l':l,'e':e})
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect('loginned')

def addquan(request,id):
    # s = cart.objects.all()
    # for i in s:
    c=cartitems.objects.filter(cart=id).order_by('-dateadded')
    if c:
        for i in c:
            if i.quantity == 0:
                i.delete()
    #     if cart.objects.filter(cart_id=request.user.id).exists():
    k =cartitems.objects.get(cart=request.user.id,productid=id)
    a=additems.objects.get(prod_id=id)
    # if k.quantity < k.gotocart:

    if k.quantity < a.stock:

                    # j=cartitems.objects.get(cart=request.user.id,productid=id)
                    k.quantity=int(k.quantity)+1
                    if a.offerprice >0:
                        k.price = a.offerprice * k.quantity
                    else:
                        k.price=a.price * k.quantity
                    k.save()
    else:
        return redirect('cartdetails')



            # c = cartitems.objects.filter(cart=request.user.id)
            # for i in c:
            #     a=additems.objects.filter(name=i)
            #     print(a)
            # print(a)
            # print(c)
            # a = additems.objects.all()
            # return render(request, 'cart.html', {'c': c, 'a': a})
            #     return redirect('cartdetails')
    return redirect('cartdetails')
    # return redirect(request.META['HTTP_REFERER'])


def lessquan(request,id):
    # k = additems.objects.get(prod_id=id)
    # print(id)
    c=cartitems.objects.filter(cart=id).order_by('-dateadded')
    if c:
        for i in c:
            if i.quantity == 0:
                i.delete()
    k=cartitems.objects.get(productid=id,cart=request.user.id)
    a=additems.objects.get(prod_id=id)

    if k.quantity!=1:
        k.quantity = int(k.quantity) - 1
        k.price=a.price * k.quantity
        k.save()
        # j = cartitems.objects.get(cart=request.user.id, productid=id)
        # j.quantity = int(j.quantity) - 1
        # j.save()


    return redirect('cartdetails')
    # return redirect(request.META['HTTP_REFERER'])


def checkout(request):
    id=request.user.id
    c=cartitems.objects.filter(cart=id).order_by('-dateadded')
    if c:
        for i in c:
            if i.quantity == 0:
                i.delete()
    if c:



        for i in c:
            # print(i.productid)
            j=additems.objects.get(prod_id=i.productid)
            if i.quantity > j.stock:
                messages.info(request,'- available quantity')
                i.quantity=j.stock
                i.save()
                return redirect('cartdetails')
        #         c=1
        #
        # if c==1:
        v = 0
        for i in c:
            if i.quantity !=0:
                v = i.price + v
        a = additems.objects.all()
        # messages.info(request,'items currently available now,please checkout immediately to purchase!')
        w = []
        # p=c.count()






        return render(request,'checkout.html',{'c':c,'a':a,'v':v,'w':w})
    else:
        return redirect('/')


def purchase(request):


    id=request.user.id
    c = cartitems.objects.filter(cart=id).order_by('-dateadded')

    if c:

        for i in c:
        # print(i.productid)
            j = additems.objects.get(prod_id=i.productid)
            if i.quantity > j.stock:
                i.quantity=j.stock
                if j.offerprice:
                    i.price=int(i.quantity)*int(j.offerprice)
                else:
                    i.price=int(i.quantity)*int(j.price)
                i.save()
                c = cartitems.objects.filter(cart=id).order_by('-dateadded')
                a = additems.objects.all()
                v = id
                print('goooggg')
                messages.error(request, 'has only')
                return HttpResponseRedirect('checkout')
                # return redirect(request.META['HTTP_REFERER'])
            elif j.stock == 0:
                # e=cartitems.objects.get(productid=j.prod_id)
                # e.delete()
                i.price=0
                i.save()
                messages.error(request, 'has')
                return HttpResponseRedirect('checkout')
        if request.method == 'POST':
            username=request.POST['username']
            purchaser=request.POST['purchaser']
            email=request.POST['email']

            # print(request.POST['phonenumber'])
            phonenumber=request.POST['phonenumber']
            housename=request.POST['housename']
            area=request.POST['area']
            location=request.POST['location']
            district=request.POST['district']
            pin=request.POST['pin']

            c = cartitems.objects.filter(cart=id).order_by('-dateadded')
            v = 0
            for i in c:
                v = i.price + v


            for i in c:
                productid=i.productid
                productname=i.cartproduct
                x=additems.objects.get(prod_id=productid)
                f=x.title
                shopname=f
                quantity=i.quantity
                price=i.price
                totalprice=v
                iii=merchshop.objects.get(shopname=shopname)
                sellinguser=iii.user
                print('ll')
                print(pin)
                print(phonenumber)
                print(purchaser)
                print(location)
                print(area)
                k=buy(username=username,purchaser=purchaser, email=email,sellinguser=sellinguser, phonenumber=phonenumber, housename=housename, area=area, location=location, district=district, pin=pin, productid=productid, productname=productname,shopname=shopname, quantity=quantity, price=price, totalprice=totalprice,dateadded=timezone.now())
                k.save()
                x.stock=x.stock-quantity
                x.save()

        user_obj = User.objects.get(id=id)
        # token = str(uuid.uuid4())
        # uidb64 = urlsafe_base64_encode(force_bytes(user_obj.pk))
        # domain = get_current_site(request).domain
        # link = reverse('changepassword',
        #                kwargs={'uidb64': uidb64, 'token': token_generator.make_token(user_obj)})

        # send_forget_password_email(user_obj,token)
        email_subject = 'product ordering successful'
        # activate_url = 'http://127.0.0.1:8000/changepassword/' + token
        # activate_url = 'http://' + domain + link
        email_body = 'hi' + user_obj.username + \
                     ',username:' + user_obj.username + \
                     ',To check ordered products go to -> profile -> my orders \n'

        # emailnew=user_obj.email

        email = EmailMessage(
            email_subject,
            email_body,
            'salmansaalu10@gmail.com',
            [user_obj.email], )

        email.send(fail_silently=False, )
        # message = 'hi ,click on link to reset your password http://127.0.0.1:8000/changepassword/'+token
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = user_obj.email
        # send_mail(subject, message, email_from, recipient_list)


        for i in c:
            i.delete()
        messages.info(request,'product ordered successfully')
        messages.success(request, 'an email is send')
        return render(request,'purchased.html')

    else:
        messages.error(request, 'has')
        return redirect('checkout')


def remove(request,id):
    s=request.user.id
    c = cartitems.objects.filter(cart=s).order_by('-dateadded')

    for i in c:
        if i.productid==id:
            i.delete()
            return redirect(request.META['HTTP_REFERER'])

    return redirect('/')











