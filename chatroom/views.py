from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Message
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Create your views here.

@login_required
def index(request):
    messages = Message.objects.order_by('-time')[:250] # prevent the page from rendering like a bazillion messages
    return render(request, "chatroom/index.html", {"user": request.user, "messages": messages})

@login_required
def sendMessage(request):
    # Use GET requet here to allow for easy broken access control hehe (impersonation of other users)
    if request.method == "GET":
        sender = User.objects.get(username=request.GET.get("username")) # This line is the most critical and is the thing which allows one user to impersonate another
        text = request.GET.get("text")
        time = timezone.now()
        Message.objects.create(sender=sender, text=text, time=time)


    # Correct code here
    # if request.method == "POST":
    #     sender = request.user
    #     text = request.POST.get("text")
    #     time = timezone.now()
    #     Message.objects.create(sender=sender, text=text, time=time)

        return redirect("/")
    return HttpResponse(status=204)