# my_password_generator
A password generator inspired by xkcd #936

# Usage

## Default dictionary

If you don't specify the dictionary, the script will use the file dictionary.txt in the same directory of the script.

## Custom dictionary

The following command returns 4 random words from the linux english dictionary
```shell
$ python3.6 generate.py dictionary=/usr/share/dict/british-english
threaded putsches absinth slenderness
```

## Output any number of words

If you want a specific number of words, use the parameter `words`
```shell
$ python3.6 generate.py words=2
flyleaves objections
```

## Import dictionaries

If you want to import some other dictionaries in the default one, use the following command:
```shell
$ python3.6 generate.py import=/usr/share/dict/british-english
$ python3.6 generate.py
penury Taiyuan decrees deplaned
```

## Remove hard-to-digit words from dictionary

You can also remove the words that are difficult to digit.
An easy-to-digit word is a word conaining letters that you have to digit alternatively with one hand and the other.
Example: "panama" is a simple-digit word because you type the "p" with the right hand, the "a" with the left hand and so on: left-right-left-right...
```shell
$ python3.6 generate.py remove_from_dictionary=hard_to_digit
$ python3.6 generate.py
flair Shanghai Alan rusk
```
