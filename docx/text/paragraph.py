# encoding: utf-8

"""
Paragraph-related proxy types.
"""

from __future__ import (
    absolute_import, division, print_function, unicode_literals
)

from ..enum.style import WD_STYLE_TYPE
from ..enum.text import WD_LINE_SPACING
from .run import Run
from ..shared import ElementProxy, Emu, Length, Parented, Pt, Twips


class Paragraph(Parented):
    """
    Proxy object wrapping ``<w:p>`` element.
    """
    def __init__(self, p, parent):
        super(Paragraph, self).__init__(parent)
        self._p = p

    def add_run(self, text=None, style=None):
        """
        Append a run to this paragraph containing *text* and having character
        style identified by style ID *style*. *text* can contain tab
        (``\\t``) characters, which are converted to the appropriate XML form
        for a tab. *text* can also include newline (``\\n``) or carriage
        return (``\\r``) characters, each of which is converted to a line
        break.
        """
        r = self._p.add_r()
        run = Run(r, self)
        if text:
            run.text = text
        if style:
            run.style = style
        return run

    @property
    def alignment(self):
        """
        A member of the :ref:`WdParagraphAlignment` enumeration specifying
        the justification setting for this paragraph. A value of |None|
        indicates the paragraph has no directly-applied alignment value and
        will inherit its alignment value from its style hierarchy. Assigning
        |None| to this property removes any directly-applied alignment value.
        """
        return self._p.alignment

    @alignment.setter
    def alignment(self, value):
        self._p.alignment = value

    def clear(self):
        """
        Return this same paragraph after removing all its content.
        Paragraph-level formatting, such as style, is preserved.
        """
        self._p.clear_content()
        return self

    def insert_paragraph_before(self, text=None, style=None):
        """
        Return a newly created paragraph, inserted directly before this
        paragraph. If *text* is supplied, the new paragraph contains that
        text in a single run. If *style* is provided, that style is assigned
        to the new paragraph.
        """
        paragraph = self._insert_paragraph_before()
        if text:
            paragraph.add_run(text)
        if style is not None:
            paragraph.style = style
        return paragraph

    @property
    def runs(self):
        """
        Sequence of |Run| instances corresponding to the <w:r> elements in
        this paragraph.
        """
        return [Run(r, self) for r in self._p.r_lst]

    @property
    def style(self):
        """
        Paragraph style for this paragraph. Read/Write.
        """
        style_id = self._p.style
        return self.part.get_style(style_id, WD_STYLE_TYPE.PARAGRAPH)

    @style.setter
    def style(self, style_or_name):
        style_id = self.part.get_style_id(
            style_or_name, WD_STYLE_TYPE.PARAGRAPH
        )
        self._p.style = style_id

    @property
    def text(self):
        """
        String formed by concatenating the text of each run in the paragraph.
        Tabs and line breaks in the XML are mapped to ``\\t`` and ``\\n``
        characters respectively.

        Assigning text to this property causes all existing paragraph content
        to be replaced with a single run containing the assigned text.
        A ``\\t`` character in the text is mapped to a ``<w:tab/>`` element
        and each ``\\n`` or ``\\r`` character is mapped to a line break.
        Paragraph-level formatting, such as style, is preserved. All
        run-level formatting, such as bold or italic, is removed.
        """
        text = ''
        for run in self.runs:
            text += run.text
        return text

    @text.setter
    def text(self, text):
        self.clear()
        self.add_run(text)

    def _insert_paragraph_before(self):
        """
        Return a newly created paragraph, inserted directly before this
        paragraph.
        """
        p = self._p.add_p_before()
        return Paragraph(p, self._parent)


class ParagraphFormat(ElementProxy):
    """
    Provides access to paragraph formatting such as justification,
    indentation, line spacing, space before and after, and widow/orphan
    control.
    """

    __slots__ = ()

    @property
    def alignment(self):
        """
        A member of the :ref:`WdParagraphAlignment` enumeration specifying
        the justification setting for this paragraph. A value of |None|
        indicates paragraph alignment is inherited from the style hierarchy.
        """
        pPr = self._element.pPr
        if pPr is None:
            return None
        return pPr.jc_val

    @alignment.setter
    def alignment(self, value):
        pPr = self._element.get_or_add_pPr()
        pPr.jc_val = value

    @property
    def line_spacing(self):
        """
        |float| or |Length| value specifying the space between baselines in
        successive lines of the paragraph. A value of |None| indicates line
        spacing is inherited from the style hierarchy. A float value, e.g.
        ``2.0`` or ``1.75``, indicates spacing is applied in multiples of
        line heights. A |Length| value such as ``Pt(12)`` indicates spacing
        is a fixed height. The |Pt| value class is a convenient way to apply
        line spacing in units of points. Assigning |None| resets line spacing
        to inherit from the style hierarchy.
        """
        pPr = self._element.pPr
        if pPr is None:
            return None
        return self._line_spacing(pPr.spacing_line, pPr.spacing_lineRule)

    @line_spacing.setter
    def line_spacing(self, value):
        pPr = self._element.get_or_add_pPr()
        if value is None:
            pPr.spacing_line = None
            pPr.spacing_lineRule = None
        elif isinstance(value, Length):
            pPr.spacing_line = value
            if pPr.spacing_lineRule != WD_LINE_SPACING.AT_LEAST:
                pPr.spacing_lineRule = WD_LINE_SPACING.EXACTLY
        else:
            pPr.spacing_line = Emu(value * Twips(240))
            pPr.spacing_lineRule = WD_LINE_SPACING.MULTIPLE

    @property
    def line_spacing_rule(self):
        """
        A member of the :ref:`WdLineSpacing` enumeration indicating how the
        value of :attr:`line_spacing` should be interpreted. Assigning any of
        the :ref:`WdLineSpacing` members :attr:`SINGLE`, :attr:`DOUBLE`, or
        :attr:`ONE_POINT_FIVE` will cause the value of :attr:`line_spacing`
        to be updated to produce the corresponding line spacing.
        """
        pPr = self._element.pPr
        if pPr is None:
            return None
        return self._line_spacing_rule(
            pPr.spacing_line, pPr.spacing_lineRule
        )

    @property
    def space_after(self):
        """
        |Length| value specifying the spacing to appear between this
        paragraph and the subsequent paragraph. |None| indicates this value
        is inherited from the style hierarchy. |Length| objects provide
        convenience properties, such as :attr:`~.Length.pt` and
        :attr:`~.Length.inches`, that allow easy conversion to various length
        units.
        """
        pPr = self._element.pPr
        if pPr is None:
            return None
        return pPr.spacing_after

    @space_after.setter
    def space_after(self, value):
        self._element.get_or_add_pPr().spacing_after = value

    @property
    def space_before(self):
        """
        |Length| value specifying the spacing to appear between this
        paragraph and the prior paragraph. |None| indicates this value is
        inherited from the style hierarchy. |Length| objects provide
        convenience properties, such as :attr:`~.Length.pt` and
        :attr:`~.Length.cm`, that allow easy conversion to various length
        units.
        """
        pPr = self._element.pPr
        if pPr is None:
            return None
        return pPr.spacing_before

    @space_before.setter
    def space_before(self, value):
        self._element.get_or_add_pPr().spacing_before = value

    @staticmethod
    def _line_spacing(spacing_line, spacing_lineRule):
        """
        Return the line spacing value calculated from the combination of
        *spacing_line* and *spacing_lineRule*. Returns a |float| number of
        lines when *spacing_lineRule* is ``WD_LINE_SPACING.MULTIPLE``,
        otherwise a |Length| object of absolute line height is returned.
        Returns |None| when *spacing_line* is |None|.
        """
        if spacing_line is None:
            return None
        if spacing_lineRule == WD_LINE_SPACING.MULTIPLE:
            return spacing_line / Pt(12)
        return spacing_line

    @staticmethod
    def _line_spacing_rule(line, lineRule):
        """
        Return the line spacing rule value calculated from the combination of
        *line* and *lineRule*. Returns special members of the
        :ref:`WdLineSpacing` enumeration when line spacing is single, double,
        or 1.5 lines.
        """
        if lineRule == WD_LINE_SPACING.MULTIPLE:
            if line == Twips(240):
                return WD_LINE_SPACING.SINGLE
            if line == Twips(360):
                return WD_LINE_SPACING.ONE_POINT_FIVE
            if line == Twips(480):
                return WD_LINE_SPACING.DOUBLE
        return lineRule
