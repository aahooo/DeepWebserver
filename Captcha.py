def main(args , details):
    if not args:
        import random,webserver,os
        from PIL import Image,ImageFont,ImageDraw
        from webserver import GetRandom
        file = open("captcha_logs/"+details['Address'][0],'w')          #file specified to ip for writing captcha value on
        rand_len = random.choice( ( 6,8,10   ) )                        #choosing how long the captcha should be
        rand = GetRandom(rand_len)                                      #creating captcha value
        name = os.environ['temp']+"\\"+GetRandom(16)+'.jpg'             #temporary captcha jpg file
        file.write(rand)
        file.close()
        background = ( random.randrange(0,255) , random.randrange(0,255) , random.randrange(0,255) )    #choosing colors randomly
        foreground = ( random.randrange(0,255) , random.randrange(0,255) , random.randrange(0,255) )    #TODO: identify which font colors cannot be correctly read
        
        img = Image.new('RGB', (1000, 300), color = background)                                 #creating image and specifing a random port to captcha string
        font_name = random.choice(os.listdir("Fonts"))
        fnt = ImageFont.truetype('Fonts/'+font_name,encoding = "utf-8" , size = 150)
        d = ImageDraw.Draw(img)
        text_x = random.randrange(0,500)                                                        #choosing a random location to write captcha on
        text_y = random.randrange(0,150)
        d.text((text_x,text_y), rand , font=fnt, fill=foreground , spacing = 2 )
        number_of_lines = random.choice((1,2,3,4,5,6))                                          #choosing how many disturbing lines should be drawn on captcha & drawing them on random locations
        for i in range(number_of_lines):
            x1 = random.randrange(0, 750)
            y1 = random.randrange(0, 300)
            x2 = random.randrange(250, 1000)
            y2 = random.randrange(0, 300)
            d.line(( (x1,y1) , (x2,y2) ) , width = 20)



        img.thumbnail((150,150), Image.ANTIALIAS)
        img.save(name)                  #saving image on temporary file then sending it to client
        img = bytes()
        
        with open(name,'rb') as image:
            img = image.read()
        os.remove(name)



        return [img, webserver.connection_status.Closed , 200 , webserver.FILETYPES.get('jpg')]
    if args:
        import webserver,os
        if os.path.isfile("captcha_logs/"+details['Address'][0]):                       #checking if client has seen a captcha

            entered = args["NONAME"][0]
            
            captcha_val = open("captcha_logs/"+details['Address'][0]).read()
            
            if captcha_val == "1":                                                      #checking if client has done captcha successfuly
                os.remove("captcha_logs/"+details['Address'][0])
                return ["Now you should try Captcha another time:)" , webserver.connection_status.Closed , 400]

            if entered == captcha_val:                                                  #checking provided value with actual captcha value
                open("captcha_logs/"+details['Address'][0] ,"w" ).write("1")            #if provided value was correct then 1 is written on temporary (captcha value containing) file
                return ["Captcha Accepted:)" , webserver.connection_status.Closed , 200]
            else:
                os.remove("captcha_logs/"+details['Address'][0])                        #entered value was incorrect
                return ["Invalid Captcha Value" , webserver.connection_status.Closed , 400]

            
        else:
            return ["" , webserver.connection_status.Closed , 400]                  #client didn't see captcha yet
