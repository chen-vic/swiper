import random
import requests
from django.core.cache import cache

from swiper import conf

def gen_rand_code(length=6):
    chars = []
    for i in range(length):
        chars.append(str(random.randint(0, 9)))
    return ''.join(chars)

def send_sms(mobile):
    '''发送短信验证码'''
    key = 'Vcode-%s' % mobile
    if cache.get(key):
        return True



    vcode = gen_rand_code() #产生验证码
    print('验证码：%s' %vcode)
    args = conf.YZX_SMS_ARGS.copy() # 原型模式
    args["param"] = vcode
    args["mobile"] = mobile

    response = requests.post(conf.YZX_SMS_API,json=args) #发送请求
    if response.status_code == 200:
        result = response.json()
        print('短信发送成功：%s' % result['msg'])
        print(result['code'])
        if result.get('code') == '000000':
            cache.set(key,vcode,600)
            print(vcode)
            return True
        else:
            return False
    return False
