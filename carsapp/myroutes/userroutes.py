import random,json
import requests
from flask import make_response,render_template,request,redirect,flash,session
from sqlalchemy import desc
from werkzeug.security import generate_password_hash,check_password_hash
from carsapp import app,db
from carsapp.models import Users,Manufacturer,Comment,Posts,Specialists,Spareparts,State,Contactus,Order,Orderdet,Payment
from carsapp.forms import Loginform,Specform

@app.route('/')
def home():
    sess = session.get('userlog')
    spec = session.get('speclog')
    specc = Specialists.query.get(spec)
    name = Users.query.get(sess)
    login = Loginform()
    post = Posts.query.order_by(desc(Posts.posts_id)).all()
    c=[]
    for i in post:
        p=i.posts_id
        count = Comment.query.filter(Comment.comment_postid==p).count()
        c.append(count)
    manu = Manufacturer.query.all()
    return render_template('user/index.html',login=login,post=post,name=name,specc=specc,manu=manu,c=c,zip=zip)

@app.route('/category/<page>/<int:id>')
def show_category(page,id):
    sess = session.get('userlog')
    spec = session.get('speclog')
    specc = Specialists.query.get(spec)
    name = Users.query.get(sess)
    login = Loginform()
    manu = Manufacturer.query.all()
    post = Posts.query.filter(Posts.posts_manucat==id).all()
    c=[]
    for i in post:
        p=i.posts_id
        count = Comment.query.filter(Comment.comment_postid==p).count()
        c.append(count)
    return render_template('user/catindex.html',post=post,c=c,zip=zip,manu=manu,login=login,name=name,specc=specc)

@app.route('/user/logout')
def user_logout():
    session.pop('userlog')
    session.pop('shoppingcart', None)
    return redirect('/')
   
@app.route('/register')
def register():
    login=Loginform()
    states = State.query.all()
    return render_template('user/register.html',states=states,login=login)

@app.route('/register/details',methods=['POST'])
def register_details():
    if request.method=='GET':
        return redirect('/')
    else:
        fullname=request.form.get('fullname')
        email=request.form.get('email')
        pwd=request.form.get('password')
        pwd1=request.form.get('password1')
        phone=request.form.get('phoneno')
        gender=request.form.get('gender')
        state=request.form.get('state')
        if fullname==''or email==''or pwd=='' or phone=='' or gender==''or state=='':
            flash('Please Complete the Fields')
            return redirect('/register')
        elif pwd!=pwd1:
            flash('Passwords do not Match')
            return redirect('/register')
        else:
            fpwd = generate_password_hash(pwd)
            d = Users(user_fullname=fullname,user_email=email,user_password=fpwd,user_phone=phone,user_gender=gender,user_state=state)
            db.session.add(d)
            db.session.commit()
            flash('Registered Successfully,Please Login')
            return redirect('/')

@app.route('/user/login',methods=['POST'])
def user_login():
    login=Loginform()
    email=login.email.data
    pwd = login.password.data
    if login.validate_on_submit():
        deets = Users.query.filter(Users.user_email==email).first()
        if deets:
            dbpass = deets.user_password
            chk=check_password_hash(dbpass,pwd)
            if chk:
                id=deets.user_id
                name=deets.user_fullname
                session['userlog']=id
                post=Posts.query.all()
                flash('Login Successful')
                return redirect('/')
            else:
                flash('Invalid Credentials')
                return render_template('user/index.html',login=login)
        else:
            flash('Invalid Credentials')
            return render_template('user/index.html',login=login)
    else:
        flash('Complete the Fields')
        return render_template('user/index.html',login=login)

@app.route('/user/create')
def user_create():
    sess=session.get('userlog')
    if sess==None:
        return redirect('/')
    else:
        
        p = Users.query.get(sess)
        pid = p.user_id
        name = p.user_fullname
        manu = Manufacturer.query.all()
        post = Posts.query.filter(Posts.posts_user_id==pid).all()
        c=[]
        for i in post:
            p=i.posts_id
            count = Comment.query.filter(Comment.comment_postid==p).count()
            c.append(count)
        return render_template('user/create.html',manu=manu,post=post,name=name,pid=pid,c=c,zip=zip)

@app.route('/user/create/post',methods=['POST'])
def create_post():
    sess=session.get('userlog')
    if sess==None:
        return redirect('/')
    else:
        p = Users.query.get(sess)
        pid=p.user_id
        title = request.form.get('title')
        manu = request.form.get('manu')
        desc = request.form.get('desc')
        b = Posts(posts_title=title,posts_manucat=manu,posts_fullpost=desc,posts_user_id=pid)
        db.session.add(b)
        db.session.commit()
        flash('Post Created Successfully')    
        return redirect('/user/create')

@app.route('/specialist/register')
def spec_reg():
    spec = Specform()
    return render_template('user/specregister.html',spec=spec)

@app.route('/specialist/details',methods=['POST'])
def spec_details():
    if request.method=='GET':
        return render_template('user/specregister.html',spec=spec)
    else:
        spec=Specform()
        fullname=spec.fullname.data
        email=spec.email.data
        pwd=spec.password.data
        pwd2=spec.password1.data
        if pwd!=pwd2:
            flash('Password do not match')
            return render_template('user/specregister.html',spec=spec)
        if spec.validate_on_submit():
            formatted =generate_password_hash(pwd)
            g = Specialists(specialists_fullname=fullname,specialists_email=email,specialists_password=formatted)
            db.session.add(g)
            db.session.commit()
            flash('Registration Successful,Please Login')
            return render_template('user/speclogin.html')


@app.route('/spec/login',methods=["GET","POST"])
def spec_login():
    login=Loginform()
    if request.method=='GET':
        return render_template('user/speclogin.html',login=login)
    else:
        email=request.form.get('email')
        pwd=request.form.get('password')
        if email==''or pwd=='':
            flash('Complete all Fields')
            return render_template('user/speclogin.html',login=login)
        else:
            d = Specialists.query.filter(Specialists.specialists_email==email).first()
            if d:
                formatted = d.specialists_password
                chk = check_password_hash(formatted,pwd)
                if chk:
                    name=d.specialists_fullname
                    session['speclog']=d.specialists_id
                    post = Posts.query.order_by(desc(Posts.posts_id)).all()
                    c=[]
                    for i in post:
                        p=i.posts_id
                        count = Comment.query.filter(Comment.comment_postid==p).count()
                        c.append(count)
                    manu = Manufacturer.query.all()
                    flash('Login Successful')
                    return render_template('user/specdash.html',post=post,name=name,zip=zip,c=c,manu=manu)

@app.route('/spec/logout')
def spec_logout():
    session.pop('speclog')
    return redirect('/')
                    
@app.route('/open/post/<id>')
def open_post(id):
    sess=session.get('userlog')
    spec=session.get('speclog')
    if sess!=None:
        n=Users.query.get(sess)
        name=n.user_fullname
        login=Loginform()
        p = Posts.query.get(id)
        posttitle = p.posts_title
        postcat = p.postmanu.manufacturer_name
        postdesc=p.posts_fullpost
        postid=p.posts_id
        c=Comment.query.filter(Comment.comment_postid==postid).all()
        return render_template('user/openthread.html',posttitle=posttitle,postcat=postcat,postdesc=postdesc,postid=postid,login=login,c=c,name=name)
    elif spec!=None:
        n = Specialists.query.get(spec)
        name = n.specialists_fullname
        login=Loginform()
        p = Posts.query.get(id)
        posttitle = p.posts_title
        postcat = p.postmanu.manufacturer_name
        postdesc=p.posts_fullpost
        postid=p.posts_id
        c=Comment.query.filter(Comment.comment_postid==postid).all()
        return render_template('user/openthread.html',posttitle=posttitle,postcat=postcat,postdesc=postdesc,postid=postid,login=login,name=name,c=c)
    else:
        flash("Please login")
        return redirect('/')

@app.route('/post/comment',methods=["POST"])
def post_comment():
    sess = session.get('userlog')
    spec=session.get('speclog')
    postid=request.form.get('postid')
    comment=request.form.get('comment')
    c=Comment(comment_fullcomment=comment,comment_postid=postid,comment_specialist_id=spec,comment_userid=sess)
    db.session.add(c)
    db.session.commit()
    return comment


@app.route('/spareparts')
def spareparts():
    sess = session.get('userlog')
    if sess==None:
        flash('Login Please')
        return redirect('/')
    else:
        n = Users.query.get(sess)
        name = n.user_fullname
        spare = Spareparts.query.all()
        return render_template('user/spareparts.html',spare=spare,name=name)

@app.route('/spareparts/details/<int:id>')
def spare_details(id):
    sess = session.get('userlog')
    if sess==None:
        return redirect('/')
    else:
        n = Users.query.get(sess)
        name = n.user_fullname
        spare = Spareparts.query.get(id)
        return render_template('user/sparedetails.html',spare=spare,name=name)

"""dicts marger for addtocart"""
def MagerDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False

@app.route('/addcart',methods=["POST"])
def addcart():
    sess = session.get('userlog')
    if sess==None:
        return redirect('/')
    try:
        spareid = request.form.get('spareparts_id')
        quantity = request.form.get('quantity')
        spare = Spareparts.query.filter(Spareparts.spareparts_id==spareid).first()
        if spareid and quantity and request.method=="POST":
            DictItems = {spareid:{"name":spare.spareparts_name,"price":spare.spareparts_amount,"quantity":quantity,"image":spare.spareparts_image}}
            if 'shoppingcart' in session:
                print(session['shoppingcart'])
                if spareid in session['shoppingcart']:
                    flash('This Product already in Cart')
                else:
                    session['shoppingcart'] = MagerDicts(session['shoppingcart'], DictItems)
                    return redirect(request.referrer)
            else:
                session['shoppingcart']=DictItems
                return redirect(request.referrer)
    except Exception as e:
        print(e)
    finally:
        return redirect(request.referrer)
'''SHow cart route'''
@app.route('/cart')
def usercart():
    sess=session.get('userlog')
    n = Users.query.get(sess)
    name = n.user_fullname
    if sess==None:
        return redirect('/')
    if "shoppingcart" not in session:
        return redirect(request.referrer)
    SubTotal = 0
    grandtotal = 0
    vat=0
    for key, prod in session['shoppingcart'].items():
        SubTotal += (float(prod['price']) * float(prod['quantity']))
        vat = ("%.2f" % (0.075 * float(SubTotal)))
        grandtotal = float(vat) + float(SubTotal)
    return render_template('user/cart.html',vat=vat,grandtotal=grandtotal,name=name)

@app.route('/remove/cart/<int:id>')
def remove_cart(id):
    if 'shoppingcart' not in session or len(session['shoppingcart']) <= 0:
        return redirect('/')
    
    try:
        session.modified = True
        for key, item in session['shoppingcart'].items():
            if int(key)==id:
                session['shoppingcart'].pop(key, None)
                return redirect('/cart')
    except Exception as e:
        print(e)
        return redirect('/cart')

@app.route('/user/buy', methods=["POST"])
def user_buy():
    sess = session.get('userlog')
    if sess==None:
        return redirect('/')
    if request.method=="POST":
        address = request.form.get('address')
        sumgrandtotal = request.form.get('grandtotal')
        #insert into order
        mo = Order(order_address=address,order_userid=sess)
        db.session.add(mo)
        db.session.commit()
        orderid = mo.order_id
        #generate ref number
        ref = int(random.random() * 1000000)
        session['refno'] = ref
        subtotal = 0
        vat = 0
        for x,y in session['shoppingcart'].items():
            subtotal = (float(y['price']) * float(y['quantity']))
            vat = ("%.2f" % (0.075 * float(subtotal)))
            grandtotal = float(vat) + float(subtotal)
            quantity = y['quantity']
            od = Orderdet(orderdet_quantity=quantity,orderdet_amt=grandtotal,orderdet_orderid=orderid,orderdet_sparepartid=x)
            db.session.add(od)
        db.session.commit()
        p = Payment(pay_userid=sess,pay_orderid=orderid,pay_ref=ref,pay_amt=sumgrandtotal)
        db.session.add(p)
        db.session.commit()
        return redirect('/confirm/sparepart')

@app.route('/confirm/sparepart',methods=["GET","POST"])
def confirm_sparepart():
    sess = session.get('userlog')
    ref = session.get('refno')
    n = Users.query.get(sess)
    name = n.user_fullname
    if sess == None or ref == None:
        return redirect("/")
    userdeets = Users.query.get(sess) 
    deets = Payment.query.filter(Payment.pay_ref==ref).first()
    if request.method=="GET":
        return render_template('user/confirmcart.html',userdeets=userdeets,deets=deets,name=name)
    else:
        data = {"email":userdeets.user_email,"amount":deets.pay_amt*100, "reference":deets.pay_ref}

        headers = {"Content-Type": "application/json","Authorization":"Bearer sk_test_9ae0a36658673083f2804e54e184c79d151a6d5f"}

        response = requests.post('https://api.paystack.co/transaction/initialize', headers=headers, data=json.dumps(data))

        rspjson = json.loads(response.text) 
        if rspjson.get('status') == True:
            authurl = rspjson['data']['authorization_url']
            session.pop('shoppingcart', None)
            return redirect(authurl)
        else:
            return "Please try again"

@app.route("/user/payverify")
def paystack():
    # reference = request.args.get('reference')
    ref = session.get('refno')
    #update our database 
    headers = {"Content-Type": "application/json","Authorization":"Bearer sk_test_9ae0a36658673083f2804e54e184c79d151a6d5f"}

    response = requests.get(f"https://api.paystack.co/transaction/verify/{ref}", headers=headers)
    rsp =response.json()#in json format
    if rsp['data']['status'] =='success':
        amt = rsp['data']['amount']
        ipaddress = rsp['data']['ip_address']
        p = Payment.query.filter(Payment.pay_ref==ref).first()
        p.pay_status = 'paid'
        db.session.add(p)
        db.session.commit()
        flash("Payment Was Successful")
        return redirect('/spareparts')  #update database and redirect them to the feedback page
    else:
        p = Payment.query.filter(Payment.pay_ref==ref).first()
        p.pay_status = 'failed'
        db.session.add(p)
        db.session.commit()
        flash("Payment Failed")
        return redirect('/cart')


@app.route('/search',methods=["POST"])
def search():
    sess=session.get('userlog')
    login=Loginform()
    if sess!=None:
        n = Users.query.get(sess)
        name = n.user_fullname
        word = request.form.get('search')
        post = Posts.query.filter(Posts.posts_title.like(f'%{word}%')).all()
        c=[]
        for i in post:
            p=i.posts_id
            count = Comment.query.filter(Comment.comment_postid==p).count()
            c.append(count)
        spare = Spareparts.query.filter(Spareparts.spareparts_name.like(f'%{word}%')).all()
        return render_template('user/search.html',post=post,spare=spare,c=c,zip=zip,name=name,login=login)
    else:
        word = request.form.get('search')
        post = Posts.query.filter(Posts.posts_title.like(f'%{word}%')).all()
        c=[]
        for i in post:
            p=i.posts_id
            count = Comment.query.filter(Comment.comment_postid==p).count()
            c.append(count)
        spare = Spareparts.query.filter(Spareparts.spareparts_name.like(f'%{word}%')).all()
        return render_template('user/search.html',post=post,spare=spare,c=c,zip=zip,login=login)


@app.route('/user/profile')
def user_profile():
    sess = session.get('userlog')
    n = Users.query.get(sess)
    name = n.user_fullname
    if sess==None:
        return redirect('/')
    else:
        user = Users.query.get(sess)
        return render_template('user/profile.html',user=user,name=name)

@app.route('/user/update/<page>',methods=['GET',"POST"])
def user_update(page):
    sess=session.get('userlog')
    if sess==None:
        return redirect('/')
    if request.method=="GET":
        return redirect('/')
    fullname=request.form.get('fullname')
    phoneno=request.form.get('phone')
    email=request.form.get('email')
    if int(sess)==int(page):
        user=Users.query.get(sess)
        user.user_fullname=fullname
        user.user_phone=phoneno
        user.user_email=email
        db.session.commit()
        flash('submitted successfully')
    return redirect('/user/profile')

@app.route('/user/payment')
def show_user_payments():
    sess = session.get('userlog')
    n = Users.query.get(sess)
    name = n.user_fullname
    if sess==None:
        return redirect('/')
    else:
        pay = Payment.query.filter(Payment.pay_userid==sess).all()
        return render_template('user/payment.html',pay=pay,name=name)


@app.route('/user/orders')
def show_user_orders():
    sess = session.get('userlog')
    n = Users.query.get(sess)
    name = n.user_fullname
    if sess==None:
        return redirect('/')
    else:
        orderpay = Order.query.join(Payment).add_columns(Payment).filter(Order.order_userid==sess).all()
        return render_template('user/order.html',orderpay=orderpay,name=name)

@app.errorhandler(404)
def carsnotfound(error):
    return render_template('user/carserror.html',error=error),404

@app.errorhandler(500)
def carsnotfound(error):
    return render_template('user/carerror.html',error=error),500

@app.route('/user/contactus',methods=["POST"])
def contactus():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    ct = Contactus(contact_name=name,contact_email=email,contact_message=message)
    db.session.add(ct)
    db.session.commit()
    flash("Message Sent")
    return redirect(request.referrer)

@app.route('/spec/profile')
def spec_profile():
    spec = session.get('speclog')
    n = Specialists.query.get(spec)
    name = n.specialists_fullname
    if spec==None:
        return redirect('/')
    else:
        allpost=[]
        postss=[]
        c=[]
        comments = Comment.query.filter(Comment.comment_specialist_id==spec).all()
        for comment in comments:
            postid = comment.comment_postid
            allpost.append(postid)
        for post in allpost:
            posts = Posts.query.get(post)
            postss.append(posts)
            count = Comment.query.filter(Comment.comment_postid==post).count()
            c.append(count)
        return render_template('user/specpost.html',post=postss,c=c,zip=zip,name=name)