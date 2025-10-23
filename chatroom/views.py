from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Message
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.db import connection

# Create your views here.

@login_required
def index(request):
    # Secure way or filtering messages and retrievng them

    # sender_username = request.POST.get("sender", "")
    # messages = Message.objects.all().order_by('-time')
    # if sender_username:
    #     messages = messages.filter(sender__username__iexact=sender_username)
    # messages = messages[:250] # prevent the page from loading like a bazillion messages
    # return render(request, "chatroom/index.html", {"user": request.user, "messages": messages, "sender_username": sender_username})


    # Comment everything in this function below this line and switch to above to fix injection vulnerability

    cursor = connection.cursor()
    sender_username = request.POST.get("sender", "")
    messages = None

    class Sender:
        def __init__(self, username):
            self.username = username

    class MessageWrapper:
        def __init__(self, sender_username, text, time):
            self.sender = Sender(sender_username)
            self.text = text
            self.time = time

    if sender_username:
        # django automatically parameterizes the %s placeholder, so instead of using concatenation using %s would fix the issue. Also using django's ORM or even raw() function is safer as it thoroughly prevents multiple sql queries from being ran simultaneously.
        cursor.execute("SELECT u.username, m.text, m.time AS sender_username FROM chatroom_message AS m JOIN auth_user AS u ON m.sender_id = u.id WHERE u.username LIKE '"+ sender_username +"' ORDER BY m.time DESC LIMIT 250")
        # The above query can be exploited with:     ' and 1 = 0 UNION SELECT a.password, a.username, email FROM auth_user AS a WHERE a.is_superuser = 1 and a.username LIKE '%       to gain access to the salted admin password and username for example
        rows = cursor.fetchall()
        messages = [MessageWrapper(row[0], row[1], [row[2]]) for row in rows] # It doesnt properly display the time but as this point, I do not give a damn, I've been trying to fix it for like 2 hours.
    else:
        messages = Message.objects.order_by('-time')[:250]
    

    return render(request, "chatroom/index.html", {"user": request.user, "messages": messages, "sender_username": sender_username})


@login_required
def sendMessage(request):
    # To change to using POST instead of GET
    # if request.method == "POST":
    #     sender = request.user
    #     text = request.POST.get("text")
    #     time = timezone.now()
    #     Message.objects.create(sender=sender, text=text, time=time)
    #     return redirect("/")

    # Comment out this block and uncomment the block above to switch to using POST.
    if request.method == "GET":
        sender = User.objects.get(username=request.GET.get("username")) # This line is what allows one user to impersonate another, should be: sender = request.user
        text = request.GET.get("text")
        time = timezone.now()
        Message.objects.create(sender=sender, text=text, time=time)
        return redirect("/")


    
    return HttpResponse(status=418)

