from django.shortcuts import render , redirect
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate , login , logout
from datetime import date
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from .models import property , person
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

propertie = property
# Create your views here.

def filt(data,filters):
    print(data,filters)
    if(filters.lower() in data.type.lower() or filters.lower() in data.foor.lower() ):
        return True
       
def public(request):
    prop = propertie.objects.all()
    count = ""
    query = ''
    if request.GET.get('search') != None:
        query = request.GET.get('search')
        prop = [item for item in prop if match(query,item)]
        if len(prop) == 0:
            count = 'No result for applied search'
        else:
            count = f'{len(prop)} results found'
        
    
    if request.GET.get('type') != None:
        print('getted')
        type = request.GET.get('type')
        status = request.GET.get('status')
        if status == 'Buy':
            status = 'sell'

       

        lsit = {'type' : type , 'status' : status }
        for i in lsit:
            prop = [item for item in prop if filt(item,lsit[i])]
        
        if len(prop) == 0:
            count = 'No result for applied filters'
        else:
            count = f'{len(prop)} results found'

    context = {'props':prop , 'msg' : count , 'query' : query}
    return render(request , 'realest/public.html' , context)

@login_required
def index(request):
    user = request.user
    prop = propertie.objects.filter(name=user)        
    count = ""
    if request.GET.get('type') != None:
        print('getted')
        type = request.GET.get('type')
        status = request.GET.get('status')
        bhk = request.GET.get('bhk')

        if status == 'Buy':
            status = 'sell'

        lsit = {'type' : type , 'status' : status}
        for i in lsit:
            prop = [item for item in prop if filt(item,lsit[i])]
        
        if len(prop) == 0:
            count = 'No result for applied filters'
        else:
            count = f'{len(prop)} results found'

    context = {'props':prop , 'msg' : count, 'op':User.username}
    return render(request , 'realest/index.html' , context)

def Logout_request(request):
	logout(request)
	return redirect("login")

def Login(request ):
    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']   
        user = authenticate(request , username=username , password=password )
        if user is not None:
            #print('authenticate')
            login(request, user)
            global usr
            usr = user
            return redirect('/dashboard')
        else:
            context = {'msg' : 'Login not successfull . Try Again','color':'danger'}
            return render(request , 'realest/login.html' , context)
    else:
        return render(request , 'realest/login.html')



def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        phone = request.POST['phone']
        mail = request.POST['mail']
        password = request.POST['pass']
        inst = person(name = name,phone=phone,mail=mail,password=password)
        try:        
            user = User.objects.create_user(username=name,password=password,email=mail)
            user.save()
            inst.save()
            context = {'msg':'User Created Successfully','color':'success'}
            return render(request , 'realest/register.html' , context )
        except IntegrityError:
            context = {'msg':'User Already Exits. Try Diffrent credential','color':'danger'}
            return render(request , 'realest/register.html' , context )


    else:
        return render(request , 'realest/register.html' )
    

@login_required
def post(request,clas):
    if request.method == 'POST':
        name = request.GET['user']

        area = request.POST['area'] + ' sqft'
        bhk = request.POST['bhk'] + ' BHK'
        price = request.POST['price']
        location = request.POST['location']
        status = request.POST['btnradior']
        propertytype = request.POST['btnradio']
        project = request.POST['project']
        desc = request.POST['desc']
        floor = request.POST['floor'] + '/' + request.POST['tfloor'] 
        type = request.GET['for']
        city = request.POST['city']    
        img = request.FILES["img"]
        
        today = date.today()
        inst = property(name=name,address=location,price=price,description=desc,
                        area=area,foor=status,date=today,type=type,project=project,
                        floor=floor,city=city,propertytype=propertytype,bhk=bhk,img=img)
        inst.save()
    if clas == 'residential': 
        params = {'head':'residential','for':'BHK'}
        return render(request , 'realest/resi.html', params)
    elif clas == 'commercial': 
        params = {'head':'commercial','for':'BHK'}
        return render(request , 'realest/corp.html', params)
    if clas == 'land': 
        params = {'head':'land','for':'BHK'}
        return render(request , 'realest/land.html', params)



@login_required
def land(request):
    if request.method == 'POST':
        name = request.GET['user']
        area = request.POST['area'] + ' sqft'
        price = request.POST['price']
        desc = request.POST['desc']
        location = request.POST['location']
        status = request.POST['btnradio']
        type = 'Land'        
        img = request.FILES["img"]
        today = date.today()
        print(status)
        inst = property(name=name,address=location,description=desc,
                        price=price,area=area,foor=status,date=today,type=type,img=img)
        inst.save()

    params = {'head':'Land'}
    return render(request , 'realest/land.html', params)

def match(query , data):
    print(data)
    if(query.lower() == data.city.lower() or query.lower() in data.address.lower()):
        return True
       
@login_required
def search(request):
 
    query = request.GET.get('search')
    prop = propertie.objects.all()
    props = [item for item in prop if match(query,item)]
    params = {'props':props}
    return render(request , 'realest/public.html', params)

@login_required
def delete(request, id):
  member = propertie.objects.get(id=id)
  member.delete()
  return HttpResponseRedirect(reverse('index'))