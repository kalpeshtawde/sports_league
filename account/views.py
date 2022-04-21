import json
from graphqlclient import GraphQLClient

from django.contrib.auth import views as auth_views
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.template import loader

from .forms import LoginForm, RegisterForm


class LoginView(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'


class RegisterView(generic.CreateView):
    form_class = RegisterForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('login')


def activate(request, token):
    client = GraphQLClient('http://0.0.0.0:8000/graphql/')
    query = """
        mutation VerifyAccount($input: String!){
          verifyAccount(token: $input) {
            errors
            success
          }
        }
    """
    variables = {'input': token}
    result = client.execute(query, variables)
    result_json = json.loads(result)
    if result_json['data']['verifyAccount']['success']:
        message = "Congratulation! Your account has been activated"
    else:
        message = "Activation link is expired. Please use app to resend activation link!"
    context = {
        'message': message,
    }
    template = loader.get_template('account/activate.html')
    return HttpResponse(template.render(context, request))


def password_reset(request, token):
    #client = GraphQLClient('http://0.0.0.0:8000/graphql/')
    #query = """
    #    mutation VerifyAccount($input: String!){
    #      verifyAccount(token: $input) {
    #        errors
    #        success
    #      }
    #    }
    #"""
    #variables = {'input': token}
    #result = client.execute(query, variables)
    #result_json = json.loads(result)
    #if result_json['data']['verifyAccount']['success']:
    #    message = "Congratulation! Your account has been activated"
    #else:
    #    message = "Activation link is expired. Please use app to resend activation link!"
    #context = {
    #    'message': message,
    #}
    context = {}
    template = loader.get_template('account/password_reset.html')
    return HttpResponse(template.render(context, request))
