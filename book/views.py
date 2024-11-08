from django.shortcuts import render, redirect
from .models import Book, Reviews
from django.shortcuts import get_object_or_404
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

def bookhome(request):
    searchTerm = request.GET.get('searchBook')
    if searchTerm:
        books = Book.objects.filter(title__contains=searchTerm)
    else:
        books = Book.objects.all()
    return render(request, 'bookhome.html', {'searchTerm':searchTerm, 'books':books})
def bookdetail(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    reviews = Reviews.objects.filter(book=book)
    return render(request, 'bookdetail.html', {'book': book, 'reviews':reviews})

@login_required
def createbookreview(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'GET' :
        return render(request, 'createbookreview.html' ,
        {'form':ReviewForm , 'book':book})
    else:
        try:
            form = ReviewForm(request.POST)
            newReview = form.save(commit=False)
            newReview.user = request.user
            newReview.book = book
            newReview.save()
            return redirect('bookdetail',newReview.book.id)
        except ValueError:
            return render(request,'createbookreview.html', {'form':ReviewForm, 'error':'非法数据'})

@login_required
def updatebookreview(request, review_id) :
    review = get_object_or_404(Reviews, pk=review_id, user=request.user)
    if request.method == 'GET':
        form = ReviewForm(instance=review)
        return render(request, 'updatebookreview.html', {'review':review, 'form':form})
    else:
        try:
            form = ReviewForm(request.POST, instance=review)
            form.save()
            return redirect('bookdetail', review.book.id)
        except ValueError:
            return render(request, 'updatebookreview.html', {'review':review, 'form':form, 'error':'提交非法数据'})

@login_required
def deletebookreview(request, review_id) :
    review = get_object_or_404(Reviews, pk=review_id, user=request.user)
    review.delete()
    return redirect('bookdetail', review.book.id)