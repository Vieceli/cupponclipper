from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
#from django.core.mail.message import BadHeaderError

class CadastrarForm(forms.Form):
    nome_completo           = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'size':'30'}) )
    senha            = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'size':'12'}) )
    senha_verifica    = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'size':'12'}))
    email               = forms.EmailField(help_text="voce@dominio.com", widget=forms.TextInput(attrs={'size':'30'}))
    


    def clean(self):
        """
        Validate fields to make sure everything's as expected.
        - postalcode is in right format and actually exists
        - service actually exists
        """
        cd = self.cleaned_data

        if 'senha' in cd and 'senha_verifica' in cd:
            if self.cleaned_data['senha'] != self.cleaned_data['senha_verifica']:
                self._errors['senha'] = forms.util.ErrorList(["Senhas incompativeis!"])

        else:
            self._errors['senha'] = forms.util.ErrorList(["Confira sua senha"])

#      raise forms.ValidationError(_(u'Please enter and confirm your password'))


        return cd

class LoginForm(forms.Form):
    email               = forms.EmailField(help_text="voce@dominio.com", widget=forms.TextInput(attrs={'size':'25'}))
    senha            = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'size':'12'}) )

    def clean(self):
        # only do further checks if the rest was valid
        if self._errors: return
            
        from django.contrib.auth import login, authenticate
        user = authenticate(username=self.data['email'],
                                password=self.data['senha'])
        if user is not None:
            if user.is_active:
                self.user = user                    
            else:
                raise forms.ValidationError( 'A sua conta esta inativa por favor entre em contato.')
        else:
            raise forms.ValidationError( 'O usuario e/ou a senha nao sao validos')
