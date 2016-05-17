from __future__ import absolute_import

import re
import pytest
from . import preprocess


def test_email_regex():
    regex = preprocess.regexes['email']
    assert regex.search('stuff <something@something.com> stuff')
    assert regex.search('stuff something@something.com stuff')
    assert regex.search('stuff s.omet.hing@so.mething.com stuff')
    assert regex.search('stuff s.omet.+1hi2ng@so.m33eta$#12hing.co4#4m stuff')
    assert not regex.search('something@something')
    assert not regex.search('somethign @something.com')
    assert not regex.search(' this is not@ an.email stuff')


def test_html():
    regex = preprocess.regexes['html']
    assert regex.search('blah <this is some fake html> blah')
    assert re.sub(regex, ' ', 'blah < this is some fake html>').strip() == 'blah'


def test_url():
    regex = preprocess.regexes['url']
    assert regex.search('blah http://something.com/ blah')
    assert regex.search('somethign https://albjkhaer blah')


def test_normalize():
    url, email = preprocess.replacements['url'], preprocess.replacements['email']
    num, dollar = preprocess.replacements['number'], preprocess.replacements['dollar']
    html = preprocess.replacements['html']
    assert preprocess.normalize(u'something https://example.com else') == u'something ' + url + u' else'
    assert (preprocess.normalize(u'this is a something@something.com longer thing https://example.com and stuff') ==
            u'this is a ' + email + u' longer thing ' + url + u' and stuff')
    assert (preprocess.normalize(u'this has some n123umbers in23 23 it') ==
            u'this has some n' + num + 'umbers in' + num + ' ' + num + ' it')
    assert (preprocess.normalize(u'some <html stuff> $cash money $$</stuff>') ==
            u'some ' + html + ' ' + dollar + 'cash money ' + dollar + html)


def test_clean():
    assert (preprocess.clean(u'something with   ..some crap][   in a..the a;ihf; \n\n and \t stuff') ==
            u'something with some crap in a the a ihf and stuff')


def test_full():
    """This is a pretty dumb integration test but it will tell me if something breaks."""
    text = u'''
    this is https://website.com for an email <somethign@somethign.com> with some stuff for $123 dollars only!
    here is another sentence.
    lots of longing for things.
    <html>some html too!</html>
    '''
    out = preprocess.make_word_list(text)
    assert out == [u'',
                   u'this',
                   u'is',
                   u'httpaddr',
                   u'for',
                   u'an',
                   u'email',
                   u'with',
                   u'some',
                   u'stuff',
                   u'for',
                   u'dollar',
                   u'number',
                   u'dollar',
                   u'onli',
                   u'here',
                   u'is',
                   u'anoth',
                   u'sentenc',
                   u'lot',
                   u'of',
                   u'long',
                   u'for',
                   u'thing',
                   u'some',
                   u'html',
                   u'too',
                   u''
                   ]


if __name__ == '__main__':
    pytest.main(['-v', __file__])
