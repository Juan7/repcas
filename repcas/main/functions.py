import requests

from django.contrib.auth.models import User
    
from accounting import models as accounting_models    
from accounts import models as account_models    
from inventory import models as inventory_models    
    
    
def update_distribution_channel():
    response = requests.get('http://localhost:8000/api/distribution-channel/')
    
    for distribution_channel in response.json():
        account_models.DistributionChannel.objects.get_or_create(
            code=distribution_channel['code'], 
            defaults={'name': distribution_channel['description']})
    return True
    
    
def update_laboratory():
    response = requests.get('http://localhost:8000/api/laboratories/')
    
    for laboratory in response.json():
        inventory_models.Laboratory.objects.get_or_create(
            code=laboratory['code'], 
            defaults={
                'name': laboratory['description'],
                'short_name': laboratory['abbreviation'],
                'discount': laboratory['financialdiscountpercentage']     
            })
    return True


def update_clients():
    response = requests.get('http://localhost:8000/api/clients/')
    
    for client in response.json():
        distribution_channel = account_models.DistributionChannel.objects.get(code=client['distributionchannelcode'])
        client_instance = account_models.Client.objects.get_or_create(
            ruc=client['documentnumber'], 
            defaults={
                'name': client['name'],
                'code': client['code'],
                'address': client['address'],
                'distribution_channel': distribution_channel,
                'credit_days': client['creditdays'],
                'credit_line': client['creditline'],
                'email': client['email']
            })[0]
        
        try:
            user = User.objects.get(username=client['documentnumber'])
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=client['documentnumber'],
                password='123456789',
                email=client['email']
            )
        account_models.Profile.objects.get_or_create(user=user, client=client_instance)

    return True


def update_invoices():
    response = requests.get('http://localhost:8000/api/billing-document/')
    
    for billing in response.json():
        try:
            client = account_models.Client.objects.get(code=billing['clientcode'])
            accounting_models.Invoice.objects.get_or_create(
                number=billing['documentnumber'], 
                document_type=billing['documenttype'],
                client=client,
                defaults={
                    'date': billing['registerdate'],
                    'due_date': billing['duedate'],
                    'amount_payed': billing['amountpaid'],
                    'total': billing['totalamount'],
                    'unique_code': billing['uniquecode']
                })[0]
        except account_models.Client.DoesNotExist:
            print(billing['clientcode'])

    return True
    

def update_products():
    response = requests.get('http://localhost:8000/api/articles/')
    
    for article in response.json():
        try:
            laboratory = inventory_models.Laboratory.objects.get(code=article['laboratorycode'])
            inventory_models.Product.objects.get_or_create(
                code=article['code'],
                defaults={
                    'name': article['description'],
                    'quantity': article['stock'],
                    'unit': article['unittype'],
                    'laboratory': laboratory,
                }
            )
        except inventory_models.Laboratory.DoesNotExist:
            print(article['laboratorycode'])
    return True


def update_distribution_channel_price():
    response = requests.get('http://localhost:8000/api/distribution-channel-price/')
    
    for channel_price in response.json():
        try:
            product = inventory_models.Product.objects.get(code=channel_price['articlecode'])
            distribution_channel = account_models.DistributionChannel.objects.get(code=channel_price['distributionchannelcode'])
            inventory_models.ProductDistributionChannel.objects.get_or_create(
                distribution_channel=distribution_channel,
                product=product,
                defaults={
                    'price': channel_price['price']
                }
            )
        except inventory_models.Product.DoesNotExist:
            print('Product', channel_price['articlecode'])
        except account_models.DistributionChannel.DoesNotExist:
            print('DistributionChannel', channel_price['distributionchannelcode'])
    return True


def update_promotions():
    response = requests.get('http://localhost:8000/api/promotions/')
    
    for promotion in response.json():
        try:
            product_parent = inventory_models.Product.objects.get(code=promotion['articlepromotionablecode'])
            product_children = inventory_models.Product.objects.get(code=promotion['articlepromotioncode'])
            inventory_models.ProductPromotion.objects.get_or_create(
                product=product_parent,
                child_product=product_children,
                start_date=promotion['startdate'],
                end_date=promotion['enddate'],
                is_active=promotion['flagenable'],
                product_quantity=promotion['quantitypromotionable'],
                child_product_quantity=promotion['quantitypromotion']
            )
        except inventory_models.Product.DoesNotExist:
            print('Parent', promotion['articlepromotionablecode'])
            print('Children', promotion['articlepromotioncode'])

    return True


def update_scales_price():
    response = requests.get('http://localhost:8000/api/scales-price/')
    
    for scale in response.json():
        try:
            product = inventory_models.Product.objects.get(code=scale['articlecode'])
            distribution_channel = account_models.DistributionChannel.objects.get(code=scale['distributionchannelcode'])
            inventory_models.ProductScale.objects.get_or_create(
                product=product,
                distribution_channel=distribution_channel,
                min_value=scale['startrange'],
                max_value=scale['endrange'],
                start_date=scale['startdate'],
                end_date=scale['enddate'],
                defaults={
                    'discount': scale['scalediscountpercentage']
                }
            )
        except inventory_models.Product.DoesNotExist:
            print('Product', scale['articlecode'])
        except account_models.DistributionChannel.DoesNotExist:
            print('DistributionChannel', scale['distributionchannelcode'])

    return True


def update_special_finantial_discount():
    response = requests.get('http://localhost:8000/api/special-finantial-discount/')
    
    for finantial_discount in response.json():
        try:
            client = account_models.Client.objects.get(code=finantial_discount['clientcode'])
            laboratory = inventory_models.Laboratory.objects.get(code=finantial_discount['laboratorycode'])
            inventory_models.SpecialFinantialDiscount.objects.get_or_create(
                    client=client,
                    laboratory=laboratory,
                    defaults={
                        'discount': finantial_discount['discountpercentage']
                    }
                )

        except account_models.Client.DoesNotExist:
            print('Product', finantial_discount['clientcode'])
        except inventory_models.Laboratory.DoesNotExist:
            print('Product', finantial_discount['laboratorycode'])
    
    return True


def update_special_price():
    response = requests.get('http://localhost:8000/api/special-price/')
    
    for special_price in response.json():
        try:
            client = account_models.Client.objects.get(code=special_price['clientcode'])
            product = inventory_models.Product.objects.get(code=special_price['articlecode'])
            inventory_models.SpecialPrice.objects.get_or_create(
                    client=client,
                    product=product,
                    start_date=special_price['startdate'],
                    end_date=special_price['enddate'],
                    defaults={
                        'discount': special_price['specialdiscountpercentage']
                    }
                )

        except account_models.Client.DoesNotExist:
            print('Client', special_price['clientcode'])
        except inventory_models.Product.DoesNotExist:
            print('Product', special_price['articlecode'])
    
    return True
