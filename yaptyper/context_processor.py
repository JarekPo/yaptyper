from django.conf import settings


def google_analytics(request):
    return {
        "GA4_MEASUREMENT_ID": settings.GA4_MEASUREMENT_ID,
        "GA4_STREAM_ID": settings.GA4_STREAM_ID,
    }
