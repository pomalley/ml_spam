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


def test_header():
    assert 'return-path' not in preprocess.strip_header(sample_email).lower()


def test_clean():
    assert (preprocess.clean(u'something with   ..some crap][   in a..the a;ihf; \n\n and \t stuff') ==
            u'something with some crap in a the a ihf and stuff')


def test_full():
    """This is a pretty dumb integration test but it will tell me if something breaks."""
    text = u'''from: someone
    header: stuff
    header_more: stuff again

    this is https://website.com for an email <somethign@somethign.com> with some stuff for $123 dollars only!
    here is another sentence.
    lots of longing for things.
    <html>some html too!</html>
    '''
    out = preprocess.make_word_list(text)
    assert out == [u'this',
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
                   u'too',]



# sample spam email from SpamAssassin public corpus
sample_email = u'''From mikeedo@emailisfun.com  Wed Jun 27 04:56:45 2001
Return-Path: <mikeedo@emailisfun.com>
Delivered-To: yyyy@netnoteinc.com
Received: from ns.mediline.co.in (unknown [203.197.32.212]) by
    mail.netnoteinc.com (Postfix) with ESMTP id 43F82130028 for
    <jm7@netnoteinc.com>; Wed, 27 Jun 2001 04:56:44 +0100 (IST)
Received: from gw02_[192.168.224.26] ([4.16.194.53]) by ns.mediline.co.in
    with Microsoft SMTPSVC(5.0.2195.1600); Wed, 27 Jun 2001 09:28:59 +0530
Received: from mail3.emailisfun.com by gw02 with ESMTP; Tue,
    26 Jun 2001 23:01:39 -0400
Message-Id: <00007409198a$00006e26$00006c63@mail3.emailisfun.com>
To: <mikeedo@emailisfun.com>
From: mikeedo@emailisfun.com
Subject: You Won The First Round! claim#	9462               27747
Date: Tue, 26 Jun 2001 23:01:34 -0400
MIME-Version: 1.0
Content-Transfer-Encoding: quoted-printable
X-Priority: 3
X-Msmail-Priority: Normal
Reply-To: wjilknmv@polbox.com
X-Originalarrivaltime: 27 Jun 2001 03:59:00.0584 (UTC) FILETIME=[7F62F680:
    01C0FEBD]


<html>

<body>

<p align=3D"center" style=3D"word-spacing: 0; margin-top: 0; margin-bottom=
: 0"><font size=3D"5" color=3D"#FF0000"><b>You Have Won The First Round!</=
b></font></p>
<p align=3D"center" style=3D"word-spacing: 0; margin-top: 0; margin-bottom=
: 0"><b><font size=3D"5" color=3D"#FF0000">Claim Your Entry Now!</font></b=
></p>
<p align=3D"center" style=3D"word-spacing: 0; margin-top: 0; margin-bottom=
: 0"><font size=3D"5" color=3D"#FF0000"><b>Collect The Prize Of The Week!<=
/b></font></p>
<p align=3D"center" style=3D"word-spacing: 0; margin-top: 0; margin-bottom=
: 0"><font size=3D"5" color=3D"#FF0000"><b><a href=3D"http://vdfe.weedwaac=
ker.com">Click Here To Collect!</a></b></font></p>

<p align=3D"center" style=3D"word-spacing: 0; margin-top: 0; margin-bottom=
: 0">&nbsp;</p>

<p align=3D"center"><font size=3D"1">We apologize for any email you may ha=
ve
inadvertently received.<br>
Please <a href=3D"http://rmkid.weedwaacker.com">CLICK HERE</a> to be remov=
ed from
future mailings.</font></p>

</body>

</html>
'''


if __name__ == '__main__':
    pytest.main(['-v', __file__])
