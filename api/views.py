from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .serializers import *
from.models import Wallet

class SignUpView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        Wallet.create_wallet_for_user(user)

class SignInView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id})

class Wallet(generics.RetrieveAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAuthenticated]

class Deposit(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        wallet = Wallet.objects.get(user=self.request.user)
        amount = serializer.validated_data['amount']
        wallet.balance += amount
        wallet.save()
        serializer.save(wallet=wallet, transaction_type='deposit')

class Withdraw(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self,serializer):
        wallet = Wallet.objects.get(user=self.request.user)
        amount = serializer.validated_data['amount']
        if amount > wallet.balance:
            raise serializers.ValidationError("Insufficient funds.")
        else:
            wallet.balance -= amount
            wallet.save()
            serializer.save(wallet=wallet, transaction_type='withdrawal')
