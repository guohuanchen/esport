"""this file connects all urls to application when being called."""
from django.conf.urls import url
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^contact/', views.contact, name='contact'),
    url(r'^login/', views.login, name='login'),
    url(r'^authenticateLogin/', views.authenticateLogin, name='authenticateLogin'),
    url(r'^authenticateRegister/', views.authenticateRegister, name='authenticateRegister'),
    url(r'^authenticated/(?P<userid>[-\w]+)', views.authenticated, name='authenticated'),
    url(r'^register/', views.register, name='register'),
    url(r'^listOfCoaches/', views.listOfCoaches, name='list_of_coaches'),
    url(r'^tutorSelected/(?P<tutor_username>[-\w]+)', views.tutorSelected, name='tutorselected'),
    url(r'^applyForCoach/', views.applyForCoach, name='applyForCoach'),
    url(r'^renderReviews/(?P<tutor_username>[-\w]+)', views.renderReviews, name='renderReviews'),
    url(r'^reviewCoach/(?P<tutor_username>[-\w]+)', views.reviewCoach, name='reviewcoach'),
    url(r'^paymentPage/(?P<tutor_username>[-\w]+)', views.paymentPage, name='paymentpage'),
    url(r'^streamPage/(?P<tutor_username>[-\w]+)', views.streamPage, name='streampage'),
    url(r'^searchCoach/', views.searchCoach, name='searchCoach'),
    url(r'^playerRank/', views.fourOfour, name='player_rank'),

]
