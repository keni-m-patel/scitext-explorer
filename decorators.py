#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 14:57:03 2018

@author: kenipatel
"""
import functools, logging
import inspect  

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class log(object):
    '''Logging decorator that allows you to log with a specific logger.'''
    # Customize these messages
#    ENTRY_MESSAGE = 'Entering: {}'
#    EXIT_MESSAGE = 'Exiting: {}'
#    VAR_MESSAGE = ' Variable: {}'

    def __init__(self, logger, event_name, object_attr):
        self.logger = logger
        self.event_name = event_name
        self.object_attr = object_attr

    def __call__(self, func):
        '''Returns a wrapper that wraps func. The wrapper will log the entry and exit points of the function with logging.INFO level. '''
        # set logger if it was not set earlier
        if not self.logger:
            logging.basicConfig()
            self.logger = logging.getLogger(func.__module__)

        @functools.wraps(func)
        def wrapper(*args, **kwds):
#            self.logger.info(self.ENTRY_MESSAGE.format(func.__name__))  # logging level .info(). Set to .debug() if you want to                        
            f_result = func(*args, **kwds)
            print(self.object_attr)
            attr = inspect.attrgetter(self.object_attr)(f_result)        
            self.logger.info(self.event_name + ': ' + str(attr))
#            self.logger.info(self.EXIT_MESSAGE.format(func.__name__))   # logging level .info(). Set to .debug() if you want to
            return f_result
        return wrapper
    
from functools import wraps
def log_event(event, objectid_attr=None, objectid_param=None):
    """Decorator to send events to the event log 
    You must pass in the event name, and may pass in some method of 
    obtaining an objectid from the decorated function's parameters or 
    return value. 
    objectid_attr: The name of an attr on the return value, to be 
        extracted via getattr(). 
    objectid_param: A string, specifies the name of the (kw)arg that 
        should be the objectid. 
    """
    def wrap(f):  
        @wraps(f)  
        def decorator(*args, **kwargs):  
            self = extract_param_by_name(f, args, kwargs, 'self')
            value = f(*args, **kwargs)  
            if objectid_attr is not None:  
                event_objectids = getattr(value, objectid_attr)  
            elif objectid_param is not None:  
                event_objectids = extract_param_by_name(f, args, kwargs, objectid_param)  
            else:  
                event_objectids = None  
            self._log_event(event, event_objectids)  
            return value  
        return decorator
    return wrap

def extract_param_by_name(f, args, kwargs, param):  
    """Find the value of a parameter by name, even if it was passed via *args or is a default value. 
    Let's start with a fictional function: 
    >>> def my_f(a,b,c='foo'): 
    ...   {"a":a,"b":b,"c":c} 
    ... 
    Works with kwargs (easy): 
    >>> extract_param_by_name(my_f, [], {'a':1}, 'a') 
    1 
    Works with args (not obvious): 
    >>> extract_param_by_name(my_f, [2], {}, 'a') 
    2 
    Works with default kwargs (bet you didn't think about that one): 
    >>> extract_param_by_name(my_f, [], {}, 'c') 
    'foo' 
    But of course you can override that: 
    >>> extract_param_by_name(my_f, [99,98,97], {}, 'c') 
    97 
    In different ways: 
    >>> extract_param_by_name(my_f, [], {'c':'gar'}, 'c') 
    'gar' 
    And dies with "grace" when you do something silly: 
    >>> extract_param_by_name(my_f, [], {}, 'a') 
    Traceback (most recent call last): 
    ... 
    LoggerBadCallerParametersException: ("Caller didn't provide a required positional parameter '%s' at index %d", 'a', 0) 
    >>> extract_param_by_name(my_f, [], {}, 'z') 
    Traceback (most recent call last): 
    ... 
    LoggerUnknownParamException: ('Unknown param %s(%r) on %s', <type 'str'>, 'z', 'my_f') 
    """  
    if param in kwargs:  
        return kwargs[param]  
    else:  
        argspec = inspect.getargspec(f)  
        if param in argspec.args:  
            param_index = argspec.args.index(param)  
            if len(args) > param_index:  
                return args[param_index]  
            if argspec.defaults is not None:  
                # argsec.defaults holds the values for the LAST entries of argspec.args  
                defaults_index = param_index - len(argspec.args) + len(argspec.defaults)  
                if 0 <= defaults_index < len(argspec.defaults):  
                    return argspec.defaults[defaults_index]  
            raise LoggerBadCallerParametersException("Caller didn't provide a required positional parameter '%s' at index %d", param, param_index)  
        else:  
            raise LoggerUnknownParamException("Unknown param %s(%r) on %s", type(param), param, f.__name__)  
class LoggerUnknownParamException(Exception):  
    pass  
class LoggerBadCallerParametersException(Exception):  
    pass  