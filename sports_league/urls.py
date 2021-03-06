"""sports_league URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Homenf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from gql.schema import schema
from graphene_file_upload.django import FileUploadGraphQLView

from account.views import LoginView, RegisterView, activate, password_reset


GraphQLView.graphiql_template = "graphene_graphiql_explorer/graphiql.html"


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<token>', activate, name='activate'),
    path('password-reset/<token>', password_reset, name='password-reset'),
    #path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema)), name="graphiql"),
    path("graphql/", csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True, schema=schema)), name="graphiql"),
]
