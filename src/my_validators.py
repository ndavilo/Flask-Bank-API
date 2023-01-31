import re

def my_password_validator(password):
    """
    Validates password input and returns a dictionary with status and message.
    
    :param password: The password string to validate
    :return: A dictionary with the following keys:
             status (bool): True if password is valid, False otherwise.
             message (str): A message indicating the validation result.
    """
    result = {'status':False , 'message':'empty'}
    
    if len(password) < 8:
        result = {'status':False, 'message':'Password must have at least 8 characters'}
    elif re.search("[a-z]", password) is None:
        result = {'status':False, 'message':'Password must contain at least one lowercase letter'}
    elif re.search("[A-Z]", password) is None:
        result = {'status':False, 'message':'Password must contain at least one uppercase letter'}
    elif re.search("[0-9]", password) is None:
        result = {'status':False, 'message':'Password must contain at least one number'}
    elif re.search("[!@#$%^&*()]", password) is None:
        result = {'status':False, 'message':'Password must contain at least one symbol (!@#$%^&*)'}
    else:
        result = {'status':True, 'message':'Valid Password'}
        
    return result

def my_username_validator(username):
    """
    Validates username input and returns a dictionary with status and message.
    
    :param username: The username string to validate
    :return: A dictionary with the following keys:
             status (bool): True if username is valid, False otherwise.
             message (str): A message indicating the validation result.
    """
    result = {'status':False , 'message':'empty'}
    
    if len(username) < 4:
        result = {'status':False, 'message':'Username must be at least 4 characters long'}
    elif not username.isalnum():
        result = {'status':False, 'message':'Username can only contain letters and numbers'}
    else:
        result = {'status':True, 'message':'Valid Username'}
        
    return result
