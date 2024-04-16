from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [ 
path("domaa/", views.domaa,name="domaa"),
path("reg/",views.reg,name="reg"),
path("nov/",views.nov,name="nov"),
path("log/",views.log,name="log"),
path("admin_users/",views.admin_users,name="admin_users"),
path("admin_users_delete/",views.admin_users_delete,name="admin_users_delete"),
path("admin_users_edit/",views.admin_users_edit,name="admin_users_edit"),
path("prof_create_document/",views.prof_create_document,name="prof_create_document"),
path("prof_view_document/",views.prof_view_document,name="prof_view_document"),
path("prof_delete_document/",views.prof_delete_document,name="prof_delete_document"),
path("prof_share_document/",views.prof_share_document,name="prof_share_document"),
path("prof_share_document_list/",views.prof_share_document_list,name="prof_share_document_list"),
path("student_shared_document/",views.student_shared_document,name="student_shared_document"),
path("admin_users_edit",views.admin_users_edit,name="admin_users_edit"),
path("ispis_studenata",views.ispis_studenata,name="ispis_studenata")

]