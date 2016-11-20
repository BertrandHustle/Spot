#testing environment

#:towey!~mtowey@10.12.213.6 PRIVMSG bowtie :ping bowtie
#irc message format

import unittest
import functions

class SpotTests(unittest.TestCase):

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

if __name__ == '__main__':
    unittest.main()
