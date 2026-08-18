from io import BytesIO
import os
from html import escape

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    HRFlowable,
    Image,
)

REG = 'Helvetica'
BOLD = 'Helvetica-Bold'
ITALIC = 'Helvetica-Oblique'


def e(v):
    return escape(str(v or ''))


def money(v):
    return f"{float(v or 0):,.2f}"


def amount_to_words(n):
    n = int(round(float(n or 0)))
    if n == 0:
        return 'Zero Rupees'

    ones = [
        '', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven',
        'Eight', 'Nine', 'Ten', 'Eleven', 'Twelve', 'Thirteen',
        'Fourteen', 'Fifteen', 'Sixteen', 'Seventeen', 'Eighteen',
        'Nineteen'
    ]
    tens = [
        '', '', 'Twenty', 'Thirty', 'Forty', 'Fifty',
        'Sixty', 'Seventy', 'Eighty', 'Ninety'
    ]

    def two(x):
        return ones[x] if x < 20 else tens[x // 10] + (
            (' ' + ones[x % 10]) if x % 10 else ''
        )

    def three(x):
        return (
            ones[x // 100] + ' Hundred' +
            ((' ' + two(x % 100)) if x % 100 else '')
        ) if x >= 100 else two(x)

    parts = []
    for div, label in [
        (10000000, 'Crore'),
        (100000, 'Lakh'),
        (1000, 'Thousand')
    ]:
        q, n = divmod(n, div)
        if q:
            parts.append(f'{three(q)} {label}')

    if n:
        parts.append(three(n))

    return ' '.join(parts) + ' Rupees'


def build_invoice_pdf(
    company,
    bill_to,
    ship_to,
    invoice_no,
    date_str,
    items,
    notes,
    terms,
    bank,
    cgst_pct,
    sgst_pct,
    received_amount,
    igst_pct=0,
    tax_mode='INTRA',
    ship_state=''
):
    buf = BytesIO()
    styles = getSampleStyleSheet()

    small = ParagraphStyle(
        'small',
        parent=styles['Normal'],
        fontSize=8.5,
        leading=11,
        fontName=REG,
    )

    doc = SimpleDocTemplate(
        buf,
        pagesize=A4,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
    )

    story = []

    company_block = Paragraph(
        f"<b>{e(company['name'])}</b><br/>"
        f"{e(company.get('address_lines'))}<br/>"
        + (
            f"GSTIN: {e(company.get('gstin'))}<br/>"
            if company.get('gstin') else ''
        )
        + (
            f"PAN: {e(company.get('pan'))}<br/>"
            if company.get('pan') else ''
        )
        + (
            f"<b>{e(company.get('website'))}</b>"
            if company.get('website') else ''
        ),
        small,
    )

    inv = Paragraph(
        f"<b>TAX INVOICE</b><br/><br/>"
        f"Invoice No. : {e(invoice_no)}<br/>"
        f"Invoice Date : {e(date_str)}",
        small,
    )

    t = Table(
        [[company_block, inv]],
        colWidths=[105 * mm, 74 * mm],
    )
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story += [t, Spacer(1, 8 * mm)]

    def party(label, p):
        return Paragraph(
            f"<b>{label}</b><br/><br/>"
            f"<b>{e(p.get('name'))}</b><br/>"
            f"{e(p.get('address_lines'))}<br/>"
            + (
                f"State: {e(p.get('state'))}<br/>"
                if p.get('state') else ''
            )
            + (
                f"GSTIN: {e(p.get('gstin'))}<br/>"
                if p.get('gstin') else ''
            )
            + (
                f"PAN: {e(p.get('pan'))}<br/>"
                if p.get('pan') else ''
            )
            + (
                f"<b>{e(p.get('website'))}</b>"
                if p.get('website') else ''
            ),
            small,
        )

    t = Table(
        [[party('BILL TO', bill_to), party('SHIP TO', ship_to)]],
        colWidths=[89.5 * mm, 89.5 * mm],
    )
    t.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story += [t, Spacer(1, 8 * mm)]

    rows = [['S.NO.', 'ITEMS', 'SAC', 'QTY.', 'RATE', 'TAX', 'AMOUNT']]
    taxable = 0

    for i, it in enumerate(items, 1):
        qty = float(it.get('qty') or 0)
        rate = float(it.get('rate') or 0)
        tax = float(it.get('tax_pct') or 0)
        pretax = qty * rate
        taxable += pretax
        amount = pretax * (1 + tax / 100)

        item = Paragraph(
            f"<b>{e(it.get('name'))}</b>"
            + (
                f"<br/><font size=7 color='#777777'>"
                f"S.CODE: {e(it.get('code'))}</font>"
                if it.get('code') else ''
            ),
            small,
        )

        rows.append([
            str(i),
            item,
            e(it.get('code')) or '-',
            f'{qty:g}',
            money(rate),
            f'{tax:g}%',
            money(amount),
        ])

    tbl = Table(
        rows,
        colWidths=[
            12 * mm, 68 * mm, 18 * mm, 14 * mm,
            24 * mm, 15 * mm, 28 * mm
        ],
    )
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f0f0f0')),
        ('FONTNAME', (0, 0), (-1, -1), REG),
        ('FONTNAME', (0, 0), (-1, 0), BOLD),
        ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (3, 0), (-1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LINEBELOW', (0, 0), (-1, 0), .75, colors.HexColor('#cccccc')),
        ('LINEBELOW', (0, 1), (-1, -1), .4, colors.HexColor('#eeeeee')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(tbl)

    is_interstate = str(tax_mode or '').upper() == 'INTER'
    cgst = 0 if is_interstate else taxable * float(cgst_pct or 0) / 100
    sgst = 0 if is_interstate else taxable * float(sgst_pct or 0) / 100
    igst = taxable * float(igst_pct or 0) / 100 if is_interstate else 0
    grand = taxable + cgst + sgst + igst
    balance = grand - float(received_amount or 0)

    subtotal_tax = cgst + sgst + igst
    tax_label = 'IGST' if is_interstate else 'CGST + SGST'

    st = Table(
        [['SUBTOTAL', tax_label, money(subtotal_tax), money(grand)]],
        colWidths=[94 * mm, 18 * mm, 24 * mm, 43 * mm],
    )
    st.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f7f7f7')),
        ('FONTNAME', (0, 0), (-1, -1), BOLD),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (2, 0), (-1, -1), 'RIGHT'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story += [st, Spacer(1, 6 * mm)]

    left = []

    if notes:
        left.append(
            f'<b>NOTES</b><br/>{e(notes)}<br/><br/>'
        )

    if terms:
        left.append(
            '<b>TERMS AND CONDITIONS</b><br/>'
            + '<br/>'.join(
                f'• {e(x)}' for x in terms if x.strip()
            )
        )

    totals = [
        ['Taxable Amount', money(taxable)],
    ]
    if is_interstate:
        totals.append([f'IGST@{float(igst_pct):g}%', money(igst)])
    else:
        totals.extend([
            [f'CGST@{float(cgst_pct):g}%', money(cgst)],
            [f'SGST@{float(sgst_pct):g}%', money(sgst)],
        ])
    totals.extend([
        ['Total Amount', money(grand)],
        ['Received Amount', money(received_amount)],
        ['Balance', money(balance)],
    ])

    tt = Table(totals, colWidths=[38 * mm, 40 * mm])
    tt.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (-1, -1), REG),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 3), (-1, 3), BOLD),
        ('FONTNAME', (0, 5), (-1, 5), BOLD),
        ('LINEABOVE', (0, 3), (-1, 3), .75, colors.HexColor('#999999')),
        ('LINEABOVE', (0, 5), (-1, 5), .75, colors.HexColor('#999999')),
    ]))

    words = Paragraph(
        f'<i>Total Amount (in words):</i><br/>'
        f'{amount_to_words(grand)}',
        ParagraphStyle(
            'words',
            parent=small,
            alignment=TA_RIGHT,
            fontSize=8,
        ),
    )

    right = Table(
        [[tt], [Spacer(1, 4)], [words]],
        colWidths=[78 * mm],
    )

    left_paragraph = Paragraph(''.join(left), small)

    bt = Table(
        [[left_paragraph, right]],
        colWidths=[100 * mm, 79 * mm],
    )
    bt.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))

    story += [
        bt,
        Spacer(1, 10 * mm),
        HRFlowable(width='100%', color=colors.HexColor('#dddddd')),
        Spacer(1, 5 * mm),
    ]

    # ---------------------------------------------------------
    # BANK DETAILS + SIGNATURE
    #
    # Do not use KeepTogether inside a Table cell here.
    # ReportLab can calculate an enormous row height when a
    # KeepTogether contains an image + flowables in a table cell.
    # A nested table gives ReportLab a normal, measurable height.
    # ---------------------------------------------------------

    bankp = Paragraph(
        f"<b>BANK DETAILS</b><br/>"
        f"Name: {e(bank.get('name'))}<br/>"
        f"IFSC Code: {e(bank.get('ifsc'))}<br/>"
        f"Account No.: {e(bank.get('account_no'))}<br/>"
        f"Bank: {e(bank.get('bank'))}"
        + (
            f"<br/>UPI ID: {e(bank.get('upi_id'))}"
            if bank.get('upi_id') else ''
        ),
        small,
    )

    sig_style = ParagraphStyle(
        'sig',
        parent=small,
        alignment=TA_RIGHT,
    )

    signature_rows = []

    logo_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'static',
        'logo.png'
    )

    if os.path.exists(logo_path):
        logo = Image(
            logo_path,
            width=42 * mm,
            height=42 * mm * 326 / 2048,
        )
        logo.hAlign = 'RIGHT'
        signature_rows.append([logo])
        signature_rows.append([Spacer(1, 4 * mm)])

    signature_rows.append([
        Paragraph(
            f"Authorised Signature for<br/>"
            f"<b>{e(company['name'])}</b>",
            sig_style,
        )
    ])

    signature_table = Table(
        signature_rows,
        colWidths=[74 * mm],
    )
    signature_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'RIGHT'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))

    ft = Table(
        [[bankp, '', signature_table]],
        colWidths=[80 * mm, 25 * mm, 74 * mm],
        hAlign='LEFT',
    )

    ft.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))

    story.append(ft)

    doc.build(story)
    buf.seek(0)
    return buf