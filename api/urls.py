from django.urls import path
from . import views

urlpatterns = [
   
    path('notes/',views.notes,name="notes"),
    # path('note/create/',views.create,name="create-note"),
    # path('note/<str:pk>/update/',views.update,name="update-note"),
    # path('note/<str:pk>/delete/',views.delete,name="delete-note"),
    path('note/<str:pk>/',views.note,name="note"),
    path('login/',views.login,name="login"),
    path('register/',views.register,name="register"),

]