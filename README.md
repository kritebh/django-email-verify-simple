## Email Verification in Django

In this project I have shown how to verify email after the registration of a user.

But I don't like the implementation in this project, I will update the repo or create a new on regarding the same.

- I have generated UUID and store in the database and then filter out same UUID from mail for verification which is not reliable.

- I want automatically expire that token and filter out user by their username not by UUID

### Here are the screenshot of Project

> Login Page

!["Login Page"](log_in.png)

> Email Sent

![](email_sent.png)

>Inbox

![](email.png)

