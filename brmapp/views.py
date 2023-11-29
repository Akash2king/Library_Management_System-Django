from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect,FileResponse,HttpResponse
from django.http import FileResponse
from .models import Book,Student
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from django.shortcuts import get_object_or_404, render
from io import BytesIO
from django.views import View
  # Create a form for student data
#home
def home(request):
    books=Book.objects.all()
    student=Student.objects.all()
    countstud=countbook=0
    cat=[]
    for i in books:
        cat.append(i.category)
    catnum=len(set(cat))
    for i in books:
        countbook+=1
    for i in student:
        countstud+=1
    values={"books":books,
            'totbook':countbook,
            'totstud':countstud,
            'totcat':catnum
            }
    return render(request,"home.html",values)
def add_student(request):
    if request.method == 'POST':
        print(request.POST)
        name=request.POST["name"]
        reg_no=request.POST["register_number"]
        dept=request.POST["department"]
        ph=request.POST["phone_no"]
        s=Student()
        s.name=name
        s.reg_number=reg_no
        s.department=dept
        s.ph_no=ph
        s.save()
        print(name,reg_no,dept,ph)
        stud=Student.objects.all()
        return render(request, 'student.html',{"student":stud})  # Redirect to a view that lists all students

    return render(request, 'add_student.html')
def student(request):
    stud=Student.objects.all()
    return render(request,"student.html",{"student":stud})

def editstudent(request):
    if request.method=="POST":
        name=request.POST["name"]
        reg_no=request.POST["register_number"]
        dept=request.POST["department"]
        ph=request.POST["phone_no"]
        
        s=Student.objects.get(id=request.POST['sid'])
        s.name=name
        s.reg_number=reg_no
        s.department=dept
        s.ph_no=ph
        s.save()
        return HttpResponseRedirect('/student')
def editstudentview(request):
    s=Student.objects.get(id=request.GET['studentid'])
    print(s)
    return render(request,"edit-student.html",{"student":s})
def deletestudent(request):
    s=Student.objects.get(id=request.GET['studentid'])
    s.delete()
    return HttpResponseRedirect('/student')


#students
#books
# Create your views here.
def helloView(request):
    books=Book.objects.all()
    category=[]
    for i in books:
        category.append(i.category)
    cat=list(set(category))
    return render(request,"viewbook.html",{"books":books,'category':cat})

def addBookView(request):
    book=Book.objects.all()
    category=[]
    for i in book:
        category.append(i.category)
    cat=list(set(category))
    return render(request,"addbook.html",{'category':cat})


def addBook(request):
    if request.method=="POST":
        tit=request.POST["title"]
        aut=request.POST["author"]
        nob=request.POST["no_of_copies"]
        nop=request.POST["book_no"]
        ecat=request.POST['category']
        ncat=request.POST['newcategory']
        if len(str(ecat)) > len(str(ncat)):
            cat=ecat
        else:
            cat=ncat
        book=Book()
        book.title=tit
        book.author=aut
        book.no_of_copies=nob
        book.book_no=nop
        book.category=cat
        book.save()
        return HttpResponseRedirect('/books')

def editBook(request):
    if request.method=="POST":
        tit=request.POST["title"]
        aut=request.POST["author"]
        nob=request.POST["no_of_copies"]
        nop=request.POST["book_no"]
        ecat=request.POST['category']
        ncat=request.POST['newcategory']
        if len(str(ecat)) > len(str(ncat)):
            cat=ecat
        else:
            cat=ncat
        book=Book.objects.get(id=request.POST['bid'])
        book.title=tit
        book.author=aut
        book.no_of_copies=nob
        book.book_no=nop
        book.category=cat
        book.save()
        return HttpResponseRedirect('/books')


def editBookView(request):
    book=Book.objects.get(id=request.GET['bookid'])
    print(book)
    b=Book.objects.all()
    categories=[]
    for i in b:
        categories.append(i.category)
    cat=list(set(categories))
    return render(request,"edit-book.html",{"book":book,'cat':cat})

class deleteBookView(View):
    def post(self, request, *args, **kwargs):
        selected_books = request.POST.getlist('selected_books')

        # Perform deletion of selected books (you may want to add some validation here)
        Book.objects.filter(id__in=selected_books).delete()

        return redirect('/books') 

def issue_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    # Assuming a user returns one copy of the book
    if book.no_of_copies > 0:
        book.no_of_copies -= 1
        book.save()
        b=Book.objects.all()
        return render(request,'issue.html',{'books':b,'mes':f"The book {book.title} has been returned. Remaining copies: {book.no_of_copies}"})
    else:
        b=Book.objects.all()
        return render(request,'issue.html',{'books':b,'mes':'no copy of this books is avilable '})
def issue_bookview(request):
    book=Book.objects.get(id=request.GET['bookid'])
    return render(request,'issue.html',{'book':book})

class BookPDFView(View):
    def get(self, request, *args, **kwargs):
        # Create a file-like buffer to receive PDF data.
        buffer = BytesIO()

        # Create the PDF object, using the buffer as its "file."
        doc = SimpleDocTemplate(buffer, pagesize=letter)

        # Header style
        header_style = ParagraphStyle(
            'Header1',
            parent=getSampleStyleSheet()['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=14,
            spaceAfter=12,
            alignment=1,  # Center alignment
        )

        # Table style
        table_style = TableStyle(
            [
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('WIDTH', (0, 0), (-1, -1), 750),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ]
        )

        # Create the story and set the title
        story = []
        title = Paragraph("KONGUNADU COLLEGE OF ENGINEERING AND TECHNOLOGY", header_style)
        story.append(title)
        story.append(Paragraph("LIBRARY", header_style))
        story.append(Paragraph("<br/><br/>", header_style))

        # Fetch book records from the database
        books = Book.objects.all()

        # Populate data with book information
        data = [["Book No", "Title", "Author", "Category", "No of Copies"]]
        for book in books:
            data.append([book.book_no, book.title, book.author, book.category, book.no_of_copies])

        # Create the table
        table = Table(data, repeatRows=1)

        # Apply the table style
        table.setStyle(table_style)
        story.append(table)

        # Build the PDF document
        doc.build(story)

        # File response with the generated PDF
        buffer.seek(0)
        response = HttpResponse(buffer, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="book_report.pdf"'
        return response