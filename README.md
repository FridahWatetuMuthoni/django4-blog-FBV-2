# Django Class based views

## How class based views handle pagination

We have to use the right page object that is passed to the template.
Django’s ListView generic view passes the page requested in a variable called page_obj.
We implement pagination in class based veiws like this:

```python

from django.views.generic import ListView

class PostLListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 4
    template_name = 'blog/post/list.html'
```

```HTML
{% extends 'blog/base.html' %}
<!--Title-->
{% block title%}My Blog {% endblock%}
<!--Content-->
{% block content %}
<h1>My Blog</h1>
<!---->
{% for post in posts %}
<h2><a href="{{post.get_absolute_url}}">{{post.title}}</a></h2>
<p class="date">Published {{post.publish}} by {{post.author}}</p>
<p>{{post.body|truncatewords:30|linebreaks}}</p>
{% endfor%} {% include './_pagination.html' with page=page_obj %} {% endblock%}

```

## Sending Emails

```python

from django.core.mail import send_mail

send_mail(
    'Django mail',
    'This email was sent with django'
    'youraccount@gmail.com',
    ['recepient@gmail.com'],
    fail_silently=False
)

```

The send_mail() function takes the subject, message, sender, and list of recipients as required arguments. By setting the optional argument fail_silently=False, we are telling it to raise an exception if the email cannot be sent. If the output you see is 1, then your email was successfully sent.

## Tags

```python
from django.db import models

#tags schema

#used for storing the tags
class Tag(models.Model):
    id = models.BigAutoField(unique=True, primary_key=True)
    name = models.CharField()
    slug = models.SlugField()

#used for storing related tagged objects
class TaggedItem(models.Model):
    id = models.BigAutoField(unique=True, primary_key=True)
    tag = models.ForeignKey(Tag, on_delete = models.CASCADE)
    content_type = models.ForeignKey(Model, on_delete = models.CASCADE)
    object_id = models.IntegerField()

```

130
