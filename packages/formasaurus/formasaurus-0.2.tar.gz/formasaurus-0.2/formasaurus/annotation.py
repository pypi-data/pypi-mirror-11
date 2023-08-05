# -*- coding: utf-8 -*-
"""
HTML forms interactive annotation utilities.
"""
from __future__ import absolute_import
import sys
import os
from six.moves.urllib.request import urlopen
from six.moves import input

import lxml.html
from lxml.html.clean import Cleaner

from formasaurus.storage import Storage, FORM_TYPES, load_html, FORM_TYPES_INV


def annotate_forms(data_folder, url_argument):
    """
    Run an interactive HTML form annotation tool.

    The process is to download a web page, display all HTML forms and for
    each form ask user about form type. The result is saved on disk:
    web page is stored as a html file and the URL and the annotation
    results are added to index.json file.
    """
    storage = Storage(data_folder)
    html, url = load_data(url_argument)
    doc = load_html(html, url)
    answers = _annotate_forms(storage, doc)
    if answers:
        storage.store_result(html, answers, url)


def check_annotated_data(data_folder):
    """
    Check that annotated data is correct; exit with code 1 if it is not.
    """
    storage = Storage(data_folder)
    ok = storage.check()
    storage.print_type_counts()
    if not ok:
        sys.exit(1)


def load_data(url_or_path):
    """
    Load binary data from a local file or an url;
    return (data, url) tuple.
    """
    if os.path.exists(url_or_path):
        raise NotImplementedError("Re-annotation is not supported yet")
        # with open(url_or_path, 'rb') as f:
        #     return f.read(), None
    else:
        return urlopen(url_or_path).read(), url_or_path


def print_form_html(form):
    """ Print a cleaned up version of <form> HTML contents """
    cleaner = Cleaner(
        forms=False,
        javascript=True,
        scripts=True,
        style=True,
        allow_tags={'form', 'input', 'textarea', 'label', 'option',
                    'select', 'submit', 'a'},
        remove_unknown_tags=False,
    )
    raw_html = lxml.html.tostring(form, pretty_print=True, encoding="unicode")
    html = cleaner.clean_html(raw_html)
    lines = [line.strip() for line in html.splitlines(False) if line.strip()]
    print("\n".join(lines))


def print_form_types(types):
    print("\nAllowed form types and their shortcuts:")
    for full_name, shortcuts in types.items():
        print("  %s %s" % (shortcuts, full_name))
    print("")


def _annotate_forms(storage, doc, form_types=None):
    """
    For each form element ask user whether it is a login form or not.
    Return an array with True/False answers.
    """
    forms = doc.xpath("//form")
    if not forms:
        print("Page has no forms.")
        return []
    else:
        print("Page has %d form(s)" % len(forms))

    fingerprints = storage.get_fingerprints()

    if form_types is None:
        form_types = FORM_TYPES

    print_form_types(form_types)
    shortcuts = "/".join(form_types.values())

    res = []
    for idx, form in enumerate(forms, 1):

        fp = storage.get_fingerprint(form)
        if fp in fingerprints:
            xpath = "//form[%d]" % idx
            tp = FORM_TYPES_INV[fingerprints[fp]]
            print("Skipping duplicate form %-10s %r" % (xpath, tp))
            res.append("X")
            continue

        print_form_html(form)

        while True:
            tp = input("\nPlease enter the form type (%s) "
                       "or ? for help: " % shortcuts).strip()
            if tp == '?':
                print_form_types(form_types)
                continue
            if tp not in set(shortcuts):
                print("Please enter one of the following "
                      "letters: %s. You entered %r" % (shortcuts, tp))
                continue
            res.append(tp)
            break

        print("="*40)

    if all(r == 'X' for r in res):
        print("Page has no new forms.")
        return []
    return res
