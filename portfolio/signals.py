from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from portfolio.models import Transaction

@receiver(pre_save, sender=Transaction)
def on_transaction_pre_save(sender, instance, **kwargs):
    transaction = instance

    if transaction.pk:
        original_transaction = sender.objects.get(pk=instance.pk)

        instance._original_transacted_asset = original_transaction.transacted_asset
        instance._original_received_asset = original_transaction.received_asset
        instance._original_transacted_quantity = original_transaction.transacted_quantity
        instance._original_received_quantity = original_transaction.received_quantity

@receiver(post_save, sender=Transaction)
def on_transaction_post_save(sender, instance, created, **kwargs):
    transaction = instance
    transacted_asset = transaction.transacted_asset
    received_asset = transaction.received_asset

    if not created:
        original_transacted_asset = transaction._original_transacted_asset
        original_received_asset = transaction._original_received_asset

        if original_transacted_asset != None:
            if transacted_asset != original_transacted_asset:
                original_transacted_asset.quantity += transaction._original_transacted_quantity
                transaction._original_transacted_asset.save()
            else:
                transacted_asset.quantity += transaction._original_transacted_quantity

        if original_received_asset != None:
            if received_asset != original_received_asset:
                original_received_asset.quantity -= transaction._original_received_quantity
                transaction._original_received_asset.save()
            else:
                received_asset.quantity -= transaction._original_received_quantity
        
    if transacted_asset:
        transacted_asset.quantity -= transaction.transacted_quantity
        transacted_asset.save()

    if received_asset:
        received_asset.quantity += transaction.received_quantity
        received_asset.save()

@receiver(post_delete, sender=Transaction)
def on_transaction_post_delete(sender, instance, **kwargs):
    transaction = instance
    transacted_asset = transaction.transacted_asset
    received_asset = transaction.received_asset

    if transacted_asset:
        transacted_asset.quantity += transaction.transacted_quantity
        transacted_asset.save()

    if received_asset:
        received_asset.quantity -= transaction.received_quantity
        received_asset.save()