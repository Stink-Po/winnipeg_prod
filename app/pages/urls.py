from django.urls import path
from .views import (index, DuctCleaning, ServicesView, AboutView,
                    FurnaceInstallation, FurnaceRepair, FurnaceCleaning,
                    AirConditionerInstallation, AirConditionerRepair, robots)

handler404 = "pages.views.handler404_view"
handler500 = "pages.views.handler500_view"
app_name = "pages"

urlpatterns = [
    path("", index, name="index"),
    path("Duct-Cleaning-in-Winnipg/", DuctCleaning.as_view(), name="duct_cleaning"),
    path("Services/", ServicesView.as_view(), name="services"),
    path("About/", AboutView.as_view(), name="about"),
    path("Furnace-Installation-in-Winnipg/", FurnaceInstallation.as_view(), name="furnace_installation"),
    path("Furnace-Repair-in-Winnipg/", FurnaceRepair.as_view(), name="furnace_repair"),
    path("Air-Conditioner-Tune-up-in-Winnipg/", AirConditionerRepair.as_view(), name="air_conditioner_tune_up"),
    path("Furnace-Cleaning-in-Winnipg/", FurnaceCleaning.as_view(), name="furnace_cleaning"),
    path("Air-Conditioner-Installation-in-Winnipg/",
         AirConditionerInstallation.as_view(),
         name="air_conditioner_installation"),
    path("robots.txt", robots, name="robots"),
]
