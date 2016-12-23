#testing environment

#:towey!~mtowey@10.12.213.6 PRIVMSG bowtie :ping bowtie
#irc message format

import unittest
import functions
import spotipy
import db_functions

class SpotTests(unittest.TestCase):

    def test_parse_message(self):
        test_irc1 = ':towey!~mtowey@10.12.213.6 PRIVMSG bowtie :ping bowtie hey can you look at 01732845? it\'s about to breach'
        test_irc2 = '#:towey!~mtowey@10.12.213.6 PRIVMSG bowtie :ping bowtie hey can you look at 01732845 it\'s about to breach:'
        test_irc3 = ':towey!~mtowey@10.12.213.6 PRIVMSG bowtie :ping bowtie :hey :can::: you::::: :look at 01732845 it\'s about to breach:'

        test_message1 = 'ping bowtie hey can you look at 01732845? it\'s about to breach'
        test_message2 = 'ping bowtie hey can you look at 01732845 it\'s about to breach:'
        test_message3 = 'ping bowtie :hey :can::: you::::: :look at 01732845 it\'s about to breach:'

        test_parse1 = functions.parse_message(test_irc1)
        test_parse2 = functions.parse_message(test_irc2)
        test_parse3 = functions.parse_message(test_irc3)

        self.assertEqual(test_parse1, test_message1)
        self.assertEqual(test_parse2, test_message2)
        self.assertEqual(test_parse3, test_message3)

    def test_parse_case_number(self):
        test_case_message1 = ':towey!~mtowey@10.12.213.6 PRIVMSG bowtie :ping bowtie hey can you look at 01732845? it\'s about to breach'
        test_case_message2 = ':towey!~mtowey@10.12.213.6 PRIVMSG bowtie :ping bowtie hey can you look at 01732845 it\'s about to breach'
        test_case_message3 = ':towey!~mtowey@10.12.213.6 PRIVMSG bowtie :ping bowtie hey can you look at 01732845 it\'s about to breach:'
        test_case_message4 = ':cbeezy_gs4!~cboyd@10.13.249.182 PRIVMSG #kankore :01732845:'
        #split results: ['', 'cbeezy_gs4!~cboyd@10.13.249.182 PRIVMSG #kankore ', '01732845', '']
        test_case_message5 = ':bowtie!~sgreenbe@10.12.212.97 PRIVMSG #kankore :hdkjlsahdkjaskjncjnkcljn::::::::01732845"sadajij'
        test_case_message6 = 'PRIVMSG #spotland :!@#*!*#@JFKASD01732845JFLA000 0123MSL:GJGjaljsdjlkaj728: 7389:128921:8309182903 829398 :::: :: : '
        #split results: ['PRIVMSG #spotland ', '!@#*!*#@JFKASD01752243JFLA000 0123MSL', 'GJGjaljsdjlkaj728', ' 7389', '128921', '8309182903 829398 ', '', '', '', ' ', '', ' ', ' ']
        test_case_number = '01732845'

        self.assertEqual(test_case_number, functions.parse_case_number(test_case_message1))
        self.assertEqual(test_case_number, functions.parse_case_number(test_case_message2))
        self.assertEqual(test_case_number, functions.parse_case_number(test_case_message3))
        self.assertEqual(test_case_number, functions.parse_case_number(test_case_message4))
        self.assertEqual(test_case_number, functions.parse_case_number(test_case_message5))
        self.assertEqual(test_case_number, functions.parse_case_number(test_case_message6))

    def test_get_case(self):
        #test to make sure he doesn't talk to unifiedbot0
        test_case_message4 = ':unifiedbot0!~PircBotX@unified-ds.gsslab.rdu2.redhat.com PRIVMSG #kankore :[1401751620] nfs mount hangs after reboot : 12WoCust, WoCust [1521] [04Sev2] [Networking] | https://c.na7.visual.force.com/apex/Case_View?sbstr=01751620 | https://access.redhat.com/support/cases/internal/#/ascension/case/01751620'
        test_result = 'test passed!'
        self.assertEqual(test_result, functions.get_case(test_case_message4))

    def test_parse_name(self):
        test_case_message = ':unifiedbot0!~PircBotX@unified-ds.gsslab.rdu2.redhat.com PRIVMSG #kankore :[1401751620] nfs mount hangs after reboot : 12WoCust, WoCust [1521] [04Sev2] [Networking] | https://c.na7.visual.force.com/apex/Case_View?sbstr=01751620 | https://access.redhat.com/support/cases/internal/#/ascension/case/01751620'
        test_name = 'unifiedbot0'
        self.assertEqual(test_name, functions.parse_name(test_case_message))

    def test_get_spotify_track(self):
        test_song_title = 'Redbone'
        test_song_message = ':bowtie!~sgreenbe@10.12.212.97 PRIVMSG #spotland :!spotify tip toen in my jordans'
        
        test_spotify_url = functions.get_spotify_track(test_song_title)
        self.assertEqual(test_spotify_url, 'https://open.spotify.com/track/3kxfsdsCpFgN412fpnW85Y')

if __name__ == '__main__':
    unittest.main()
