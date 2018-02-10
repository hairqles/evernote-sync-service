import unittest
from parser import ENMLToHTML

class TestENMLToHTML(unittest.TestCase):

    def test_convert_table_to_p(self):
        content = "<table><tbody><tr><td><p>Foo<b>Bold</b></p><p>Bar</p></td></tr><tr><td>Row2</td></tr></tbody></table>"
        output = "<p>Foo<b>Bold</b></p><p>Bar</p><p>Row2</p>"
        html = ENMLToHTML(content)
        self.assertEqual(unicode(html), output)

    def test_convert_strong_to_b(self):
        content = "<strong>Foo</strong>"
        output = "<b>Foo</b>"
        html = ENMLToHTML(content)
        self.assertEqual(unicode(html), output)

    def test_strip_tags(self):
        content = "<div><font>Foo</font></div>"
        output = "Foo"
        html = ENMLToHTML(content)
        self.assertEqual(unicode(html), output)

    def test_strip_attributes(self):
        content = "<p style=\"foo bar\" id=\"fo\">Foo</p>"
        output = "<p>Foo</p>"
        html = ENMLToHTML(content)
        self.assertEqual(unicode(html), output)
        
    def test_strip_empty_tags(self):
        content = "<p>\n      \n</p>"
        output = ""
        html = ENMLToHTML(content)
        self.assertEqual(unicode(html), output)

if __name__ == '__main__':
    unittest.main()

# <p>Foo<b>Bold</b></p><p>Bar</p><p>Row2</p>
# <p>Foo<b>Bold</b></p><p>Bar</p><p>Row2</p>