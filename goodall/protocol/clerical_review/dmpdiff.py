from collections import namedtuple
from enum import Enum

from .diff_match_patch import diff_match_patch


class DiffType(Enum):
    EQUAL = 'equal'
    DIFF = 'diff'
    TRANPOSE = 'transpose'
    INSERT = 'insert'
    DELETE = 'delete'

Diff = namedtuple('Diff', ['text_1', 'text_2', 'type'])

def is_transpose(front, middle, back):
    return (front[0] == DMPDiff.DIFF_DELETE or front[0] == DMPDiff.DIFF_INSERT) and middle[0] == DMPDiff.DIFF_EQUAL and back[0] == -front[0] and front[1] == back[1]


class DMPDiff(object):
    DIFF_DELETE = -1
    DIFF_INSERT = 1
    DIFF_EQUAL = 0

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.dmp = diff_match_patch()
        self.diff = self.dmp.diff_main(a, b)
        self.dmp.diff_cleanupSemantic(self.diff)
        self.process()

    def process(self):
        new_diff = []
        if len(self.diff) > 0:
            zip_diff = zip(self.diff, self.diff[1:] + [None], self.diff[2:] + [None] * 2)
            for front, middle, back in zip_diff:
                if front[0] == self.DIFF_EQUAL:
                    new_diff.append(Diff(front[1], front[1], DiffType.EQUAL))
                elif middle and front[0] == -middle[0]:
                    new_diff.append(Diff(front[1], middle[1], DiffType.DIFF))
                    next(zip_diff, None)
                elif middle and back and middle[0] == DMPDiff.DIFF_EQUAL and back[0] == -front[0] and front[1] == back[1]:
                    new_diff.append(Diff(front[1], middle[1], DiffType.TRANPOSE))
                    next(zip_diff, None)
                    next(zip_diff, None)
                elif front[0] == self.DIFF_INSERT:
                    new_diff.append(Diff(front[1], None, DiffType.INSERT))
                elif front[0] == self.DIFF_DELETE:
                    new_diff.append(Diff(None, front[1], DiffType.DELETE))
                else:
                    raise ValueError('uncaught sequence of diffs')

        self.processed_diff = new_diff

    def mask(self, f_equal = None, f_different = None, f_transpose = None, f_insert = None, f_delete = None):
        masked_diff = []

        for (text_1, text_2, difftype) in self.processed_diff:
            if difftype == DiffType.EQUAL:
                if f_equal:
                    masked_text_1, masked_text_2 = f_equal(text_1)
                else:
                    masked_text_1, masked_text_2 = (text_1, text_1)

            elif difftype == DiffType.DIFF:
                if f_different:
                    masked_text_1, masked_text_2 = f_different(text_1, text_2)
                else:
                    masked_text_1, masked_text_2 = (text_1, text_2)

            elif difftype == DiffType.TRANPOSE:
                if f_transpose:
                    masked_text_1, masked_text_2 = f_transpose(text_1, text_2)
                else:
                    masked_text_1, masked_text_2 = (text_1 + text_2, text_2 + text_1)

            elif difftype == DiffType.INSERT:
                if f_insert:
                    masked_text_1, masked_text_2 = f_insert(text_1)
                else:
                    masked_text_1, masked_text_2 = (text_1, '')

            elif difftype == DiffType.DELETE:
                if f_delete:
                    masked_text_1, masked_text_2 = f_delete(text_2)
                else:
                    masked_text_1, masked_text_2 = ('', text_2)

            masked_diff.append(Diff(masked_text_1, masked_text_2, difftype))

        self.masked_diff = masked_diff

    @property
    def num_changes(self):
        changes = 0

        for old, new in zip(self.processed_diff, self.masked_diff):
            if old.text_1:
                for old_char, new_char in zip(list(old.text_1), list(new.text_1)):
                    if old_char != new_char:
                        changes += 1

            if old.text_2:
                for old_char, new_char in zip(list(old.text_2), list(new.text_2)):
                    if old_char != new_char:
                        changes += 1

        return changes

    @property
    def html2(self):
        a = []
        b = []

        for (text_1, text_2, difftype) in self.masked_diff:
            text_1 = (text_1.replace("&", "&amp;").replace("<", "&lt;")
                    .replace(">", "&gt;").replace("\n", "&para;<br>"))
            text_2 = (text_2.replace("&", "&amp;").replace("<", "&lt;")
                    .replace(">", "&gt;").replace("\n", "&para;<br>"))

            if difftype == DiffType.EQUAL:
                a.append('<span>%s</span>' % text_1)
                b.append('<span>%s</span>' % text_2)
            elif difftype == DiffType.DIFF:
                a.append('<span class=\"text-danger\">%s</span>' % text_1)
                b.append('<span class=\"text-danger\">%s</span>' % text_2)
            elif difftype == DiffType.TRANPOSE:
                a.append('<span class=\"text-info\">%s</span>' % text_1)
                b.append('<span class=\"text-info\">%s</span>' % text_2)
            elif difftype == DiffType.INSERT:
                a.append('<span class=\"text-success\">%s</span>' % text_1)
                b.append('<span>%s</span>' % text_2)
            elif difftype == DiffType.DELETE:
                a.append('<span>%s</span>' % text_1)
                b.append('<span class=\"text-success\">%s</span>' % text_2)

        return ''.join(a), ''.join(b)

    @property
    def html(self):
        a = []
        b = []

        for (text_1, text_2, difftype) in self.masked_diff:
            text_1 = (text_1.replace("&", "&amp;").replace("<", "&lt;")
                    .replace(">", "&gt;").replace("\n", "&para;<br>"))
            text_2 = (text_2.replace("&", "&amp;").replace("<", "&lt;")
                    .replace(">", "&gt;").replace("\n", "&para;<br>"))

            if difftype == DiffType.EQUAL:
                a.append('<span>%s</span>' % text_1)
                b.append('<span>%s</span>' % text_2)
            elif difftype == DiffType.DIFF:
                a.append('<span class=\"text-diff\">%s</span>' % text_1)
                b.append('<span class=\"text-diff\">%s</span>' % text_2)
            elif difftype == DiffType.TRANPOSE:
                a.append('<span class=\"text-transpose\">%s</span>' % text_1)
                b.append('<span class=\"text-transpose\">%s</span>' % text_2)
            elif difftype == DiffType.INSERT:
                a.append('<span class=\"text-diff\">%s</span>' % text_1)
                b.append('<span>%s</span>' % text_2)
            elif difftype == DiffType.DELETE:
                a.append('<span>%s</span>' % text_1)
                b.append('<span class=\"text-diff\">%s</span>' % text_2)

        return ''.join(a), ''.join(b)
