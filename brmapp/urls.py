
from django.contrib import admin
from django.urls import path,include,re_path
from .views import *

urlpatterns = [
    path('',home,name='home'),
    path("books/",helloView),
    path("add-book/",addBookView),
    path("add-book/add",addBook,name='addbook'),
    path("edit-book/",editBookView),
    path("edit-book/edit",editBook),
    path("delete-book",deleteBookView.as_view(),name='deletebook'),
    path('add-student/', add_student,name='add_student'),
    path('add-student/student/',student),
    path('student/',student),
    path('edit-student/',editstudentview),
    path('edit-student/edit',editstudent),
    path('delete-student',deletestudent),
    path('generate_pdf/', BookPDFView.as_view(), name='generate_pdf'),
    path('issue-book/<int:book_id>/', issue_book, name='issue_book'),
    path('issue-book/',issue_bookview,name='issue_bookview'),
   
]
