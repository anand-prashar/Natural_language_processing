'''
Edited on Aug 25, 2017
@editor: anand
'''

import unittest
from limerick import LimerickDetector

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.ld = LimerickDetector()

    def test_rhyme(self):
        print 'RHYMETEST_BELOW'
        print self.ld.rhymes("defiance", "compliance")

    def test_syllables(self):
        s = []
        #try: self.assertEqual(self.ld.guess_syllables("dog"), 1)
        #except: s.append(1)
        try: self.assertEqual(self.ld.guess_syllables("asdf"), 1)
        except: s.append(2)
        try: self.assertEqual(self.ld.guess_syllables("letter"), 2)
        except: s.append(3)
        try: self.assertEqual(self.ld.guess_syllables("washington"), 3)
        except: s.append(4)
        try: self.assertEqual(self.ld.guess_syllables("dock"), 1)
        except: s.append(5)
        try: self.assertEqual(self.ld.guess_syllables("dangle"), 2)
        except: s.append(6)
        try: self.assertEqual(self.ld.guess_syllables("thrive"), 1)
        except: s.append(7)
        try: self.assertEqual(self.ld.guess_syllables("fly"), 1)
        except: s.append(8)
        try: self.assertEqual(self.ld.guess_syllables("placate"), 2)
        except: s.append(9)
        try: self.assertEqual(self.ld.guess_syllables("renege"), 2)
        except: s.append(10)
        
        try: self.assertEqual(self.ld.guess_syllables("advertisement"), 5)
        except: s.append(11)

        print '\nNumber of failed syllables tests:', str(len(s))
        if len(s)!=0: print 'Failed syllables tests:', ','.join([str(x) for x in s])

    def test_examples(self):

        a = """
a woman whose friends called a prude
on a lark when bathing all nude
saw a man come along
and unless we are wrong
you expected this line to be lewd
        """

        b = """while it's true all i've done is delay
in defense of myself i must say
today's payoff is great
while the workers all wait
"""

        c =  """
THIS THING IS SUPPOSED TO RHYME
BUT I SIMPLY DON'T GOT THE TIME
WHO CARES IF I MISS,
NOBODY WILL READ THIS
I'LL END THIS HERE POEM POTATO
"""

        d = """There was a young man named Wyatt
whose voice was exceedingly quiet
And then one day
it faded away"""

        e = """An exceedingly fat friend of mine,
When asked at what hour he'd dine,
Replied, "At eleven,     
At three, five, and seven,
And eight and a quarter past nine"""

        f = """A limerick fan from Australia
regarded his work as a failure:
his verses were fine
until the fourth line"""

        g = """There was a young lady one fall
Who wore a newspaper dress to a ball.
The dress caught fire
And burned her entire
Front page, sporting section and all."""

        h = "dog\ndog\ndog\ndog\ndog"
        
        i = """When we shook our hands with science
the digital era came in compliance
as algorithms came along
vision of computer became strong
it's enthralling to see that machine and humans have such a beautiful alliance"""


        
        s = []

        try: self.assertEqual(self.ld.is_limerick(a), True)
        except: s.append('a')
        try: self.assertEqual(self.ld.is_limerick(b), False)
        except: s.append('b')
        try: self.assertEqual(self.ld.is_limerick(c), False)
        except: s.append('c')
        try: self.assertEqual(self.ld.is_limerick(d), False)
        except: s.append('d')
        try: self.assertEqual(self.ld.is_limerick(f), False)
        except: s.append('e')
        try: self.assertEqual(self.ld.is_limerick(e), True)
        except: s.append('f')
        try: self.assertEqual(self.ld.is_limerick(g), True)
        except: s.append('g')
        try: self.assertEqual(self.ld.is_limerick(h), True)
        except: s.append('h')
        
        print self.ld.is_limerick(i)

        print 'Number of failed limerick tests:', str(len(s))
        if len(s)!=0: print 'Failed limerick tests:', ','.join(s)

if __name__ == '__main__':
    unittest.main()
