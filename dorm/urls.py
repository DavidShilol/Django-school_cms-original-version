from django.urls import path
from . import views


app_name = 'dorm'
urlpatterns = [
	path('login/', views.LoginView.as_view(), name='login'),
	path('register/', views.RegisterView.as_view(), name='register'),
	path('logout/', views.logout, name='logout'),
	path('dormadmin/', views.DormadminIndex, name='DormadminIndex'),
	path('building/', views.BuildingView.as_view(), name='BuildingView'),
	path('building/<int:building_num>/', views.RoomView.as_view(), name='RoomView'),
	path('teacher/', views.TeacherIndex, name='TeacherIndex'),
	path('student/', views.StudentView.as_view(), name='StudentView'),
	path('building/<int:building_num>/<int:room_num>/', views.RoomDetailView.as_view(), name="RoomDetail"),
	path('studentsearch/', views.StudentSearch.as_view(), name="StudentSearch"),
	path('request/', views.RequestView.as_view(), name="RequestView"),
	path('dormsearch/', views.DormSearch.as_view(), name="DormSearch"),
	path('dormsearch/<int:building_num>/<int:room_num>/', views.DormSearchDetail.as_view(), name="DormSearchDetail"),
	path('person/', views.PersonView.as_view(), name="PersonView"),
]

