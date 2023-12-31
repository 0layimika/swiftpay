from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user
class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['user','balance']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
