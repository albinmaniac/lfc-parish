from .models import Parish

def parish_data(request):
    return {
        "global_parish": Parish.objects.first()
    }