#cython: language_level=3

from cpython cimport bool
from libc.stdlib cimport free

cdef extern from 'cmark.h':
    int CMARK_OPT_SOURCEPOS
    int CMARK_OPT_HARDBREAKS
    int CMARK_OPT_NORMALIZE
    int CMARK_OPT_SMART
    int CMARK_OPT_SAFE
    char *cmark_markdown_to_html(const char *text, size_t len, int options)


def markdown_to_html(
    str text, bool sourcepos=False, bool hardbreaks=False,
    bool normalize=False, bool smart=False, bool safe=False
):
    cdef int options = 0
    if sourcepos:
        options |= CMARK_OPT_SOURCEPOS
    if hardbreaks:
        options |= CMARK_OPT_HARDBREAKS
    if normalize:
        options |= CMARK_OPT_NORMALIZE
    if smart:
        options |= CMARK_OPT_SMART
    if safe:
        options |= CMARK_OPT_SAFE

    md_bytes = text.encode('utf-8')
    result = cmark_markdown_to_html(md_bytes, len(md_bytes), options)
    result_py = result.decode('utf-8')
    free(result)
    return result_py
