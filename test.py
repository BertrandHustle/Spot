#testing environment

#:towey!~mtowey@10.12.213.6 PRIVMSG bowtie :ping bowtie
#irc message format

import unittest
import functions
import spotipy

class SpotTests(unittest.TestCase):

    def test_parse_message(self):
        test_irc1 = '#:towey!~mtowey@10.12.213.6 PRIVMSG bowtie :ping bowtie hey can you look at 01732845? it\'s about to breach'
        test_irc2 = '#:towey!~mtowey@10.12.213.6 PRIVMSG bowtie :ping bowtie hey can you look at 01732845 it\'s about to breach:'

        test_message1 = 'ping bowtie hey can you look at 01732845? it\'s about to breach'
        test_message2 = 'ping bowtie hey can you look at 01732845 it\'s about to breach:'

        test_parse1 = functions.parse_message(test_irc1)
        test_parse2 = functions.parse_message(test_irc2)

        self.assertEqual(test_parse1, test_message1)
        self.assertEqual(test_parse2, test_message2)

    def test_parse_case_number(self):

        test_case_message1 = '#:towey!~mtowey@10.12.213.6 PRIVMSG bowtie :ping bowtie hey can you look at 01732845? it\'s about to breach'
        test_case_message2 = '#:towey!~mtowey@10.12.213.6 PRIVMSG bowtie :ping bowtie hey can you look at 01732845 it\'s about to breach'
        test_case_message3 = '#:towey!~mtowey@10.12.213.6 PRIVMSG bowtie :ping bowtie hey can you look at 01732845 it\'s about to breach:'

        case_number1 = functions.parse_case_number(test_case_message1)
        case_number2 = functions.parse_case_number(test_case_message2)
        case_number3 = functions.parse_case_number(test_case_message3)

        self.assertEqual(case_number1, '01732845')
        self.assertEqual(case_number2, '01732845')
        self.assertEqual(case_number3, '01732845')

    def test_get_spotify_track(self):

        test_song_title = 'Redbone'

        test_spotify_url = functions.get_spotify_track(test_song_title)

        self.assertEqual(test_spotify_url, 'https://open.spotify.com/track/47l9wxr6RwgoTSfnseBRcf')

if __name__ == '__main__':
    unittest.main()
