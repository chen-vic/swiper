from django.core.cache import cache
from django.http import JsonResponse
# Create your views here.
from user import logics
from common import stat
from user.models import User


def get_vcode(request):
    '''用户获取验证码'''
    phonenum = request.GET['phonenum']
    success = logics.send_sms(phonenum)
    if success:
        return JsonResponse({'code': stat.OK, 'data':None})
    else:
        return JsonResponse({'code': stat.SMS_ERR, 'data':None})


def submit_vcode(request):
    phonenum = request.POST.get('phonenum')
    vcode =request.POST.get('vcode')
    key = 'Vcode-%s' % phonenum
    cached_vcode = cache.get(key)
    print(cached_vcode)
    if vcode and vcode==cached_vcode:  # 防止用户未输入验证码
        print(1)
        try:
            user = User.objects.get(phonenum=phonenum)  #获取用户
        except User.DoesNotExist:
            user = User.objects.create(phonenum=phonenum,nickname=phonenum)  # 创建新用户
        # 记录用户登陆状态
        request.session['uid'] = user.id
        print(2)
        return JsonResponse({'code': stat.OK, 'data': user.to_dic()})
    else:
        return JsonResponse({'code': stat.VCODE_ERR, 'data': None})


def get_profile(request):
    return JsonResponse({})


def set_profile(request):
    return JsonResponse({})


def upload_avatar(request):
    return JsonResponse({})
