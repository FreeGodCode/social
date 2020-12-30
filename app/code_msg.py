# -*- coding: utf-8  -*-
# @Author: ty
# @File name: code_msg.py 
# @IDE: PyCharm
# @Create time: 12/28/20 9:06 PM
from app.models import Response

# 通用
# SUCCESS = BaseResult(status=0, msg='操作成功')
SERVER_ERROR = Response(status=500, msg='系统错误')
PARAM_ERROR = Response(status=50001, msg='参数错误')
VERIFY_CODE_ERROR = Response(status=50002, msg='验证码错误')

# 权限
USER_NOT_LOGIN = Response(status=403, msg='请先登录')
USER_NOT_ACTIVE = Response(status=403, msg='帐号未激活')
USER_DISABLED = Response(status=403, msg='帐号已禁用')
USER_NOT_ACTIVE_OR_DISABLED = Response(status=403, msg='帐号未激活或已被禁用')
USER_NOT_HAD_PERMISSION = Response(status=403, msg='没有权限')

# 用户相关
CHANGE_PASSWORD_SUCCESS = Response(status=1, msg='密码修改成功')
PASSWORD_ERROR = Response(status=50101, msg='密码错误')
USER_NOT_EXIST = Response(status=50102, msg='用户不存在')
CHANGE_PASSWORD_FAIL = Response(status=50103, msg='密码修改失败')
EMAIL_EXIST = Response(status=50104, msg='该邮箱已存在')
REPEAT_SIGNED = Response(status=50105, msg='不能重复签到')

SEND_RESET_PASSWORD_MAIL = Response(status=0, msg='重置密码邮件已发送,请前往邮箱查看')
RE_SEND_ACTIVATE_MAIL = Response(status=0, msg='重新发送邮件成功,请前往邮箱查看邮件激活你的帐号')
REGISTER_SUCCESS = Response(status=0, msg='用户注册成功,请前往注册邮箱查看激活邮件,激活你的帐号后登录')
LOGIN_SUCCESS = Response(status=0, msg='登录成功')

# 帖子
HAD_ACCEPTED_ANSWER = Response(status=50201, msg='已有被采纳的回答')
COMMENT_SUCCESS = Response(status=0, msg='回帖成功')
DELETE_SUCCESS = Response(status=0, msg='删除成功')

# 参数校验相关50001
# 用户
PASSWORD_LENGTH_ERROR = Response(status=50001, msg='密码长度在6-16之间')
PASSWORD_REPEAT_ERROR = Response(status=50001, msg='两次输入密码不一致')
EMAIL_ERROR = Response(status=50001, msg='邮箱格式不正确')
EMAIL_EMPTY = Response(status=50001, msg='邮箱不能为空')
USERNAME_EMPTY = Response(status=50001, msg='昵称不能为空')
NOW_PASSWORD_EMPTY = Response(status=50001, msg='两次输入密码不一致')

# 帖子
POST_TITLE_EMPTY = Response(status=50001, msg='标题不能为空')
POST_CODE_ERROR = Response(status=50001, msg='验证码错误')
POST_CONTENT_EMPTY = Response(status=50001, msg='内容不能为空')
POST_CATALOG_EMPTY = Response(status=50001, msg='所属专栏不能为空')
POST_COIN_EMPTY = Response(status=50001, msg='悬赏金币不能为空')
CATALOG_EMPTY = Response(status=50001, msg='所属专栏不能为空')

# 文件
FILE_EMPTY = Response(status=50001, msg='没有上传任何文件')
UPLOAD_NOT_ALLOWED = Response(status=50001, msg='文件格式不支持')
