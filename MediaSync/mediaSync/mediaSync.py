'''
Created on Jul 20, 2013

@author: Kyle
'''
from mediaSync.bootstraper import Bootstraper

if __name__ == '__main__':
    
    # Bootstrap application
    bootstrapper = Bootstraper()
    bootstrapper.boot()
    
    # 
    context = bootstrapper.app
    