#!/usr/bin/env python3.6

import unittest
from unittest.mock import patch
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


if __name__ == '__main__':
    unittest.main()