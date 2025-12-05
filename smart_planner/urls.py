from django.urls import path
from . import views

app_name = 'smart_planner'
urlpatterns = [
    path('',views.index, name='index'),
    path('topics/',views.topics, name='topics'),
    path('topics/<int:topic_id>/', views.topic, name = 'topic'),
    path('new_topic/', views.new_topic, name = 'new_topic'),
    path('new_note/<int:topic_id>/', views.new_note, name = 'new_note'),
    path('edit_note/<int:note_id>/', views.edit_note, name = 'edit_note'),
    path('topics/<int:topic_id>/delete', views.delete_topic, name = 'delete_topic'),
    path('<int:note_id>/delete', views.delete_note, name = 'delete_note'),
    path('search/', views.search_notes, name = 'search_notes'),
]