from django.db import models
from django.conf import settings
from datetime import date, datetime
from calendar import monthrange
from django.db.models import Count

"""
*User Table:	A database table is stores all user information for either a student or a coach. It contains all basic info of what a user should have.
*Fields: 		userid: character field used to grab the ID from steam
				email: email of the user
				pname: steam persona
				rank: Containing the Rank or how experience a user is
				skypeid: Skeype ID that need to do audio chat 
				twitchid: twitchid ID that is used for video streaming
"""
class User(models.Model):
		userid = models.CharField(primary_key=True, max_length=100, blank=False, null=False)
		password = models.CharField(max_length=18, blank=False, null=False)
		email = models.EmailField(blank=False, null=False)
		pname = models.CharField(max_length=100, blank=False, null=False)
		rank = models.CharField(max_length=100, blank=False, null=False)
		skypeid = models.CharField(max_length=100, blank=False, null=False)
		twitchid = models.CharField(max_length=100, blank=False, null=False)
		def __str__(self):
				return  self.userid + " " + self.email + " " + self.pname

"""
*Coach Table:	A database table containing coach and it's atrributese, where has to be in User table.
*Fields: 		userid: ForeignKey meaning it has to be a instance of coach
				server: server of the the coach.
				champion: A list of heros that the Coach is good at.
				role: positions the coach is expert in.
				pricerate: FloatField rate the coach is charing the student
				avatar: Profile picture we grab from steam
				rating: the overall rating of the coach
				overview: A TextField containing the description of the Coach and the information the coach want to let the user know
"""
class Coach(models.Model):
	 userid = models.ForeignKey('User', on_delete=models.CASCADE)
	 server = models.CharField(max_length = 50, blank = False, null = False)
	 champion = models.CharField(max_length = 500, blank = False, null = False)
	 role = models.CharField(max_length = 500, blank = False, null = False)
	 pricerate = models.PositiveIntegerField(default = 0,  blank = False, null = False)
	 avatar = models.URLField(blank=False, null=False)
	 rating = models.IntegerField(default = 0,  blank = False, null = False)
	 overview = models.TextField(blank=True)
	 def __str__(self):
				return  self.userid.userid + " " + self.champion + " " + str(self.rating) + " " + self.server + " " + str(self.pricerate) + " " + self.overview 


	 # How to use this function 
	 # Ex: 
	 #   Before doing anything, first select a coach 
	 #			selected_coach = Coach.objects.get(userid='Name')  Name is the name of your coach ex: Name='fei'.
	 #   														   By Doing get(), you are getting the object of the Coach.
	 #	 Next:
	 #			selected_coach.num_student()					   Use the selected coach to call this function and you will get the number of student such coach has
	 def num_student(self):
	 		students = Coaching.objects.filter(coach=self)
	 		num_stu = students.aggregate(Count('student',distinct=True))
	 		return num_stu['student__count']
	 # The function below allows you to get Rank of Coach
	 # How to use this function
	 #	selected_coach = Coach.objects.get(userid= 'name')   input Coach object, and userid name. and get a specific coach object
	 # 	Then just 
	 #			selected_coach.getRank()    This will return you the Rank of the selected coach.
	 def getRank(self):
	 		return self.userid.rank


"""
*Coaching Table:A database table containing the information of user been coached
*Fields: 		coach: ForeignKey meaning it has to be a instance of coach
				student: Student is the person who hires coach, this has to be in the database
				date: The date that this order was submitted
				pricerate: FloatField rate the coach is charing the student
				quantity: The unit of hour the user is applying for
				request: Special requests for any other adiditional information.
"""
class Coaching(models.Model):
	 coach = models.ForeignKey('Coach', on_delete=models.CASCADE)
	 student = models.ForeignKey('User', on_delete=models.CASCADE)
	 date = models.DateTimeField(auto_now_add = False, auto_now = "True")
	 pricerate = models.PositiveIntegerField(default = 0,  blank = False, null = False)
	 quantity = models.IntegerField(default = 0,  blank = False, null = False)
	 request = models.TextField(blank=True)
	 def __str__(self):
				return self.coach.userid.userid + " " + self.student.userid + " " + str(self.date) + " " + str(self.pricerate) + " " + str(self.quantity)


"""
*ReviewingTable:A database table containing the information of students reviewing coach
*Fields: 		coach: ForeignKey meaning it has to be a instance of coach
				student: Student is the person who hires coach, this has to be in the database
				skill_stars: rating coach skill
				communication_stars: rating coach commnunication
				helpfulness_stars: rating eoach helpfulness
				comment: Comment that the student had on the coach
				date: The date that the review is submitted
"""
class Reviewing(models.Model):
	 coach = models.ForeignKey('Coach', on_delete=models.CASCADE)
	 student = models.ForeignKey('User', on_delete=models.CASCADE)
	 skill_stars = models.PositiveIntegerField(blank=False, null=True)
	 communication_stars = models.PositiveIntegerField(blank=False, null=True)
	 helpfulness_stars = models.PositiveIntegerField(blank=False, null=True)
	 comment = models.TextField(blank=False, null=False)
	 date = models.DateTimeField(auto_now_add=False, auto_now=False)
	 def __str__(self):
			return self.coach.userid.userid + " " + self.student.userid + " " + str(self.skill_stars) + " " + str(self.date) + " " + self.comment


class Blacklist(models.Model):
	 userid = models.ForeignKey('User', on_delete=models.CASCADE)
	 date = models.DateTimeField(auto_now_add = False, auto_now = "True")
	 reason = models.TextField(blank = False, null=False)
	 #should we add another field of admin so taht we know who put these people into the blacklist
	 def __str__(self):
				return  " " + str(self.date) + " " + self.reason

class Report(models.Model):
	 student = models.ForeignKey('User', on_delete=models.CASCADE)
	 coach = models.ForeignKey('Coach', on_delete=models.CASCADE)
	 reason = models.TextField(blank=False, null=False)
	 date = models.DateTimeField(auto_now_add=False, auto_now=False)
	 def __str__(self):
			return self.student + " " + self.coach + " "  + str(self.date) + " " + self.reason


class Champions(models.Model):
   champion = models.CharField(primary_key=True, max_length=100, blank=False, null=False)
   def __str__(self):
        return self.champion


class transaction(models.Model):
	def __init__(self, *args, **kwargs):
		super(transaction, self).__init__(*args, **kwargs)
		import stripe
		stripe.api.key = settings.STRIPE_API_KEY
		self.stripe = stripe

	#transaction number
	transaction_id = models.CharField(max_length = 32)
	transaction_date = models.DateTimeField(auto_now_add = True, auto_now=False)

	def charge(self, price_in_cents, number, exp_month, exp_year, cvc):
			if self.transaction_id:
					return False, Exception(message = "Already charged.")
			try:
					response = self.stripe.Charge.create(amount = price_in_cents, currency = "usd", card = {"number": number, "exp_month": exp_month, "exp_year": exp_year, "cvc": cvc, "address_line1": self.address1, "address_line2": self.address2, "zip_code": self.zip_code, "state": self.state,}, description = "Thank You, Happy Gaming!")
					self.transcation_id = response.id
			except self.stripe.CardError, ce:
					return False, ce
			return True, response
