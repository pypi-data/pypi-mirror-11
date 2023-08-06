systempay
=========

Systempay (Banque Populaire) client for SOAP API.

Usage
-----

.. code-block:: python

  from datetime import datetime
  from systempay.client import Client, TEST
  
  url = 'https://paiement.systempay.fr/vads-ws/ident-v2.1?wsdl'
  shop_id = 'xxxxxxxxx'
  certificate = 'xxxxxxxxxxxxxxxxx'
  
  systempay = Client(url, shop_id, certificate, TEST, 'Europe/Paris')
  
  ident = systempay.factory.create('identCreationInfo')
  
  ident.transmissionDate = systempay.get_local_datetime_format(datetime.now())
  ident.cardIdent = '3'
  ident.cardNumber = '5138xxxxxxxxxxxx'
  ident.cardNetwork = 'MASTERCARD'
  ident.cardExpirationDate = systempay.get_utc_datetime_format(datetime(2015, 10, 1, 0, 0, 0))
  ident.cvv = '999'
  ident.customerMail = 'foo@bar.com'
  
  signature = systempay.format_and_get_signature(ident)
  r = systempay.service.identCreate(ident, signature)
