import config as CF
import pytesseract
from selenium import webdriver
from PIL import Image
#================访问网页=============
#实例化浏览器对象
driver=webdriver.Chrome()
#访问网页
driver.get('http://jwc104.ncu.edu.cn:8081/jsxsd/')
#================输入用户名，密码=====
#元素定位用户名，密码的位置
driver.find_element_by_xpath('//*[@id="userAccount"]').send_keys(CF.config["username"])
driver.find_element_by_xpath('//*[@id="userPassword"]').send_keys(CF.config["password"])
#driver.find_element_by_xpath('//*[@id="RANDOMCODE"]').send_keys('%s'%(yzm))
#================截取验证码===========
# 截取登录框再截取验证码
driver.save_screenshot('a.png')
#元素定位二验证码的位置
y_element=driver.find_element_by_xpath('//*[@id="SafeCodeImg"]')
#print(y_element.location)
#print(y_element.size)
#为找到验证码的位置，找出截图需要的四个位置元素的位点
left=y_element.location['x']
top=y_element.location['y']
right=left+y_element.size['width']
bottom=top+y_element.size['height']
#按位点截图，必须对四个位点的位置修改，不然截不到验证码的位置
img=Image.open('a.png')
img=img.crop((left+197,top+90,right+197,bottom+90))
img.save('c.png')
#================识别验证码===========
#将图像灰度化
im=Image.open('c.png')
imgry=im.convert('L')
imgry.save('d.png')
#将图像二值化
threshold=140
table=[]
for i in range(256):
    if i<threshold:
        table.append(0)
    else:
        table.append(1)
out=imgry.point(table,'1')
out.save('b'+'c.png')
#图像识别
text=pytesseract.image_to_string(out)
#print(text)
#exit()
#================输入验证码，点击登陆==
driver.find_element_by_xpath('//*[@id="RANDOMCODE"]').send_keys('%s'%(text))
driver.find_element_by_xpath('//*[@id="btnSubmit"]').click()




































