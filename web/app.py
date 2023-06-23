import sys
import os

from flask import Flask, jsonify, request, current_app as app
from flask_restful import Api
from flask_cors import CORS, cross_origin
from datetime import datetime, timedelta

import epaycosdk.epayco as epayco

app = Flask(__name__)

CORS(app, supports_credentials=True)
app.config['CORS_HEADERS'] = 'Content-Type'

api = Api(app)

options = { 
    "apiKey":       os.getenv("EPAYCO_API_KEY"),
    "privateKey":   os.getenv("EPAYCO_PRIVATE_KEY"),
    "test":         os.getenv("EPAYCO_TEST_PAYMENTS"),
    "lenguage":     os.getenv("EPAYCO_LANGUAGE")
}

objepayco = epayco.Epayco(options)

def create_token_card(posted_data): 
    card_info = {
        "card[number]":     posted_data['card_number'],
        "card[exp_year]":   posted_data['card_exp_year'],
        "card[exp_month]":  posted_data['card_exp_month'],
        "card[cvc]":        posted_data['card_cvc']
    }
    return objepayco.token.create(card_info)

def create_customer(posted_data, token_card):  
    customer_info = {
        "token_card": token_card,
        "name":       posted_data['name'],
        "last_name":  posted_data['last_name'], 
        "email":      posted_data['email'],
        "phone":      posted_data['phone'],
        "default":    True        
    }
    return objepayco.customer.create(customer_info)

def create_subscription(posted_data, token_card, customer):
    subscription_info = {
        "token_card":           token_card,
        "customer":             customer,
        "id_plan":              posted_data['id_plan'],
        "doc_type":             posted_data['doc_type'],
        "doc_number":           posted_data['doc_number'],
        "url_confirmation":     posted_data['url_confirmation'],
        "method_confirmation":  posted_data['method_confirmation']
    }
    return objepayco.subscriptions.create(subscription_info)

@app.route('/pay-subscription', methods = ['POST'])
@cross_origin()
def pay_subscription():
    posted_data = request.get_json()
    
    error_message = ''
    error_response = {
        'success':      False,
        'error':        error_message,
        'status code':  500
    }

    try:
        create_card_response =  create_token_card(
            posted_data = posted_data
        )
        if(create_card_response['success'] != True):
            error_message='Create token card error.'
            return jsonify(error_response)
        
        token_card = create_card_response['id']

        create_customer_response = create_customer(
            posted_data = posted_data, 
            token_card  = token_card
        )
        if(create_customer_response['success'] != True):
            error_message='Create customer error.'
            return jsonify(error_response)
        
        customer_id = create_customer_response['data']['customerId']

        create_subscription_response = create_subscription(
            posted_data = posted_data, 
            token_card  = token_card, 
            customer    = customer_id
        )
        if(create_subscription_response['success'] != True):
            error_message='Create subscription error.'
            return jsonify(error_response)
        
        subscription_info = {
            "customer":     customer_id,
            "token_card":   token_card,
            "id_plan":      posted_data['id_plan'],
            "doc_type":     posted_data['doc_type'],
            "doc_number":   posted_data['doc_number'],
            "ip":           posted_data['ip']
        }
        return objepayco.subscriptions.charge(subscription_info)
    
    except Exception as ex:
        print(ex, file=sys.stderr)
        retMap = {
            'success':      False,
            'error':        f"(Error: {ex})",
            'status code':  500
        }
        return jsonify(retMap)
    
@app.route('/credit-card-payment', methods = ['POST'])
@cross_origin()
def credit_card_payment():
    posted_data = request.get_json()
    
    error_message = ''
    error_response = {
        'success':      False,
        'error':        error_message,
        'status code':  500
    }

    try:
        create_card_response =  create_token_card(
            posted_data = posted_data
        )
        if(create_card_response['success'] != True):
            error_message='Create token card error.'
            return jsonify(error_response)
        
        token_card = create_card_response['id']

        create_customer_response = create_customer(
            posted_data = posted_data, 
            token_card  = token_card
        )
        if(create_customer_response['success'] != True):
            error_message='Create customer error.'
            return jsonify(error_response)
        
        customer_id = create_customer_response['data']['customerId']
        
        payment_info = {
            "token_card":                   token_card,
            "customer_id":                  customer_id,
            "doc_type":                     posted_data['doc_type'],
            "doc_number":                   posted_data['doc_number'],
            "name":                         posted_data['name'],
            "last_name":                    posted_data['last_name'], 
            "email":                        posted_data['email'],
            "bill":                         posted_data['bill'],
            "description":                  posted_data['description'],
            "value":                        posted_data['value'],
            "tax":                          posted_data['tax'],
            "tax_base":                     posted_data['tax_base'],
            "currency":                     posted_data['currency'],
            "dues":                         posted_data['dues'],
            "ip":                           posted_data['ip'],
            "url_response":                 posted_data['url_response'],
            "url_confirmation":             posted_data['url_confirmation'],
            "method_confirmation":          posted_data['method_confirmation'],
            "use_default_card_customer":    True
        }
        return objepayco.charge.create(payment_info)
    
    except Exception as ex:
        print(ex, file=sys.stderr)
        retMap = {
            'success':      False,
            'error':        f"(Error: {ex})",
            'status code':  500
        }
        return jsonify(retMap)

@app.route('/cancel-subscription', methods = ['POST'])
@cross_origin()
def cancel_subscription():
    posted_data = request.get_json()

    try:   
        return objepayco.subscriptions.cancel(posted_data['customer'])
    
    except Exception as ex:
        print(ex, file=sys.stderr)
        retMap = {
            'success':      False,
            'error':        f"(Error: {ex})",
            'status code':  500
        }
        return jsonify(retMap)

@app.route('/list-of-banks', methods = ['GET'])
@cross_origin()
def list_of_banks():
    try:   
        return objepayco.bank.pseBank(True)
    
    except Exception as ex:
        print(ex, file=sys.stderr)
        retMap = {
            'success':      False,
            'error':        f"(Error: {ex})",
            'status code':  500
        }
        return jsonify(retMap)
    
@app.route('/pse-payment', methods = ['POST'])
@cross_origin()
def pse_payment():
    posted_data = request.get_json()    

    try:
        pse_info = {
            "bank":                         posted_data['bank'],
            "invoice":                      posted_data['invoice'],
            "description":                  posted_data['description'],
            "value":                        posted_data['value'],
            "tax":                          posted_data['tax'],
            "tax_base":                     posted_data['tax_base'],
            "currency":                     posted_data['currency'],
            "doc_type":                     posted_data['doc_type'],
            "doc_number":                   posted_data['doc_number'],
            "name":                         posted_data['name'],            
            "last_name":                    posted_data['last_name'], 
            "email":                        posted_data['email'],
            "cell_phone":                   posted_data['cell_phone'],
            "ip":                           posted_data['ip'],
            "url_response":                 posted_data['url_response'],
            "url_confirmation":             posted_data['url_confirmation'],
            "metodoconfirmacion":           posted_data['metodoconfirmacion'],
            "country":                      'CO',
            "type_person":                  '0',
        }
        return objepayco.bank.create(pse_info)
    
    except Exception as ex:
        print(ex, file=sys.stderr)
        retMap = {
            'success':      False,
            'error':        f"(Error: {ex})",
            'status code':  500
        }
        return jsonify(retMap)
    
@app.route('/list-of-cash-methods', methods = ['GET'])
@cross_origin()
def list_of_cash_methods():
    try:
        retMap = {
            'cash_methods': [
                {
                    'id'    : 'efecty',
                    'name'  : 'Efecty'
                },
                {
                    'id'    : 'gana',
                    'name'  : 'Gana'
                },
                {
                    'id'    : 'redservi',
                    'name'  : 'Red Servi'
                },
                {
                    'id'    : 'puntored',
                    'name'  : 'Punto Red'
                },
                {
                    'id'    : 'sured',
                    'name'  : 'Su Red'
                }
            ],
        }   
        return jsonify(retMap)
    
    except Exception as ex:
        print(ex, file=sys.stderr)
        retMap = {
            'success':      False,
            'error':        f"(Error: {ex})",
            'status code':  500
        }
        return jsonify(retMap)
    
@app.route('/cash-payment', methods = ['POST'])
@cross_origin()
def cash_payment():
    posted_data = request.get_json()
    today       = datetime.today().date()
    end_date    = today + timedelta(days = 1)

    try:
        cash_info = {
            "invoice":                      posted_data['invoice'],
            "description":                  posted_data['description'],
            "value":                        posted_data['value'],
            "tax":                          posted_data['tax'],
            "tax_base":                     posted_data['tax_base'],
            "currency":                     posted_data['currency'],
            "doc_type":                     posted_data['doc_type'],
            "doc_number":                   posted_data['doc_number'],
            "name":                         posted_data['name'],            
            "last_name":                    posted_data['last_name'], 
            "email":                        posted_data['email'],
            "cell_phone":                   posted_data['cell_phone'],
            "ip":                           posted_data['ip'],
            "url_response":                 posted_data['url_response'],
            "url_confirmation":             posted_data['url_confirmation'],
            "metodoconfirmacion":           posted_data['metodoconfirmacion'],
            "end_date":                     str(end_date),
            "type_person":                  '0'
        }
        return objepayco.cash.create(posted_data['method'], cash_info)
    
    except Exception as ex:
        print(ex, file=sys.stderr)
        retMap = {
            'success':      False,
            'error':        f"(Error: {ex})",
            'status code':  500
        }
        return jsonify(retMap)

@app.route('/')
def welcome():
    return 'DevPaul Payments Rest API!'  

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=1616)
