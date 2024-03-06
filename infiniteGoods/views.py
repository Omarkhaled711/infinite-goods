'''
views model for main application
'''
from django.shortcuts import render


def home(req):
    '''
    The home page (root) of our website
    '''
    return render(req, 'index.html')
