# coding: utf-8
import datetime
import time
import arrow

# django classes
from django.conf import settings
from django.utils.log import getLogger
from django.core.cache import caches

# django_th classes
from django_th.services.services import ServicesMgr
# th_rss classes
from th_rss.models import Rss
from th_rss.lib.feedsservice import Feeds
from django_th.publishing_limit import PublishingLimit

logger = getLogger('django_th.trigger_happy')

cache = caches['th_rss']


class ServiceRss(ServicesMgr):

    def __init__(self, token=None):
        pass

    def read_data(self, token, trigger_id, date_triggered):
        """
            get the data from the service

            :param trigger_id: trigger ID to process
            :param date_triggered: the date of the last trigger
            :type trigger_id: int
            :type date_triggered: datetime
            :return: list of data found from the date_triggered filter
            :rtype: list
        """
        now = arrow.utcnow().to(settings.TIME_ZONE)
        published = ''
        my_feeds = []

        # get the URL from the trigger id
        rss = Rss.objects.get(trigger_id=trigger_id)

        logger.debug("RSS Feeds from %s : url %s", rss.name, rss.url)

        # retrieve the data
        feeds = Feeds(**{'url_to_parse': rss.url}).datas()

        if hasattr(feeds.feed, 'published_parsed'):
            published = datetime.datetime.utcfromtimestamp(
                time.mktime(feeds.feed.published_parsed))
        elif hasattr(feeds.feed, 'updated_parsed'):
            published = datetime.datetime.utcfromtimestamp(
                time.mktime(feeds.feed.updated_parsed))

        if published == '':
            published = now
        else:
            published = arrow.get(str(published),
                                  'YYYY-MM-DD HH:mm:ss').to(settings.TIME_ZONE)

        date_triggered = arrow.get(
            str(date_triggered),
            'YYYY-MM-DD HH:mm:ss').to(settings.TIME_ZONE)

        if date_triggered is not None and\
           published is not None and\
           now >= published and\
           published >= date_triggered:
            my_feeds = feeds.entries
            cache.set('th_rss_' + str(trigger_id), my_feeds)
            cache.set('th_rss_uuid_{}'.format(rss.uuid), my_feeds)
        # return the data
        return my_feeds

    def process_data(self, trigger_id):
        """
            get the data from the cache
            :param trigger_id: trigger ID from which to save data
            :type trigger_id: int
        """
        cache_data = cache.get('th_rss_' + str(trigger_id))
        return PublishingLimit.get_data('th_rss', cache_data, trigger_id)
