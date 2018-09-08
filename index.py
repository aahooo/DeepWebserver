def main(args , details):
    import os
    message = ""
    contains = os.listdir()
    for i in contains:
        if os.path.isfile(i):
            message += '<a href="{}">{}</><br>'.format(i , i.split('.')[0])
        else:
            message += '<a href="{}">{}</><br>'.format(i , i+'.dir')


    

    return [message , 'close' , 200]
