"""Unit tests for source.py.

Most of the tests are in testdata/. This is just a few things that are too small
for full testdata tests.
"""

__author__ = ['Ryan Barrett <granary@ryanb.org>']

import re

from granary import microformats2
from granary import testutil


class Microformats2Test(testutil.HandlerTest):

  def test_properties_override_h_as_article(self):
    for prop, verb in ('like-of', 'like'), ('repost-of', 'share'):
      obj = microformats2.json_to_object(
        {'type': ['h-entry', 'h-as-note'],
          'properties': {prop: ['http://foo/bar']}})
      self.assertEquals('activity', obj['objectType'])
      self.assertEquals(verb, obj['verb'])

  def test_verb_require_of_suffix(self):
    for prop in 'like', 'repost':
      obj = microformats2.json_to_object(
        {'type': ['h-entry', 'h-as-note'],
         'properties': {prop: ['http://foo/bar']}})
      self.assertNotIn('verb', obj)

  def test_h_as_article(self):
    obj = microformats2.json_to_object({'type': ['h-entry', 'h-as-article']})
    self.assertEquals('article', obj['objectType'])

  def test_html_content_and_summary(self):
    for expected_content, expected_summary, value in (
        ('my html', 'my val', {'value': 'my val', 'html': 'my html'}),
        ('my html', None, {'html': 'my html'}),
        ('my val', 'my val', {'value': 'my val'}),
        ('my str', 'my str', 'my str'),
        (None, None, {})):
      obj = microformats2.json_to_object({'properties': {'content': value,
                                                         'summary': value}})
      self.assertEquals(expected_content, obj.get('content'))
      self.assertEquals(expected_summary, obj.get('summary'))

  def test_photo_property_is_not_url(self):
    """handle the case where someone (incorrectly) marks up the caption
    with p-photo
    """
    mf2 = {'properties':
           {'photo': ['the caption', 'http://example.com/image.jpg']}}
    obj = microformats2.json_to_object(mf2)
    self.assertEquals('http://example.com/image.jpg', obj['image']['url'])

  def test_photo_property_has_no_url(self):
    """handle the case where the photo property is *only* text, not a url"""
    mf2 = {'properties':
           {'photo': ['the caption', 'alternate text']}}
    obj = microformats2.json_to_object(mf2)
    self.assertFalse(obj.get('image'))

  def test_nested_compound_url_object(self):
    mf2 = {'type': ['h-as-repost'],
           'properties': {
             'repost-of': [{
               'type': ['h-outer'],
               'properties': {
                 'url': [{
                   'type': ['h-inner'],
                   'properties': {'url': ['http://nested']},
                 }],
               },
             }],
           }}
    obj = microformats2.json_to_object(mf2)
    self.assertEquals('http://nested', obj['object']['url'])

  def test_object_to_json_unescapes_html_entities(self):
    self.assertEquals({
      'type': ['h-entry'],
      'properties': {'content': [{
        'html': 'Entity &lt; <a href="http://my/link">link too</a>',
        'value': 'Entity < link too',
      }]},
     }, microformats2.object_to_json({
        'content': 'Entity &lt; link too',
        'tags': [{'url': 'http://my/link', 'startIndex': 12, 'length': 8}]
      }))

  def test_object_to_json_note_with_in_reply_to(self):
    self.assertEquals({
      'type': ['h-entry'],
      'properties': {
        'content': [{
          'html': '@hey great post',
          'value': '@hey great post',
        }],
        'in-reply-to': ['http://reply/target'],
      },
    }, microformats2.object_to_json({
        'content': '@hey great post',
      }, ctx={
        'inReplyTo': [{
          'url': 'http://reply/target',
        }]
      }))

  def test_object_to_html_note_with_in_reply_to(self):
    expected = """\
<article class="h-entry">
<span class="u-uid"></span>
<div class="e-content p-name">
@hey great post
</div>
<a class="u-in-reply-to" href="http://reply/target"></a>
</article>
"""
    result = microformats2.object_to_html({
      'content': '@hey great post',
    }, ctx={
      'inReplyTo': [{
        'url': 'http://reply/target',
      }]
    })
    self.assertEquals(re.sub('\n\s*', '\n', expected),
                      re.sub('\n\s*', '\n', result))

  def test_render_content_link_with_image(self):
    self.assert_equals("""\
foo
<p>
<a class="link" href="http://link">
<img class="thumbnail" src="http://image" alt="name" />
<span class="name">name</span>
</a>
</p>""", microformats2.render_content({
        'content': 'foo',
        'tags': [{
          'objectType': 'article',
          'url': 'http://link',
          'displayName': 'name',
          'image': {'url': 'http://image'},
        }]
      }))

  def test_render_content_converts_newlines_to_brs(self):
    self.assert_equals("""\
foo<br />
bar<br />
<a href="http://baz">baz</a>
""", microformats2.render_content({
  'content': 'foo\nbar\nbaz',
  'tags': [{'url': 'http://baz', 'startIndex': 8, 'length': 3}]
}))

  def test_render_content_omits_tags_without_urls(self):
    self.assert_equals("""\
foo
<a class="tag" href="http://baz">baz</a>
<a class="tag" href="http://baj"></a>
""", microformats2.render_content({
        'content': 'foo',
        'tags': [{'displayName': 'bar'},
                 {'url': 'http://baz', 'displayName': 'baz'},
                 {'url': 'http://baj'},
               ],
      }))

  def test_render_content_location(self):
    self.assert_equals("""\
foo
<div class="h-card p-location">
  <div class="p-name"><a class="u-url" href="http://my/place">My place</a></div>

</div>
""", microformats2.render_content({
        'content': 'foo',
        'location': {
          'displayName': 'My place',
          'url': 'http://my/place',
        }
      }))

  def test_escape_html_attribute_values(self):
    self.assert_equals("""\
<article class="h-entry">
<span class="u-uid"></span>

<div class="h-card p-author">
<div class="p-name">a " b ' c</div>
<img class="u-photo" src="img" alt="" />
</div>

<div class="e-content p-name">

<p>
<img class="thumbnail" src="img" alt="d &amp; e" />
<span class="name">d & e</span>
</p>
</div>

</article>""", microformats2.object_to_html({
        'author': {'image': {'url': 'img'}, 'displayName': 'a " b \' c'},
        'attachments': [{'image': {'url': 'img'}, 'displayName': 'd & e'}],
      }))

  def test_mention_and_hashtag(self):
    self.assert_equals("""
<a class="p-category" href="http://c"></a>
<a class="u-mention" href="http://m">m</a>""",
                       microformats2.render_content({
        'tags': [{'objectType': 'mention', 'url': 'http://m', 'displayName': 'm'},
                 {'objectType': 'hashtag', 'url': 'http://c'}],
      }))

  def test_get_string_urls(self):
    for expected, objs in (
        ([], []),
        (['asdf'], ['asdf']),
        ([], [{'type': 'h-ok'}]),
        ([], [{'properties': {'url': ['nope']}}]),
        ([], [{'type': ['h-ok'], 'properties': {'no': 'url'}}]),
        (['good1', 'good2'], ['good1',
                            {'type': ['h-ok']},
                            {'type': ['h-ok'], 'properties': {'url': ['good2']}}]),
        (['nested'], [{'type': ['h-ok'], 'properties': {'url': [
            {'type': ['h-nested'], 'url': ['nested']}]}}]),
        ):
      self.assertEquals(expected, microformats2.get_string_urls(objs))

  def test_img_blank_alt(self):
    self.assertEquals('<img class="bar" src="foo" alt="" />',
                      microformats2.img('foo', 'bar', None))
