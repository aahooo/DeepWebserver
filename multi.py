def main(args , details):
    if args:
        if len(args.items())>0:
            s = 1
            for i in args.items():
                if i[0]=="NONAME":continue
                s*=int(i[1])
                message = """<title>You got it</title>
    <h1>Its Working!</h1><br>
    <h2>Your Result is {}</h2>
    <a href="/">Back To Home</a>
    """.format(s)
    else :message = """<title>You got it</title>
<h1>Its Working!</h1>
<a href="/">Back To Home</a>
"""
    constatus = "close"
    status = 200

    return [message , constatus , status]
