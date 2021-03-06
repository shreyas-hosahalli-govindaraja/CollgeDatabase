from django.http import HttpResponse,Http404
from django.shortcuts import render,redirect
from oauth2client import client, crypt
from django.conf import settings
from django.db.models import Q
import re

#importing models
from .models import Accesslog,University,College,User,Courses_College_Map,Courses,StudyField

#TEMP
def index(request):
	context = {
	}
	return render(request, 'frontendapp/index.html', context)

def getsessionvar(request):
	userid = ''
	name = ''
	picture = ''
	email = ''
	if request.session.has_key('userid'):
			userid = request.session['userid']
			name = request.session['name']
			picture = request.session['picture']
			email = request.session['email']
	context = {
		'suserid' : userid,
		'sname' : name,
		'spicture' : picture,
		'semail' : email,
	}
	return context


# Landing page of frontendapp
def home(request):
	sessioncontext = getsessionvar(request)
	trendingcollegelist = College.objects.filter().order_by("-visit_count")[:5]
	trendingcourselist = Courses.objects.filter().order_by("-visit_count")[:5]
	context = {
			"trendingcollegelist" : trendingcollegelist,
			"trendingcourselist" : trendingcourselist,
	}
	context.update(sessioncontext)
	return render(request, 'frontendapp/home.html', context)

#Google sign in tokensignin
def tokensignin(request):
	context = {}
	CLIENT_ID = settings.CLIENT_ID
	if request.method == "POST":
		token = request.POST['idtoken']
	try:
	    idinfo = client.verify_id_token(token, CLIENT_ID)
	    if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
	        raise crypt.AppIdentityError("Wrong issuer.")
	except crypt.AppIdentityError:
		    return HttpResponse("failed")
	userid = idinfo['sub']
	request.session['userid'] = userid
	request.session['name'] = idinfo['name']
	request.session['picture'] = idinfo['picture']
	request.session['email'] = idinfo['email']
	return HttpResponse("logged in")

#logout
def logout(request):
	for sesskey in request.session.keys():
		del request.session[sesskey]
	request.session.flush()
	request.session.modified = True
	return redirect('home')

#Courses
def courses(request):
	course_list = Courses.objects.all()
	field_list = StudyField.objects.all()
	field_course_map = {}
	for field in field_list:
		temp = []
		for course in course_list:
			if(course.field == field):
				temp.append(course)
		field_course_map[field] = temp
	context = {
		"field_list" : field_list,
		"course_list": course_list,
		"field_course_map": field_course_map,
	}
	sessioncontext = getsessionvar(request)
	context.update(sessioncontext)
	return render(request,'frontendapp/courses.html',context)


def viewcourse(request,course_id):
	course= Courses.objects.get(id = course_id)
	course.visit_count += 1
	course.save()
	college_list = Courses_College_Map.objects.filter(course__id = course_id).values("college")
	college_list = College.objects.filter(id__in = college_list)
	context = {
		"college_list":college_list,
		"course":course,
	}
	sessioncontext = getsessionvar(request)
	context.update(sessioncontext)
	return render(request,"frontendapp/viewcourse.html",context)

#TEMP
def results(request):
	return HttpResponse("Results")

# Search result page
def search(request):
	college_list = []
	university_list = []
	byplace_list = []
	#POST - searches the database for the requested collge
	if request.method == "POST":
		search_content = request.POST['collegename']
		# aliases
		search_content = str(search_content).lower()
		if(search_content=='bangalore'):
			search_content = 'bengaluru'
		elif(search_content=='bombay'):
			search_content = 'mumbai'
		elif(search_content=='Madras'):
			search_content ='chennai'
		# querying db
		university_list = University.objects.filter( Q(name__icontains = search_content) | Q(alias__icontains = search_content))[:10]
		college_list = College.objects.filter(Q(name__icontains = search_content) | Q(alias__icontains = search_content))[:10]
		address_list = College.objects.all()
		pattern = re.compile(search_content)
		for addr in address_list:
			if(pattern.search(str(addr.address).lower())):
				byplace_list.append(addr)
		print(byplace_list)
	else:
		search_type = request.GET.get('search_type','college')
		if search_type == 'university':
			university_list = University.objects.all()[:10]
		else:
			college_list = College.objects.all()[:10]
	context = {
		'college_list': college_list,
		'university_list':university_list,
		'byplace_list':byplace_list,
	}
	sessioncontext = getsessionvar(request)
	context.update(sessioncontext)
	return render(request, 'frontendapp/search.html', context)


# College display
def college(request,college):
	if college.isdigit():
		try:
			obj_col = College.objects.get(id = college)
			course_list = Courses_College_Map.objects.filter(college = obj_col).values("course_id")
			course_list = Courses.objects.filter(id__in = course_list)
			obj_col.visit_count += 1
			obj_col.save()
		except College.DoesNotExist:
			raise Http404("You seem to be lost!")
	else:
		try:
			obj_col = College.objects.get(name = college)
			course_list = Courses_College_Map.objects.filter(college = obj_col).values("course_id")
			course_list = Courses.objects.filter(id__in = course_list)
			obj_col.visit_count += 1
			obj_col.save()
		except College.DoesNotExist:
			raise Http404("You seem to be lost!")

	#placed one offer
	placed2016 = obj_col.placement_num_placed-obj_col.placement_num_with_two_offers
	placed2015 = obj_col.placement_num_placed1-obj_col.placement_num_with_two_offers1
	placed2014 = obj_col.placement_num_placed2-obj_col.placement_num_with_two_offers2
	#total stud
	notplaced2016 = obj_col.placement_num_eligible-obj_col.placement_num_placed
	notplaced2015 = obj_col.placement_num_eligible1-obj_col.placement_num_placed1
	notplaced2014 = obj_col.placement_num_eligible2-obj_col.placement_num_placed2
	#twooffer
	twooffer2016 = obj_col.placement_num_with_two_offers
	twooffer2015 = obj_col.placement_num_with_two_offers1
	twooffer2014 = obj_col.placement_num_with_two_offers2

	placed2016pct = 0
	placed2015pct = 0
	placed2014pct = 0

	if(obj_col.placement_num_placed!=0 and obj_col.placement_num_eligible!=0):
		if(obj_col.placement_num_placed!=0 and obj_col.placement_num_eligible!=0):
			if(obj_col.placement_num_placed!=0 and obj_col.placement_num_eligible!=0):
				placed2016pct = round((float(obj_col.placement_num_placed)/float(obj_col.placement_num_eligible))*100,2)
				placed2015pct = round((float(obj_col.placement_num_placed1)/float(obj_col.placement_num_eligible1))*100,2)
				placed2014pct = round((float(obj_col.placement_num_placed2)/float(obj_col.placement_num_eligible2))*100,2)

	context = {
		'college' : obj_col,
		'course_list' : course_list,
		'placed2016' : placed2016,
		'placed2015' : placed2015,
		'placed2014' : placed2014,
		'notplaced2016' : notplaced2016,
		'notplaced2015' : notplaced2015,
		'notplaced2014' : notplaced2014,
		'twooffer2016' : twooffer2016,
		'twooffer2015' : twooffer2015,
		'twooffer2014' : twooffer2014,
		'placed2016pct' : placed2016pct,
		'placed2015pct' : placed2015pct,
		'placed2014pct' : placed2014pct,
	}
	sessioncontext = getsessionvar(request)
	context.update(sessioncontext)
	return render(request, 'frontendapp/college.html', context)

# University display
def university(request,university):
	if university.isdigit():
		try:
			obj_uni = University.objects.get(id = university)
			obj_uni.visit_count = obj_uni.visit_count+ 1
			obj_uni.save()
			college_list = College.objects.filter(university = obj_uni)
		except University.DoesNotExist:
			raise Http404("You seem to be lost!")
	else:
		try:
			obj_uni = University.objects.get(name = university)
			obj_uni.visit_count = obj_uni.visit_count+ 1
			college_list = College.objects.filter(university = obj_uni)
		except University.DoesNotExist:
			raise Http404("You seem to be lost!")
	context = {
		'university' : obj_uni,
		'college_list': college_list,
	}
	sessioncontext = getsessionvar(request)
	context.update(sessioncontext)
	return render(request, 'frontendapp/university.html', context)
