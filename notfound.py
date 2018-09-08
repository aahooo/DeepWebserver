def main(args , details):
	message  = "<title>404 Error</title>"
	message += "<H1>If You're not Me , Then You are Probably Lost </H1>"
	message += "<H3><a href=\"/\">Get Back Home</a></H3>"
	if details.get("Referer"):
		message += "<H5><a href=\"{}\">Or Where You Came From</a></H5>".format(details.get("Referer"))
	
	
	return [message , "close" , 404]