from datetime import datetime

# from app import db




#
# class City(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#
#     def __repr__(self):
#         return '<city> %r' % self.id
#
#
# class Post(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
#     subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'))
#     city_id = db.Column(db.Integer, db.ForeignKey('city.id'))
#     title = db.Column(db.String(100), nullable=False)
#     description = db.Column(db.Text, nullable=False)
#     to_price = db.Column(db.Integer, nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow)
#     is_active = db.Column(db.Boolean, default=True)
#     image = db.Column(db.String(100), nullable=False, default='default.jpg')
#     views = db.Column(db.Integer, default=0)
#     category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))
#     subcategory = db.relationship('Subcategory', backref=db.backref('posts', lazy='dynamic'))
#     city = db.relationship('City', backref=db.backref('posts', lazy='dynamic'))

# user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, blank=True, null=True)
# category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
# subcategory = models.ForeignKey(Subcategory, related_name='posts', on_delete=models.CASCADE)
# city = models.ForeignKey(City, related_name='posts', on_delete=models.PROTECT, blank=True, null=True)
# subscription = models.ForeignKey(Subscription, related_name='posts', on_delete=models.PROTECT, blank=True, null=True)
# title = models.CharField(max_length=100)
# description = models.TextField(max_length=300, blank=True, null=True)
# from_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
# to_price = models.DecimalField(max_digits=20, decimal_places=2, blank=True, null=True)
# image = models.ImageField(upload_to='products/%Y/%m/%d', verbose_name='Фотография', blank=True, null=True)
# date_created = models.DateTimeField(auto_now_add=True)
# email = models.EmailField(max_length=100, default='No email')
# phone_number = PhoneNumberField(default='No number')
# wa_number = PhoneNumberField(default='No number')
# is_activated = models.BooleanField(default=True)
# views = models.IntegerField(default=0)
# status = models.CharField(max_length=100, choices=STATUS, default='in_progress')
