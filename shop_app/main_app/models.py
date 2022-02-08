import uuid
from django.db import models
from account.models import Account


class Addresses(models.Model):
    id = models.AutoField(primary_key=True)
    account_of = models.ForeignKey(Account, on_delete=models.CASCADE)
    recipient_name = models.CharField(max_length=30, blank=True)
    address = models.TextField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.id


class Products(models.Model):
    prod_id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=25, blank=True)
    price = models.PositiveSmallIntegerField()
    description = models.TextField()
    qty = models.PositiveSmallIntegerField()
    image = models.CharField(max_length=500)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.name


class OrdersList(models.Model):
    PROCESSING = 'PR'
    READY_FOR_PICKUP = 'RY'
    DELIVERY = 'DE'
    COMPLETE = 'CM'
    STATUS = [
        (PROCESSING, 'Order Received! Order Processing...'),
        (READY_FOR_PICKUP, 'Order Ready and waiting for Pickup!'),
        (DELIVERY, 'Order out for Delivery'),
        (COMPLETE, 'Order Complete.'),
    ]
    batch_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    account_of = models.ForeignKey(Account, on_delete=models.DO_NOTHING, blank=True)
    order_status = models.CharField(max_length=2, choices=STATUS, default=PROCESSING)

    def __str__(self):
        return str(self.batch_id)


class Orders(models.Model):
    PROCESSING = 'PR'
    READY_FOR_PICKUP = 'RY'
    DELIVERY = 'DE'
    COMPLETE = 'CM'
    STATUS = [
        (PROCESSING, 'Order Received! Order Processing...'),
        (READY_FOR_PICKUP, 'Order Ready and waiting for Pickup!'),
        (DELIVERY, 'Order out for Delivery'),
        (COMPLETE, 'Order Complete.'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch_id = models.ForeignKey(OrdersList, on_delete=models.CASCADE)
    addresses_id = models.ForeignKey(Addresses, on_delete=models.DO_NOTHING)
    prod_id = models.ManyToManyField(Products)
    order_status = models.CharField(max_length=2, choices=STATUS, default=PROCESSING)

    def __str__(self):
        return str(self.id)

