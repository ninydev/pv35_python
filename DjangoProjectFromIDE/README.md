# Django GraphQL Project

This project demonstrates how to integrate GraphQL into a Django application using `graphene-django`.

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
