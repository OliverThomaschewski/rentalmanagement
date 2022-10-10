from collections import namedtuple
from datetime import date, datetime, timedelta
from pickle import NONE, TRUE
import random
import sqlite3
from tabnanny import check
from urllib import request
import pandas as pd
import numpy as np
import requests
import paypalrestsdk
from paypalrestsdk import Invoice



client_id_sb= "AeQNSEMsc8wY9sq61tVlsJai63Cr0iHSBUHsX-RK0lAL-uLdKeIL32WhFMnFa8z9kzcU3VLrjdo8NkH-"
secret_sb = "ENuWGMIZEnn-_n6VEWI-iPmi7dWLBpfvu21CMheGTJAgsI0JqRZ1DPEqf6tfS2c-YHAvQCbIoIkP5Juw"

client_id_live = "AUCVGo93ectJHLc9LN-4YpWv2Z-PmlMOpfuTFodJ7SsYmaE4OUjUQSZebElH9p3Bjo4_MpoNB4DtRmOa"
secret_live = "EOELZLHdXpGPhwOJfywT82Id4h2xy2-M19rv3SA18NkrmM7pL84y0ccvg0YJ657DL-onwNTbBtY3I--P"
paypalrestsdk.configure(

    {
        "mode": "sandbox",
        "client_id": client_id_sb,
        "client_secret": secret_sb
    }
)
invoice = Invoice({
    
'merchant_info': {
    "email": "mail@outleih.de",
    "first_name": "Oliver",
    "last_name": "Thomaschewski",
    "business_name": "Outleih",
    "phone": {
      "country_code": "0049",
      "national_number": "017623978262"
    },

    "address":{
      "line1": "Friedrichsbergerstr. 4",
      "city": "Berlin",
      "postal_code": "10243"
    }
    
  },


  "billing_info": [{
    "email": "o.thomaschewski@gmail.com",
    
    
  }],

  # Billing Info Ende

  


  "items": [{
      "name": "Widgets",
      "description": "Das ist die Bescheibung test",
      "quantity": 20,
      "unit_price": {
        "currency": "EUR",
        "value": 2
                    }
            },
        {
        "name": "Item 2",
        "quantity": 3,
        "unit_price": {
        "currency": "EUR",
        "value": 10
                    }
        }
            ],

        # Items Ende


  "note": """Rückgabe bis blablabla
     Bei verspäteter Rückgabe wird eine weitere Wochenleihe fällig""",
    

 
  
  "shipping_cost": {
      "amount": {
          "currency": "EUR",
          "value": 0.49
      }
  }



    })




response = invoice.create()
invoice.send()
print(response)