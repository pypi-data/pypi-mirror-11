# -*- coding:utf-8 -*-

import redis
import time
import datetime
import urlparse
import socket
import json
from contextlib import contextmanager

try:
    from django.conf import settings
except ImportError:
    import config as settings

from bs4 import BeautifulSoup

from .utils import parse_yandex, parse_google
from .mixin import openYandexMixin

MAX_OPEN_LINKS = 50


class TimeoutError(Exception):
    pass


def getData(string, server, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(120)
    print server + ':' + str(port)
    s.connect((server, port))
    s.send(string)
    data = ''
    text = ''
    now = datetime.datetime.now()

    while True:
        data += s.recv(1024)
        if (datetime.datetime.now() - datetime.timedelta(seconds=60)) > now:
            raise TimeoutError

        if '###end###' in data:
            text = data.replace('###end###', '')
            break
    return BeautifulSoup(text)


def getServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(120)
    s.connect(settings.ANTI_BALANCER)
    string = "###GET_SERVER###"
    s.send(string)
    data = ''
    text = ''
    now = datetime.datetime.now()

    while True:
        data += s.recv(1024)
        if (datetime.datetime.now() - datetime.timedelta(seconds=60)) > now:
            raise TimeoutError

        if '###end###' in data:
            text = data.replace('###end###', '')
            break
    server, port = text.split(':')
    return text, server, int(port)


class openYandex(openYandexMixin):
    def __init__(self, key):
        self.key = key
        self.rds = redis.Redis(**settings.ANTI_REDIS_CONF)

    @contextmanager
    def ip_port(self):
        # Получаем  ip+port из балансера
        for counter in xrange(5):
            try:
                self.redis_key, self.server, self.port = getServer()
                break
            except (TimeoutError, socket.timeout) as exc:
                self.soup = '<p>%s</p>' % exc
                time.sleep(3)

        # Получаем состояние воркера
        try:
            self.state = json.loads(self.rds.get(self.redis_key))
        except:
            self.state = {'counter': 0, 'state': True}

        # Выполняем контекст
        for counter in xrange(5):
            try:
                yield
                break
            except Exception as exc:
                self.soup = '<p>%s</p>' % exc
                time.sleep(3)
            finally:
                self.update_state()

    def update_state(self):
        """ Обновление состояния браузера и рестарт в случае надобности """
        if hasattr(self, 'redis_key'):
            self.state['counter'] += 1
            if self.state['counter'] >= MAX_OPEN_LINKS:
                string = '###restart###'
                getData(string, self.server, self.port)
                self.state['counter'] = 0
            self.state['state'] = False
            self.rds.set(self.redis_key, json.dumps(self.state))

    def get_soup(self, url, save=True, counter=0, normalize=False):
        """ Получение супа в ответе сервера """
        self.url = url
        self.save = save
        self.counter = counter
        self.normalize = normalize
        with self.ip_port():
            parse_url = urlparse.urlparse(url)
            self.hostname = parse_url.hostname
            self.query = parse_url.query
            if isinstance(self.query, unicode):
                self.query = self.query.encode('utf8')

            string = '###split###'.join((url, self.key))
            soup = getData(string, self.server, self.port)

        if save:
            data = self.saveData(soup)
            if normalize:
                return data
        return soup

    def formatData(self, soup):
        """ Формирование данных """
        if 'yandex.ru' == self.hostname:
            data = parse_yandex(soup, self.query)
            if data is False:
                data = self.get_soup(self.url, self.save, self.counter, self.normalize)
        if 'www.google.ru' == self.hostname:
            data = parse_google(soup, self.query)
        return data

    def saveData(self, soup):
        """ Сохранение в базу """
        data = self.formatData(soup)
        self.rds.set('page:' + self.url, json.dumps(data))
        return data

openGoogle = openYandex
