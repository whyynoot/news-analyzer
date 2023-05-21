from rest_framework import serializers

class BaseModel:
    def retrain(text, label):
        # Existing model training based on text and label
        pass
    
    def train(dataset):
        # Traing model from big dataset
        pass

    def process(text):
        # Expected result
        pass

class BaseModelSerializer(serializers.Serializer):
    text = serializers.CharField()
    label = serializers.ChoiceField(choices=['neutral', 'attack'])

    def update(self, validated_data):
        text = validated_data['text']
        label = validated_data['label']
        result = BaseModel.retrain(text, label)
        return {'result': result}

class BaseModelProcessSerializer(serializers.Serializer):
    text = serializers.CharField()

    def create(self, validated_data):
        text = validated_data['text']
        result = BaseModel.process(text)
        return {'result': result}