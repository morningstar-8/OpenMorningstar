# from qcloudsms_py.httpclient import HTTPError  # NOTE: 官方版本未适配python3.9
# from qcloudsms_py import SmsMultiSender, SmsSingleSender
from .lib.tencentsms.httpclient import HTTPError
from .lib.tencentsms import SmsMultiSender, SmsSingleSender
import ssl
# ssl._create_default_https_context = ssl._create_unverified_context
from Morningstar.settings.common import TENCENT_SMS_APP_ID
from Morningstar.settings.common import TENCENT_SMS_APP_KEY
from Morningstar.settings.common import TENCENT_SMS_SIGN


def send_sms_single(phone_num, template_id, template_param_list):
    """
    单条发送短信
    :param phone_num: 手机号
    :param template_id: 腾讯云短信模板ID
    :param template_param_list: 短信模板所需参数列表，例如:【验证码：{1}，描述：{2}】，则传递参数 [888,666]按顺序去格式化模板
    :return:
    """
    appid = TENCENT_SMS_APP_ID
    appkey = TENCENT_SMS_APP_KEY
    sms_sign = TENCENT_SMS_SIGN
    sender = SmsSingleSender(appid, appkey)
    try:
        response = sender.send_with_param(
            86, phone_num, template_id, template_param_list, sign=sms_sign)
    except HTTPError as e:
        response = {'result': 1000, 'errmsg': "网络异常发送失败"}
    return response


def send_sms_multi(phone_num_list, template_id, param_list):
    """
    批量发送短信
    :param phone_num_list:手机号列表
    :param template_id:腾讯云短信模板ID
    :param param_list:短信模板所需参数列表，例如:【验证码：{1}，描述：{2}】，则传递参数 [888,666]按顺序去格式化模板
    :return:
    """
    appid = TENCENT_SMS_APP_ID
    appkey = TENCENT_SMS_APP_KEY
    sms_sign = TENCENT_SMS_SIGN
    sender = SmsMultiSender(appid, appkey)
    try:
        response = sender.send_with_param(
            86, phone_num_list, template_id, param_list, sign=sms_sign)
    except HTTPError as e:
        response = {'result': 1000, 'errmsg': "网络异常发送失败"}
    return response


if __name__ == '__main__':
    result1 = send_sms_single("19850052801", 1278656, [123520, ])
    print(result1)

    result2 = send_sms_single(
        ["15131255089", "15131255089", "15131255089", ], 1278656, [999, ])
    print(result2)
