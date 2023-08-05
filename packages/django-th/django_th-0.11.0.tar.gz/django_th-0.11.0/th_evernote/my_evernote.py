# coding: utf-8
from __future__ import unicode_literals

import sys
import arrow

# evernote API
from evernote.api.client import EvernoteClient
from evernote.edam.notestore import NoteStore
import evernote.edam.type.ttypes as Types
from evernote.edam.error.ttypes import EDAMSystemException
from evernote.edam.error.ttypes import EDAMErrorCode

# django classes
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.conf import settings
from django.utils.log import getLogger
from django.core.cache import caches


# django_th classes
from django_th.services.services import ServicesMgr
from django_th.models import UserService, ServicesActivated
from django_th.html_entities import HtmlEntities
from django_th.publishing_limit import PublishingLimit
from th_evernote.models import Evernote
from th_evernote.sanitize import sanitize


"""
    handle process with evernote
    put the following in settings.py

    TH_EVERNOTE = {
        'sandbox': True,
        'consumer_key': 'abcdefghijklmnopqrstuvwxyz',
        'consumer_secret': 'abcdefghijklmnopqrstuvwxyz',
    }
    sanbox set to True to make your test and False for production purpose

    TH_SERVICES = (
        ...
        'th_evernote.my_evernote.ServiceEvernote',
        ...
    )

"""

logger = getLogger('django_th.trigger_happy')

cache = caches['th_evernote']


class ServiceEvernote(ServicesMgr):

    def __init__(self, token=None):
        self.sandbox = settings.TH_EVERNOTE['sandbox']
        self.consumer_key = settings.TH_EVERNOTE['consumer_key']
        self.consumer_secret = settings.TH_EVERNOTE['consumer_secret']

        kwargs = {'consumer_key': self.consumer_key,
                  'consumer_secret': self.consumer_secret,
                  'sandbox': self.sandbox}

        if token:
            kwargs = {'token': token, 'sandbox': self.sandbox}

        self.client = EvernoteClient(**kwargs)

    def read_data(self, trigger_id, date_triggered):
        """
            get the data from the service
            :param trigger_id: trigger ID to process
            :param date_triggered: the date of the last trigger
            :type trigger_id: int
            :type date_triggered: datetime
            :return: list of data found from the date_triggered filter
            :rtype: list
        """
        data = []

        # get the data from the last time the trigger has been started
        # the filter will use the DateTime format in standard
        new_date_triggered = arrow.get(
            str(date_triggered), 'YYYYMMDDTHHmmss')

        new_date_triggered = str(new_date_triggered).replace(
            ':', '').replace('-', '')
        date_filter = "created:{}".format(new_date_triggered[:-6])

        # filter
        my_filter = NoteStore.NoteFilter()
        my_filter.words = date_filter

        # result spec to tell to evernote
        # what information to include in the response
        spec = NoteStore.NotesMetadataResultSpec()
        spec.includeTitle = True
        spec.includeAttributes = True

        our_note_list = self.note_store.findNotesMetadata(
            self.token, my_filter, 0, 100, spec)

        whole_note = ''
        for note in our_note_list.notes:
            whole_note = self.note_store.getNote(
                self.token, note.guid, True, False, False, False)
            data.append(
                {'title': note.title,
                 'link': whole_note.attributes.sourceURL,
                 'content': whole_note.content})

        cache.set('th_evernote_' + str(trigger_id), data)

        return data

    def process_data(self, trigger_id):
        """
            get the data from the cache
            :param trigger_id: trigger ID from which to save data
            :type trigger_id: int
        """
        cache_data = cache.get('th_evernote_' + str(trigger_id))
        return PublishingLimit.get_data('th_evernote', cache_data, trigger_id)

    def save_data(self, token, trigger_id, **data):
        """
            let's save the data
            don't want to handle empty title nor content
            otherwise this will produce an Exception by
            the Evernote's API

            :param trigger_id: trigger ID from which to save data
            :param **data: the data to check to be used and save
            :type trigger_id: int
            :type **data:  dict
            :return: the status of the save statement
            :rtype: boolean
        """
        title = ''
        content = ''
        status = False

        title = self.set_note_title(data)
        content = self.set_note_content(data)

        if len(title):
            # get the evernote data of this trigger
            trigger = Evernote.objects.get(trigger_id=trigger_id)

            try:
                self.note_store = self.client.get_note_store()
            except EDAMSystemException as e:
                # rate limite reach have to wait 1 hour !
                if e.errorCode == EDAMErrorCode.RATE_LIMIT_REACHED:
                    sentance = "Rate limit reached {code}"
                    sentance += "Retry your request in {msg} seconds"
                    sentance += " - date set to cache again until"
                    sentance += " limit reached"
                    logger.warn(sentance.format(
                        code=e.errorCode,
                        msg=e.rateLimitDuration))
                    # put again in cache the data that could not be
                    # published in Evernote yet
                    cache.set('th_evernote_' + str(trigger_id), data)
                    return True
                else:
                    logger.critical(e)
                    return False
            except Exception as e:
                logger.critical(e)
                return False

            # note object
            note = Types.Note()
            if trigger.notebook:
                notebook_id = 0
                tag_id = []
                # get the notebookGUID ...
                notebook_id = self.get_notebook(trigger)
                # create notebookGUID if it does not exist then return its id
                note.notebookGuid = self.set_notebook(trigger, notebook_id)

                # ... and get the tagGUID if a tag has been provided
                tag_id = self.get_tag(trigger)
                tag_id = self.set_tag(trigger, tag_id)

                if trigger.tag is not '':
                    # set the tag to the note if a tag has been provided
                    note.tagGuids = tag_id

                logger.debug("notebook that will be used %s", trigger.notebook)

            # attribute of the note: the link to the website
            note_attribute = self.set_note_attribute(data)
            if note_attribute:
                note.attributes = note_attribute

            # footer of the note
            footer = self.set_note_footer(data, trigger)
            content += footer

            note.title = title
            note.content = self.set_evernote_header()
            note.content += self.get_sanitize_content(content)

            # create the note !
            try:
                created_note = self.note_store.createNote(note)
                sentance = str('note %s created') % created_note.guid
                logger.debug(sentance)
                status = True
            except EDAMSystemException as e:
                if e.errorCode == EDAMErrorCode.RATE_LIMIT_REACHED:
                    sentance = "Rate limit reached {code}"
                    sentance += "Retry your request in {msg} seconds"
                    logger.warn(sentance.format(
                        code=e.errorCode,
                        msg=e.rateLimitDuration))
                    # put again in cache the data that could not be
                    # published in Evernote yet
                    cache.set('th_evernote_' + str(trigger_id), data)
                    return True
                else:
                    logger.critical(e)
                    return False
            except Exception as e:
                logger.critical(e)
                return False

        else:
            sentence = "no title provided for trigger ID {} and title {}"
            logger.critical(sentence.format(trigger_id, title))
            status = False
        return status

    def get_notebook(self, trigger):
        """
            get the notebook from its name
        """
        notebook_id = 0
        notebooks = self.note_store.listNotebooks()
        # get the notebookGUID ...
        for notebook in notebooks:
            if notebook.name.lower() == trigger.notebook.lower():
                notebook_id = notebook.guid
                break
        return notebook_id

    def set_notebook(self, trigger, notebook_id):
        """
            create a notebook
        """
        if notebook_id == 0:
            new_notebook = Types.Notebook()
            new_notebook.name = trigger.notebook
            new_notebook.defaultNotebook = False
            notebook_id = self.note_store.createNotebook(
                new_notebook).guid

        return notebook_id

    def get_tag(self, trigger):
        """
            get the tags from his Evernote account
        """
        tag_id = []
        if trigger.tag is not '':
            listtags = self.note_store.listTags()
            # cut the string by piece of tag with comma
            if ',' in trigger.tag:
                for my_tag in trigger.tag.split(','):
                    for tag in listtags:
                        # remove space before and after
                        # thus we keep "foo bar"
                        # but not " foo bar" nor "foo bar "
                        if tag.name.lower() == my_tag.lower().lstrip().rstrip():
                            tag_id.append(tag.guid)
                            break
            else:
                for tag in listtags:
                    if tag.name.lower() == trigger.tag.lower():
                        tag_id.append(tag.guid)
                        break
        return tag_id

    def set_tag(self, trigger, tag_id):
        """
            create a tag if not exists
        """
        # tagGUID does not exist:
        # create it if a tag has been provided
        if tag_id == 0 and trigger.tag is not '':
            new_tag = Types.Tag()
            new_tag.name = trigger.tag
            tag_id = self.note_store.createTag(new_tag).guid

        return tag_id

    def set_evernote_header(self):
        """
            preparing the hearder of Evernote
        """
        prolog = '<?xml version="1.0" encoding="UTF-8"?>'
        prolog += '<!DOCTYPE en-note SYSTEM \
        "http://xml.evernote.com/pub/enml2.dtd">\n'
        return prolog

    def get_sanitize_content(self, content):
        """
            tidy and sanitize content
        """
        enml = sanitize(content)
        # python 2
        if sys.version_info.major == 2:
            return enml.encode('ascii', 'xmlcharrefreplace')
        else:
            return str(enml)

    def set_note_title(self, data):
        """
            handle the title from the data
        """
        title = ''
        # if no title provided, fallback to the URL which should be provided
        # by any exiting service
        title = (data['title'] if 'title' in data else data['link'])
        # decode html entities if any
        title = HtmlEntities(title).html_entity_decode

        # python 2
        if sys.version_info.major == 2:
            title = title.encode('utf8', 'xmlcharrefreplace')

        return title

    def set_note_content(self, data):
        """
            handle the content from the data
        """
        content = ''
        if 'content' in data:
            if type(data['content']) is list or type(data['content']) is tuple\
               or type(data['content']) is dict:
                if 'value' in data['content'][0]:
                    content = data['content'][0].value
            else:
                if type(data['content']) is str:
                    content = data['content']
                else:
                    # if not str or list or tuple
                    # or dict it could be feedparser.FeedParserDict
                    # so get the item value
                    content = data['content']['value']

        elif 'summary_detail' in data:
            if type(data['summary_detail']) is list or\
               type(data['summary_detail']) is tuple or\
               type(data['summary_detail']) is dict:
                if 'value' in data['summary_detail'][0]:
                    content = data['summary_detail'][0].value
            else:
                if type(data['summary_detail']) is str:
                    content = data['summary_detail']
                else:
                    # if not str or list or tuple
                    # or dict it could be feedparser.FeedParserDict
                    # so get the item value
                    content = data['summary_detail']['value']

        elif 'description' in data:
            content = data['description']

        content = HtmlEntities(content).html_entity_decode

        return content

    def set_note_attribute(self, data):
        """
           add the link of the 'source' in the note
           get a NoteAttributes object
        """
        na = False
        if 'link' in data:
            na = Types.NoteAttributes()
            # add the url
            na.sourceURL = data['link']
            # add the object to the note
            return na

    def set_note_footer(self, data, trigger):
        """
            handle the footer of the note
        """
        footer = ''
        if 'link' in data:
            provided_by = _('Provided by')
            provided_from = _('from')
            footer_from = "<br/><br/>{} <em>{}</em> {} <a href='{}'>{}</a>"

            # python 2
            if sys.version_info.major == 2:
                description = trigger.trigger.description.encode(
                    'ascii', 'xmlcharrefreplace')
            else:
                description = trigger.trigger.description
            footer = footer_from.format(
                provided_by, description, provided_from,
                data['link'], data['link'])

        return footer

    def get_evernote_client(self, token=None):
        """
            get the token from evernote
        """
        if token:
            return EvernoteClient(
                token=token,
                sandbox=self.sandbox)
        else:
            return EvernoteClient(
                consumer_key=self.consumer_key,
                consumer_secret=self.consumer_secret,
                sandbox=self.sandbox)

    def auth(self, request):
        """
            let's auth the user to the Service
        """
        client = self.get_evernote_client()
        callback_url = 'http://%s%s' % (
            request.get_host(), reverse('evernote_callback'))
        request_token = client.get_request_token(callback_url)

        # Save the request token information for later
        request.session['oauth_token'] = request_token['oauth_token']
        request.session['oauth_token_secret'] = request_token[
            'oauth_token_secret']

        # Redirect the user to the Evernote authorization URL
        # return the URL string which will be used by redirect()
        # from the calling func
        return client.get_authorize_url(request_token)

    def callback(self, request):
        """
            Called from the Service when the user accept to activate it
        """
        try:
            client = self.get_evernote_client()
            # finally we save the user auth token
            # As we already stored the object ServicesActivated
            # from the UserServiceCreateView now we update the same
            # object to the database so :
            # 1) we get the previous objet
            us = UserService.objects.get(
                user=request.user,
                name=ServicesActivated.objects.get(name='ServiceEvernote'))
            # 2) then get the token
            us.token = client.get_access_token(
                request.session['oauth_token'],
                request.session['oauth_token_secret'],
                request.GET.get('oauth_verifier', '')
            )
            # 3) and save everything
            us.save()
        except KeyError:
            return '/'

        return 'evernote/callback.html'
