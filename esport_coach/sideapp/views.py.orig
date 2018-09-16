"""
this file calls all page functions and renders the pages with given context.
"""
from .forms import *
from .models import *
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render_to_response, redirect, render
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core import serializers
from django.db.models import Count
import json
import requests
from pprint import pprint

def home(request):
    return render(request, "home.html")

def login(request):
<<<<<<< local
=======

>>>>>>> other
    form = AuthenticateForm(request.POST)
    if form.is_valid():
        userid = form.cleaned_data.get('userid')
        password = form.cleaned_data.get('password')
    context = {"form" : form}
    return render(request, "loginAuthentication.html", context)


def authenticated(request, userid):
    print userid
    context = {
        'userid': userid,
    }
    return render(request, "home.html", context)


def authenticateLogin(request):
    if request.is_ajax:
        response_error1 = 'not found'
        response_error2 = "Error getting your info from the form."

        try:
            userid = request.GET.get('userid')
            password = request.GET.get('password')
            try:
                login_userid = User.objects.get(userid=userid, password=password)
                return HttpResponse(userid)
            except:
                return HttpResponse(response_error1)
        except:
            return HttpResponse(response_error2)
    else:
        raise Http404


def register(request):

    form = RegistrationForm(request.POST)
    if form.is_valid():
        userid = form.cleaned_data.get('userid')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        pname = form.cleaned_data.get('pname')
        skypeid = form.cleaned_data.get('skypeid')
        twitchid = form.cleaned_data.get('twitchid')
    context = {"form" : form}
    return render(request, "register.html", context)

def authenticateRegister(request):

    if request.is_ajax:
        response_error1 = 'User already exists'
        response_error2 = "Error getting your info from the form."

        try:
            userid = request.GET.get('userid')
            password = request.GET.get('password')
            email = request.GET.get('email')
            pname = request.GET.get('pname')
            skypeid = request.GET.get('skypeid')
            twitchid = request.GET.get('twitchid')
            try:
                login_userid = User.objects.get(userid=userid, password=password, email=email, pname=pname)
                return HttpResponse(response_error1)
            except:
                summonerName = str(pname)
                r = requests.get('https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/'+summonerName+'?api_key=8340953c-a577-4057-bcfb-962e98780cb1')
                if r.status_code == 404:
                    return HttpResponse("404")
                elif r.status_code == 400:
                    return HttpResponse("400")
                elif r.status_code == 401:
                    return HttpResponse("401")
                elif r.status_code == 429:
                    return HttpResponse("429")
                elif r.status_code == 500:
                    return HttpResponse("500")
                elif r.status_code == 503:
                    return HttpResponse("503")
                else:
                    key = r.json()
                    summonerNameValue = key[summonerName]["name"]
                    summonerId = str(key[summonerName]["id"])
                    r = requests.get('https://na.api.pvp.net/api/lol/na/v2.5/league/by-summoner/'+summonerId+'/entry?api_key=8340953c-a577-4057-bcfb-962e98780cb1')
                    summonerInfo = r.json()
                    summonerRank = summonerInfo[summonerId][0]["tier"]
                    summonerDivision = summonerInfo[summonerId][0]['entries'][0]['division']
                    user = User(userid=userid, password=password, email=email, pname=pname, rank=summonerRank, skypeid=skypeid, twitchid=twitchid)
                    user.save()
                    # context = {"value":summonerRank,
                    #            "division":summonerDivision,
                    #            "name":summonerNameValue}
                    # return render(request, "authenticated.html", context)
                return HttpResponse(userid)
        except:
            return HttpResponse(response_error2)
    else:
        raise Http404
    pass

    # context = {"value":"must provide a Summoner name"}
    # if request.method == 'GET':

    # return render(request, "register.html")



def logout(request):
    auth_logout(request)
    return redirect('/')


def contact(request):
    """
    Contact function which creates a contact
    form with some context and renders it.
    """
    form = ContactForm(request.POST)

    if form.is_valid():
        email = form.cleaned_data.get('email')
        message = request.POST.get('message', '')
        #message = form.cleaned_data.get('messsage')
        #print(message)
        username = form.cleaned_data.get('username')
        subject = 'Customers Enquiries'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, settings.EMAIL_HOST_USER]
        contact_message = "%s: %s via %s"%(username, message, email)
        send_mail(subject, contact_message, from_email, to_email, fail_silently=True)


    context = {"form" : form}
    return render(request, "contact.html", context)


def list_of_coaches(request):
    coaches_list = []

    all_users = User.objects.all()
    for user in all_users:
        coaches = user.coach_set.all()    # It should always return a query set of one coach instance.
        for coach in coaches:
            reviews = coach.reviewing_set.all()
            avg_review = 0;
            for review in reviews:
                avg_review = int((review.skill_stars+review.communication_stars+review.helpfulness_stars)/3)
            coaches_list.append([user.pname, user.rank, coach.server, coach.champion, coach.role, avg_review, coach.pricerate, user.userid])

    context = {'coaches': coaches_list}
    return render(request, "listOfCoachesPage.html", context)

def searchCoach(request):
    if request.is_ajax:
        try:
            server = request.GET.get('Server')
            role = request.GET.get('Role')
            hero = request.GET.get('Champion')
            rank = request.GET.get('Rank')
            priceRange = request.GET.get('price')

            if (priceRange == "$1-$10"):
                price_minRange = 1
                price_maxRange = 10
            elif priceRange == "$10-$20":
                price_minRange = 10
                price_maxRange = 20
            elif priceRange == "$20-$30":
                price_minRange = 20
                price_maxRange = 30
            elif priceRange == "$30-$40":
                price_minRange = 30
                price_maxRange = 40
            elif priceRange == "$40-$50":
                price_minRange = 40
                price_maxRange = 50

            spec_filter = {}
            if server != 'Region Server' and server != "------":
                spec_filter['coach__server'] = server
            if role != 'Role' and role != "------":
                spec_filter['coach__role'] = role
            if hero != 'Champion' and hero != "------":
                spec_filter['coach__champion'] = hero
            if rank != 'Rank' and rank != "------":
                spec_filter['rank__contains'] = rank
            if priceRange != 'Price Rate' and priceRange != "------":
                spec_filter['coach__pricerate__range'] = (price_minRange,price_maxRange)

            users = User.objects.filter(**spec_filter)
            coaches_list = []
            for user in users:
                query_coach_att = user.coach_set.filter(userid=user.userid)
                for att_as_coach in query_coach_att:
                    coaches_list.append({'pname': user.pname,
                                         'rank': user.rank,
                                         'server': att_as_coach.server,
                                         'champion': att_as_coach.champion,
                                         'role': att_as_coach.role,
                                         'rating': att_as_coach.rating,
                                         'pricerate': att_as_coach.pricerate})
            formData = json.dumps({'coaches':coaches_list})
            if coaches_list == []:
                return HttpResponse('not found')
            return HttpResponse(formData)

        except KeyError:
            return HttpResponse('Error')
    else:
        raise Http404


def tutorselected(request, tutor_username):
    coach_info = []
    avg_review = 0;
    user = User.objects.get(userid=tutor_username)
    coaches = user.coach_set.all()    # It should always return a query set of one coach instance.
    for coach in coaches:
        reviews = coach.reviewing_set.all()
        for review in reviews:
            avg_review = int((review.skill_stars+review.communication_stars+review.helpfulness_stars)/3)
        coach_info = {"pname":user.pname, "rank":user.rank, "server":coach.server, "champion":coach.champion, 'avatar':coach.avatar, "avg_review":avg_review, "pricerate":coach.pricerate, "overview":coach.overview, "skypeid":user.skypeid, "twitchid":user.twitchid, "userid":user.userid}

    context = {
        'coach': coach_info,
        }
    return render(request, "tutorSelectedPage.html", context)


def reviewcoach(request, tutor_username):
    if request.is_ajax:
        # Response messages:
        response_sucess = "Thanks for your honest review!"
        response_error1 = "Error: Must input a comment."
        response_error2 = "Error: You have rated this coach already! If you need to modify/remove your previous rating for this coach, please contact us."

        try:
            user_reviewer = Reviewing.objects.get(coach__userid=tutor_username, student__userid='kelly')
            skill = request.GET.get('ratingSkill')
            communication = request.GET.get('ratingCommunication')
            helpfulness = request.GET.get('ratingHelpfulness')
            review_comment = request.GET.get('textarea_review')

            # if skill == "":
            #     skill == 0
            # else:
            #     skill = int(skill)
            # if communication == "":
            #     communication == 0
            # else:
            #     communication = int(communication)
            # if helpfulness == "":
            #     helpfulness == 0
            # else:
            #     helpfulness = int(helpfulness)
            # if review_comment == "":
            #     return HttpResponse(response_error1)

            # coach_selected = Signup.objects.get(username=tutor_username)
            # all_users_reviews = coach_selected.reviews_set.all()
            # rating = Reviews(id=None, coach=coach_selected, reviewer=user_reviewer, skill_stars=skill, communication_stars=communication, helpfulness_stars=helpfulness, comment=review_comment)
            # rating.save()

            return HttpResponse(response_sucess)

        except:
            return HttpResponse(response_error2)
    else:
        raise Http404

def renderReviews(request,tutor_username):
    if request.is_ajax:
        sum_all_avg_reviews = 0
        num_reviews = 0
        list_reviews = []
        try:
            coach = Coach.objects.get(userid=tutor_username)
            all_users_reviews = coach.reviewing_set.all()
        except KeyError:
            return HttpResponse("error")

        # for user_review in all_users_reviews:
        #     avg_review = int((user_review.skill_stars + user_review.communication_stars + user_review.helpfulness_stars)/3)
        #     # list_reviews.append({"skill":user_review.skill_stars, "communication":user_review.communication_stars, "helpfulness":user_review.helpfulness_stars, "avg_review":avg_review, "comment":user_review.comment,"reviewer":user_review.reviewer})

        response = serializers.serialize('json',all_users_reviews)
        return HttpResponse(response)
    else:
        raise Http404

def paymentpage(request, tutor_username):
    user = User.objects.get(userid=tutor_username)
    coaches = user.coach_set.all()

    for coach in coaches:
        reviews = coach.reviewing_set.all()
        for review in reviews:
            avg_review = int((review.skill_stars+review.communication_stars+review.helpfulness_stars)/3)
        coach_info = {"pname":user.pname, "rank":user.rank, "server":coach.server, "champion":coach.champion, "avg_review":avg_review, "pricerate":coach.pricerate, "skypeid":user.skypeid, "twitchid":user.twitchid, "userid":user.userid}

    # if request.is_ajax:
    #     lesson_duration = request.POST['lesson_duration']
    #     lesson_date_time = request.POST['lesson_date_time']

    #     context = lesson_duration + "," + lesson_date_time
    #     return HttpResponse(context)
    # else:
    #     raise Http404
    context = {
        "coach":coach_info,
    }

    return render(request, "summaryReceiptPage.html", context)

def streampage(request, tutor_username):
    user = User.objects.get(userid=tutor_username)
    coaches = user.coach_set.all()

    for coach in coaches:
        reviews = coach.reviewing_set.all()
        for review in reviews:
            avg_review = int((review.skill_stars+review.communication_stars+review.helpfulness_stars)/3)
        coach_info = {"pname":user.pname, "rank":user.rank, "server":coach.server, "champion":coach.champion, "avg_review":avg_review, "pricerate":coach.pricerate, "skypeid":user.skypeid, "twitchid":user.twitchid, "userid":user.userid}

    context = {'coach': coach_info}
    return render(request, "streamPage.html", context)


def charge(request):
    form = SalePaymentForm(request.POST or None)
    if form.is_valid():
        return render(request, "summaryReceiptPage.html", context)
    context = {"form" : form}
    return render(request, "checkout.html", context)

def fourOfour(request):
    """
    submit email for notice
    """
    form = errorForm(request.POST)

    if form.is_valid():
        email = form.cleaned_data.get('email')
        subject = 'Player Ranking Page Down'
        from_email = settings.EMAIL_HOST_USER
        to_email = [from_email, settings.EMAIL_HOST_USER]
        contact_message = "Let me know if the page is up.... %s"%(email)
        send_mail(subject, contact_message, from_email, to_email, fail_silently=True)
        return render(request, "base.html")
    context = {"form" : form}
    return render(request, "404.html", context)
