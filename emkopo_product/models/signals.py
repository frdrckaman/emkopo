from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.test import APIRequestFactory
import uuid

from emkopo_api.serializers import ProductCatalogSerializer
from emkopo_api.views import ProductCatalogXMLView
from emkopo_product.models import ProductCatalog, TermsCondition, Fsp


@receiver(post_save, sender=ProductCatalog)
@receiver(post_save, sender=TermsCondition)
def send_product_catalog_to_third_party(sender, instance, created, **kwargs):
    """
    Signal to trigger the API call whenever a ProductCatalog or TermsCondition instance is created or updated.
    """
    # Fetch the Sender and FSPCode from the Fsp model where name = 'Sender' and code = 'FSPCode'
    fsp = Fsp.objects.all().first()

    if not fsp:
        print("FSP not found")
        return

    # Retrieve all products from the catalog
    products = ProductCatalog.objects.all()
    serializer = ProductCatalogSerializer(products, many=True)

    # Generate a unique MsgId
    msg_id = str(uuid.uuid4())

    # Convert the serialized data to XML format
    xml_data = ProductCatalogXMLView().convert_to_xml(serializer.data, fsp, msg_id)

    # Simulate sending the data to the third party
    response = ProductCatalogXMLView().send_to_third_party(xml_data)

    if response.status_code == 200:
        print("Data sent successfully (simulated)")
    else:
        print("Failed to send data (simulated)")
