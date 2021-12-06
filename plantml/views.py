from django.db import models
from django.http import HttpResponse, HttpResponseNotFound, response
from django.shortcuts import render
from .models import Message
from django.views.generic import TemplateView, FormView, View, ListView, DetailView, CreateView
from .forms import SearchForm, UploadForm, MessageForm, SubscribeForm
from django.db.models import Q
import tensorflow as tf
import numpy as np
from PIL import Image
import random

from .models import Message, Disease, TeamMember, Review, Subscriber

# Create your views here.

class HomePageView(View):
    
    def get(self, request):
        form = MessageForm()
        subscribe = SubscribeForm()
        search_form = SearchForm(request.GET)
        if search_form.is_valid() and request.GET.get('keyWord') != None:
            query = request.GET.get('keyWord')
            lookups= Q(plant_name__icontains=query)|Q(disease_name__icontains=query)
            
            result = Disease.objects.filter(lookups)[:12]

            return render(request, 'list_diseases.html', {'object_list' : result, 'form' : search_form})

        
        team = TeamMember.objects.all()
        return render(request, 'index.html', {'form': form, 
                                              'subscribe_form' : subscribe, 
                                              'search_form' : search_form,
                                              'team' : team})
    
    def post(self, request):
        form = MessageForm(request.POST)
        subscribe_form = SubscribeForm(request.POST)
        if form.is_valid() and request.method == 'POST':
            # process the data in form.cleaned_data as required
            # redirect to a new URL:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            message = request.POST.get('message')

            msg = Message(name = name, email = email, phone = phone, msg = message)
            msg.save()

            return render(request, 'confirmation.html', {"confirm" : "Your message has been sent"})

        elif subscribe_form.is_valid() and request.method == 'POST':
            email = request.POST.get('email')

            subscribe = Subscriber(username=email+'.aifarm',email=email)
            subscribe.save()

            return render(request, 'confirmation.html', {"confirm" : "Thanks For Subscribe"})


class DiseaseInfoView(ListView):
    template_name = 'info.html'
    model = Disease
    context_object_name = 'object_list'

    def get_queryset(self):
        return Disease.objects.first()


class DiseaseDetailView(DetailView):
    model = Disease
    template_name = 'info.html'
    context_object_name = 'object_list'

class AllDiseaseView(ListView, FormView):
    template_name = 'list_diseases.html'
    model = Disease
    context_object_name = 'object_list'
    form_class = SearchForm

    def post(self, request):
        search_form = SearchForm(request.POST)     
        if search_form.is_valid() and request.POST.get('keyWord') != None:
            query = request.POST.get('keyWord')
            lookups= Q(plant_name__icontains=query)|Q(disease_name__icontains=query)
            
            result = Disease.objects.filter(lookups)[:12]

            return render(request, 'list_diseases.html', {'object_list' : result, 'form' : search_form})


    def get_queryset(self):
        return Disease.objects.all()[:12]
    

class PredicPageView(TemplateView):
    template_name = 'info.html'
    model = Disease
    context_object_name = 'object_list'

    def get(self, request, disease):
        plant_name, *disease_name= disease.split()
        disease_name = ' '.join(disease_name)

        result = Disease.objects.filter(plant_name=plant_name,disease_name=disease_name).first()

        return render(request, self.template_name, {'object_list' : result})


class PredictionView(View):

    MODEL = tf.keras.models.load_model('/home/shafayat/Desktop/PlantML/model/plant_model_save.h5')

    CLASS_NAMES = ['Pepper Baterial Spot',
                    'Pepper Healthy',
                    'Potato Early Blight',
                    'Potato Late Blight',
                    'Potato Healthy',
                    'Tomato Bacterial Spot',
                    'Tomato Early Blight',
                    'Tomato Late Blight',
                    'Tomato Leaf Mold',
                    'Tomato Septoria Leaf Spot',
                    'Tomato Two-Spotted Spider Mite',
                    'Tomato Target Spot',
                    'Tomato Yellow Leaf Curl Virus',
                    'Tomato Mosaic Virus',
                    'Tomato Healthy']

    def get(self, request):
        form = UploadForm()
        return render(request, 'upload.html', {'form': form})
    
    def post(self, request):
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # redirect to a new URL:
            image = request.FILES['uploaded_file']
            opened_img = Image.open(image.file)
            resized_img = (opened_img.resize((256,256))).convert('RGB')
            np_image = np.array(resized_img)
            image_batch = np.expand_dims(np_image, 0)

            predictions = self.MODEL.predict(image_batch)
            disease = self.CLASS_NAMES[np.argmax(predictions[0])]
            plant_name, *predicted_class = disease.split()
            predicted_class = " ".join(predicted_class)
            confidence = np.max(predictions[0]) * 100
            
            return render(request, 'predict.html', {
                'plant_name': plant_name,
                'disease_name': predicted_class,
                'confidence': round(float(confidence), 2),
                'disease': disease
            })

class ReviewListView(ListView, FormView):
    model = Review
    template_name = "review_list.html"
    form_class = SearchForm

    def post(self, request):
        search_form = SearchForm(request.POST)     
        if search_form.is_valid() and request.POST.get('keyWord') != None:
            query = request.POST.get('keyWord')
            lookups= Q(plant_name__icontains=query)|Q(disease_name__icontains=query)
            
            result = Disease.objects.filter(lookups)[:12]

            return render(request, 'list_diseases.html', {'object_list' : result, 'form' : search_form})

    def get_queryset(self):
        return Review.objects.all().order_by('-review_dt')[:12]

class ReviewCreateView(CreateView):
    model = Review
    template_name = "review.html"
    fields = ['name', 'email', 'comment']
    success_url = '/review-list'






