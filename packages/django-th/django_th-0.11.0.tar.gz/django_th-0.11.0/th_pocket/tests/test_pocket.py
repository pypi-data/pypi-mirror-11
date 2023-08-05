# coding: utf-8
import datetime
import time

from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from th_pocket.models import Pocket
from django_th.models import TriggerService, UserService, ServicesActivated


class PocketTest(TestCase):

    """
        PocketTest Model
    """
    def setUp(self):
        try:
            self.user = User.objects.get(username='john')
        except User.DoesNotExist:
            self.user = User.objects.create_user(
                username='john', email='john@doe.info', password='doe')

    def create_triggerservice(self, date_created="20130610",
                              description="My first Service", status=True):
        user = self.user
        service_provider = ServicesActivated.objects.create(
            name='ServiceRss', status=True,
            auth_required=False, description='Service RSS')
        service_consumer = ServicesActivated.objects.create(
            name='ServicePocket', status=True,
            auth_required=True, description='Service Pocket')
        provider = UserService.objects.create(user=user,
                                              token="",
                                              name=service_provider)
        consumer = UserService.objects.create(user=user,
                                              token="AZERTY1234",
                                              name=service_consumer)
        return TriggerService.objects.create(provider=provider,
                                             consumer=consumer,
                                             user=user,
                                             date_created=date_created,
                                             description=description,
                                             status=status)

    def create_pocket(self):
        trigger = self.create_triggerservice()
        tag = 'test'
        url = 'http://foobar.com/somewhere/in/the/rainbow'
        title = 'foobar'
        tweet_id = ''
        status = True
        return Pocket.objects.create(tag=tag, url=url, title=title,
                                     tweet_id=tweet_id, trigger=trigger,
                                     status=status)

    def test_pocket(self):
        p = self.create_pocket()
        self.assertTrue(isinstance(p, Pocket))
        self.assertEqual(p.show(), "My Pocket %s" % p.url)

    """
        Form
    """
    # no need to test if the tag is filled or not as it's not mandatory


try:
    from unittest import mock
except ImportError:
    import mock


class ServicePocketTest(TestCase):
    """
       ServicePocketTest
    """
    def setUp(self):
        self.date_triggered = datetime.datetime(2013, 6, 10, 00, 00)
        self.data = {'link': 'http://foo.bar/some/thing/else/what/else',
                     'title': 'what else'}

    def test_process_data(self, token='AZERTY123', trigger_id=1):
        since = int(
            time.mktime(datetime.datetime.timetuple(self.date_triggered)))

        datas = list()
        self.assertTrue(isinstance(self.date_triggered, datetime.datetime))
        self.assertTrue(token)
        self.assertTrue(isinstance(trigger_id, int))
        self.assertTrue(isinstance(since, int))
        self.assertTrue(isinstance(datas, list))

        pocket_instance = mock.Mock()
        pocket_instance.method(since=since, state="unread")
        pocket_instance.method.assert_called_with(since=since, state="unread")

        return datas

    def test_save_data(self, token='AZERTY123', trigger_id=1):

        the_return = False
        self.assertTrue(token)
        self.assertTrue(isinstance(trigger_id, int))
        self.assertIn('link', self.data)
        self.assertIn('title', self.data)
        self.assertIsNotNone(self.data['link'])
        self.assertNotEqual(self.data['title'], '')

        # from th_pocket.models import Pocket as PocketModel
        # trigger = PocketModel.objects.get(trigger_id=trigger_id)
        # tags = trigger.tag.lower()
        tags = ('test')

        title = ''
        title = (self.data['title'] if 'title' in self.data else '')

        pocket_instance = mock.Mock(return_value=True)
        pocket_instance.method(url=self.data['link'], title=title, tags=tags)
        pocket_instance.method.assert_called_with(url=self.data['link'],
                                                  title=title, tags=tags)

        if pocket_instance():
            the_return = True

        return the_return

    def test_get_config_th(self):
        """
            does this settings exists ?
        """
        self.assertTrue(settings.TH_POCKET)
        self.assertIn('consumer_key', settings.TH_POCKET)

    def test_get_config_th_cache(self):
        self.assertIn('th_pocket', settings.CACHES)

    def test_auth(self):
        pass

    def test_callback(self):
        pass
