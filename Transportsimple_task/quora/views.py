from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash 
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages 
from .forms import SignUpForm, EditProfileForm, QuestionForm, AnswerForm
from django.urls import reverse
from .models import Question, Answer, Liked
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render,HttpResponseRedirect

# Create your views here.

# Create your views here.
def home(request):
    quest_list = Question.objects.all()[:15]
    context = {'quest_list': quest_list}
    return render(request, 'home.html', context)


def login_user (request):
	if request.method == 'POST': #if someone fills out form , Post it 
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:# if user exist
			login(request, user)
			messages.success(request,('Youre logged in'))
			return redirect('home') #routes to 'home' on successful login  
		else:
			messages.success(request,('Error logging in'))
			return redirect('login') #re routes to login page upon unsucessful login
	else:
		return render(request, 'login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request,('Youre now logged out'))
	return redirect('home')

def register_user(request):
	if request.method =='POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request,user)
			messages.success(request, ('Youre now registered'))
			return redirect('home')
	else: 
		form = SignUpForm() 

	context = {'form': form}
	return render(request, 'register.html', context)

def edit_profile(request):
	if request.method =='POST':
		form = EditProfileForm(request.POST, instance= request.user)
		if form.is_valid():
			form.save()
			messages.success(request, ('You have edited your profile'))
			return redirect('home')
	else: 		#passes in user information 
		form = EditProfileForm(instance= request.user) 

	context = {'form': form}
	return render(request, 'edit_profile.html', context)
	#return render(request, 'edit_profile.html',{})



def change_password(request):
	if request.method =='POST':
		form = PasswordChangeForm(data=request.POST, user= request.user)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, ('You have edited your password'))
			return redirect('home')
	else: 		#passes in user information 
		form = PasswordChangeForm(user= request.user) 

	context = {'form': form}
	return render(request, 'change_password.html', context)

def create_question(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = QuestionForm(request.POST)
            if form.is_valid():
                question = form.save(commit=False)
                question.author = request.user
                question.save()
                return HttpResponseRedirect(reverse('question_detail', args=[question.pk]))
        else:
            form = QuestionForm()

        return render(request, 'create_question.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse('account:login'))




def like_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    liked, created = Liked.objects.get_or_create(answer=answer, user=request.user)
    if not created:
        liked.delete()
    return HttpResponseRedirect(reverse('question_detail', args=[answer.question.pk]))

def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = question.answer_set.all()
    liked_answers = request.user.answer_likes.values_list('answer', flat=True)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            my_answer = form.save(commit=False)
           
            my_answer.question = question
            my_answer.author = request.user
           
            my_answer.save()
            return redirect('question_detail', pk=question.pk)
    else:
        form = AnswerForm()
        context = {
        'question': question,
        'answers': answers,
        'liked_answers': liked_answers,
        'form': form, }
    return render(request, 'question_detail.html', context)