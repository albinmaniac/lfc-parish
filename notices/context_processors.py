from .models import Notice

def latest_notice(request):
    notice = Notice.objects.filter(is_active=True).order_by("-created_at").first()
    return {"popup_notice": notice}