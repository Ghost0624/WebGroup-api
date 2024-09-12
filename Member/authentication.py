import jwt, datetime
from rest_framework import exceptions

def create_access_token(id):  
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Correct way to set expiration  
    return jwt.encode({  
        'user_id': id,  
        'exp': expiration,  
        'iat': datetime.datetime.utcnow()  
    }, 'access_secret', algorithm='HS256')  

def decode_access_token(token):
    try:
        payload = jwt.decode(token, 'access_secret', algorithms='HS256')

        return payload['user_id']
    except:
        raise exceptions.AuthenticationFailed('unauthenticated')

def create_refresh_token(id):  
    # Assuming you want a refresh token that lasts longer, e.g., 1 hour  
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=10)  
    return jwt.encode({  
        'user_id': id,  
        'exp': expiration,  
        'iat': datetime.datetime.utcnow()
    }, 'refresh_secret', algorithm='HS256')

def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, 'refresh_secret', algorithms='HS256')

        return payload['user_id']
    except:
        raise exceptions.AuthenticationFailed('unauthenticated')