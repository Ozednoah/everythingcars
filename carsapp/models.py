import datetime
from carsapp import db

class Admin(db.Model): 
    admin_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    admin_username = db.Column(db.String(255), nullable=False)
    admin_password = db.Column(db.String(255), nullable=False)
    admin_lastlogin = db.Column(db.DateTime(), onupdate=datetime.datetime.utcnow())

class Users(db.Model):
    user_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    user_fullname = db.Column(db.String(255), nullable=False)
    user_email = db.Column(db.String(255), nullable=False, unique=True)
    user_password = db.Column(db.String(255), nullable=False)
    user_gender = db.Column(db.String(255), nullable=False)
    user_phone = db.Column(db.String(255), nullable=False)
    #foreign key
    user_state = db.Column(db.Integer(), db.ForeignKey("state.state_id"))

    #relattionship
    userstate = db.relationship('State', back_populates = 'stateuser')
    userposts = db.relationship('Posts', back_populates = 'postuser')
    

class Manufacturer(db.Model):
    manufacturer_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    manufacturer_name = db.Column(db.String(255), nullable=False)
    #relattionship
    manuspare = db.relationship('Spareparts', back_populates = 'sparemanu')
    manuposts = db.relationship('Posts', back_populates = 'postmanu')


class Posts(db.Model):
    posts_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    posts_title = db.Column(db.String(255), nullable=False)
    posts_fullpost = db.Column(db.Text())
    posts_time = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    #foreign key
    posts_manucat = db.Column(db.Integer(), db.ForeignKey("manufacturer.manufacturer_id"))
    posts_user_id = db.Column(db.Integer(), db.ForeignKey("users.user_id"))
     #relattionship
    postmanu = db.relationship('Manufacturer', back_populates = 'manuposts')
    postuser = db.relationship('Users', back_populates = 'userposts')
    postcomment = db.relationship('Comment', back_populates = 'compost')

class Specialists(db.Model):
    specialists_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    specialists_fullname = db.Column(db.String(255), nullable=False)
    specialists_email = db.Column(db.String(255), nullable=False)
    specialists_password = db.Column(db.String(255), nullable=False)
     #relattionship
    speciacomment = db.relationship('Comment', back_populates = 'comspec')

class State(db.Model):
    state_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    state_name = db.Column(db.String(255), nullable=False)
    #relationship
    stateuser = db.relationship('Users', back_populates = 'userstate')

class Comment(db.Model):
    comment_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    comment_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    comment_fullcomment = db.Column(db.Text())
    #foreignkey
    comment_userid = db.Column(db.Integer(), db.ForeignKey("users.user_id"))
    comment_postid = db.Column(db.Integer(), db.ForeignKey("posts.posts_id"))
    comment_specialist_id = db.Column(db.Integer(), db.ForeignKey("specialists.specialists_id"))
    #relationship
    comspec = db.relationship('Specialists', back_populates = 'speciacomment')
    compost = db.relationship('Posts', back_populates = 'postcomment')
    comuser = db.relationship('Users', backref='usercom')

class Suppliers(db.Model):
    suppliers_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    suppliers_name = db.Column(db.String(255), nullable=False)
    suppliers_location = db.Column(db.String(255), nullable=False)
    suppliers_phone = db.Column(db.String(255), nullable=False)
    suppliers_email = db.Column(db.String(255), nullable=False)
    #relatonship
    suppspare = db.relationship('Spareparts', back_populates = 'sparesupp')

class Spareparts(db.Model):
    spareparts_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    spareparts_image = db.Column(db.String(255), nullable=False)
    spareparts_name = db.Column(db.String(255), nullable=False)
    spareparts_amount = db.Column(db.String(255), nullable=False)
    #foreignkeys
    spareparts_manuid = db.Column(db.Integer(), db.ForeignKey("manufacturer.manufacturer_id"))
    spareparts_supplierid = db.Column(db.Integer(), db.ForeignKey("suppliers.suppliers_id"))
    #relationship
    sparemanu = db.relationship('Manufacturer', back_populates = 'manuspare')
    sparesupp = db.relationship('Suppliers', back_populates = 'suppspare')

class Order(db.Model):
    order_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    order_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    order_address = db.Column(db.String(1000), nullable=False)
    order_status = db.Column(db.Enum("pending","delivered"), default="pending")
    order_userid = db.Column(db.Integer(), db.ForeignKey("users.user_id"))
    #relationship
    user = db.relationship('Users', backref='myorders')


class Orderdet(db.Model):
    orderdet_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    orderdet_quantity = db.Column(db.Integer(), nullable=False)
    orderdet_amt = db.Column(db.Float(), nullable=False)
    orderdet_orderid = db.Column(db.Integer(), db.ForeignKey("order.order_id"))
    orderdet_sparepartid = db.Column(db.Integer(), db.ForeignKey("spareparts.spareparts_id"))
    #relationship
    orderdet_order = db.relationship('Order', backref='order_orderdetails')
    orderdet_spare = db.relationship('Spareparts', backref='spare_orderdetails')

class Payment(db.Model):
    pay_id = db.Column(db.Integer(), primary_key=True,autoincrement=True)
    pay_userid = db.Column(db.Integer(), db.ForeignKey("users.user_id"))
    pay_orderid = db.Column(db.Integer(), db.ForeignKey("order.order_id"))
    pay_ref = db.Column(db.Integer(), nullable=False)
    pay_date = db.Column(db.DateTime(), default=datetime.datetime.utcnow())
    pay_status = db.Column(db.Enum("pending","paid","failed"), default="pending")
    pay_amt=db.Column(db.Float())
    pay_response=db.Column(db.Text(), nullable=True)
    #relationship
    #set up relationship with myorder
    pay_order = db.relationship('Order', backref='orderpay')
    pay_user = db.relationship('Users', backref='users_payments')

class Contactus(db.Model):
    contact_id=db.Column(db.Integer(), primary_key=True,autoincrement=True)
    contact_name=db.Column(db.String(255), nullable=False)
    contact_email=db.Column(db.String(100), nullable=True)
    contact_message=db.Column(db.Text(), nullable=True)

