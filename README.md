# cyberserc_project_25
A small webapp created with multiple easily exploitable vulnerabilities.

## Specification
Create a webapp which contains at least 5 different flaws from the OWASP Top 10 list. (In my case I used the [2017 Top 10 list](https://raw.githubusercontent.com/OWASP/Top10/master/2017/OWASP%20Top%2010-2017%20(en).pdf))

### I will use the 2017 list which is as follows:
A1:2017 - Injection

A2:2017 - Broken Authentication 

A3:2017 - Sensitive Data Exposure

A4:2017 - XML External Entities (XXE)

A5:2017 - Broken Access Control

A6:2017 - Security Misconfiguration

A7:2017 - Cross-Site Scripting (XSS)

A8:2017 - Insecure Deserialization

A9:2017 - Using Components with Known Vulnerabilities

A10:2017 - Insufficient Logging & Monitoring

CSRF can also be used as a vulnerability even though it's not listed.

The application should have fixes to all the flaws included which are provided through commented code.

The code should (almost) always also contain the fix of the flaw. The fix should be commented out. Do not use git branches or versions for fixes. Just provide the commented fixes and the flaws in one version.

In addition, you should add screenshots for each flaw demonstrating the effect of the flaw before and after the fix. Typically, the screenshots should be of your browser. Make sure that the screenshots do not contain any sensitive information. You can have multiple screenshots demonstrating the effect. Store them in a screenshots folder of your repository and name them flaw-1-before-1.png, flaw-1-after-1.png, and so on.

## Project Setup
Required for setup of this project are [Python 3](https://www.python.org/downloads/) and [Django](https://pypi.org/project/Django/)

```python
python manage.py runserver
```

Users that are added at the beginning are as follows:
Username : Password
```
user1 : user1
user2 : user2
```

## Flaws
### A1:2017 - Injection
### A2:2017 - Broken Authentication
[Uses](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/baseproject/settings.py#L77) a [custom session engine](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/baseproject/simplesession.py)
which generates session-id's very predictably which means that by bruteforcing session-id's we can skip authentication.

This [script](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/baseproject/session_hijack/sessionhijack.py) can be used to demonstrate session hijacking in action with this site. It outputs the HTML data accesssible by the user with that session id. Thus an attacker can for example read all of the messages in the chatroom. Screenshots for [before](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/baseproject/screenshots/sessionhijacking-before) and [after](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/main/baseproject/screenshots/sessionhijacking-after) as well as the [fix](https://github.com/Kivi-Vuorilehto/cyberserc_project_25/blob/103413503cc3a1e8c5cbc258cb30c6dc113f635c/baseproject/settings.py#L77) can be found at those hyperlinks.


### A3:2017 - Sensitive Data Exposure
Using HTTP to transport unencrypted traffic. Additionally using GET requests to transport added messages which makes interception even easier (though browser history even).
(Attach wireshark screenshot here and get traffic from cookie inspect element)
To fix this you need to switch to HTTPS hehe not so easy

### A5:2017 - Broken Access Control
When sending a message, the system only checks if the sender is logged in, not whether the sender given in the input is actually the sender, and thus users can impersonate each other in the chatroom.
(Two screenshots, one shows the username and address bar paste, the other the effects)

### A7:2017 - Cross-Site Scripting (XSS)
Straight <script> blocks can be sent through the textbox and they are marked as safe as to allow for easy XSS vulnerabilities.
(Just show paste in box then alert effect on next)

