#!/usr/bin/python3
import sys


class CharacterSet:
    # Some arbitrary character that's not part of the set of available characters
    repeatCharacter = 'µ'
    # UK typeable characters, because I'm British
    characterSet = "1234567890-=!\"£$%^&*()_+qwertyuiop[]QWERTYUIOP{" \
                   "}asdfghjkl;'#ASDFGHJKL:@~\\zxcvbnm,./ |ZXCVBNM<>?" + repeatCharacter


class Grid:
    columns = 12
    rows = 8
    assert (len(CharacterSet.characterSet) == rows * columns)
    output = ''
    charactersRemaining = CharacterSet.characterSet
    lines = []

    def __init__(self, k=''):
        self.key = k
        while len(self.key) > 0:
            self.nextChar = self.key[0]
            self.output = self.output + self.nextChar
            self.key = self.key.replace(self.nextChar, '')
            self.charactersRemaining = self.charactersRemaining.replace(self.nextChar, '')
        while len(self.charactersRemaining) > 0:
            self.nextChar = self.charactersRemaining[0]
            self.output = self.output + self.nextChar
            self.key = self.key.replace(self.nextChar, '')
            self.charactersRemaining = self.charactersRemaining.replace(self.nextChar, '')
        assert (len(self.output) == self.rows * self.columns)
        self.gather_lines()

    def gather_lines(self):
        self.lines = []
        for i in range(self.rows):
            row_start = self.columns * i
            row_finish = self.columns * (i + 1)
            self.lines.append(self.output[row_start:row_finish])

    def encrypt(self, digram):
        assert (len(digram) == 2)
        il = digram[0]
        ir = digram[1]
        if il == ir:
            ir = CharacterSet.repeatCharacter
        for line in self.lines:
            if line.find(il) > -1:
                left_column = line.find(il)
                left_row = line
            if line.find(ir) > -1:
                right_column = line.find(ir)
                right_row = line
        if left_row == right_row:
            l, r = left_row[(left_column + 1) % self.columns], right_row[(right_column + 1) % self.columns]
        else:
            if left_column == right_column:
                l, r = self.lines[(self.lines.index(left_row) + 1) % self.rows][left_column], \
                       self.lines[(self.lines.index(right_row) + 1) % self.rows][right_column]
            else:
                l, r = left_row[right_column], right_row[left_column]
        if r == CharacterSet.repeatCharacter:
            r = l
        return l + r

    def decrypt(self, digram):
        assert (len(digram) == 2)
        il = digram[0]
        ir = digram[1]
        if il == ir:
            ir = CharacterSet.repeatCharacter
        for line in self.lines:
            if line.find(il) > -1:
                left_column = line.find(il)
                left_row = line
            if line.find(ir) > -1:
                right_column = line.find(ir)
                right_row = line
        if left_row == right_row:
            l, r = left_row[(left_column - 1) % self.columns], right_row[(right_column - 1) % self.columns]
        else:
            if left_column == right_column:
                l, r = self.lines[(self.lines.index(left_row) - 1) % self.rows][left_column], \
                       self.lines[(self.lines.index(right_row) - 1) % self.rows][right_column]
            else:
                l, r = left_row[right_column], right_row[left_column]
        if r == CharacterSet.repeatCharacter:
            r = l
        return l + r

    def encrypt_string(self, cleartext):
        ct = cleartext
        cyphertext = ''
        if len(ct) % 2 == 1:
            ct = ct + CharacterSet.repeatCharacter
        for i in range(len(ct) // 2):
            cyphertext = cyphertext + self.encrypt(ct[i * 2:(i * 2) + 2])
        return cyphertext

    def decrypt_string(self, cyphertext):
        ct = cyphertext
        cleartext = ''
        if len(ct) % 2 == 1:
            ct = ct + CharacterSet.repeatCharacter
        for i in range(len(ct) // 2):
            cleartext = cleartext + self.decrypt(ct[i * 2:(i * 2) + 2])
        return cleartext


def main():
    if len(sys.argv) == 1:
        print("Specify a key and, optionally, a message to encrypt")
        exit(1)
    grid = Grid(sys.argv[1])
    if len(sys.argv) == 2:
        for line in grid.lines:
            print('  '.join(line))
    if len(sys.argv) == 3:
        print(grid.encrypt_string(sys.argv[2]))
    if len(sys.argv) == 4 and sys.argv[2] == '-d':
        print(grid.decrypt_string(sys.argv[3]))


main()
