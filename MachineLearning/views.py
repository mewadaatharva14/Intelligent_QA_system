from django.shortcuts import render,redirect
from .forms import InputForm
from .qa_python import import_pdf, text_splitter, load_model, get_answer
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import login,logout

# Load model once
# tokenizer, model = load_model()

def greeting(request):
    answer = None

    if request.method == "POST":
        form = InputForm(request.POST, request.FILES)
        if form.is_valid():
            question = form.cleaned_data.get('question')
            pdf_file = request.FILES.get('pdf_reader')

            if not pdf_file:
                answer = "Please upload a PDF file."
            else:
                text = import_pdf(pdf_file)
                chunks = text_splitter(text)
                tokenizer, model = load_model()
                answer = get_answer(question, chunks, tokenizer, model)
    else:
        form = InputForm()

    return render(request, 'index2.html', {'form': form, 'answer': answer})

def index(request):
    return render(request,'index.html')

def login_view(request):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect("home")  # or any success URL
    return render(request, "login.html", {"form": form})

def signup_view(request):
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)  # auto login after signup
        return redirect("home")
    return render(request, "signup.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("home")