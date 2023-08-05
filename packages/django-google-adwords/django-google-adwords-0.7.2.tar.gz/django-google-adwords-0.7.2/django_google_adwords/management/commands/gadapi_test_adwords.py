from __future__ import print_function
from django.core.management.base import BaseCommand, CommandError
from ...helper import paged_request


class Command(BaseCommand):
    args = '[ideas|stats]'
    help = "Test connection to Google Adwords API for the GetTargetingIdeaService."

    def handle(self, *args, **options):
        keywords = ['seo', 'adwords', 'adwords seo']

        if len(args) == 0:
            raise CommandError("Expected args %s." % self.args)

        request_type = args[0]

        if request_type == 'ideas':
            selector = {
                'searchParameters': [
                    {
                        'xsi_type': 'RelatedToQuerySearchParameter',
                        'queries': keywords
                    },
                    {
                        'xsi_type': 'LanguageSearchParameter',
                        'languages': [{'id': '1000'}]
                    },
                    {
                        'xsi_type': 'LocationSearchParameter',
                        'locations': [{'id': '2036'}]
                    },
                ],
                'ideaType': 'KEYWORD',
                'requestType': 'IDEAS',
                'requestedAttributeTypes': ['KEYWORD_TEXT', 'SEARCH_VOLUME'],
            }
        elif request_type == 'stats':
            selector = {
                'searchParameters': [
                    {
                        'xsi_type': 'RelatedToQuerySearchParameter',
                        'queries': keywords
                    },
                    {
                        'xsi_type': 'LanguageSearchParameter',
                        'languages': [{'id': '1000'}]
                    },
                    {
                        'xsi_type': 'LocationSearchParameter',
                        'locations': [{'id': '2036'}]
                    },
                ],
                'ideaType': 'KEYWORD',
                'requestType': 'STATS',
                'requestedAttributeTypes': ['KEYWORD_TEXT', 'SEARCH_VOLUME'],
            }
        else:
            raise CommandError('Unknown request type: %s' % request_type)

        for (data, selector) in paged_request('GetTargetingIdeaService', selector):
            print(data)
