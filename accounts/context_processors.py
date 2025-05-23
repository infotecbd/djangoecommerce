from accounts.models import ContactInfo  # replace with the actual app where ContactInfo model is

def contact_info(request):
    contact = ContactInfo.objects.first()
    return {'contact_info': contact}
