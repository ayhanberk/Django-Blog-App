from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,reverse
from .forms import ArticleForm
from .models import Article,Comment
from django.contrib import messages
from django.contrib.auth.decorators import login_required # login_required decorater 


# Create your views here.
#Url geldiği zaman gösterilecek fonksiyonları buraya yaz.

def articles(request):
    keyword = request.GET.get("keyword")

    if keyword:
        articles = Article.objects.filter(title__contains = keyword) # titlelarında verilen keyworde uygun articelları databasede arama sorgusu.
        return render(request, "articles.html",{"articles":articles})
    articles = Article.objects.all()
    return render(request,"articles.html",{"articles":articles})

def index(request):
    context = {
        "numbers":[1,2,3,4,5,6]
    }
    # return HttpResponse("Anasayfa") #Http dönmek istediğimiz zaman bu komutu kullanıyoruz.
    return render(request, "index.html",context) #templates klasörü içindeki index dosyasını arar ve öyle bir dosya var ise o dosyayı sayfaya yansıtır

def about(request):
    return render(request, "about.html")

@login_required(login_url= "user:login") # user uygulaması altındaki login urlsıne git
def dashboard(request):
    articles = Article.objects.filter(author = request.user)
    context = {
        "articles": articles
    }
    return render(request,"dashboard.html",context)

@login_required(login_url= "user:login") # user uygulaması altındaki login urlsıne git
def addArticle(request):

    form = ArticleForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        article = form.save(commit=False) # article objesi oluştur ama save(database'e yazma işlemini) işlemini gerçekleştirme
        article.author = request.user
        article.save()# veritabanına article'ı kaydetme işlemi
        messages.success(request, "Makale Başarıyla Oluşturuldu.")
        return redirect("article:dashboard") # article uygulaması altındaki dashboard urlsıne git
    return render(request,"addarticle.html",{"form":form})

def detail(request,id):
    # article = Article.objects.filter(id = id).first # gördüğü ilk değeri dönmesi için .first komutu kullanılır.
    article = get_object_or_404(Article,id = id)

    comments = article.comments.all()
    return render(request,"detail.html",{"article":article,"comments":comments})

@login_required(login_url= "user:login") # user uygulaması altındaki login urlsıne git
def updateArticle(request,id):
    article = get_object_or_404(Article,id = id)
    form = ArticleForm(request.POST or None, request.FILES or None,instance= article)
    # instance article article objesindeki tüm bilgiler formun içine yazılacaktır. 
    if(article.author != request.user):
        messages.info(request,"Bu Makaleye Erişiminiz Bulunmamaktadır. Lütfen bilgilerinizi kontrol ediniz!")
        return redirect("article:dashboard")
    else:
        if form.is_valid():
            article = form.save(commit=False) # article objesi oluştur ama save(database'e yazma işlemini) işlemini gerçekleştirme
            article.author = request.user
            article.save()# veritabanına article'ı kaydetme işlemi
            messages.success(request, "Makale Başarıyla Güncellendi.")
            return redirect("article:dashboard") # article uygulaması altındaki dashboard urlsıne git

        return render(request,"update.html",{"form":form})

@login_required(login_url= "user:login") # user uygulaması altındaki login urlsıne git
def deleteArticle(request,id):
    article = get_object_or_404(Article,id = id)
    if(article.author != request.user):
        messages.info(request,"Bu Makaleye Erişiminiz Bulunmamaktadır. Lütfen bilgilerinizi kontrol ediniz!")
        return redirect("article:dashboard")
    else:
        article.delete() # veritabanından article silme işlemi
        messages.success(request,"Makale Başarıyla Silindi.")
        return redirect("article:dashboard") # article uygulaması altındaki dashboard urlsıne git

def addComment(request,id):
    article = get_object_or_404(Article,id=id)
    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")
        newComment = Comment(comment_author = comment_author, comment_content = comment_content)
        newComment.article = article
        newComment.save()
    # return redirect("/articles/article/"+str(id))
    return redirect(reverse("article:detail",kwargs={"id":id})) #dinamik url redirect işlemi için