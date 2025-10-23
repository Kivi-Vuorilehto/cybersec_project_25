# Cybersecurity Base Project I
A small webapp created with multiple easily exploitable vulnerabilities.

## Specification
Create a webapp which contains at least 5 different flaws from the OWASP Top 10 list. (In my case I used the [2017 Top 10 list](https://raw.githubusercontent.com/OWASP/Top10/master/2017/OWASP%20Top%2010-2017%20(en).pdf))

The code contains a fix to all other listed vulnerabilities except sensitive data exposure. The fixes and screenshots of the vulnerabilities are linked in the expanded sections below.

## Project Setup
Required for setup of this project are [Python 3](https://www.python.org/downloads/) and [Django](https://pypi.org/project/Django/)

To run the project simply run:

```python
python manage.py runserver
```

The website is hosted at localhost:8000 by default.

Users that are added at the beginning are as follows:
Username : Password
```
user1 : user1
user2 : user2
```

## Flaws
### A1:2017 - Injection

As an example, with the filter ```' and 1 = 0 UNION SELECT a.password, a.username, email FROM auth_user AS a WHERE a.is_superuser = 1 and a.username LIKE '%``` we can retrieve the salted admin credentials. You could modify this to retrieve any data stored inside the database file. The results of this filter can be seen in the 
[injection-before screenshot](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/screenshots/injection-before.png). 
After implementing the [fix](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/4b0c7becc3cf44c299af844c57e89045d91e4bc8/chatroom/views.py#L24), the results of it without the vulnerability can be seen in the 
[injection-after screenshot](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/screenshots/injection-after.png).

### A2:2017 - Broken Authentication
[Uses](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/4b0c7becc3cf44c299af844c57e89045d91e4bc8/baseproject/settings.py#L77) a 
[custom session engine](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/baseproject/simplesession.py)
which generates session-id's very predictably which means that by bruteforcing session-id's we can skip authentication.

This [script](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/session_hijack/sessionhijack.py) can be used to demonstrate session hijacking in action with this site. It outputs the HTML data accesssible by the user with that session id. Thus an attacker can for example read all of the messages in the chatroom. Screenshots for 
[before](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/screenshots/sessionhijacking-before.png) and 
[after](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/screenshots/sessionhijacking-after.png) as well as the 
[fix](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/4b0c7becc3cf44c299af844c57e89045d91e4bc8/baseproject/settings.py#L76) can be found.


### A3:2017 - Sensitive Data Exposure
Using HTTP to transport unencrypted traffic. Additionally using GET requests to transport added messages which makes interception even easier (though browser history even).
A [screenshot](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/screenshots/insecure_data_transmission.png) highlighting this is provided.
To fix the fundamental issue one would have to switch to HTTPS which is not within the scope of this project. However, a fix is provided to using POST instead of GET in order to prevent the data being extremely easily accessible. It is in two parts, one in [views.py](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/4b0c7becc3cf44c299af844c57e89045d91e4bc8/chatroom/views.py#L63) and the other in 
[index.html](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/4b0c7becc3cf44c299af844c57e89045d91e4bc8/chatroom/templates/chatroom/index.html#L42).


### A5:2017 - Broken Access Control
When sending a message, the system only checks if the sender is logged in, not whether the sender given in the input is actually the sender, and thus users can impersonate each other in the chatroom. The vulnerability being exploited can be seen in the [setup](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/screenshots/broken-access_control-before-exploit.png) and [effect](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/screenshots/broken-access-control-before-effect.png) screenshots.
The fix to this can be found in [views.py](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/4b0c7becc3cf44c299af844c57e89045d91e4bc8/chatroom/views.py#L65) and additionally the insecure username field should be removed from [index.html](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/4b0c7becc3cf44c299af844c57e89045d91e4bc8/chatroom/templates/chatroom/index.html#L44).


### A7:2017 - Cross-Site Scripting (XSS)
The textarea is completely unsanitised and Javascript can be sent through it to any user who loads it. An [example](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/screenshots/xss-before-exploit.png) showcasing that and its effect 
[before](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/screenshots/xss-before-effect.png) and 
[after](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/screenshots/xss-after.png) fixing it are in screenshots.
The [fix](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/4b0c7becc3cf44c299af844c57e89045d91e4bc8/chatroom/templates/chatroom/index.html#L28) is on L28 of chatroom/templates/chatroom/index.html
