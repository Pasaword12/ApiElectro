from django.urls import path
from .views import FacturaList, OrdenTrabajoList, OrdenTrabajoDetalle, ReparacionList, OrdenTrabajoListado


urlpatterns=[
    path('', OrdenTrabajoList.as_view(), name='ordenTrabajo'),
    path('<int:id>', OrdenTrabajoDetalle.as_view(), name='ordenTrabajoDetalle'),
    path('estado-factura/', FacturaList.as_view(), name='factura'),
    path('reparacion/', ReparacionList.as_view(), name='reparacion'),
] 