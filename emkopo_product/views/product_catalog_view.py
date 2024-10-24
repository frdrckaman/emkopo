import base64

from django.conf import settings
from django.views.generic.base import TemplateView
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.response import Response
from rest_framework import status
from xml.etree.ElementTree import Element, SubElement, tostring
import uuid

from emkopo_api.mixins import log_and_make_api_call
from emkopo_auth.mixins import LoginMixin
from emkopo_constants.constants import OUTGOING
from emkopo_mixins.date_mixins import convert_date_format
from emkopo_mixins.signature import load_private_key, sign_data
from emkopo_product.models import ProductCatalog, Currency, TermsCondition, Fsp


class ProductCatalogView(LoginMixin, TemplateView):
    template_name = f"emkopo_product/bootstrap/product-catalog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = ProductCatalog.objects.filter(status=1)
        context.update(
            products=products
        )
        return context


def add_product(request, url=None):
    if request.method == 'POST':
        created = ProductCatalog.objects.create(
            ProductCode=request.POST['ProductCode'],
            ProductName=request.POST['ProductName'],
            ProductDescription=request.POST['ProductDescription'],
            ForExecutive=request.POST['ForExecutive'],
            MinimumTenure=request.POST['MinimumTenure'],
            MaximumTenure=request.POST['MaximumTenure'],
            InterestRate=request.POST['InterestRate'],
            ProcessFee=request.POST['ProcessFee'],
            Insurance=request.POST['Insurance'],
            MaxAmount=request.POST['MaxAmount'],
            MinAmount=request.POST['MinAmount'],
            RepaymentType=request.POST['RepaymentType'],
            Currency=request.POST['Currency']
        )

        if created:
            res = 'success'
            message = 'Request submitted successful'
        else:
            res = 'error'
            message = ('Error occurred while processing the request,please check your inputs '
                       'and try gain')

        notification = res + '&message=' + message
        url = "?response=".join(
            [reverse(f'emkopo_product:{request.POST.get("next_url_name")}'), notification])
    return redirect(url)


def add_currency(request, url=None):
    if request.method == 'POST':
        created = Currency.objects.get_or_create(
            name=request.POST['name'],
            code=request.POST['code'],
        )

        if created:
            res = 'success'
            message = 'Request submitted successful'
        else:
            res = 'error'
            message = ('Error occurred while processing the request,please check your inputs '
                       'and try gain')

        notification = res + '&message=' + message
        url = "?response=".join(
            [reverse(f'emkopo_product:{request.POST.get("next_url_name")}'), notification])
    return redirect(url)


def add_terms(request, url=None):
    if request.method == 'POST':
        created = TermsCondition.objects.update_or_create(
            ProductCatalog_id=request.POST['ProductCatalog'],
            TermsConditionNumber=request.POST['TermsConditionNumber'],
            Description=request.POST['Description'],
            TCEffectiveDate=convert_date_format(request.POST['TCEffectiveDate']),
        )

        if created:
            res = 'success'
            message = 'Request submitted successful'
        else:
            res = 'error'
            message = ('Error occurred while processing the request,please check your inputs '
                       'and try gain')

        notification = res + '&message=' + message
        url = "?response=".join(
            [reverse(f'emkopo_product:{request.POST.get("next_url_name")}'), notification])
    return redirect(url)


def update_product(request, res=None, message=None, url=None):
    if request.method == 'POST':
        try:
            product_id = request.POST.get("id")
            product = ProductCatalog.objects.get(pk=product_id)

            product.ProductCode = request.POST['ProductCode']
            product.ProductName = request.POST['ProductName']
            product.ProductDescription = request.POST['ProductDescription']
            product.ForExecutive = request.POST['ForExecutive']
            product.MinimumTenure = request.POST['MinimumTenure']
            product.MaximumTenure = request.POST['MaximumTenure']
            product.InterestRate = request.POST['InterestRate']
            product.ProcessFee = request.POST['ProcessFee']
            product.Insurance = request.POST['Insurance']
            product.MaxAmount = request.POST['MaxAmount']
            product.MinAmount = request.POST['MinAmount']
            product.RepaymentType = request.POST['RepaymentType']
            product.Currency = request.POST['Currency']

            product.save()

            res = 'success'
            message = 'Request Approved successful'
        except Exception as e:
            res = 'error'
            message = ('Error occurred while processing the request,please check your inputs '
                       'and try again')

    notification = res + '&message=' + message
    url = "?response=".join(
        [reverse(f'emkopo_product:{request.POST.get("next_url_name")}'), notification])

    return redirect(url)


def update_terms(request, res=None, message=None):
    if request.method == 'POST':
        try:
            terms = TermsCondition.objects.get(pk=request.POST.get("id"))
            terms.TermsConditionNumber = request.POST.get('TermsConditionNumber')
            terms.Description = request.POST.get('Description')
            terms.TCEffectiveDate = convert_date_format(request.POST.get('TCEffectiveDate'))

            terms.save()

            res = 'success'
            message = 'Request Approved successful'
        except Exception as e:
            res = 'error'
            message = ('Error occurred while processing the request,please check your inputs '
                       'and try again')

    notification = res + '&message=' + message
    url = "?response=".join(
        [reverse(f'emkopo_product:{request.POST.get("next_url_name")}'), notification])

    return redirect(url)


def delete_product(request, res=None, message=None):
    if request.method == 'POST':
        try:

            fsp = Fsp.objects.all().first()

            if not fsp:
                return Response({"error": "FSP not found"}, status=status.HTTP_404_NOT_FOUND)

            product = ProductCatalog.objects.get(pk=request.POST.get("id"))

            # Generate the XML data for API call
            xml_data = generate_xml_for_decommission(product, fsp)

            # Simulate the API call to the third-party system
            # response = send_to_third_party(xml_data)

            log_and_make_api_call(
                request_type=OUTGOING,
                payload=xml_data,
                signature="XYZ",  # Replace with actual signature if available
                url=settings.ESS_UTUMISHI_API
                # Replace with actual endpoint URL
            )

            ProductCatalog.objects.filter(pk=request.POST.get("id")).update(status=False)

            res = 'success'
            message = 'Request Approved successful'

        except ProductCatalog.DoesNotExist:
            res = 'error'
            message = 'Product not found.'
        except Exception as e:
            res = 'error'
            message = ('Error occurred while processing the request, please check your inputs '
                       'and try again')

    notification = res + '&message=' + message
    url = "?response=".join(
        [reverse(f'emkopo_product:{request.POST.get("next_url_name")}'), notification])

    return redirect(url)


def delete_terms(request, res=None, message=None):
    if request.method == 'POST':
        try:
            terms = TermsCondition.objects.get(pk=request.POST.get("id"))
            terms.status = False
            terms.save()
            res = 'success'
            message = 'Request Approved successful'
        except Exception as e:
            res = 'error'
            message = ('Error occurred while processing the request,please check your inputs '
                       'and try again')

    notification = res + '&message=' + message
    url = "?response=".join(
        [reverse(f'emkopo_product:{request.POST.get("next_url_name")}'), notification])

    return redirect(url)


def generate_xml_for_decommission(product, fsp):
    """
    Generate XML data for product decommission message.
    """
    # Create the root element
    document = Element("Document")
    data_elem = SubElement(document, "Data")

    # Create the header element
    header = SubElement(data_elem, "Header")
    SubElement(header, "Sender").text = fsp.name  # Get Sender from Fsp model
    SubElement(header, "Receiver").text = "ESS_UTUMISHI"
    SubElement(header, "FSPCode").text = fsp.code  # Get FSPCode from Fsp model
    SubElement(header, "MsgId").text = str(uuid.uuid4())  # Generate unique MsgId
    SubElement(header, "MessageType").text = "PRODUCT_DECOMMISSION"

    # Add the product code to the MessageDetails element
    message_details = SubElement(data_elem, "MessageDetails")
    SubElement(message_details, "ProductCode").text = product.ProductCode

    # Convert the XML Element to string (we'll sign this string)
    xml_string = tostring(document, encoding="utf-8").decode("utf-8")

    # Load the private key to sign the data
    private_key = load_private_key(settings.EMKOPO_PRIVATE_KEY)

    # Convert the XML string to bytes
    xml_bytes = xml_string.encode('utf-8')

    # Sign the XML data (xml_bytes) using the private key
    signature = sign_data(private_key, xml_bytes)

    # Encode the signature in base64
    signature_b64 = base64.b64encode(signature).decode('utf-8')

    # Add the Signature element to the document
    SubElement(document, "Signature").text = signature_b64

    # Convert the final XML (with the signature) to string
    final_xml_string = tostring(document, encoding="utf-8").decode("utf-8")

    return final_xml_string

