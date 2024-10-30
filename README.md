# Simple Django Blog

1. Setup and activate the virtual environment
    
    ```shell
    # create environment
    python3 -m venv .venv --prompt=blog-venv

    # Activate environment
    source .venv/bin/activate
    ```

2. Install Django in virtual environment

    ```shell
    pip install Django
    ```

3. Create requirements file

    ```shell
    pip freeze > requirements.txt
    ```

4. Create a Django project

    ```shell
    django-admin startproject config .
    ```

5. Create the core Django app

    ```shell
    django-admin startapp core
    ```

6. Create the blog app

    ```shell
    django-admin startapp blog
    ```

## App Configuration

1. Register apps in the settings.py

    ```python
    INSTALLED_APPS = [
        # .....
        "core.apps.CoreConfig",
        "blog.apps.BlogConfig",
    ]
    ```

2. Create a `urls.py` file in the `core` app:

    ```python
    from django.urls import path

    app_name = "core"

    urlpatterns = []
    ```

3. Create a `urls.py` file in the `blog` app:

    ```python
    from django.urls import path

    app_name = "blog"

    urlpatterns = []
    ```

4. Add the url paths to the `config/urls.py` file:

    ```python
    from django.urls import include
    urlpatterns = [
        # ....
        path("", include("core.urls", namespace="core")),
        path("blog/", include("blog.urls", namespace="blog")),
    ]
    ```

## Model configuration

1. Create the User model in core app

    ```python
    from django.contrib.auth.models import AbstractUser

    class User(AbstractUser):
        pass
    ```

    in the settings.py file:

    ```python
    AUTH_USER_MODEL = "core.User"
    ```

    > **This configuration should be done before making or running any migrations**

2. Create Category model in the `blog/models.py` file:

    ```python
    class Category(models.Model):
        name = models.CharField(max_length=50)
    ```

3. Create the `Post` model in `blog/models.py` file:

    ```python
    from core.models import User


    class Post(models.Model):
        title = models.CharField(max_length=255)
        body = models.TextField()
        created_on = models.DateTimeField(auto_now_add=True)
        updated_on = models.DateTimeField(auto_now=True)
        categories = models.ManyToManyField("Category", related_name="posts")
        author = models.ForeignKey(User, on_delete=models.CASCADE)
    ```

4. Create the `Comment` model in the `blog/models.py` file:

    ```python
    class Comment(models.Model):
        body = models.TextField()
        created_on = models.DateTimeField(auto_now_add=True)
        post = models.ForeignKey("Post", on_delete=models.CASCADE)
        author = models.ForeignKey(User, on_delete=models.CASCADE)
    ```

5. Run migrations:

    ```shell 
    # Create migration files
    python manage.py makemigrations

    # Apply migrations
    python manage.py migrate
    ```

## Admin Site Configuration

1. Register the User model in core app:

    ```python 
    from django.contrib.auth.admin import UserAdmin
    from .models import User

    admin.site.register(User, UserAdmin)
    ```

2. Register the `Category`, `Post` and `Comment` models in the `blog` app:

    ```python
    from .models import Category, Post, Comment

    class CategoryAdmin(admin.ModelAdmin):
        pass

    class PostAdmin(admin.ModelAdmin):
        pass

    class CommentAdmin(admin.ModelAdmin):
        pass


    admin.site.register(Category, CategoryAdmin)
    admin.site.register(Post, PostAdmin)
    admin.site.register(Comment, CommentAdmin)
    ```

3. Create a superuser

    ```shell
    python manage.py createsuperuser
    ```

4. Add `__str__()`  to each of the models

## View Configuration

In the the `blog/views.py` create the following function-based views:
    - `blog_index()`
    - `blog_detail()`
    - `blog_category()`

1. Import `Post` and `Comment` models

    ```python
    from .models import Post, Comment
    ```

2. Create `blog_index()` view:

    ```python
    def blog_index(request):
        posts = Post.objects.all().order_by("-created_on")
        context = {
            "posts": posts,
        }
        return render(request, "blog/index.html", context)
    ```

3. Create `blog_category` view:

    ```python
    def blog_category(request, category):
        posts = Post.objects.filter(categories__name__contains=category)
        context = {
            "category": category,
            "posts": posts,
        }
        return render(request, "blog/category.html", context)
    ```

4. Create `blog_detail()` view:

    ```python
    def blog_detail(request, pk):
        post = Post.objects.get(pk=pk)
        comments = Comment.objects.filter(post=post)
        context = {
            "comments": comments,
            "post": post,
        }
        return render(request, "blog/detail.html", context)
    ```

## Template setup

1. Create the `templates/blog` directory inside `blog` app

2. Create the `index.html` template in `templates/blog` directory:

    ```
    {% block page_title %}
    <h2>Blog Posts</h2>
    {% endblock page_title %}

    {% block page_content %}
        {% block posts %}
            {% for post in posts %}
                <h3><a href="{% url 'blog_detail' post.pk %}">{{ post.title }}</a></h3>
                <small>
                    {{ post.created_on.date }} | Categories:
                    {% for category in post.categories.all %}
                        <a href="{% url 'blog_category' category.name %}">
                            {{ category.name }}
                        </a>
                    {% endfor %}
                </small>
                <p>{{ post.body | slice:":400" }}...</p>
            {% endfor %}
        {% endblock posts %}
    {% endblock page_content %}
    ```

3. Create the `category.html` template in the `blog/templates/blog` directory:

    ```
    {% extends "blog/index.html" %}

    {% block page_title %}
        <h2>{{ category }}</h2>
    {% endblock page_title %}
    ```

4. Create the `detail.html` template in `blog/templates/blog` directory:

    ```
    {% block page_title %}
        <h2>{{ post.title }}</h2>
    {% endblock page_title %}

    {% block page_content %}
        <small>
            {{ post.created_on.date }} | Categories:
            {% for category in post.categories.all %}
                <a href="{% url 'blog_category' category.name %}">
                    {{ category.name }}
                </a>
            {% endfor %}
        </small>
        <p>{{ post.body | linebreaks }}</p>
    {% endblock page_content %}
    ```

## Create URL routes

1. In the `blog/urls.py` file add the routes for the views:

    ```python
    from . import views

    urlpatterns = [
        path("", views.blog_index, name="blog_index"),
        path("post/<int:pk>/", views.blog_detail, name="blog_detail"),
        path("category/<category>", views.blog_category, name="blog_category"),
    ]
    ```