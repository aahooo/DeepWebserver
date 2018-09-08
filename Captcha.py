def main(args , details):
    import random,webserver,os
    from PIL import Image,ImageFont,ImageDraw
    from webserver import GetRandom
    file = open("captcha_logs/"+details['Address'][0],'w')
    rand = GetRandom(6)
    name = os.environ['temp']+"\\"+GetRandom(16)+'.jpg'
    file.write(rand)
    file.close()
    
    img = Image.new('RGB', (100, 30), color = (73, 0, 137))
    font_name = random.choice(os.listdir("Fonts"))
    fnt = ImageFont.truetype('Fonts/'+font_name, 15)
    d = ImageDraw.Draw(img)
    d.text((10,10), rand , font=fnt, fill=(255, 255, 0))
    number_of_lines = random.choice((1,2,3))
    for i in range(number_of_lines):
        x1 = random.randrange(0, 75)
        y1 = random.randrange(0, 30)
        x2 = random.randrange(25, 100)
        y2 = random.randrange(0, 30)
        d.line(( (x1,y1) , (x2,y2) ) , width = 2)



        
    img.save(name)
    img = bytes()
    
    with open(name,'rb') as image:
        img = image.read()
    os.remove(name)



    return [img, webserver.connection_status.Closed , 200 , webserver.FILETYPES.get('jpg')]
