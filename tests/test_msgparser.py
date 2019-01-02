from unittest import TestCase

from modules.msg_parser import get_messages


class ParserTest(TestCase):
    def test_comments(self):
        text = '''\
           # comment 0
           :key
              # comment 1
        
        value
                
        # comment2
        '''

        self.assertEqual(get_messages(text), {'key': 'value'})
