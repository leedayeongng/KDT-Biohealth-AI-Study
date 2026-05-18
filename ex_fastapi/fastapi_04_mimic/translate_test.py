#pip install googletrans==4.0.0-rc1
from googletrans import Translator
translator = Translator()
#en to ko
text = 'pneumonia'
result = translator.translate(text, src="en", dest="ko")
print(f'en:{text} -> ko : {result.text}')
result2=translator.translate(text, src="ko", dest="en")
print(f'ko:{result.text} -> en : {result2.text}')