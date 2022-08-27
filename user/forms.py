from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı")
    password = forms.CharField(label="Parola",widget=forms.PasswordInput)
    

class RegisterForm(forms.Form):
    name = forms.CharField(label="İsim")
    surname = forms.CharField(label="Soyisim")
    username = forms.CharField(max_length=50,label="Kullanıcı Adı")
    email = forms.EmailField(label="Email adresi")
    password = forms.CharField(max_length=20,label="Parola",widget= forms.PasswordInput)
    confirm = forms.CharField(max_length=20,label="Parola Doğrulama",widget=forms.PasswordInput)
    # https://docs.djangoproject.com/en/4.1/ref/forms/api/ django forms api dökümanı
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")
        first_name = self.cleaned_data.get("name")
        last_name = self.cleaned_data.get("surname")
        email = self.cleaned_data.get("email")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolanız Uyuşmuyor...")
        values = {
            "username":username,
            "password":password,
            "first_name":first_name,
            "last_name":last_name,
            "email":email,
        }
        return values

    