from abc import ABC, abstractmethod
import random
import string

from .dmpdiff import DMPDiff


class Mask(ABC):
    minimum_disclosure = True

    def __init__(self, append_original=False, html=False):
        self.append_original = append_original
        self.html = html
        self.init_mask()

    def apply(self, a, b):
        diff = DMPDiff(a, b)
        diff.mask(f_equal=self.mask_equal, f_different=self.mask_different, f_transpose=self.mask_transpose, f_insert=self.mask_insert, f_delete=self.mask_delete)
        num_changes = diff.num_changes

        new_a, new_b = diff.html if self.html else diff.safe

        if self.append_original:
            if len(a) > 0:
                new_a = '{} ({})'.format(new_a, a)
            if len(b) > 0:
                new_b = '{} ({})'.format(new_b, b)  

        return new_a, new_b, num_changes

    def init_mask(self):
        pass

    @abstractmethod
    def mask_equal(self, text):
        pass

    @abstractmethod
    def mask_different(self, text_1, text_2):
        pass

    @abstractmethod
    def mask_transpose(self, substring_1, substring_2):
        pass

    @abstractmethod
    def mask_insert(self, text):
        pass

    @abstractmethod
    def mask_delete(self, text):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

class MinimalMask(Mask):
    name = 'Minimal Mask'

    def init_mask(self):
        pass

    def mask_equal(self, text):
        return text, text

    def mask_different(self, text_1, text_2):

        return text_1, text_2

    def mask_transpose(self, substring_1, substring_2):
        return substring_1 + substring_2, substring_2 + substring_1

    def mask_insert(self, text):
        return text, ''

    def mask_delete(self, text):
        return '', text

class BaselineMask(MinimalMask):
    name = 'No Mask'
    minimum_disclosure = False


class RandomAlphabetMask(Mask):
    name = 'Random Alphabet Mask'

    def init_mask(self):
        digits = list(string.digits)
        random.shuffle(digits)

        alphabet_lower = list(string.ascii_lowercase)
        random.shuffle(alphabet_lower)

        self.alphabet = {}

        for key, value in zip(string.ascii_lowercase, alphabet_lower):
            self.alphabet[key] = value
            self.alphabet[key.upper()] = value.upper()

        for key, value in zip(string.digits, digits):
            self.alphabet[key] = value

    def mask_equal(self, text):
        text = ''.join(self.alphabet[character] if character in self.alphabet.keys() else character for character in text)

        return text, text

    def mask_different(self, text_1, text_2):
        text_1 = ''.join(self.alphabet[character] if character in self.alphabet.keys() else character for character in text_1) 
        text_2 = ''.join(self.alphabet[character] if character in self.alphabet.keys() else character for character in text_2) 

        len_1 = len(text_1)
        len_2 = len(text_2)

        if len_1 > len_2:
            text_2 = text_2 + '_' * (len_1 - len_2)
        elif len_2 > len_1:
            text_1 = text_1 + '_' * (len_2 - len_1)

        return text_1, text_2

    def mask_transpose(self, substring_1, substring_2):
        text_1 = ''.join(self.alphabet[character] if character in self.alphabet.keys() else character for character in substring_1 + substring_2) 
        text_2 = ''.join(self.alphabet[character] if character in self.alphabet.keys() else character for character in substring_2 + substring_1) 

        return text_1, text_2

    def mask_insert(self, text):
        text = ''.join(self.alphabet[character] if character in self.alphabet.keys() else character for character in text) 

        return text, '_' * len(text)

    def mask_delete(self, text):
        text = ''.join(self.alphabet[character] if character in self.alphabet.keys() else character for character in text) 

        return '_' * len(text), text


class DifferenceMask(Mask):
    name = 'Difference Mask'

    def mask_equal(self, text):
        text = ''.join('*' if character.isalnum() else character for character in text)

        return text, text

    def mask_different(self, text_1, text_2):
        len_1 = len(text_1)
        len_2 = len(text_2)

        if len_1 > len_2:
            text_2 = text_2
        elif len_2 > len_1:
            text_1 = text_1

        return text_1, text_2

    def mask_transpose(self, substring_1, substring_2):
        return substring_1 + substring_2, substring_2 + substring_1

    def mask_insert(self, text):
        return text, ''

    def mask_delete(self, text):
        return '', text


class FullMask(Mask):
    name = 'Full Mask'

    def mask_equal(self, text):
        text = ''.join('*' if character.isalnum() else character for character in text)

        return text, text

    def mask_different(self, text_1, text_2):
        len_1 = len(text_1)
        len_2 = len(text_2)

        text_1 = 'X' * len_1
        text_2 = 'X' * len_2

        if len_1 > len_2:
            text_2 = text_2
        elif len_2 > len_1:
            text_1 = text_1

        return text_1, text_2

    def mask_transpose(self, substring_1, substring_2):
        substring_1 = 'A' * len(substring_1)
        substring_2 = 'B' * len(substring_2)

        return substring_1 + substring_2, substring_2 + substring_1

    def mask_insert(self, text):
        return 'X' * len(text), ''

    def mask_delete(self, text):
        return '', 'X' * len(text)

MASKS = {
    'none': BaselineMask,
    'minimal': MinimalMask,
    #'random_alphabet': RandomAlphabetMask,
    'difference': DifferenceMask,
    'full': FullMask,
}

def create_mask(mask_name:str) -> Mask:
    """
    Create a mask object based on the given mask name.

    :param mask_name: The name of the mask to create.
    :return: An instance of the corresponding Mask class.
    :raises ValueError: If the mask name is not in the MASKS dictionary.
    """
    if mask_name not in MASKS:
        raise ValueError(
            f"Invalid mask name '{mask_name}'. Valid options are: {', '.join(MASKS.keys())}")

    # Retrieve the mask class and instantiate it
    mask_class = MASKS[mask_name]
    return mask_class()