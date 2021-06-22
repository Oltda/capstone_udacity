import json
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from flask import Flask, request
import os
from os import environ

AUTH0_DOMAIN = 'dev-j1fpxr2o.eu.auth0.com'

ALGORITHMS = ['RS256']
API_AUDIENCE = 'warehouse'


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    if 'Authorization' not in request.headers:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'The header is not valid',
            'success': False
        }, 401)
    auth_header = request.headers['Authorization']
    header_parts = auth_header.split(' ')

    if len(header_parts) != 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'The header is not valid',
            'success': False
        }, 401)

    elif header_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'The header is not bearer',
            'success': False
        }, 401)
    return header_parts[1]



def check_permissions(permission, payload):

    if 'permissions' not in payload:
        raise AuthError({
            'code': 'missing_permission',
            'description': 'The permission is missing',
            'success': False
        }, 400)


    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'missing_permission',
            'description': 'you do not have the required permission',
            'success': False
        }, 401)
    return True




def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.',
            'success': False
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
                'description': 'Token expired.',
                'success': False
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.',
                'success': False
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.',
                'success': False
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key.',
        'success': False
    }, 400)


def requires_auth(permission=""):

    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            jwt = get_token_auth_header()
            try:
                payload = verify_decode_jwt(jwt)
            except:
                raise AuthError({
                    'code': 'invalid_token',
                    'description': 'Token is not valid.',
                    'success': False
                }, 401)

            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator