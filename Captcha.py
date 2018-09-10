def main(args , details):
    import random,webserver,os
    from PIL import Image,ImageFont,ImageDraw
    from webserver import GetRandom
    file = open("captcha_logs/"+details['Address'][0],'w')
    rand_len = random.choice( ( 6,8,10   ) )
    rand = GetRandom(rand_len)
    name = os.environ['temp']+"\\"+GetRandom(16)+'.jpg'
    file.write(rand)
    file.close()
    background = ( random.randrange(0,255) , random.randrange(0,255) , random.randrange(0,255) )
    foreground = ( random.randrange(0,255) , random.randrange(0,255) , random.randrange(0,255) )
    
    img = Image.new('RGB', (1000, 300), color = background)
    font_name = random.choice(os.listdir("Fonts"))
    fnt = ImageFont.truetype('Fonts/'+font_name,encoding = "utf-8" , size = 150)
    d = ImageDraw.Draw(img)
    text_x = random.randrange(0,750)
    text_y = random.randrange(0,200)
    d.text((text_x,text_y), rand , font=fnt, fill=foreground , spacing = 2 )
    number_of_lines = random.choice((1,2,3,4,5,6))
    for i in range(number_of_lines):
        x1 = random.randrange(0, 750)
        y1 = random.randrange(0, 300)
        x2 = random.randrange(250, 1000)
        y2 = random.randrange(0, 300)
        d.line(( (x1,y1) , (x2,y2) ) , width = 20)



        
    img.save(name)
    img = bytes()
    
    with open(name,'rb') as image:
        img = image.read()
    os.remove(name)



    return [img, webserver.connection_status.Closed , 200 , webserver.FILETYPES.get('jpg')]
