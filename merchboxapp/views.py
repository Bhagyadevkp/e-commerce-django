import datetime
import random
from collections import Counter

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.forms import ModelForm
from django.shortcuts import render, HttpResponse, redirect

# Create your views here.



from django.http import  HttpResponseRedirect
from django.utils import timezone


from merchboxapp.models import additems, catelog, merchshop, subcatelog
from shopcart.models import cartitems, buy


def first(request):
    # addedprod = additems.objects.filter(user_id=request.user.id)
    addedprod = additems.objects.all()

    for f in addedprod:
        s = f.expdate - timezone.now()
        # print(s)
        if s <= datetime.timedelta(0):
            # print('hai')
            v = additems.objects.get(pk=f.id)
            # print(v.prod_id)
            v.flag = 0
            c=cartitems.objects.filter(productid=v.prod_id)
            c.delete()
            v.save()


        elif f.stock == 0:
            v = additems.objects.get(pk=f.id)
            c = cartitems.objects.filter(productid=v.prod_id)
            c.delete()

        else:
            nhu=0

    # i=additems.objects.filter(title).exists()

    addprod = merchshop.objects.filter(productavailability=1).order_by('-dateadded')
    # for i in addprod:


    for i in addprod:
        ii=0
        aa=additems.objects.filter(title=i.shopname)
        for j in aa:

                if j.flag == 1 and j.stock >0:
                    ii=1

                    break
        if ii != 1:
            # print(i.shopname)
            # print(i.productavailability)
            i.productavailability=0
            i.save()
        else:
            pass

    d=catelog.objects.all()
    e=subcatelog.objects.all()

    # for j in d:
    #
    #     for i in e:
    #
    #         if j.id is i.maincategoryname.id:
    #             # print(i.maincategoryname)
    #             pass



    u=merchshop.objects.all()
    ar=[]
    for i in u:
        # print(i.shopname)
        j=buy.objects.filter(shopname=i.shopname)

        for k in j:
            # print(k.shopname)
            w=int(k.quantity)
            for c in range(1,w+1):
                # print(c)
                ar.append(k.shopname)
    # print(ar)


    # res = max(set(ar), key = ar.count)
    result = [item for items, c in Counter(ar).most_common() for item in [items] * c]
    # print(result)

    arr=[]
    u=1
    for i in result:
        if i not in arr:
            if u<=5:
                # r=merchshop
                arr.append(i)
                u=u+1
            else:
                break

    ar2=[]
    for i in arr:
        c=merchshop.objects.all()
        for j in c:
            if i == j.shopname:
                ar2.append(j.id)

    w=merchshop.objects.filter(shopname__in=arr)
    # for i in w:
    #     print(i.shopname)
    # k=merchshop.objects.filter(shopname_in=arr)
    # # print(k)
    # for i in k:
    #     print(i.title)

    # print(ar)
    return  render(request,'index.html',{'addprod':addprod,'d':d,'e':e,'w':w})

@login_required(login_url='loginned')
def add(request,id,name,subcategoryname):

    # print(id)
    # print('working')
    e=merchshop.objects.get(id=id)
    if e.user.id==request.user.id:
        if request.method == 'POST':
                # print('working2')
                while True:
                  smallest = 1000
                  largest = 9999
                  random_number = random.randint(smallest, largest - 1)
                  if additems.objects.filter(prod_id=random_number).exists():
                        pass
                    # print('good')
                    # messages.error(request, "choose another number for ur product")
                    # return render(request, 'add.html')
                  else:
                        break
            # print('working inside')
                names = request.POST['name']



                # print(random_number)


                f = catelog.objects.get(name=name)
                c = subcatelog.objects.get(subcategoryname=subcategoryname)
                subcategory=c.subcategoryname
                # f=catelog.objects.get(name=request.POST['category'])

                category = catelog.objects.get(id=f.id)

                # print(request.user.id)
                # s=merchshop.objects.get(user_id=request.user.id)

                s = merchshop.objects.get(id=id)
                prod_id=random_number
                slug=random_number


                title = s.shopname
                tt=merchshop.objects.get(shopname=title)
                tt.dateadded=timezone.now()
                tt.save()
                desc =  request.POST['desc']
                k=  request.POST['price']
                price=int(k)
                if request.POST['offerprice']:
                    c=request.POST['offerprice']
                    f=int(c)
                    offerprice = f
                else:
                    offerprice = 0


                # print(offerprice)
                # print(price)
                offerprice=int(offerprice)
                price=int(price)
                if offerprice > price :
                    messages.success(request, "offer price should be less than price")
                    print('1st')
                    return render(request, 'add.html')
                if offerprice < 0:
                    messages.success(request, "offer price should be above 0")
                    print('second')
                    return render(request, 'add.html')
                if price <= 0:
                    messages.success(request, "offer price should be above 0")
                    print('third')
                    return render(request, 'add.html')
                # offerprice = request.POST.get('offerprice',False)
                w = request.POST['stock']
                stock=int(w)
                flag=1
                image1 = request.FILES['image1']
                image2 = request.FILES.get('image2', False)
                image3 = request.FILES.get('image3', False)
                image4 = request.FILES.get('image4', False)

                user = User.objects.get(pk=request.user.id)
                # print(user.username)
                dealer=user.username
                # print(s.phonenumber)
                phonenumber =s.phonenumber
                addinfo = additems(offerprice=offerprice,stock=stock,flag=flag,slug=slug,prod_id=prod_id,name=names,image1=image1,image2=image2,image3=image3,image4=image4,category=category,subcategory=subcategory,title=title,desc=desc,price=price,dealer=dealer,phonenumber=phonenumber,user=user,expdate=timezone.now()+datetime.timedelta(days=10))
                # print(slug)
                addinfo.save()
                messages.success(request, "submitted successfully")
                if additems.objects.filter(title=title).exists():
                    c=merchshop.objects.get(shopname=title)

                    # print(c.productavailability)
                    c.productavailability = 1
                    c.save()

                return redirect('profile')
        else:
            # a=merchshop.objects.get(id=id)
            # b=catelog.objects.get(name=name)
            # c=subcatelog.objects.get(subcategoryname=subcategoryname)
            # return render(request,'add.html',{'a':a,'b':b,'c':c})
            return render(request,'add.html')

    else:
        return redirect('profile')



# def extshop(request):
#
#     if merchshop.objects.filter(user=request.user.id).exists():
#             viewshop=merchshop.objects.filter(user_id=request.user.id)
#             # print('good1')
#             # distinct_users = addshop.objects.all().values('user_id').distinct()
#             # for i in viewshop:
#             #     print(i.shopname)
#             # s=merchshop.objects.get(shopname=viewshop.shopname)
#             # s=merchshop.objects.get()
#             # print(s.shopname)
#             return render(request, "viewshop.html",{'viewshop':viewshop})
#     else:
#             messages.error(request, 'you have not registered anyshop')
#             return render(request, "merchant.html")

def addshop(request):
    if request.method=='POST':

        s=request.POST['shopname']
        # print(s)

        if merchshop.objects.filter(shopname=s).exists():
            # print('hood')
            messages.error(request,'this name is already used')
            return render(request,'addshop.html')



        else:


            phonenumber=request.POST['phonenumber']
            # p=int(phonenumber)
            c=len(phonenumber)

            # for i in range(0,c):
            #     print(i)
            #     for j in range(0,10):
            #         print(j)
            #
            #         if phonenumber[i] is j:
            #             break;
            #         if j is 9:
            #
            #             messages.error(request, 'please enter a valid phonenumber')
            #             return render(request, 'addshop.html')



            # if p is not type(int):
            #     messages.error(request, 'please enter a valid phonenumber')
            #     return render(request, 'addshop.html')
            shopimage1=request.FILES.get('shopimage1',False)
            shopimage2 = request.FILES.get('shopimage2', False)
            shopimage3 = request.FILES.get('shopimage3', False)
            shopimage4 = request.FILES.get('shopimage4', False)
            location=request.POST['location']
            city=request.POST['city']
            district=request.POST['district']
            user = User.objects.get(pk=request.user.id)
            addinfo = merchshop(shopname=s, phonenumber=phonenumber, shopimage1=shopimage1,shopimage2=shopimage2,shopimage3=shopimage3,shopimage4=shopimage4, user=user,location=location,city=city,district=district)
            addinfo.save()
            messages.success(request,'shop created successfully,choose add to existing shop option to start adding products')
            return redirect('profile')

    else:
        return render(request,'addshop.html')


def detailprod(request,id):
    iid=id
    print(id)
    if merchshop.objects.filter(id=iid).exists():
        print(id)
        just=merchshop.objects.get(id=iid)
        print("good")
        detailprodct = additems.objects.filter(title=just.shopname,flag=1,stock__gt= 0)
        # for i in detailprodct:
        #     print(i.name)
        # a=cartitems.objects.filter(cart=request.user.id)
        # l = [p.productid for p in a]
        d=catelog.objects.all()
        e=subcatelog.objects.all()
        return render(request,'detailprod.html',{'detailprodct':detailprodct,'just':just,'d':d,'e':e})
    else:
        d=catelog.objects.all()
        e=subcatelog.objects.all()
        return render(request, 'detailprod.html', {'d':d,'e':e})

    # return render(request, 'detailprod.html')


def filter(request,name):
    # print(name)
    try:
        # print(name)
        o=subcatelog.objects.get(subcategoryname=name)
        # print(o)
        a=additems.objects.distinct("title").filter(subcategory=o.subcategoryname)

        for i in a:
            print(i.title)
        # a=additems.objects.distinct("category").filter(category=c.id)
        # print('iiii')
        # c=additems.objects.distinct("title").filter(subcategory=a.subcategory)
        # print('ll')
        # for i in c:
        #     print(i)

        # for i in c:
        #     print(i.title)
        b=merchshop.objects.filter(productavailability=1).order_by('-dateadded')

        # addprod = merchshop.objects.filter(productavailability=1).order_by('-dateadded')
        d = catelog.objects.all()
        e=subcatelog.objects.all()

        return render(request, 'index.html', { 'd': d,'a':a,'b':b,'e':e})

    except:
        return redirect('/')


def myorders(request):
    s=request.user
    if buy.objects.filter(purchaser=s).exists():
        a=buy.objects.filter(purchaser=s)
        b=additems.objects.all()
        return render(request,'myorders.html',{'a':a,'b':b})
    else:
        return redirect('profile')


def ordersplaced(request):
    s=request.user.id
    n=merchshop.objects.filter(user=s)
    for i in n:
        if buy.objects.filter(shopname=i.shopname).exists():


            k=merchshop.objects.filter(user=s)
            p=additems.objects.all()
            v=buy.objects.all()
            return render(request,'ordersplaced.html',{'k':k,'v':v,'p':p})
        else:
            vv=1
            return render(request,'ordersplaced.html',{'vv':vv})

def singleproductdetail(request,id):
    if additems.objects.filter(prod_id=id).exists():
        s=additems.objects.get(prod_id=id)
        a = cartitems.objects.filter(cart=request.user.id).order_by('-dateadded')
        l = [p.productid for p in a]
        ww=additems.objects.all()
        d=catelog.objects.all()
        e=subcatelog.objects.all()
        # print(e.name)
        # print(e.title)
        return render(request,'singleproductdetail.html',{'s':s,'l':l,'d':d,'e':e})
    else:
        d=catelog.objects.all()
        e=subcatelog.objects.all()
        return render(request, 'singleproductdetail.html',{'d':d,'e':e})

def search(request):
    prodt=None
    query=None

    if 'search' in request.GET:

        query=request.GET.get('search').lower()
        
        
        length = len(query)
        prodt=merchshop.objects.filter(productavailability=1).order_by('-dateadded')
        vars = []
        p = 1
        for i in prodt:
            l=0
            for j in range(0,length):
                try:
                    if i.shopname[j].lower() == query[j]:
                        l+=1
                        if l==len(query):
                                p=0
                                vars.append(i.shopname)
                    else:
                        break
                except:
                    break      

        d = catelog.objects.all()
        e=subcatelog.objects.all()
        print(vars)
        return render(request,'index.html',{'search':prodt,'vars':vars,'d':d,'p':p,'e':e})


    else:
        return redirect('/')


def searchproduct(request):

    if 'searchproduct' in request.GET:

        query = request.GET.get('searchproduct').lower()

        # print(query)
        length = len(query)
        prodt = additems.objects.filter(flag=1,stock__gt= 0).order_by('-date')
        vars = []
        p = 1
        for i in prodt:
            l = 0
            for j in range(0, length):
                try:
                    if i.name[j].lower() == query[j]:
                        l += 1
                        if l == len(query):
                            p=0
                            vars.append(i.name)
                    else:
                        break
                except:
                    break        
        o=merchshop.objects.all()
        d = catelog.objects.all()
        e=subcatelog.objects.all()

        return render(request, 'searchproduct.html', {'searchproduct': prodt, 'vars': vars, 'd': d,'p':p,'e':e,'o':o})


def searchlocation(request):
    print('hoo11')
    if 'searchlocation' in request.GET:
        print('hoo')
        query = request.GET.get('searchlocation').lower()

        # print(query)
        length = len(query)
        prodt = merchshop.objects.filter(productavailability=1).order_by('-dateadded')
        location = []
        p = 2
        for i in prodt:
            l = 0
            for j in range(0, length):
                try:
                    if i.location[j].lower() == query[j]:
                        l += 1
                        if l == len(query):
                            p=0
                            location.append(i.shopname)
                           

                    else:
                        break
                except:
                    break        

        district=[]            
        
        
        for i in prodt:
                l = 0
                for j in range(0, length):
                    try:
                        if i.district[j].lower() == query[j]:
                            l += 1
                            if l == len(query):
                                p=0
                                district.append(i.shopname)
                        else:
                            break    
                    except:
                        break              

        # print(district)                                 

        d = catelog.objects.all()
        e=subcatelog.objects.all()

        return render(request, 'index.html', {'searchlocation': prodt, 'location': location,'district':district, 'd': d,'p':p,'e':e})

@login_required(login_url='loginned')
def categcreation(request,id):
    shop=merchshop.objects.get(id=id)


    if shop.user.id == request.user.id:
        categcreations=catelog.objects.all()
        subcategcreation=subcatelog.objects.all()
        return render(request,'categcreation.html',{'categcreations':categcreations,'shop':shop,'subcategcreation':subcategcreation})
    else:
        return redirect('profile')

# def subcategcreation(request,name,id):
#     if name :
#         c = catelog.objects.get(name=name)
#     else:
#         return redirect('/')
#
#     subcateg=subcatelog.objects.filter(maincategoryname=c.id)
#     shop=merchshop.objects.get(id=id)
#     # for i in subcateg:
#     #   print(i.subcategoryname)
#     return render(request,'subcategceation.html',{'c':c,'shop':shop,'subcateg':subcateg})


def profile2(request):
    print('pp')
    return  render(request,'profile2.html')


def extexp(request):
    c=additems.objects.all()
    for i in c:
        i.expdate = timezone.now() + datetime.timedelta(days=150)
        if i.stock == 0:
            i.flag=0
        else:
            i.flag=1
            ww = merchshop.objects.filter(shopname=i.title)
            for e in ww:
                e.productavailability = 1
                e.save()
        i.save()

    return redirect('/')