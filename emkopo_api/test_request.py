import requests

# The URL of your local Django API endpoint
url = 'http://127.0.0.1:8000/api/product-catalog/'

# Your XML data as a string
xml_data = """
<Document>
  <Data>
    <Header>
      <Sender>FSPSystem</Sender>
      <Receiver>ESS_UTUMISHI</Receiver>
      <FSPCode>1001</FSPCode>
      <MsgId>FSP12346</MsgId>
      <MessageType>PRODUCT_DETAIL</MessageType>
    </Header>
    <MessageDetails>
      <ProductCode>123456</ProductCode>
      <ProductName>Mkopo Wa Nyumba</ProductName>
      <ProductDescription>Payment Must be Made in Full</ProductDescription>
      <ForExecutive>true</ForExecutive>
      <MinimumTenure>12</MinimumTenure>
      <MaximumTenure>72</MaximumTenure>
      <InterestRate>10</InterestRate>
      <ProcessFee>5</ProcessFee>
      <Insurance>7</Insurance>
      <MaxAmount>10000000</MaxAmount>
      <MinAmount>100000</MinAmount>
      <RepaymentType>Flat</RepaymentType>
      <Currency>TZS</Currency>
      <TermsCondition>
        <TermsConditionNumber>123456</TermsConditionNumber>
        <Description>Payment Must be Made in Full</Description>
        <TCEffectiveDate>2021-10-10</TCEffectiveDate>
      </TermsCondition>
      <TermsCondition>
        <TermsConditionNumber>123457</TermsConditionNumber>
        <Description>Loan must be paid within time</Description>
        <TCEffectiveDate>2021-10-10</TCEffectiveDate>
      </TermsCondition>
    </MessageDetails>
  </Data>
  <Signature>XYZ</Signature>
</Document>
"""

# Set the headers
headers = {'Content-Type': 'application/xml'}

# Send the request to the local Django server
response = requests.post(url, data=xml_data, headers=headers)

# Print the response
print(f"Status Code: {response.status_code}")
print(f"Response Body: {response.text}")
