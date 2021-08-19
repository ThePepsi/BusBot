#pip install imgkit
#install https://wkhtmltopdf.org/downloads.html

import imgkit

path = 'Prototypes\\p_Pictures\\wkhtmltoimage\\wkhtmltoimage.exe'
config = imgkit.config(wkhtmltoimage=path)
imgkit.from_file('Prototypes\\p_Pictures\\test.html', 'Prototypes\\p_Pictures\\out.jpg',config=config)

#import pdfkit
#path = 'C:\\Program Files\\wkhtmltopdf\\bin'
#config = imgkit.configuration(wkhtmltoimg=path)
#pdfkit.from_url("http://google.com", "out.pdf", configuration=config)