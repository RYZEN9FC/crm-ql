INVOICE MODULE - CONTINUATION BUILD

What was added
- Manager-only Invoices module and Invoice Settings page.
- Search/select a company from Contacts to prefill Bill To details.
- Prefilled Bill To fields remain editable per invoice without overwriting the saved company.
- Ship To defaults to Bill To, but can be changed.
- Dynamic line items (item/service, SAC/code, quantity, rate, tax).
- Editable CGST, SGST, received amount, notes and terms.
- Automatic financial-year invoice numbering using your configurable prefix.
- Invoice history stored in SQLite as snapshots, so later contact changes do not change old invoices.
- PDF download based on the layout/logic of the supplied invoice generator.
- Company Contacts now store Billing Address, GSTIN and PAN for future invoice prefilling.
- Default QuantumLoop seller/bank details seeded from the supplied invoice generator and editable in Invoice Settings.

Install
  pip install -r requirements.txt

Run
  python app.py

Then log in as a manager. The database migrations run automatically at startup.
