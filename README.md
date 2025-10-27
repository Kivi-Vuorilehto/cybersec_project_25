# Cybersecurity Base Project I
A small web application intentionally created with multiple, easily exploitable vulnerabilities for coursework.

## Specification
Create a webapp which contains at least 5 different flaws from the OWASP Top 10 list. (In my case I used the [2017 Top 10 list](https://raw.githubusercontent.com/OWASP/Top10/master/2017/OWASP%20Top%2010-2017%20(en).pdf))

The code contains a fix to all other listed vulnerabilities except sensitive data exposure. The fixes and screenshots of the vulnerabilities are linked in the expanded sections below.

## Project Setup
Required for setup of this project are [Python 3](https://www.python.org/downloads/) and [Django](https://pypi.org/project/Django/)

If you wish to use the project using HTTPS ([read A3](https://github.com/Kivi-Vuorilehto/cybersec_project_25?tab=readme-ov-file#a32017---sensitive-data-exposure)), you will also need [django-extensions](https://pypi.org/project/django-extensions/), [Werkzeug](https://pypi.org/project/Werkzeug/) and [pyOpenSSL](https://pypi.org/project/pyOpenSSL/)

To start the server simply run:

```python
python manage.py runserver
```

The website is hosted at localhost:8000 by default.

Existing users with the format "username : password" are:

```
user1 : user1
user2 : user2
```

There is also an admin account added by default if you wish to try the SQL injection exploit provided:
```
admin : admin
```

## Flaws
### A1:2017 - Injection
Injection is the process of supplying hostile data to any kind of interpreter. This can result in data breaches, data loss or denial of access.

In this case, the filter feature which allows a user to filter shown messages in the chatroom to a single user is vulnerable to injection. This is because the data sent through the filter field is directly concatenated to an SQL query without parameterization. 

The flaw originates from [L41 in chatroom/views.py](https://github.com/Kivi-Vuorilehto/cybersec_project_25/blob/8d7cd041dc53588b0316648e0295e4debf08c23b/chatroom/views.py#L41), where an execute() is run with improper protections.

As an example, the following data can be used as the filter in order to retrieve the admin username and password hash:
```
' and 1 = 0 UNION SELECT a.password, a.username, email FROM auth_user AS a WHERE a.is_superuser = 1 and a.username LIKE '%
```

This being shown in action can be found the screenshots folder, under: 
[injection-before screenshot](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/screenshots/injection-before.png).

To fix this flaw, follwing the instructions of [L14 in chatroom/views.py](https://github.com/Kivi-Vuorilehto/cybersec_project_25/blob/8d7cd041dc53588b0316648e0295e4debf08c23b/chatroom/views.py#L14) would suffice. The fix consists of utilizing Django's Object Relational Mapping (ORM) to interact with the database and not insecurely concatenating the data which means that the data is parameterized. With the current newest Django version there is no vulnerability identified in the ORM operations used.

The same exploit attempted results in this after the fix: 
[injection-after screenshot](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/screenshots/injection-after.png).


### A2:2017 - Broken Authentication
Broken authentication refers to cases where authentication is not securely implemented and allows an attacker to gain unauthorized access. This can result in data breaches, data loss, denial of access, identity theft or even complete system takeover. 

In this case, the app is vulnerable due to a [custom session engine](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/baseproject/simplesession.py). It assigns session ids in a predictable manner in the following format:
```
session-0, session-1, session-2 ...
```
This allows an attacker to brute force session-ids to find an unexpired session which can be used to access the chatroom with a user's account. 

Additionally the app does not employ Multi-Factor Authentication (MFA). This also leaves it vulnerable to credential stuffing. The fix for this is out of scope for the project, but could be implemented through the use of an authentication app, email or sms. Additionally rate limiting could be introduced to make brute forcing accounts harder.

This [script](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/session_hijack/sessionhijack.py) can be used to demonstrate session hijacking in action with this site. It outputs the HTML data accesssible by the user with that session id. 

This being shown in action can be found in the screenshots folder under:
[sessionhijacking-before](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/screenshots/sessionhijacking-before.png).

To fix this flaw, one can simply remove [L78 in baseproject/settings.py](https://github.com/Kivi-Vuorilehto/cybersec_project_25/blob/7f41920ff9556831c987ea9a81fb4e43402ae17c/baseproject/settings.py#L78) 
which specifies the use of the custom session engine, and regenerate currently valid session-ids. This will make the app utilize Django's default session engine which generates secure session-ids which are not brute forceable in any worthwhile timeframe.

Effect of the same exploit attempted after the fix:
[sessionhijacking-after](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/screenshots/sessionhijacking-after.png).


### A3:2017 - Sensitive Data Exposure
Sensitive data exposure refers to cases where transmitted sensitive information is inadequately protected and allows an attacker to gain access to it. 

In this case, the app is vulnerable due to all traffic being transmitted with HTTP. This includes usernames and passwords, as well as the messages sent in the chatroom.

A screenshot called [insecure-data-transmission-before](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/screenshots/insecure-data-transmission-before.png) highlights this.

To solve this issue, we would have to switch to using HTTPS instead of HTTP. In this case I don't believe that there is another solution. 

The fix is having a certificate authority provide you with an SSL certificate, which we can use to enable HTTPS transmission for all data. To simulate this in development, I have generated my own local certificate which I have **not** shared in this repo. If you want to simulate a HTTPS connection yourself, you can follow the instructions found on this [answer](https://stackoverflow.com/a/77708864) to generate your own.

This fix would not work as is in deployment, however the same principle applies and the steps to enable it in deployment in the code are on 
[L41 in baseproject/settings.py](https://github.com/Kivi-Vuorilehto/cybersec_project_25/blob/17c0d5ab8512f1f2b4076c4513dbef274202a006/baseproject/settings.py#L41).

Afterwards the server can be run using a locally generated SSL certificate using:

```
python manage.py runserver_plus --cert-file certs/name.pem --key-file certs/name-key.pem
```

The effect of capturing the packets when using HTTPS can be seen in the screenshot [insecure-data-transmission-after](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/screenshots/insecure-data-transmission-after.png).


There is another flaw in the project in terms of sensitive data exposure. It sends the message content a user wants to post [using a GET request](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/96ae46a3b36d5f8fb5ad168951aa7a114be64308/chatroom/templates/chatroom/index.html#L40). 
This means that the data transmitted can be captured from the URL without the need to intercept the packets in a network. 
A fix is provided for this in 
[chatroom/views.py L52](https://github.com/Kivi-Vuorilehto/cybersec_project_25/blob/8d7cd041dc53588b0316648e0295e4debf08c23b/chatroom/views.py#L52) and
[chatroom/templates/chatroom/index.html L42](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/96ae46a3b36d5f8fb5ad168951aa7a114be64308/chatroom/templates/chatroom/index.html#L42).

While communications between persons like the conversation in this chatroom is not required to be secure by default, I believe that it should ideally be as secure as possible.


### A5:2017 - Broken Access Control
Broken access control refers to a vulnerability where an attacker can perform actions or access data that they should not be able to with their current privileges. 

In this case, when posting a new message to the chatroom, the app takes the username of the sender from the data submitted with the GET (or POST) request. This means that by submitting a custom request, one logged in user can impersonate another and send messages to the room in their name.
This is possible due to [chatroom/views.py L62](https://github.com/Kivi-Vuorilehto/cybersec_project_25/blob/8d7cd041dc53588b0316648e0295e4debf08c23b/chatroom/views.py#L62), and the field in [chatroom/templates/chatroom/index.html L44](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/96ae46a3b36d5f8fb5ad168951aa7a114be64308/chatroom/templates/chatroom/index.html#L44).

The exploit can be seen in action in screenshots called [broken-access_control-before-exploit](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/screenshots/broken-access_control-before-exploit.png) and [broken-access-control-before-effect](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/screenshots/broken-access-control-before-effect.png).

To fix this flaw, follow the instructions commented in [chatroom/views.py L62](https://github.com/Kivi-Vuorilehto/cybersec_project_25/blob/8d7cd041dc53588b0316648e0295e4debf08c23b/chatroom/views.py#L62) and [chatroom/templates/chatroom/index.html L45](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/96ae46a3b36d5f8fb5ad168951aa7a114be64308/chatroom/templates/chatroom/index.html#L45).

The previous exploit would simply now send that message content in the logged in user's name.


### A7:2017 - Cross-Site Scripting (XSS)
Cross-site scripting refers to a vulnerability where an attacker can inject malicious scripts somewhere where it will be executed by another user.

In this case, the processing to data sent through the text area is flawed, and does not sanitize the input. This means that Javascript can be sent through it, which is stored in the database and loaded on every time a user visits the chatroom.

This is made possible due to the |safe filter on the textarea in [chatroom/templates/chatroom/index.html L28](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/96ae46a3b36d5f8fb5ad168951aa7a114be64308/chatroom/templates/chatroom/index.html#L28). This designates the field as exempt from the Django's autoescaping which would prevent this.

The exploit in action can be seen in the screenshots [xss-before-exploit](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/screenshots/xss-before-exploit.png) and [xss-before-effect](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/screenshots/xss-before-effect.png).

To fix this vulnerability follow the commented instruction in [chatroom/templates/chatroom/index.html L29](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/96ae46a3b36d5f8fb5ad168951aa7a114be64308/chatroom/templates/chatroom/index.html#L29).

The effect of the exploit after the fix can be seen in [xss-after](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/screenshots/xss-after.png).