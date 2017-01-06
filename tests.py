#!/usr/bin/env python3.6

import unittest
from unittest.mock import patch, call, Mock, mock_open as mock_mock_open
from unittest import skip
import tempfile, generate, os

class TestFunctional(unittest.TestCase):

    def test_can_generate_password_from_specific_filename(self):
        # Horse create a new file containing a lot of words
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(b'correct\nhorse\nbattery\nstaple')
        dict_file_name = temp_file.name
        temp_file.close()

        # Horse then executes the password generator to use that dictionary
        args = [f'dictionary={dict_file_name}']
        output = generate.run(args)

        # The script outputs 4 random words from the dictionary
        self.assertIn('correct', output)
        self.assertIn('horse', output)
        self.assertIn('battery', output)
        self.assertIn('staple', output)

        os.remove(dict_file_name)

    def test_can_create_dictionary_from_other_file(self):
        try:
            os.remove('dictionary.txt')
        except FileNotFoundError:
            pass

        # Mrs. Staple wants to create a special dictionary for her passwords
        ## create a random file containing various words
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(b'panama\npal\nwow\nlake\nhello\nuseless')
        dict_file_name = temp_file.name
        temp_file.close()

        # She first calls the script to import a dictionary
        output = generate.run(f'import={dict_file_name}'.split())
        self.assertEqual('', output.strip())

        # Then Mrs Staple calls the script telling to keep only the words that are easy to digit (LRLRLR)
        output = generate.run('remove_from_dictionary=hard_to_digit'.split())
        self.assertEqual('', output.strip())

        # In the end, executing the script without parameters it returns an easy password to digit
        output = generate.run()
        self.assertIn('panama', output)
        self.assertIn('pal', output)
        self.assertIn('wow', output)
        self.assertIn('lake', output)
        self.assertNotIn('hello', output)
        self.assertNotIn('useless', output)

        os.remove(dict_file_name)
        os.remove('dictionary.txt')


class TestPasswordGenerator(unittest.TestCase):

    @patch('generate.open')
    def test_uses_default_dictionary(self, mock_open):
        mock_open.side_effect = FileNotFoundError()
        generate.run()
        self.assertEqual(mock_open.call_args[0], ('dictionary.txt',))
        generate.run([])
        self.assertEqual(mock_open.call_args[0], ('dictionary.txt',))

    @patch('generate.open')
    def test_uses_custom_dictionary(self, mock_open):
        mock_open.side_effect = FileNotFoundError()
        args = ['dictionary=use_this_dictionary']
        generate.run(args)
        self.assertEqual(mock_open.call_args[0], ('use_this_dictionary',))

    def test_returns_error_if_dictionary_file_does_not_exists(self):
        args = ['dictionary=use_this_dictionary']
        output = generate.run(args)
        self.assertIn('Dictionary file does not exists', output)

class TestImportDictionary(unittest.TestCase):

    def test_import_from_another_dictionary_to_default_one(self):
        m = mock_mock_open(read_data='word1\nword2') # TODO: mock_mock_open it's a very ugly name
        m.set_return_value = 'file'

        with patch('generate.open', m):
            generate.run(f'import=import_file_name'.split())

        self.assertIn(call('import_file_name', 'r'), m.mock_calls)
        self.assertIn(call('dictionary.txt', 'a'), m.mock_calls)
        handle = m()
        self.assertIn(call('word1\nword2'), handle.write.mock_calls)

class TestRemoveFromDictUsingRules(unittest.TestCase):

    def test_identify_words_easy_to_digit(self):
        ''' An easy-to-digit word is a word conaining letters that you have to digit alternatively with one hand and
            the other.
            Example: "panama" is a simple-digit word because you type the "p" with the right hand, the "a" with the left
            hand and so on: left-right-left-right...
        '''
        self.assertEqual(generate.is_easy_to_digit('panama'), True)
        self.assertEqual(generate.is_easy_to_digit('panamal'), True)
        self.assertEqual(generate.is_easy_to_digit('lap'), True)
        self.assertEqual(generate.is_easy_to_digit('pool'), False)
        self.assertEqual(generate.is_easy_to_digit('alwoo'), False)

    def test_easy_to_digit_is_case_insensitive(self):
        ''' An easy-to-digit word is a word conaining letters that you have to digit alternatively with one hand and
            the other.
            Example: "panama" is a simple-digit word because you type the "p" with the right hand, the "a" with the left
            hand and so on: left-right-left-right...
        '''
        self.assertEqual(generate.is_easy_to_digit('pANama'), True)
        self.assertEqual(generate.is_easy_to_digit('pOoL'), False)

    def test_can_remove_hard_to_digit_words(self):
        m = mock_mock_open(read_data='panama\npal\nwow\nlake\nhello\nuseless') # TODO: mock_mock_open it's a very ugly name

        with patch('generate.open', m):
            generate.run(f'remove_from_dictionary=hard_to_digit'.split())

        handle = m()
        self.assertIn(call('dictionary.txt', 'r'), m.mock_calls)
        self.assertIn(call('dictionary.txt', 'w'), m.mock_calls)
        write_call_parameters = ' '.join([','.join(c[0]) for c in handle.write.call_args_list])
        self.assertIn('panama', write_call_parameters)
        self.assertIn('pal', write_call_parameters)
        self.assertIn('wow', write_call_parameters)
        self.assertIn('lake', write_call_parameters)
        self.assertNotIn('hello', write_call_parameters)
        self.assertNotIn('useless', write_call_parameters)


if __name__ == '__main__':
    unittest.main()