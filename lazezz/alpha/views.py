import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas
from django.http import request,HttpResponse
from django.shortcuts import render,redirect
from django.http import request,HttpResponse,HttpResponseRedirect, JsonResponse
from alpha.models import user_account,restaurants, foods, orders, user_cart,user_cart_new, AdminpanelProfile
# it was imported when doing admin user login  part for adform
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.core import serializers
from django.db import connection
# Create your views here.


from django.db.models import Sum, Avg, Max, Min, Count
from django.db import connection

# Create your views here.
rid = 100
def addRestaurant(request):
    return render(request, 'AddRestaurant_page.html')
def partnerwithus(request):
    return render(request, 'PartnerWithUs.html')

def register_restaurant(request):
    mb = request.POST.get('rphone')
    nm = request.POST.get('rname')
    onm = request.POST.get('oname')
    pd = request.POST.get('rpass')
    rig = request.FILES.get('rimg')
    radha = request.POST.get('radha')
    rpan = request.POST.get('rpan')
    rg = request.POST.get('rgstin')
    rfs = request.POST.get('rfssai')
    rbnk = request.POST.get('baccno')
    rfsc = request.POST.get('ifsc')
    radd = request.POST.get('address')
    rcity = request.POST.get('city')
    item1 = request.POST.get('r1')
    item1Img = request.FILES.get('r1img')
    item2 = request.POST.get('r2')
    item2Img = request.FILES.get('r2img')
    item3 = request.POST.get('r3')
    item3Img = request.FILES.get('r3img')
    item4 = request.POST.get('r4')
    item4Img = request.FILES.get('r4img')
    item5 = request.POST.get('r5')
    item5Img = request.FILES.get('r5img')

    rest = restaurants.objects.create(
        sname = nm,
        oname = onm,
        password = pd,
        sphone = mb,
        sadd = radd,
        aadhaar = radha,
        pan = rpan,
        gstin = rg,
        fssai_no = rfs,
        baccno = rbnk,
        ifsc = rfsc,
        city = rcity,
        rest_img = rig
    )
    rest.save()
    fd1 = foods(
        sid = rest.sid,
        fname= item1,
        fimg = item1Img,
        price = request.POST.get('r1price')
    )
    fd2 = foods(
        sid = rest.sid,
        fname= item2,
        fimg = item2Img,
        price = request.POST.get('r2price')
    )
    fd3 = foods(
        sid = rest.sid,
        fname= item3,
        fimg = item3Img,
        price = request.POST.get('r3price')
    )

    fd4 = foods(
        sid = rest.sid,
        fname= item4,
        fimg = item4Img,
        price = request.POST.get('r4price')
    )
    fd5 = foods(
        sid = rest.sid,
        fname= item5,
        fimg = item5Img,
        price = request.POST.get('r5price')
    )
    fd = foods.objects.bulk_create([fd1, fd2, fd3, fd4, fd5])
    return render(request, 'registered_successfully.html')

def login_into_restaurant(request):
    data = {}
    hist_users = []
    if request.method == 'POST':
        ph = request.POST.get('mobno')
        pd = request.POST.get('pass')
        print('IN Post block')
        print(ph, pd)
        try:
            data = restaurants.objects.get(sphone = ph, password = pd)
            print('After data')
            if data is not None:
                if data.verification == 1:
                    print('Before Login')
                    login(request, data)
                    print('After Login')
                    request.session['rph'] = data.sphone
                    request.session['rid'] = data.sid
                    request.session['total'] = []
                    print('Before products')
                    #Fetching All foods related to the restaurant
                    prod = foods.objects.filter(sid = data.sid)
                    # print('prod : ', prod)
                    # Fetching all the orders related to restaurant
                    ords = orders.objects.filter(sid = data.sid, t_active=0).order_by('phone', 'date')
                    # print(ords)
                    # print(ords.values())
                    request.session['online_count'] = 0
                    request.session['online_count'] = orders.objects.filter(sid = data.sid, t_active = 0, o_active = 1).count()
                    print(request.session['online_count'])
                    d = {}                   
                    for each in ords:
                        if each.phone not in d and each.o_active == 1:
                            a = user_account.objects.filter(phone = each.phone).values()
                            # d[each.phone] = [tp.get('total_purchased') for tp in a]
                            d[each.phone] = []
                            hist_users.append(a)
                    print(d)
                    cur = connection.cursor()
                    cur.execute(f"select phone, name, sum(price) from alpha_orders, alpha_foods where alpha_orders.fid = alpha_foods.fid and alpha_foods.sid = {request.session['rid']} and alpha_orders.o_active = 0 group by phone")
                    hist_users = cur.fetchall()

                    cur.execute(f"select phone, name, alpha_foods.fname, alpha_foods.price, date from alpha_orders, alpha_foods where alpha_orders.fid = alpha_foods.fid and alpha_orders.sid = {request.session['rid']} and alpha_orders.o_active=0 order by date")
    
                    history = cur.fetchall()
                    print(history)
                    # print(history)
                    request.session['items'] = d
                    print(request.session['items'])
                    t_worth = restaurants.objects.get(sid = data.sid).total_purchased
                    print('Total Purchased  = ', t_worth)
                    t_fds = foods.objects.filter(sid = request.session['rid'], avail=1).count()
                    print('Total Foods  = ', t_fds)
                    to = orders.objects.filter(sid = request.session['rid']).values()
                    print('Total Orders  = ', to, 'length = ', len(to))
                    df1 = pandas.DataFrame(prod.values())
                    print('DF1 = ', df1)
                    if len(to) != 0:
                        print('check1')
                        df = pandas.DataFrame(to)
                        print(f'DF = {df}')
                        # print(df['date'].month, df['date'].year, df['date'].day)
                        # print(df.info())
                        df['date'] = pandas.to_datetime(df['date'])
                        df['month'] = df['date'].dt.month
                        df['year'] = df['date'].dt.year
                        
                        # print(df1)
                        # print(t_worth)
                        ndf = df.merge(df1, on=['fid', 'sid'], how='inner')
                        # print(ndf)

                        p_count = ndf.groupby('fname')['fname'].count()
                        # p_count = p_count.to_dict()
                        print('p_count = ', p_count)

                        myexplode = [0.1 for each in p_count]
                        plt.pie(p_count, labels=p_count.index, explode=myexplode, autopct='%d')
                        plt.xlabel('Food Items')
                        plt.title('Food Selling Stats')
                        plt.style.use('seaborn-bright')
                        plt.savefig(f"static/images/top_product{request.session['rid']}.png")
                        plt.close()

                        p_count = ndf.groupby(['year', 'month']).agg({
                            'price':'sum',
                            'name':'count'
                        })
                        p1 = list(p_count['price'])
                        p2 = list(p_count['name'])
                        d1 = p_count.to_dict()
                        p_count.reset_index(inplace=True)
                        print(p_count)

                        plt.bar(p_count['month'], p_count['price'], color='yellow', width=0.2)
                        plt.bar(p_count['month'], p_count['name'], color='red', width=0.2)
                        plt.xlabel('Month')
                        plt.ylabel('Value')
                        plt.title('Monthwise-Stats')
                        plt.legend(['Month-price', 'Month-customers'])
                        plt.xticks(ticks=p_count['month'])
                        plt.savefig(f"static/images/year-month-stats{request.session['rid']}.jpg")
                        plt.close()

                        plt.bar(p_count['year'], p_count['price'], color='orange', width=0.2)
                        plt.bar(p_count['year'], p_count['name'], color='red', width=0.2)
                        plt.xlabel('Year')
                        plt.ylabel('Value')
                        plt.title('YearWise-stats')
                        plt.xticks(ticks=p_count['year'])
                        plt.savefig(f"static/images/yearstats{request.session['rid']}.jpg")
                        plt.close()
                    print('check2')
                    top_three_records = []
                    if len(ords.values()) != 0:
                        order = pandas.DataFrame(ords.values())
                        print('check2')
                        order['date'] = pandas.to_datetime(order['date'])
                        order['month'] = order['date'].dt.month
                        order['year'] = order['date'].dt.year
                        print('check3')
                        order = order.groupby('month').count()
                        order.reset_index(inplace=True)

                        ordall = pandas.DataFrame(orders.objects.all().values())
                        print('check4')
                        ordall['date'] = pandas.to_datetime(ordall['date'])
                        ordall['month'] = ordall['date'].dt.month
                        ordall['year'] = ordall['date'].dt.year
                        orderall = ordall.groupby('month').count()
                        orderall.reset_index(inplace=True)

                        print('check5')
                        plt.plot(order['month'], order['sid'], 'o--r')
                        plt.plot(orderall['month'], orderall['sid'], '*-g')
                        plt.title('Orderwise stats')
                        plt.xlabel('Month')
                        plt.ylabel('Count')
                        plt.xticks(list(range(1, 13)))
                        plt.legend(['Total Orders', 'Your Orders'])
                        plt.savefig(f"static/images/order_stats{request.session['rid']}.jpg")
                        plt.close()
                        
                        print('check6')
                        top_three_customers = pandas.DataFrame(ords.values())
                        print('Top Three customers', top_three_customers)
                        top_three = top_three_customers.groupby('phone').count()
                        print('check7')
                        top_three.sort_values(by='id', ascending=False, inplace=True)
                        top_three = top_three.iloc[0:3].reset_index()
                        top_three_phone_list = top_three['phone']
                        print(top_three_phone_list)
                        top_three_records = []
                        for each in top_three_phone_list:
                            top_three_records.append(user_account.objects.get(phone = each))
                        print(top_three_records)
                        print('check8')
                    return render(request, 'dashboard_home.html', {'user' : data, 'products':prod, 'orders':ords, 'huser':hist_users, 'history':history, 't_worth':t_worth, 't_fds':t_fds, 'to':len(to), 'top_three':top_three_records})
                    # return render(request, 'dashboard_home.html', {'user' : data, 'products':prod, 'orders':ords, 'huser':hist_users, 'history':history})
                else:
                    return render(request, 'registered_successfully.html')
        except:
            return render(request, 'Wrong_password.html')
    elif request.session.session_key != None:
        # print(request.session['rid'])
        hist_users = []
        data = restaurants.objects.get(sphone = request.session['rph'], sid=request.session['rid'])
        prod = foods.objects.filter(sid = data.sid)
        ords = orders.objects.filter(sid = data.sid, t_active=0).order_by('phone', 'date')
        
        cur = connection.cursor()
        cur.execute(f"select phone, name, sum(price) from alpha_orders, alpha_foods where alpha_orders.fid = alpha_foods.fid and alpha_foods.sid = {request.session['rid']} and alpha_orders.o_active = 0 group by phone")
        hist_users = cur.fetchall()

        cur.execute(f"select phone, name, alpha_foods.fname, alpha_foods.price, date from alpha_orders, alpha_foods where alpha_orders.fid = alpha_foods.fid and alpha_orders.sid = {request.session['rid']} and alpha_orders.o_active=0 order by date")
 
        history = cur.fetchall()
        
        t_worth = restaurants.objects.get(sid = request.session['rid']).total_purchased
        t_fds = foods.objects.filter(sid = request.session['rid'], avail=1).count()
        to = orders.objects.filter(sid = request.session['rid']).values()
        
        df1 = pandas.DataFrame(prod.values())
        if len(to) != 0:
            df = pandas.DataFrame(to)
            df['date'] = pandas.to_datetime(df['date'])
            df['month'] = df['date'].dt.month
            df['year'] = df['date'].dt.year
            # print(df)
            # print(df1)

            ndf = df.merge(df1, on=['fid', 'sid'], how='inner')
            # print(ndf)

            p_count = ndf.groupby('fname')['fname'].count()
            # p_count = p_count.to_dict()
            # print(p_count)
            fonts = {'family':'Montserrat', 'size':'large', 'wrap':'break-word'}
            myexplode = [0.1 for each in p_count]
            plt.pie(p_count, labels=p_count.index, explode=myexplode, autopct="%d %%")
            plt.xlabel('Food Items', fontdict=fonts)
            plt.title('Food Selling Stats')
            plt.style.use('seaborn-bright')
            plt.savefig(f"static/images/top_product{request.session['rid']}.png")
            plt.close()


            p_count = ndf.groupby(['year', 'month']).agg({
                'price':'sum',
                'name':'count'
            })
            p1 = list(p_count['price'])
            p2 = list(p_count['name'])
            # d1 = p_count.to_dict()
            p_count.reset_index(inplace=True)
            # print(p_count)

            plt.bar(p_count['month'], p_count['price'], color='yellow', width=0.2)
            plt.bar(p_count['month'], p_count['name'], color='red', width=0.2)
            plt.xlabel('Month')
            plt.ylabel('Value')
            plt.title('Monthwise-Stats')
            plt.legend(['Month-price', 'Month-customers'])
            plt.xticks(ticks=p_count['month'])
            plt.savefig(f"static/images/year-month-stats{request.session['rid']}.jpg")
            plt.close()

            plt.bar(p_count['year'], p_count['price'], color='orange', width=0.2)
            plt.bar(p_count['year'], p_count['name'], color='red', width=0.2)
            plt.xlabel('Year')
            plt.ylabel('Value')
            plt.title('YearWise-stats')
            plt.xticks(ticks=p_count['year'])
            plt.savefig(f"static/images/yearstats{request.session['rid']}.jpg")
            plt.close()
        top_three_records = []
        if len(ords.values()) != 0:
            order = pandas.DataFrame(ords.values())
            order['date'] = pandas.to_datetime(order['date'])
            order['month'] = order['date'].dt.month
            order['year'] = order['date'].dt.year
            order = order.groupby('month').count()
            order.reset_index(inplace=True)
            print(order[['month', 'sid']])

            ordall = pandas.DataFrame(orders.objects.all().values())
            ordall['date'] = pandas.to_datetime(ordall['date'])
            ordall['month'] = ordall['date'].dt.month
            ordall['year'] = ordall['date'].dt.year
            orderall = ordall.groupby('month').count()
            orderall.reset_index(inplace=True)
            print(orderall[['month', 'sid']])

            plt.plot(order['month'], order['sid'], 'o--r')
            plt.plot(orderall['month'], orderall['sid'], 'x-g')
            plt.title('Orderwise stats')
            plt.xlabel('Month')
            plt.ylabel('Count')
            plt.xticks(list(range(1, 13)))
            plt.legend(['Total Orders', 'Your Orders'])
            plt.savefig(f"static/images/order_stats{request.session['rid']}.jpg")
            plt.close()

            top_three_customers = pandas.DataFrame(ords.values())
            top_three = top_three_customers.groupby('phone').count()
            top_three.sort_values(by='id', ascending=False, inplace=True)
            top_three = top_three.iloc[0:3].reset_index()
            top_three_phone_list = top_three['phone']
            top_three_records = []
            for each in top_three_phone_list:
                top_three_records.append(user_account.objects.get(phone = each))

        return render(request, 'dashboard_home.html', {'user':data, 'products' : prod, 'orders':ords, 'huser':hist_users, 'history':history, 't_worth':t_worth, 't_fds':t_fds, 'to':len(to), 'top_three':top_three_records})
    else:
        print('in else block')
        return redirect('/addrest')
        
def update_food_item(request):
    if request.session.session_key != None:
        fd = request.POST.get('fid')
        sd = request.POST.get('sid')
        fnm = request.POST.get('fname')
        fprice = request.POST.get('fprice')
        favail = request.POST.get('availchk')
        # print(fd, sd, fnm, fprice, favail)
        if favail == 'yes':
            favail = 1
        else:
            favail = 0

        foods.objects.filter(fid = fd, sid = sd).update(fname = fnm, price = fprice, avail = favail)
        return redirect('/login_rest')
    else:
        return redirect('/addrest')
def delete_food_item(request):
    if request.session.session_key != None:
        fd = request.GET.get('fd')
        sd = request.GET.get('sd')
        foods.objects.filter(fid=fd, sid=sd).delete()
        return redirect('/login_rest')
    else:
        return redirect('/addrest')

def add_food_item(request):
    if request.session.session_key != None:
        sd = request.POST.get('sid')
        fnm = request.POST.get('fname')
        fprice = request.POST.get('fprice')
        favail = request.POST.get('availchk1')
        fmg = request.FILES.get('fmg')
        if favail == 'on':
            favail = 1
        else:
            favail = 0
        print(sd, fnm, fprice, favail, fmg)
        foods.objects.create(sid = sd, fname = fnm, price =fprice, avail = favail, fimg = fmg)
        return redirect('/login_rest')
    else:
        return redirect('/addrest')

def accept_request(request):
    if request.session.session_key != None:
        od = request.GET.get('od')
        fd = request.GET.get('fd')
        sd = request.GET.get('sd')
        ph = request.GET.get('ph')
        quantity = request.GET.get('quantity')
        print(od, fd, sd, ph, 'quantity = ', quantity)
        d = request.session['items']
        food = foods.objects.filter(fid = fd, sid = sd).values('fname', 'price')
        print(food)
        # lis = request.session['total']
        # for f in food:
        #     lis.append(f.get('price'))
        # print(lis)
        # d[ph] = lis
        # request.session['total'] = lis
        # print(d)
        # for val in d:
        #     if d[val] != 0 and type(d[val]) is list:
        #         d[val] = sum(d[val])
        # print(d)
        # request.session['items'] = d
        print(d)
        for f in food:
            print(f.get('price'), type(f.get('price')))
            t = f.get('price') * int(quantity)
            d[ph].append(t)
        request.session['items'] = d
        print(d)
        orders.objects.filter(id=od, sid=sd).update(o_active=0)
        
        return redirect('/login_rest')
    else:
        return redirect('/addrest')

def accept_orders_online(request):
    if request.session.session_key != None:
        sd = request.GET.get('sid')
        restaurants.objects.filter(sid = sd).update(o_active = 1)
        return redirect('/login_rest')
    else:
        return redirect('/addrest')


def update_profile(request):
    if request.session.session_key != None:
        if request.method == 'POST':
            data = restaurants.objects.get(sid = request.session['rid'])
            rph = request.POST.get('rphone')
            rps = request.POST.get('rpass')
            rmg = request.FILES.get('rimg')
            bnk = request.POST.get('bank')
            ifc = request.POST.get('ifsc')

            data.sphone = rph
            data.password = rps
            data.baccno = bnk
            data.ifsc = ifc
            if rmg is not None:
                data.rest_img = rmg
            data.save()
            return redirect('/login_rest')
        else:
            data = restaurants.objects.get(sid = request.session['rid'])
            return render(request, 'update_profile.html', {'user':data})
    else:
        return redirect('/addrest')


def logout_from_restaurant(request):
    print('online_count = ',request.session['online_count'])
    if request.session['online_count'] != 0:
        print('logout if condition executed')
        d = request.session['items']
        print('logout if condition executed')
        print(d)
        for val in d:
            if d[val] != 0 and type(d[val]) is list:
                d[val] = sum(d[val])
            user_account.objects.filter(phone = val).update(total_purchased = (d[val]+user_account.objects.get(phone = val).total_purchased))
        print(d)
        total = 0
        for val in d:
                total += d[val]
        total += restaurants.objects.get(sid = request.session['rid']).total_purchased
        request.session['total'] = total
        print(request.session['total'])
        restaurants.objects.filter(sid = request.session['rid']).update(total_purchased = request.session['total'])
        # request.session['online_count'] = orders.objects.filter(sid = request.session['rid'], o_active = 1, t_active = 0).aggregate(Count('id'))
    logout(request)
    # print('online_count = ',request.session['online_count'])
    print('Session Key = ', request.session.session_key)
    return redirect('/addrest')

def getNewOrders(request):
    if request.session.session_key != None:
        ords = orders.objects.filter(sid=request.session['rid'], o_active=1).values()
        return JsonResponse({'orders':[ords]}, 'application/json')


#### User Part Starts from below



# aditya part
def set_location(request):
    return render(request,'start.html')

def edit_page(request):
    print('session key = ', request.session.session_key)
    if request.session.session_key !=None:
        mob=request.GET.get('mobile')
        print(mob)
        data=user_account.objects.get(phone=mob)
        if request.method=="POST":
            n=request.POST.get("nam")
            p1=request.POST.get("pw1")
            p2=request.POST.get("pw2")
            ph=request.POST.get("mob")
            pic=request.FILES["uploadnew"]
            print(n,p1,p2,ph,pic)
            if p1==p2:
                # os.remove(data.cimg.path)
                # print(data.cimg.path)
                user_account.objects.filter(phone=mob).delete()
                user_account.objects.create(phone=ph, name=n, password=p1, cimg = pic)
                # cur = connection.cursor()
                # print(f"update alpha_user_account set cimg = '{pic}' where phone='{ph}'")
                # cur.execute(f"update alpha_user_account set cimg = '{pic}' where phone='{ph}'")
                
                return render(request,'edit_page.html',{"done":1})
        


        return render(request,'edit_page.html',{"user":data,"done":0})
    else:

         return HttpResponseRedirect('/city')


def my_profile(request):
      if request.session.session_key != None:
        #  mob = request.GET.get('mobile')
         mob = request.session.get('ph')
        #  this passes query set and to fetch data for loop is applied
         data=user_account.objects.filter(phone=mob) 
        #  this gives the object only specific data no need for loop 
         data1=user_account.objects.get(phone=mob)
         print(data)
         print(data1)
        #  cty = request.GET.get('city') # comming from food_select.html through query string
         return render(request,'edit_profile.html',{"user":data1})

      else:
        return redirect('/logout')

def city_location(request):
    d={}
    print('inside city_location view')
    print('session key = ', request.session.session_key)
    if request.method=="POST":
            try:
                mob=request.POST.get("mob")
                pwd=request.POST.get("pwd")
                data=user_account.objects.get(phone=mob)
                # data = authenticate(username='my', password=pwd)
                print(data.password,data.phone,data.name)
            except:
                 return render(request,'error.html')
            if data is not None:
                if (data.password)==pwd:
                # if data is not None:
                    print('hello')
                    n=data.name
                    login(request,data)
                    request.session['sess_nm']=n
                    request.session['ph'] = mob
                    request.session['cart_list'] = []
                    # print(data.last_login)
                    # d={"show":data}

                    # data=restaurants.objects.all() 
                    # print(data)
                    # return HttpResponseRedirect('city2')
                    return render(request,'location2.html',{"mob":mob})
                else:
                    print('in else')
                    return render(request,'error.html')
                        #    return HttpResponse("welcome to clone of location Page>>>>")# along with customer name passed??? in dictionary form
        
                    #   return HttpResponse("Not Allowed!!!")
    if request.session.session_key != None:
        if request.GET.get('cty') != None:
            d={}
            uid = request.GET.get('cty')
            print(uid+" welcome to select_rest")
            data=restaurants.objects.filter(city=uid)
            # print(data)
            fds = []
            for each in data:
                fds.append(foods.objects.filter(sid = each.sid)[0:2])
            d={"city": uid, 'foods':fds, 'data':data}
            print(d)
            return render(request,'select_rest.html',{"data":data,"cty":uid, 'foods':fds})
        else:
            return render(request, 'location2.html')
    else:                 
         return render(request,'location.html')
   

def sign_up(request):
    print('inside sign_up view')
    if request.method=="POST":
            n=request.POST.get("nam")
            p1=request.POST.get("pw1")
            p2=request.POST.get("pw2")
            ph=request.POST.get("mob")
            pic=request.FILES.get("upCtrl")
            print(n,p1,p2,ph,pic)
            if p1==p2:
                d=user_account.objects.create(phone=ph,name=n,password=p1,cimg=pic)
                print(d)
                d.save()
                # return HttpResponse("Data Saved>>>>")
                # return HttpResponseRedirect('/city')
                return render(request,'location.html')

    return render(request,'signup.html')


@login_required(login_url='/city')
def verified(request):
     return render(request,'location2.html')

# @login_required(login_url='/city')
# def rest_view(request,uid):
#     d={}
#     print(uid+" welcome to select_rest")
#     data=restaurants.objects.filter(city=uid)
#     # print(data)
#     fds = []
#     for each in data:
#         fds.append(foods.objects.filter(sid = each.sid).values_list()[0:2])
#     d={"city": uid, 'foods':fds, 'data':data}
#     print(d)
#     return render(request,'select_rest.html',{"data":data,"cty":uid, 'foods':fds})

# def food_select(request):
#     if request.session.session_key != None:
#         cty = request.GET.get('city') # comming from food_select.html through query string
#         fnm = request.GET.get('fnm')
#         fds = foods.objects.filter(fname=fnm)
#         print(fds)
#         rts = []
#         pc=[]
#         for each in fds:
#             rts.append(restaurants.objects.filter(sid=each.sid, city=cty))
#             pc.append(foods.objects.filter(sid=each.sid, fname=fnm))
#         print(rts, pc)
#         for a in pc:
#             for b in a:
#                 print(b.sid,b.price)
#         return render(request, 'foods_select.html', {'rests':rts,'food':pc})

#     else:
#          return redirect('/city')
def food_select(request):
    if request.session.session_key != None:
        cty = request.GET.get('city') # comming from food_select.html through query string
        fnm = request.GET.get('fnm')
        fds = foods.objects.filter(fname=fnm)
        # print("foods selected=",fds)
        rts = []
        pr = {}
        for each in fds:
            data=restaurants.objects.get(sid=each.sid)
            g=data.city
            if g==cty:
                rts.append(data)  
        # print("list is",rts)
        for every in rts:
            pr[every] = foods.objects.filter(sid = every.sid, fname=fnm) 
        print("dict is",pr.items())   

        cart =request.session.get('cart')
        if not cart:
            request.session['cart']={}
        cty = request.GET.get('city') # comming from food_select.html through query string
        # shid = request.GET.get('sid')
        sname=request.GET.get('sname')
        # request.session['sid']=shid
        # print(cty, shid, sname)
        # fdl= foods.objects.filter(sid=shid)
        rimg=request. GET.get('rimg')
        l=0
        if request.method=="POST":
             fn=request.POST.get('food_nam')
             fi=request.POST.get('food_id')
             si=request.POST.get('shop_id')
             print("Aditya==",si)
             request.session['sid']=si
             remove=request.POST.get('remove')
             print("data from form=",fn,fi,si)
             cart=request.session.get('cart')
             if cart:
                 quantity=cart.get(fi)
                 if quantity:
                     if remove:
                         if quantity<=1:
                             cart.pop(fi)
                         else:
                             cart[fi]=quantity-1
                     else:
                         cart[fi]=quantity+1
                 else:
                     cart[fi]=1
             else:
                 cart={}
                 cart[fi]=1
             request.session['cart']=cart
             l=len(cart)
             print('no of items=',l)

             print('usercart',request.session['cart'])
        #  if cty != None:
        #     request.session['fdl'] = list(fdl)
        #  a = request.GET.get('name')@
        #  b = request.GET.get('fhid')@
        #  c = request.GET.get('shid')@
        #  if a != None:
        #     # request.session['cart_list'] += [(a, b, c)]
        #     # request.session['cart_list'][b] = (a, c)
        #     user_cart.objects.create(phone=request.session['ph'],name=request.session['sess_nm'], fid=b, sid=c)@
        # #  print(request.session['cart_list'])
        #  c = user_cart.objects.filter(phone = request.session['ph']).count()@
        #  print(a, b, c)@
        #  return render(request,'rest_selected.html',{"foodl":fdl, "shopnam": sname,"cty":cty,"rimg":rimg, "sid":shid, 'count':c})@
        # #  return render(request,'rest_selected.html',request.session['d'])  

        return render(request, 'foods_select.html', {'pr':pr.items(),"cty":cty,'fnm':fnm,"count":l})

    else:
         return redirect('/city')

   
def rest_done(request):
      if request.session.session_key != None:
         cart =request.session.get('cart')
         if not cart:
             request.session['cart']={}
         cty = request.GET.get('city') # comming from food_select.html through query string
         shid = request.GET.get('sid')
         sname=request.GET.get('sname')
         request.session['sid']=shid
         print(cty, shid, sname)
         fdl= foods.objects.filter(sid=shid)
         rimg=request. GET.get('rimg')
         l=0
         if request.method=="POST":
             fn=request.POST.get('food_nam')
             fi=request.POST.get('food_id')
             si=request.POST.get('shop_id')
             remove=request.POST.get('remove')
             print("data from form=",fn,fi,si)
             cart=request.session.get('cart')
             if cart:
                 quantity=cart.get(fi)
                 if quantity:
                     if remove:
                         if quantity<=1:
                             cart.pop(fi)
                         else:
                             cart[fi]=quantity-1
                     else:
                         cart[fi]=quantity+1
                 else:
                     cart[fi]=1
             else:
                 cart={}
                 cart[fi]=1
             request.session['cart']=cart
             l=len(cart)
             print('no of items=',l)

             print('usercart',request.session['cart'])
        #  if cty != None:
        #     request.session['fdl'] = list(fdl)
        #  a = request.GET.get('name')@
        #  b = request.GET.get('fhid')@
        #  c = request.GET.get('shid')@
        #  if a != None:
        #     # request.session['cart_list'] += [(a, b, c)]
        #     # request.session['cart_list'][b] = (a, c)
        #     user_cart.objects.create(phone=request.session['ph'],name=request.session['sess_nm'], fid=b, sid=c)@
        # #  print(request.session['cart_list'])
        #  c = user_cart.objects.filter(phone = request.session['ph']).count()@
        #  print(a, b, c)@
        #  return render(request,'rest_selected.html',{"foodl":fdl, "shopnam": sname,"cty":cty,"rimg":rimg, "sid":shid, 'count':c})@
        # #  return render(request,'rest_selected.html',request.session['d'])
         return render(request,'rest_selected.html',{"foodl":fdl, "shopnam": sname,"cty":cty,"rimg":rimg, "sid":shid,"count":l})
      
      else:
        return redirect('/city')
      

def my_cart(request):
    if request.session.session_key!=None:
        lis=[]
        lisq=[]
        print(list(request.session.get('cart').keys()))
        print(list(request.session.get('cart').values()))
        fd=list(request.session.get('cart').keys())
        for i in fd:
            products=foods.objects.get(fid=i)
            lis.append(products)
        print(lis)
        for a in lis:
            print(a.fname)
            print(a.fid)
            print(a.price)

        
        return render(request,'my_cart.html',{'products':lis})
    else:
        return redirect('/city')
           

# def addcart(request):
#     if request.session.session_key != None:
#         carts = user_cart.objects.filter(phone=request.session['ph'])
#         lis = []
#         tp = 0
#         for cart in carts:
#             # a = (foods.objects.filter(fid=cart.fid, sid=cart.sid).values('fimg', 'fname', 'price'))
#             a = (foods.objects.get(fid=cart.fid, sid=cart.sid))
#             # for each in a:
#             #     tp += each['price']
#             request.session['cart_list'].append(a)
#         print(request.session['cart_list'])
#         # request.session['cart_list'] = serializers.serialize('json', lis)
#         request.session['cart_list'] =serializers.serialize('json', request.session['cart_list'])
#         print(request.session['cart_list'])

        
#         print(lis)
#         return render(request, 'cart.html', {'carts':request.session['cart_list']})

# def final_checkout(request):
#     if request.session.session_key != None:
#         print('inside function')
#         print('session value = ', request.session['cart_list'])
#         print('NAme = ', request.session['sess_nm'])
#         lis = request.session['cart_list']
#         for each in lis:
#             print('inside loop')
#             a = orders.objects.create(fid=each.fid, sid=each.sid, phone=request.session['ph'], name=request.session['sess_nm'], o_active=1, t_active=0, address='India')
#             a.save()
#         return render(request, 'cart.html', {'carts':request.session['cart_list']})
    
def checkout(request):
    if request.session.session_key != None:
        if request.method=='POST':
            lis=[]
            add=request.POST.get('address')
            ph=request.POST.get('phone')
            print(add,ph)
            name1=request.session.get('sess_nm')
            phbysess=request.session.get('ph')
            cart=request.session.get('cart')
            shid=request.session.get('sid')
            # products=list(cart.keys())
            fd=list(request.session.get('cart').keys())
            for i in fd:
                products=foods.objects.get(fid=i)
                lis.append(products)
            total=0
            for a in lis:
                 print(a.fid,cart.get(str(a.fid)),shid)
                 d=user_cart_new.objects.create(product=a.fid,phone=ph,quantity=cart.get(str(a.fid)),price=a.price,address=add)
                 d.save()
                 total += ((a.price)*(cart.get(str(a.fid))))
                 
            print("orders places in cart")
            # print(request.session['shid'])
            # sto=request.session['shid']
            print(total)

            for a in lis:
                 d=orders.objects.create(fid=a.fid,quantity=cart.get(str(a.fid)),sid=shid,phone=ph,name=name1,address=add,o_active=1)
                 d.save()
                #  price=a.price, to ro price attribute 
            print('data saved to orders')
        # after making entry in orders table
        request.session['cart']={}
        # request.session['sid']=0
        print('data empty')
        user_cart_new.objects.filter(phone=phbysess).delete()
        # print(name1,phbysess,cart,lis,sep='\n')
        return render(request, 'complete.html')
    else:
        return redirect('/city')
    return render(request, 'my_cart.html')

def confirmed(request):
    if request.session.session_key != None:
        return render(request,'complete.html')
    else:
        return redirect('/city')


def logout_view(request):
    print('inside logout_view(request) function')
    logout(request)
    return HttpResponseRedirect('/')

# Lazezz siteadmin part -- Manan Ravi

def loginPage(request):
    user={}
    if request.method=='POST':
        unm=request.POST.get('name')
        pwd=request.POST.get('pass')
            
            #user = profile.objects.filter(emp_nm=unm)
            # user = authenticate(username=unm, password=pwd)
            # user = AdminpanelProfile.objects.all().values()
        user = AdminpanelProfile.objects.get(emp_nm = unm,emp_pass = pwd)
        if user is not None:
            login(request,user)
            request.session['ss_nm']=user.emp_nm  #creating variable name for session.
            request.session['ss_em']=user.emp_pass
            userdict = {'emp_nm':user.emp_nm, 'emp_id':user.emp_id, 'emp_mob':user.emp_mob}
            request.session['admin_det'] = userdict
            data = restaurants.objects.all()
            # return render(request,"request.html",{"data":data})
            return redirect('/request')

        elif user is None:
            return render(request,"aerror.html")
    return render(request, 'login.html')
    


def lazezz_admin_signup(request):
    if request.method=='POST':
        unm=request.POST.get('unm')
        id=request.POST.get('id')
        mob=request.POST.get('mob')
        pwd=request.POST.get('pass')
        u=AdminpanelProfile.objects.create(emp_nm=unm,emp_id=id,emp_mob=mob,emp_pass=pwd)
        u.save()
    return render (request,'asignup.html')
   
    




def requests(request):   
    if request.session.session_key != None:   
        data = restaurants.objects.all()
        return render(request,"request.html",{"data":data, 'user':request.session['admin_det']})
    return redirect('/a_login')


def averified(request):
    if request.session.session_key != None:  
        data=restaurants.objects.filter(verification=1)
        return render(request,"verified.html",{"data": data, 'user':request.session['admin_det']})
    return redirect('/a_login')


def unverified(request):
    if request.session.session_key != None:
        data=restaurants.objects.filter(verification=0)
        return render(request,"unverified.html",{"data": data, 'user':request.session['admin_det']})
    return redirect('/a_login')


def editdata(request,sid):
    if request.session.session_key != None:
        if request.method=="POST":
            i=request.POST.get('rid')
            restaurants.objects.filter(sid=sid)

            n=request.POST.get('rname')
            restaurants.objects.filter(sid=sid)

            o=request.POST.get('owname')
            restaurants.objects.filter(sid=sid)


            ph=request.POST.get('mob')
            restaurants.objects.filter(sid=sid)

            a=request.POST.get('add')
            restaurants.objects.filter(sid=sid)

            ac=request.POST.get('aad')
            restaurants.objects.filter(sid=sid)

            pn=request.POST.get('panc')
            restaurants.objects.filter(sid=sid)

            g=request.POST.get('gst')
            restaurants.objects.filter(sid=sid)

            f=request.POST.get('fssai')
            restaurants.objects.filter(sid=sid)

            b=request.POST.get('acc')
            restaurants.objects.filter(sid=sid)

            ic=request.POST.get('ifsc')
            restaurants.objects.filter(sid=sid)

            c=request.POST.get('city')
            restaurants.objects.filter(sid=sid)

            v=request.POST.get('verify')
            restaurants.objects.filter(sid=sid).update(verification=v)

            oa=request.POST.get('o')
            restaurants.objects.filter(sid=sid)

            ta=request.POST.get('t')
            restaurants.objects.filter(sid=sid)

            r=request.POST.get('img')
            restaurants.objects.filter(sid=sid)

            l=request.POST.get('ll')
            restaurants.objects.filter(sid=sid)

            return redirect('/request')

        data=restaurants.objects.get(sid=sid)
        return render(request,"edit.html",{"data":data, 'user':request.session['admin_det']})
    return redirect('/a_login')
    

def error(request):
    return render(request,'error.html')

def lazezz_admin_logout_view(request):
    if request.session.session_key != None: 
        print('inside logout')
        logout(request)
        return redirect('/a_login')
    print('inside logout outside')
    return redirect('/a_login')