from django.db import models
import models.base_model.BaseModel as m
from rest_framework.views import APIView
from rest_framework.response import Response
import models.trainer as mt

models = mt.get_models()

class ModelPredictionAPIView(APIView):
    def post(self, request, model_name):
        serializer = m.BaseModelProcessSerializer(data=request.data)
        if serializer.is_valid() and model_name in models:
            # Получение модели из фабрики
            model = models[model_name]
            # Обработка данных и прогнозирование с помощью модели
            result = model.process(serializer.validated_data['text'])
            return Response({"result": result})
        else:
            return Response(serializer.errors, status=400)

class ModelTrainerAPIView(APIView):
    def post(self, request, model_name):
        serializer = m.BaseModelSerializer(data=request.data)
        if serializer.is_valid() and model_name in models:
            # Получение модели из фабрики
            model = models[model_name]
            # Обработка данных и прогнозирование с помощью модели
            result = model.retrain(serializer.validated_data['text'], serializer.validated_data['label'])
            return Response({"result": result})
        else:
            return Response(serializer.errors, status=400)