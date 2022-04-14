import os,math,random
from flask import make_response,render_template,request,redirect,flash,session
from werkzeug.security import generate_password_hash, check_password_hash
from carsapp import app,db
from carsapp.models import Admin, Manufacturer, Order, Orderdet, Payment,Users,Suppliers,Spareparts
from carsapp.myroutes.userroutes import spareparts


@app.route('/admin/login')
def admin_login():
    return render_template('admin/adminlogin.html')

@app.route('/admin/dashboard',methods=['POST'])
def admin_dash():
    name = request.form.get('adminname')
    pwd = request.form.get('adminpwd')
    if name=='' or pwd=='':
        flash('Please complete the fields')
        return redirect('/admin/login')
    else:
        ad = Admin.query.filter(Admin.admin_username==name,Admin.admin_password==pwd).first()
        if ad:
            session['adminlog']=ad.admin_id
            manu=Manufacturer.query.all()
            return render_template('admin/manu.html',manu=manu)
        else:
            flash('invalid credentials')
            return render_template('admin/adminlogin.html')

@app.route('/admin/signout')
def admin_signout():
    session.pop('adminlog')
    return redirect('/admin/login')

@app.route('/admin/manufacturer')
def manufacturer():
    manu=Manufacturer.query.all()
    return render_template('admin/manu.html',manu=manu)

@app.route('/admin/users')
def adminusers():
    user = Users.query.all()
    return render_template('admin/user.html',user=user)

@app.route('/admin/user/delete/<id>')
def delete_user(id):
    sess=session.get('adminlog')
    if sess==None:
        return redirect('/admin/login')
    else:
        b = db.session.query(Users).get(id)
        db.session.delete(b)
        db.session.commit()
        flash(f'{b.user_fullname} deleted successfully')
        return redirect('/admin/users')

@app.route('/admin/spareparts')
def admin_spareparts():
    adminlog = session.get('adminlog')
    if adminlog==None:
        return redirect('/admin/login')
    else:
        spare=Spareparts.query.all()
        return render_template('admin/spare.html',spare=spare)

@app.route('/admin/spareparts/add',methods=["GET","POST"])
def admin_add_spareparts():
    adminlog = session.get('adminlog')
    if adminlog==None:
        return redirect('/admin/login')
    elif request.method=="GET":
        manu = Manufacturer.query.all()
        supp = Suppliers.query.all()
        return render_template('admin/addspare.html',manu=manu,supp=supp)
    else:
        year = request.form.get('year')
        amt = request.form.get('amount')
        manufac = request.form.get('manu')
        carmodel = request.form.get('model')
        supp = request.form.get('supplier')
        image=request.files.get('img')
        orijoname=image.filename
        ext=os.path.splitext(orijoname)
        fn=math.ceil(random.random()*10000)
        save_as=str(fn)+ext[1]
        #check your extension type
        allowed=['.jpg','.png','.gif','.webp']
        if ext[1].lower() in allowed:
            image.save(f'carsapp/static/assets/img/{save_as}')
            p = Spareparts(spareparts_image=save_as,spareparts_name  =year,spareparts_amount=amt,spareparts_modelid=carmodel,spareparts_manuid=manufac,spareparts_supplierid=supp)
            db.session.add(p)
            db.session.commit()
            flash('Sparepart added successfully')
            return redirect('/admin/spareparts')
        else:
            flash('Please Upload only jpg,png,gif or webp images')
            return redirect("/admin/spareparts/add")

@app.route('/admin/suppliers')
def admin_suppliers():
    adminlog = session.get('adminlog')
    if adminlog ==None:
        return redirect('/admin/login')
    else:
        supp = Suppliers.query.all()
        return render_template('admin/supp.html',supp=supp)

@app.route('/admin/suppliers/add',methods=['GET','POST'])
def admin_suppliers_add():
    adminlog = session.get('adminlog')
    if adminlog==None:
        return redirect('/admin/login')
    elif request.method =="GET":
        return render_template('admin/addsupp.html')
    else:
        suppname = request.form.get('name')
        supplocation = request.form.get('location')
        suppphone = request.form.get('phone')
        suppemail = request.form.get('email')
        p = Suppliers(suppliers_name=suppname,suppliers_location=supplocation,suppliers_phone=suppphone,suppliers_email=suppemail)
        db.session.add(p)
        db.session.commit()
        flash('Supplier Added Successfully')
        return redirect('/admin/suppliers')

@app.route('/admin/payments')
def admin_payments():
    adminlog = session.get('adminlog')
    if adminlog==None:
        return redirect('/admin/login')
    else:
        payment = Payment.query.all()
        return render_template('admin/payments.html',payment=payment)

@app.route('/admin/orders')
def admin_orders():
    adminlog = session.get('adminlog')
    if adminlog==None:
        return redirect('/admin/login')
    else:
        orders = Order.query.all()
        return render_template('admin/orders.html',orders=orders)

@app.route('/order/details/<int:id>')
def show_order_details(id):
    adminlog = session.get('adminlog')
    if adminlog==None:
        return redirect('/admin/login')
    else:
        orderdet = Orderdet.query.filter(Orderdet.orderdet_orderid==id).all()
        return render_template('admin/orderdetails.html',orderdet=orderdet)

@app.route('/order/edit/<int:id>',methods=["POST"])
def admin_edit_status(id):
    adminlog = session.get('adminlog')
    status = request.form.get('status')
    if adminlog==None:
        return redirect('/admin/login')
    else:
        order = Order.query.get(id)
        order.order_status = status
        db.session.commit()
        return redirect(request.referrer)