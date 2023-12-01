from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Question , Answer

class EditProfileForm(UserChangeForm):
	
	password = forms.CharField(label="", widget=forms.TextInput(attrs={'type':'hidden'}))
	class Meta:
		model = User
		#excludes private information from User
		fields = ('username', 'first_name', 'last_name', 'email','password',)
		  



class SignUpForm(UserCreationForm):
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="First Name", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="Last Name", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control', 'placeholder':'User Name'}),
            'password1': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'}),
            'password2': forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirm Password'}),
        }

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

class QuestionForm(forms.ModelForm):
    question = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class':'form-floating form-control w-75 m-3 p-3','placeholder':'Add Your Question here Like "What" , "How" , "Where" , "Why" etc.'}),
        )


    class Meta:
        model = Question
        fields = ('question',)



class AnswerForm(forms.ModelForm):
    ans = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'rows': 4, 'cols': 40, 'class':'form-floating form-control w-50','placeholder':'Write Your Thought Here.'}),
        )


    class Meta:
        model = Answer
        fields =('ans',)

    def save(self, commit=True):
        answer = Answer(ans=self.cleaned_data['ans'])
        if commit:
            answer.save()
        return answer