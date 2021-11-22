from django.db import models
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.utils.translation import templatize
from django.views.generic import TemplateView, FormView, View, ListView, DetailView
from .forms import UploadForm
import tensorflow as tf
import numpy as np
from PIL import Image

from .models import Message, Disease, TeamMember, Review, Subscriber

# Create your views here.


class HomePageView(TemplateView):
    template_name = 'index.html'
        

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

    

class AllDiseaseView(ListView):
    template_name = 'list_diseases.html'
    model = Disease
    context_object_name = 'object_list'

    def get_queryset(self):
        return Disease.objects.all()


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






