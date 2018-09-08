def main(args , details):
    import random,webserver,os
    from PIL import Image,ImageFont,ImageDraw
    from webserver import GetRandom
    file = open("captcha_logs/"+details['Address'][0],'w')
    rand = GetRandom(6)
    name = os.environ['temp']+"\\"+GetRandom(16)+'.jpg'
    file.write(rand)
    file.close()
    
    img = Image.new('RGB', (100, 30), color = (73, 109, 137))
    fnt = ImageFont.truetype('Fonts/BOOKOSB.TTF', 15)
    d = ImageDraw.Draw(img)
    d.text((10,10), rand , font=fnt, fill=(255, 255, 0))
    img.save(name)
    img = bytes()
    
    with open(name,'rb') as image:
        img = image.read()
    os.remove(name)



    return [img, webserver.connection_status.Closed , 200 , webserver.FILETYPES.get('jpg')]
