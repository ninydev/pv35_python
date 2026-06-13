# Django GraphQL Project

This project demonstrates how to integrate GraphQL into a Django application using `graphene-django`, as well as setting up Server-Sent Events (SSE) for real-time notifications.

## How to add GraphQL to Django

1.  **Install the library:**
    ```bash
    pip install graphene-django
    ```

2.  **Add to `INSTALLED_APPS`:**
    In your `settings.py`, add `graphene_django` to the `INSTALLED_APPS` list:
    ```python
    INSTALLED_APPS = [
        # ...
        'graphene_django',
    ]
    ```

3.  **Define the Schema:**
    Create a file named `schema.py` in your main project folder (where `settings.py` is). In this file, you define the types (based on your models) and the queries you can make. See `djangopv35_v1/schema.py` for an example of querying the `News` model.

4.  **Configure Graphene in `settings.py`:**
    Tell Graphene where to find your schema by adding this to `settings.py`:
    ```python
    GRAPHENE = {
        'SCHEMA': 'djangopv35_v1.schema.schema' # Path to your schema variable
    }
    ```

5.  **Add the GraphQL Endpoint:**
    In your main `urls.py`, import `GraphQLView` and add a path for it. Enable `graphiql=True` to get a built-in interface for testing queries in the browser.
    ```python
    from graphene_django.views import GraphQLView
    from django.views.decorators.csrf import csrf_exempt

    urlpatterns = [
        # ...
        path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    ]
    ```

## Testing GraphQL

1.  Run the server: `python manage.py runserver`
2.  Open your browser and navigate to `http://127.0.0.1:8000/graphql`
3.  You will see the GraphiQL interface (the "player").

### Example Query

To fetch all news articles, you can run the following query in the GraphiQL interface:

```graphql
query {
  allNews {
    id
    title
    content
    createdAt
    createdBy {
      username
    }
    coverImage
  }
}
```

To fetch a specific news article by ID:

```graphql
query {
  newsById(id: "1") {
    title
    content
  }
}
```

## How to add Server-Sent Events (SSE)

1. **Install required packages:**
   ```bash
   pip install django-eventstream channels daphne
   ```

2. **Update `settings.py`:**
   Add the following to `INSTALLED_APPS`:
   ```python
   INSTALLED_APPS = [
       'daphne', # Must be at the top or above django.contrib.staticfiles
       # ...
       'django_eventstream',
   ]
   ```
   Configure the ASGI application:
   ```python
   ASGI_APPLICATION = 'djangopv35_v1.asgi.application'
   ```

3. **Configure ASGI (`asgi.py`):**
   When using modern versions of Django (3.0+) and Daphne, `django-eventstream` works seamlessly with standard Django URL routing. You can leave your `asgi.py` as default:
   ```python
   import os
   from django.core.asgi import get_asgi_application

   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangopv35_v1.settings')

   application = get_asgi_application()
   ```

4. **Update `urls.py`:**
   Add the endpoint for the EventStream directly to your main `urls.py`:
   ```python
   import django_eventstream

   urlpatterns = [
       # ...
       path('events/', include(django_eventstream.urls), {'channels': ['news-feed']}),
   ]
   ```

5. **Send Events (Signals):**
   Use Django signals to send an event when a model is created. For example, in `news/signals.py`:
   ```python
   from django.db.models.signals import post_save
   from django.dispatch import receiver
   from django_eventstream import send_event
   from .models import News

   @receiver(post_save, sender=News)
   def send_news_update(sender, instance, created, **kwargs):
       if created:
           send_event('news-feed', 'message', {'text': f'Нова новина: {instance.title}'})
   ```

6. **Listen for Events on the Frontend (JavaScript):**
   In your HTML template, use the built-in `EventSource` API:
   ```javascript
   var eventSource = new EventSource('/events/');

   eventSource.onmessage = function(event) {
       var data = JSON.parse(event.data);
       console.log("Новое событие:", data.text);
       // Отобразите уведомление пользователю
   };
   ```

To test SSE, run your server using Daphne (`python manage.py runserver`), open the news list page, and create a new news article in another tab or via the admin panel. You will receive a real-time notification on the opened page without refreshing it!
