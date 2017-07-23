
import requests
from PIL import Image, ImageFilter
import pytesseract
import http.cookiejar
import urllib.request as urllib2
import http.cookies
import urllib.request
import  urllib.parse
import get_info_me

from bs4 import BeautifulSoup as soup
img_url = "http://59.69.173.117/jwweb/sys/ValidateCode.aspx"
send_url = "http://59.69.173.117/jwweb/_data/index_LOGIN.aspx"
path_info = "D:\yanzheng"
filename = 'cookie.txt'
userid = '2016010326'
passwd = '721026'
img_name = 'a.png'

code = 'xxxx'
header = {
    'Cookie' : 'ASP.NET_SessionId=mwmesqyvvkqvpbfaafglfeby',
    'Host':'59.69.173.117',
    'User-Agent':'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)'
}

postdata = {
    'UserID' : userid,
    'PassWord':passwd,
    'cCode':code,
    '__VIEWSTATE':'''dDwtMjM1NDY4NDcxO3Q8O2w8aTwxPjtpPDM+O2k8NT47aTw3Pjs+O2w8dDxwPGw8VGV4dDs+O2w85rKz5Y2X56eR5oqA5a2m6Zmi5paw56eR5a2m6ZmiOz4+Ozs+O3Q8cDxsPFRleHQ7PjtsPFw8c2NyaXB0IHR5cGU9InRleHQvamF2YXNjcmlwdCJcPgpcPCEtLQpmdW5jdGlvbiBDaGtWYWx1ZSgpewogdmFyIHZVPWRvY3VtZW50LmFsbC5VSUQuaW5uZXJUZXh0XDsKIHZVPXZVLnN1YnN0cmluZygwLDEpK3ZVLnN1YnN0cmluZygyLDMpXDsKIHZhciB2Y0ZsYWcgPSAiWUVTIlw7dHJ5ewogaWYgKGRvY3VtZW50LmFsbC5Vc2VySUQudmFsdWU9PScnKXsKIGFsZXJ0KCfpobvlvZXlhaUnK3ZVKyfvvIEnKVw7ZG9jdW1lbnQuYWxsLlVzZXJJRC5mb2N1cygpXDtyZXR1cm4gZmFsc2VcOwp9CiBlbHNlIGlmIChkb2N1bWVudC5hbGwuUGFzc1dvcmQudmFsdWU9PScnKXsKIGFsZXJ0KCfpobvlvZXlhaXlr4bnoIHvvIEnKVw7ZG9jdW1lbnQuYWxsLlBhc3NXb3JkLmZvY3VzKClcO3JldHVybiBmYWxzZVw7Cn0KIGVsc2UgaWYgKGRvY3VtZW50LmFsbC5jQ29kZS52YWx1ZT09JycgJiYgdmNGbGFnID09ICJZRVMiKXsKIGFsZXJ0KCfpobvlvZXlhaXpqozor4HnoIHvvIEnKVw7ZG9jdW1lbnQuYWxsLmNDb2RlLmZvY3VzKClcO3JldHVybiBmYWxzZVw7Cn0KIGVsc2UgeyBkb2N1bWVudC5hbGwuZGl2TG9nTm90ZS5pbm5lckhUTUw9J+ato+WcqOmAmui/h+i6q+S7vemqjOivgS4uLuivt+eojeWAmSEnXDsKIHJldHVybiB0cnVlXDt9Cn1jYXRjaChlKXt9Cn0KZnVuY3Rpb24gU2VsVHlwZShvYmopewogdmFyIHM9b2JqLm9wdGlvbnNbb2JqLnNlbGVjdGVkSW5kZXhdLnVzcklEXDsKIHZhciB3PW9iai5vcHRpb25zW29iai5zZWxlY3RlZEluZGV4XS5Qd2RJRFw7CiBkb2N1bWVudC5hbGwuVUlELmlubmVySFRNTD1zXDsKIHNlbFR5ZU5hbWUoKVw7Cn0KZnVuY3Rpb24gb3BlbldpbkxvZyh0aGVVUkwsdyxoKXsKdmFyIFRmb3JtLHJldFN0clw7CmV2YWwoIlRmb3JtPSd3aWR0aD0iK3crIixoZWlnaHQ9IitoKyIsc2Nyb2xsYmFycz1ubyxyZXNpemFibGU9bm8nIilcOwpwb3A9d2luZG93Lm9wZW4odGhlVVJMLCd3aW5LUFQnLFRmb3JtKVw7IC8vcG9wLm1vdmVUbygwLDc1KVw7CmV2YWwoIlRmb3JtPSdkaWFsb2dXaWR0aDoiK3crInB4XDtkaWFsb2dIZWlnaHQ6IitoKyJweFw7c3RhdHVzOm5vXDtzY3JvbGxiYXJzPW5vXDtoZWxwOm5vJyIpXDsKaWYodHlwZW9mKHJldFN0cikhPSd1bmRlZmluZWQnKSBhbGVydChyZXRTdHIpXDsKfQpmdW5jdGlvbiBzaG93TGF5KGRpdklkKXsKdmFyIG9iakRpdiA9IGV2YWwoZGl2SWQpXDsKaWYgKG9iakRpdi5zdHlsZS5kaXNwbGF5PT0ibm9uZSIpCntvYmpEaXYuc3R5bGUuZGlzcGxheT0iIlw7fQplbHNle29iakRpdi5zdHlsZS5kaXNwbGF5PSJub25lIlw7fQp9CmZ1bmN0aW9uIHNlbFR5ZU5hbWUoKXsKICBkb2N1bWVudC5hbGwudHlwZU5hbWUudmFsdWU9ZG9jdW1lbnQuYWxsLlNlbF9UeXBlLm9wdGlvbnNbZG9jdW1lbnQuYWxsLlNlbF9UeXBlLnNlbGVjdGVkSW5kZXhdLnRleHRcOwp9CmZ1bmN0aW9uIHdpbmRvdy5vbmxvYWQoKXsKCXZhciBzUEM9d2luZG93Lm5hdmlnYXRvci51c2VyQWdlbnQrd2luZG93Lm5hdmlnYXRvci5jcHVDbGFzcyt3aW5kb3cubmF2aWdhdG9yLmFwcE1pbm9yVmVyc2lvbisnIFNOOk5VTEwnXDsKdHJ5e2RvY3VtZW50LmFsbC5wY0luZm8udmFsdWU9c1BDXDt9Y2F0Y2goZXJyKXt9CnRyeXtkb2N1bWVudC5hbGwuVXNlcklELmZvY3VzKClcO31jYXRjaChlcnIpe30KdHJ5e2RvY3VtZW50LmFsbC50eXBlTmFtZS52YWx1ZT1kb2N1bWVudC5hbGwuU2VsX1R5cGUub3B0aW9uc1tkb2N1bWVudC5hbGwuU2VsX1R5cGUuc2VsZWN0ZWRJbmRleF0udGV4dFw7fWNhdGNoKGVycil7fQp9CmZ1bmN0aW9uIG9wZW5XaW5EaWFsb2codXJsLHNjcix3LGgpCnsKdmFyIFRmb3JtXDsKZXZhbCgiVGZvcm09J2RpYWxvZ1dpZHRoOiIrdysicHhcO2RpYWxvZ0hlaWdodDoiK2grInB4XDtzdGF0dXM6IitzY3IrIlw7c2Nyb2xsYmFycz1ub1w7aGVscDpubyciKVw7CndpbmRvdy5zaG93TW9kYWxEaWFsb2codXJsLDEsVGZvcm0pXDsKfQpmdW5jdGlvbiBvcGVuV2luKHRoZVVSTCl7CnZhciBUZm9ybSx3LGhcOwp0cnl7Cgl3PXdpbmRvdy5zY3JlZW4ud2lkdGgtMTBcOwp9Y2F0Y2goZSl7fQp0cnl7Cmg9d2luZG93LnNjcmVlbi5oZWlnaHQtMzBcOwp9Y2F0Y2goZSl7fQp0cnl7ZXZhbCgiVGZvcm09J3dpZHRoPSIrdysiLGhlaWdodD0iK2grIixzY3JvbGxiYXJzPW5vLHN0YXR1cz1ubyxyZXNpemFibGU9eWVzJyIpXDsKcG9wPXBhcmVudC53aW5kb3cub3Blbih0aGVVUkwsJycsVGZvcm0pXDsKcG9wLm1vdmVUbygwLDApXDsKcGFyZW50Lm9wZW5lcj1udWxsXDsKcGFyZW50LmNsb3NlKClcO31jYXRjaChlKXt9Cn0KZnVuY3Rpb24gY2hhbmdlVmFsaWRhdGVDb2RlKE9iail7CnZhciBkdCA9IG5ldyBEYXRlKClcOwpPYmouc3JjPSIuLi9zeXMvVmFsaWRhdGVDb2RlLmFzcHg/dD0iK2R0LmdldE1pbGxpc2Vjb25kcygpXDsKfQpcXC0tXD4KXDwvc2NyaXB0XD47Pj47Oz47dDw7bDxpPDE+Oz47bDx0PDtsPGk8MD47PjtsPHQ8cDxsPFRleHQ7PjtsPFw8b3B0aW9uIHZhbHVlPSdTVFUnIHVzcklEPSflraYgIOWPtydcPuWtpueUn1w8L29wdGlvblw+Clw8b3B0aW9uIHZhbHVlPSdURUEnIHVzcklEPSflt6UgIOWPtydcPuaVmeW4iOaVmei+heS6uuWRmFw8L29wdGlvblw+Clw8b3B0aW9uIHZhbHVlPSdTWVMnIHVzcklEPSfluJAgIOWPtydcPueuoeeQhuS6uuWRmFw8L29wdGlvblw+Clw8b3B0aW9uIHZhbHVlPSdBRE0nIHVzcklEPSfluJAgIOWPtydcPumXqOaIt+e7tOaKpOWRmFw8L29wdGlvblw+Cjs+Pjs7Pjs+Pjs+Pjt0PHA8cDxsPFRleHQ7PjtsPOmqjOivgeeggemUmeivr++8gVw8YnJcPueZu+W9leWksei0pe+8gTs+Pjs+Ozs+Oz4+Oz6rUibqKcRWN8Z3yXCsXJF4LAAvYA==''',
    '__VIEWSTATEGENERATOR':'4B596BA9',
    'Sel_Type':'STU',
    'typeName':'%D1%A7%C9%FA',
    'pcInfo':'''Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)x860 SN:NULL'''
}


def get_bin_table():
    threshold  =   155
    table  =  []
    for  i  in  range( 256 ):
        if  i  <  threshold:
            table.append(0)
        else:
            table.append(255)

    return table
def save_cook(filename,url):
    # cookie = http.cookiejar.MozillaCookieJar(filename)
    # handler = urllib2.HTTPCookieProcessor(cookie)
    # opener = urllib2.build_opener(handler)
    # response = opener.open(url)
    # cookie.save(ignore_discard=True, ignore_expires=True)
    # print(cookie)
    cookie = save_img(header)  # 保存图片
    header['Cookie'] = cookie

def get_cookie(filename):
    cookie= http.cookiejar.MozillaCookieJar()
    cookie.load(filename,ignore_discard=True,ignore_expires=True)
    return urllib2.HTTPCookieProcessor(cookie)

def save_img(header):
    
    # opener = urllib2.build_opener(cookie)
    # req = urllib2.Request(url,headers=header)
    # result = opener.open(req)
    a = urllib.request.urlretrieve(img_url,img_name,data= urllib.parse.urlencode(header).encode())
    cookie = a[1]['Set-Cookie'][0:-8]
    return cookie





def left_zone(img, x, y):
    sum = img.getpixel((x + 1, y)) + \
          img.getpixel((x + 1, y + 1)) + \
          img.getpixel((x + 1, y - 1)) + \
          img.getpixel((x, y + 1)) + \
          img.getpixel((x, y - 1))
    if sum >= 1020:
        return 255
    else:
        return 0


def right_zone(img, x, y):
    sum = img.getpixel((x - 1, y)) + \
          img.getpixel((x - 1, y + 1)) + \
          img.getpixel((x - 1, y - 1)) + \
          img.getpixel((x, y + 1)) + \
          img.getpixel((x, y - 1))
    if sum >= 1020:
        return 255
    else:
        return 0


def up_zone(img, x, y):
    sum = img.getpixel((x - 1, y)) + \
          img.getpixel((x + 1, y)) + \
          img.getpixel((x - 1, y + 1)) + \
          img.getpixel((x, y + 1)) + \
          img.getpixel((x + 1, y + 1))
    if sum >= 1020:
        return 255
    else:
        return 0


def down_zone(img, x, y):
    sum = img.getpixel((x - 1, y)) + \
          img.getpixel((x + 1, y)) + \
          img.getpixel((x - 1, y - 1)) + \
          img.getpixel((x, y - 1)) + \
          img.getpixel((x + 1, y - 1))
    if sum >= 1020:
        return 255
    else:
        return 0


def min_zone(img, x, y):
    sum = img.getpixel((x - 1, y + 1)) + \
          img.getpixel((x - 1, y)) + \
          img.getpixel((x - 1, y - 1)) + \
          img.getpixel((x, y + 1)) + \
          img.getpixel((x, y - 1)) + \
          img.getpixel((x + 1, y + 1)) + \
          img.getpixel((x + 1, y)) + \
          img.getpixel((x + 1, y - 1))
    if sum >= (255 * 6):
        return 255
    else:
        return 0


def remove_noise(img, x, y):
    cur_pixel = img.getpixel((x, y))
    width = img.width
    height = img.height
    if cur_pixel == 255:
        return 255
    else:
        if x == 0:
            if y == 0 or y == height:
                return 255
            else:
                return left_zone(img, x, y)
        if x == width:
            if y == 0 or y == height:
                return 255
            else:
                return right_zone(img, x, y)
        if y == 0:
            if x == 0 or x == width:
                return 255
            else:
                return up_zone(img, x, y)
        if y == height:
            if x == 0 or x == width:
                return 255
            else:
                return down_zone(img, x, y)

        return min_zone(img, x, y)


def list_set_img(list_img, img_):
    w, h = img_.size
    i = 0
    for x in range(w):
        for y in range(h):
            if list_img[i] == None:
                list_img[i] = 0
            img_.putpixel((x, y), list_img[i])
            i = i + 1
    return img_


def clear_img(img):
    w, h = img.size
    list_img = []
    for x in range(w):
        for y in range(h):
            list_img.append(remove_noise(img, x, y))
    return list_img


def read_img(img_):
    code = pytesseract.image_to_string(img_)
    return code


def gif_to_png(img_url):
    img_ = Image.open(img_url)
    img_.save('a1.png', 'png')
    return 'a1.png'


def to_black(img):
    img = img.convert('L')
    table = get_bin_table()
    img_ = img.point(table, '1')
    return img_


def return_code(filename):
    list_img = []
    img = filename
    img = Image.open(img)
    img = to_black(img)
    list_img = clear_img(img)
    return read_img(list_set_img(list_img, img))

def test_user(html):
    doc = soup(html)
    # print(html)
    if doc.select('#divLogNote')[0].string == '正在加载权限数据...':
        print('登陆成功！！！！')
        get_info_me.get_stu_info(header, userid)
    else:
        the_send()




def the_send():
    global postdata,code,cookie
    save_cook(filename,img_url)#保存cookie
    code = return_code(img_name).replace(' ', '')
    cookie = get_cookie(filename)#获取cookie
    postdata['cCode'] = code
    to_postdata = urllib.parse.urlencode(postdata).encode()
    # #伪造cookie发送

    # test_user(the_send(send_url,cookie,postdata))


    req = urllib2.Request(send_url,data=to_postdata,headers=header)
    # opener = urllib2.build_opener(cookie)
    result = urllib2.urlopen(req)
    test_user(result.read().decode('gb2312'))


