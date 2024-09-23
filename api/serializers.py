from api.exceptions import AtLeastOneAssetRequiredError, CryptocurrencyNotFoundError, MissingAssetQuantityError
from portfolio.models import Asset, Cryptocurrency, Transaction
from rest_framework import serializers

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
    
    def validate(self, data):
        if not data.get('received_asset') and not data.get('transacted_asset'):
            raise AtLeastOneAssetRequiredError()
        
        if data.get('received_asset') and not data.get('received_quantity'):
            raise MissingAssetQuantityError('received_asset')

        if data.get('transacted_asset') and not data.get('transacted_quantity'):
            raise MissingAssetQuantityError('transacted_asset')

        return data
    
    def to_internal_value(self, data):
        received_asset = data.get('received_asset')
        transacted_asset = data.get('transacted_asset')

        if received_asset:
            try:
                cryptocurrency = Cryptocurrency.objects.get(ticker_symbol=received_asset)
            except Cryptocurrency.DoesNotExist:
                raise CryptocurrencyNotFoundError('received_asset', received_asset)

            asset, created = Asset.objects.get_or_create(cryptocurrency=cryptocurrency)
            data['received_asset'] = asset.pk
        
        if transacted_asset:
            try:
                cryptocurrency = Cryptocurrency.objects.get(ticker_symbol=transacted_asset)
            except Cryptocurrency.DoesNotExist:
                raise CryptocurrencyNotFoundError('transacted_asset', transacted_asset)

            asset, created = Asset.objects.get_or_create(cryptocurrency=cryptocurrency)
            data['transacted_asset'] = asset.pk
        
        return super().to_internal_value(data)
    
    def to_representation(self, transaction):
        representation = super().to_representation(transaction)
        
        if transaction.received_asset:
            representation['received_asset'] = transaction.received_asset.cryptocurrency.ticker_symbol
        
        if transaction.transacted_asset:
            representation['transacted_asset'] = transaction.transacted_asset.cryptocurrency.ticker_symbol
        
        return representation
