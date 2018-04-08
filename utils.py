colors = {
    'cyan':      '\033[94m',

    'blue':      '\033[94m',
    'info':      '\033[94m',
    
    'green':     '\033[92m',
    'ok':        '\033[92m',
    'success':   '\033[92m',
    'True':      '\033[92m',
    
    'yellow':    '\033[93m',
    'warning':   '\033[93m',
    
    'error':     '\033[91m',
    'red':       '\033[91m',
    'False':     '\033[91m',
    
    'none':      '\033[0m', 
    'end':       '\033[0m', 
    'endc':      '\033[0m', 

    #below here are less often supported
    'bold':      '\033[1m', 
    'faint':     '\033[2m', 
    'italic':    '\033[3m', 
    'underline': '\033[4m',  
    'underline': '\033[4m',  
    'underline': '\033[4m', 

    # probably not supported
    'blink':     '\033[5m',  
    'fastblink': '\033[6m',  
}

def cprint(message, color='none'):
    print(colors[color]+str(message)+colors['endc'])