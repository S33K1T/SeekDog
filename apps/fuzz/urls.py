from django.urls import path
from apps.fuzz import views

urlpatterns = [
    # BaseFuzz
    path('BaseFuzz/',views.GetBaseFuzzyPage),
    path('BaseFuzz/Fuzz/',views.BaseFuzzy),
    # CustomFuzz
    path('CustomFuzz/',views.GetCustomFuzzPage),
    path('CustomFuzz/ReplaceText/',views.GetReplaceText),
    path('CustomFuzz/Fuzz/',views.CustomFuzz),
    # PayloadUpdate
    path('payloadUpdate/',views.GetPayloadUpdatePage ),
    path('payloadUpdate/Update',views.PayloadUpdate),
]