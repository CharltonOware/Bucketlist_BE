import json
import os
from flask import request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from dotenv import load_dotenv

#Grab the folder where the script runs
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

#Delare Auth0 api parameters
AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
ALGORITHMS = os.environ.get('ALGORITHMS')
API_AUDIENCE = os.environ.get('API_AUDIENCE')

## AuthError Exception
'''
A standard way to communicate auth failure modes.
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

## Auth Header
def get_token_auth_header():
    '''Gets the Access Token from the Authorization Header.'''
    auth = request.headers.get('Authorization', None)
    #Raise error if no authorization header is provided
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    #Raise error if the authorization header is not Bearer token
    auth_header_parts = auth.split() #Split header into its constituent parts
    if auth_header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)
    #Raise error if token is not included
    elif len(auth_header_parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found'
        }, 401)
    elif len(auth_header_parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be Bearer token'
        }, 401)

    #Assign token to a variable token
    token = auth_header_parts[1]
    return token

'''
Implement verify_decode_jwt(token) method
@INPUTS
    token: a json web token (string)

it should be an Auth0 token with key id (kid)
it should verify the token using Auth0 /.well-known/jwks.json
it should decode the payload from the token
it should validate the claims
return the decoded payload
'''
def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed'
        }, 401)
    
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token, 
                rsa_key, 
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience issuer'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse the authentication token'
            }, 400)
    
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key'
    }, 400)
