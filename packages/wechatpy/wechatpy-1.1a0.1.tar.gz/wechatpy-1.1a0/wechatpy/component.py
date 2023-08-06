# -*- coding: utf-8 -*-
"""
    wechatpy.component
    ~~~~~~~~~~~~~~~

    This module provides client library for WeChat Open Platform

    :copyright: (c) 2015 by hunter007.
    :license: MIT, see LICENSE for more details.
"""
from __future__ import absolute_import, unicode_literals
import time
import json
import six
import requests

from wechatpy._compat import get_querystring
from wechatpy.session.memorystorage import MemoryStorage
from wechatpy.exceptions import WeChatClientException, APILimitedException
from wechatpy.client import WeChatComponentClient


class BaseWeChatComponent(object):

    API_BASE_URL = 'https://api.weixin.qq.com/cgi-bin/'

    def __init__(self,
                 component_appid,
                 component_appsecret,
                 component_verify_ticket,
                 session=None):
        """
        :param component_appid: 第三方平台appid
        :param component_appsecret: 第三方平台appsecret
        :param component_verify_ticket: 微信后台推送的ticket，此ticket会定时推送
        """
        self.component_appid = component_appid
        self.component_appsecret = component_appsecret
        self.expires_at = None
        self.session = session or MemoryStorage()

        if isinstance(session, six.string_types):
            from shove import Shove
            from wechatpy.session.shovestorage import ShoveStorage

            querystring = get_querystring(session)
            prefix = querystring.get('prefix', ['wechatpy'])[0]

            shove = Shove(session)
            storage = ShoveStorage(shove, prefix)
            self.session = storage
        self.session.set(
            'component_verify_ticket', component_verify_ticket, 600)

    @property
    def component_verify_ticket(self):
        return self.session.get('component_verify_ticket')

    def _request(self, method, url_or_endpoint, **kwargs):
        if not url_or_endpoint.startswith(('http://', 'https://')):
            api_base_url = kwargs.pop('api_base_url', self.API_BASE_URL)
            url = '{base}{endpoint}'.format(
                base=api_base_url,
                endpoint=url_or_endpoint
            )
        else:
            url = url_or_endpoint

        if 'params' not in kwargs:
            kwargs['params'] = {}
        if isinstance(kwargs['params'], dict) and \
                'component_access_token' not in kwargs['params']:
            kwargs['params'][
                'component_access_token'] = self.access_token
        if isinstance(kwargs['data'], dict):
            kwargs['data'] = json.dumps(kwargs['data'])

        res = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        try:
            res.raise_for_status()
        except requests.RequestException as reqe:
            raise WeChatClientException(
                errcode=None,
                errmsg=None,
                client=self,
                request=reqe.request,
                response=reqe.response
            )

        return self._handle_result(res, method, url, **kwargs)

    def _handle_result(self, res, method=None, url=None, **kwargs):
        result = res.json()
        if 'errcode' in result:
            result['errcode'] = int(result['errcode'])

        if 'errcode' in result and result['errcode'] != 0:
            errcode = result['errcode']
            errmsg = result['errmsg']
            if errcode == 42001:
                # access_token expired, fetch a new one and retry request
                self.fetch_component_access_token()
                kwargs['params']['component_access_token'] = self.session.get(
                    'component_access_token'
                )
                return self._request(
                    method=method,
                    url_or_endpoint=url,
                    **kwargs
                )
            elif errcode == 45009:
                # api freq out of limit
                raise APILimitedException(
                    errcode,
                    errmsg,
                    client=self,
                    request=res.request,
                    response=res
                )
            else:
                raise WeChatClientException(
                    errcode,
                    errmsg,
                    client=self,
                    request=res.request,
                    response=res
                )

        return result

    def fetch_access_token(self):
        """
        获取 component_access_token
        详情请参考 https://open.weixin.qq.com/cgi-bin/showdocument?action=dir_list\
        &t=resource/res_list&verify=1&id=open1419318587&token=&lang=zh_CN

        :return: 返回的 JSON 数据包
        """
        url = '{0}{1}'.format(
            self.API_BASE_URL,
            'component/api_component_token'
        )
        return self._fetch_access_token(
            url=url,
            data=json.dumps({
                'component_appid': self.component_appid,
                'component_appsecret': self.component_appsecret,
                'component_verify_ticket': self.component_verify_ticket
            })
        )

    def _fetch_access_token(self, url, data):
        """ The real fetch access token """
        res = requests.post(
            url=url,
            data=data
        )
        try:
            res.raise_for_status()
        except requests.RequestException as reqe:
            raise WeChatClientException(
                errcode=None,
                errmsg=None,
                client=self,
                request=reqe.request,
                response=reqe.response
            )
        result = res.json()
        if 'errcode' in result and result['errcode'] != 0:
            raise WeChatClientException(
                result['errcode'],
                result['errmsg'],
                client=self,
                request=res.request,
                response=res
            )

        expires_in = 7200
        if 'expires_in' in result:
            expires_in = result['expires_in']
        self.session.set(
            'component_access_token',
            result['component_access_token'],
            expires_in
        )
        self.expires_at = int(time.time()) + expires_in
        return result

    @property
    def access_token(self):
        """ WeChat component access token """
        access_token = self.session.get('component_access_token')
        if access_token:
            if not self.expires_at:
                # user provided access_token, just return it
                return access_token

            timestamp = time.time()
            if self.expires_at - timestamp > 60:
                return access_token

        self.fetch_access_token()
        return self.session.get('component_access_token')


class WeChatComponent(BaseWeChatComponent):

    def create_preauthcode(self):
        """
        获取预授权码
        """
        return self._post(
            '/component/api_create_preauthcode',
            data={
                'component_appid': self.component_appid
            }
        )

    def query_auth(self, authorization_code):
        """
        使用授权码换取公众号的授权信息

        :params authorization_code: 授权code,会在授权成功时返回给第三方平台，详见第三方平台授权流程说明
        """
        return self._post(
            '/component/api_query_auth',
            data={
                'component_appid': self.component_appid,
                'authorization_code': authorization_code
            }
        )

    def refresh_authorizer_token(
            self, authorizer_appid, authorizer_refresh_token):
        """
        获取（刷新）授权公众号的令牌

        :params authorizer_appid: 授权方appid
        :params authorizer_refresh_token: 授权方的刷新令牌
        """
        return self._post(
            '/component/api_authorizer_token',
            data={
                'component_appid': self.component_appid,
                'authorizer_appid': authorizer_appid,
                'authorizer_refresh_token': authorizer_refresh_token
            }
        )

    def get_authorizer_info(self, authorizer_appid):
        """
        获取授权方的账户信息

        :params authorizer_appid: 授权方appid
        """
        return self._post(
            '/component/api_get_authorizer_info',
            data={
                'component_appid': self.component_appid,
                'authorizer_appid': authorizer_appid,
            }
        )

    def get_authorizer_option(self, authorizer_appid, option_name):
        """
        获取授权方的选项设置信息

        :params authorizer_appid: 授权公众号appid
        :params option_name: 选项名称
        """
        return self._post(
            '/component/api_get_authorizer_option',
            data={
                'component_appid': self.component_appid,
                'authorizer_appid': authorizer_appid,
                'option_name': option_name
            }
        )

    def set_authorizer_option(
            self, authorizer_appid, option_name, option_value):
        """
        设置授权方的选项信息

        :params authorizer_appid: 授权公众号appid
        :params option_name: 选项名称
        :params option_value: 设置的选项值
        """
        return self._post(
            '/component/api_set_authorizer_option',
            data={
                'component_appid': self.component_appid,
                'authorizer_appid': authorizer_appid,
                'option_name': option_name,
                'option_value': option_value
            }
        )

    def get_client_by(self, authorization_code):
        """
        通过授权码直接获取 Client 对象

        :params authorization_code: 授权code,会在授权成功时返回给第三方平台，详见第三方平台授权流程说明
        """
        result = self.query_auth(authorization_code)
        access_token = result['authorization_info']['authorizer_access_token']
        refresh_token = result['authorization_info']['authorizer_refresh_token']  # NOQA
        authorizer_appid = result['authorization_info']['authorizer_appid']  # noqa
        return WeChatComponentClient(
            authorizer_appid,
            access_token,
            refresh_token,
            self
        )

    def get_client(self,
                   authorizer_appid,
                   authorizer_refresh_token,
                   authorizer_access_token=None):
        """
        通过 authorizer_appid, access_token, refresh_token获取 Client 对象

        :params authorizer_appid: 授权公众号appid
        :params authorizer_refresh_token: 刷新令牌
        :params authorizer_access_token: 授权方令牌
        """
        if not authorizer_access_token:
            ret = self.refresh_authorizer_token(
                authorizer_appid,
                authorizer_refresh_token
            )
            authorizer_access_token = ret['authorizer_access_token']
            authorizer_refresh_token = ret['authorizer_refresh_token']

        return WeChatComponentClient(
            authorizer_appid,
            authorizer_access_token,
            authorizer_refresh_token,
            self
        )
