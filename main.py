# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import itertools


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def xor(text, key):
    infkey = itertools.chain.from_iterable(itertools.repeat(key))
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(text, infkey))


encrypted_passwd = '\x0b\x04\x0a\x18\x12\x16\x19\x01'
key = 'key2decrypt2decrypt'

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    encrypted_passwd = '\x0b\x04\x0a\x18\x12\x16\x19\x01'
    key = 'key'

    print_hi( xor(encrypted_passwd, key))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
