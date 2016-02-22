def find_domain(webpage):
    """
    Accepts webpage (a string) and removes the Protocol, Subdomain and Path. Returns domain (a string).
    EX: if webpage is "http://news.google.com/world" then domain is "google.com"
    """
    domain = ''

    start = False
    stop = False
    for c in webpage:
        if start == True and c == '/':
            stop = True
        if start == True and stop == False:
            domain = domain + c
        if c == '.':
            start = True
    return domain

print find_domain('http://news.bbc.co.uk/england')