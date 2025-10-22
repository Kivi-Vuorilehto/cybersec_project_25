# cyberserc_project_25
A small webapp created with multiple vulnerabilities

## Specification
Create a webapp which contains at least 5 different flaws from the OWASP Top 10 list.

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

https://raw.githubusercontent.com/OWASP/Top10/master/2017/OWASP%20Top%2010-2017%20(en).pdf

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
A1:2017 - Injection\
A2:2017 - Broken Authentication\
A3:2017 - Sensitive Data Exposure\
A5:2017 - Broken Access Control\
A7:2017 - Cross-Site Scripting (XSS)

