
import requests
    
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
        accounts_models.Client.objects.get_or_create(
            code=client['code'], 
            defaults={
                'name': laboratory['description'],
                'short_name': laboratory['abbreviation'],
                'discount': laboratory['financialdiscountpercentage']     
            })
#        
#    class Client(models.Model):
#    name = models.CharField(max_length=254)
#    image = models.ImageField(upload_to=get_file_path, blank=True, null=True)
#    ruc = models.CharField(max_length=11)
#
#    address = models.CharField(max_length=254)
#    email = models.EmailField(max_length=254)
#    phone = models.CharField(max_length=20, null=True, blank=True)
#    
#    distribution_channel = models.ForeignKey(DistributionChannel, on_delete=models.CASCADE)
#
#    is_active = models.BooleanField(default=True)
#    created_at = models.DateTimeField(auto_now_add=True)
#    updated_at = models.DateTimeField(auto_now=True)
#
#    def __str__(self):
#        return f'{self.name} ({self.ruc})'
#
#
#class Profile(models.Model):
#    user = models.OneToOneField(User, on_delete=models.CASCADE)
#    client = models.ForeignKey(Client, on_delete=models.CASCADE)
#    phone = models.CharField(max_length=20, null=True, blank=True)
#
#    is_active = models.BooleanField(default=True)
#    created_at = models.DateTimeField(auto_now_add=True)
#    updated_at = models.DateTimeField(auto_now=True)
#    
#    return True
    