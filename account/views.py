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
    message = ''
    messageStatus = False
    if request.method =='POST':
        password1 = request.POST.get('password1','')
        password2 = request.POST.get('password2','')
        client = GraphQLClient('http://0.0.0.0:8000/graphql/')
        query = """
           mutation PasswordReset($password1: String!, $password2:String!, $token:String!){
             passwordReset(newPassword1: $password1, newPassword2: $password2, token: $token) {
               errors
               success
             }
           }
        """        
        variables = {'token': token, 'password1':password1, 'password2':password2}
        result = client.execute(query, variables)
        result_json = json.loads(result)
        if result_json['data']['passwordReset']['success']:
           message = "Your password has been set."
           messageStatus = True
        elif result_json['data']['passwordReset']['errors']:
            if 'nonFieldErrors' in result_json['data']['passwordReset']['errors']:
                message = result_json['data']['passwordReset']['errors']['nonFieldErrors'][0]['message']
            elif 'newPassword2' in result_json['data']['passwordReset']['errors']:
                message = result_json['data']['passwordReset']['errors']['newPassword2'][0]['message']            
            else:
                message = "Something Went Wrong. Try Again!"
        else:
           message = "Link is expired!"
    context = {
       'messageStatus': messageStatus,
       'message': message,
       'token': token,
    }
    template = loader.get_template('account/password_reset.html')
    return HttpResponse(template.render(context, request))

