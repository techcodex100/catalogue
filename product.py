from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import Optional
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from io import BytesIO
import os
from datetime import datetime
import requests

app = FastAPI()

# ------------ SETTINGS -----------------
# Static image size for all images in the catalog (in points)
IMAGE_WIDTH = 240
IMAGE_HEIGHT = 160

# ------------ MODELS -----------------
class CompanyData(BaseModel):
    name: str
    website: Optional[str] = ""
    address: Optional[str] = ""
    phone: Optional[str] = ""
    email: Optional[str] = ""

class ProductData(BaseModel):
    name: str
    hs_code: Optional[str] = ""
    quantity: Optional[str] = ""
    unit: Optional[str] = ""
    fcl_type: Optional[str] = ""
    packaging: Optional[str] = ""
    quantity_per_fcl: Optional[str] = ""
    description: Optional[str] = ""
    specifications: Optional[str] = ""
    image_path: Optional[str] = ""
    client_name: Optional[str] = ""
    rate: Optional[str] = ""
    expiry_date: Optional[str] = ""
    company: Optional[CompanyData] = None


# ------------ HEADER / FOOTER -----------------
def header_footer(canvas, doc, company: CompanyData):
    width, height = A4
    canvas.saveState()

    # Header Left
    if company and company.website:
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.grey)
        canvas.drawString(40, height - 30, company.website)

    # Header Right
    if company and company.name:
        canvas.setFont("Helvetica-Bold", 12)
        canvas.setFillColor(colors.black)
        canvas.drawRightString(width - 40, height - 30, company.name.upper())

    # Sub Header
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.black)
    canvas.drawRightString(width - 40, height - 43, "Product Catalog")

    # Footer
    if company:
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.black)
        footer_text = f"{company.name}, {company.address or ''}"
        canvas.drawCentredString(width / 2, 30, footer_text)

        contact_text = " • ".join(filter(None, [
            f"Tel: {company.phone}" if company.phone else "",
            f"Email: {company.email}" if company.email else ""
        ]))
        if contact_text:
            canvas.drawCentredString(width / 2, 18, contact_text)

    canvas.restoreState()


# ------------ ROUTES -----------------
@app.get("/")
def home():
    return {"message": "Catalog PDF Generator is running. Use POST /generate-catalog-pdf/"}


def _build_pdf_bytes(data: ProductData) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4, rightMargin=40, leftMargin=40,
        topMargin=80, bottomMargin=60
    )
    elements = []
    styles = getSampleStyleSheet()

    # Title
    title_style = ParagraphStyle('title_style', parent=styles['Heading1'],
                                 alignment=1, textColor=colors.darkblue)
    elements.append(Paragraph(data.name.upper(), title_style))
    elements.append(Spacer(1, 20))

    # Description (single paragraph)
    if data.description:
        elements.append(Paragraph("<b>Description:</b>", styles['Heading3']))
        desc_html = data.description.replace("\n", "<br/>")
        elements.append(Paragraph(desc_html, styles['Normal']))
        elements.append(Spacer(1, 12))

    # Specifications (single paragraph)
    if data.specifications:
        elements.append(Paragraph("<b>Specifications:</b>", styles['Heading3']))
        specs_html = data.specifications.replace("\n", "<br/>")
        elements.append(Paragraph(specs_html, styles['Normal']))
        elements.append(Spacer(1, 12))

    # Additional Details
    extra_details = []
    if data.client_name:
        extra_details.append(("Client Name", data.client_name))
    if data.rate:
        extra_details.append(("Rate", data.rate))
    if data.expiry_date:
        extra_details.append(("Expiry Date", data.expiry_date))

    if extra_details:
        elements.append(Paragraph("<b>Additional Details:</b>", styles['Heading3']))
        table = Table(extra_details, colWidths=[120, 300])
        table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.grey),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 12))

    # Product Details
    details = [
        ("HS Code", data.hs_code),
        ("Quantity", data.quantity),
        ("Unit", data.unit),
        ("FCL Type", data.fcl_type),
        ("Packaging", data.packaging),
        ("Quantity per FCL", data.quantity_per_fcl)
    ]
    details = [d for d in details if d[1]]
    if details:
        elements.append(Paragraph("<b>Product Details:</b>", styles['Heading3']))
        table = Table(details, colWidths=[120, 300])
        table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.grey),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 20))

    # Single Image
    if data.image_path:
        elements.append(Paragraph("<b>Image:</b>", styles['Heading3']))
        base_dir = os.path.dirname(__file__)
        raw_path = (data.image_path or "").strip().strip('"').strip("'")
        try:
            # Support file:// URLs for local absolute paths
            if raw_path.lower().startswith("file://"):
                # Normalize file URL to local path, handle both file:///C:/... and file://C:/...
                file_part = raw_path.replace("file://", "").lstrip("/")
                raw_path = file_part

            if raw_path.lower().startswith(("http://", "https://")):
                safe_url = raw_path.replace(" ", "%20")
                resp = requests.get(safe_url, timeout=10)
                resp.raise_for_status()
                img_bytes = BytesIO(resp.content)
                image_reader = ImageReader(img_bytes)
                im = Image(image_reader, width=IMAGE_WIDTH, height=IMAGE_HEIGHT)
                elements.append(im)
                elements.append(Spacer(1, 10))
            else:
                # Normalize local path variants to maximize success on Windows
                candidates = []
                # Expand ~ and environment vars
                expanded = os.path.expandvars(os.path.expanduser(raw_path))
                normalized = os.path.normpath(expanded)
                candidates.append(normalized)
                if not os.path.isabs(normalized):
                    candidates.append(os.path.normpath(os.path.join(base_dir, normalized)))
                # Try swapping slashes as a fallback
                swapped = normalized.replace("\\", "/")
                if swapped != normalized:
                    candidates.append(swapped)
                    if not os.path.isabs(swapped):
                        candidates.append(os.path.join(base_dir, swapped))

                chosen_path = None
                for candidate in candidates:
                    if os.path.exists(candidate):
                        chosen_path = candidate
                        break

                if chosen_path:
                    im = Image(chosen_path, width=IMAGE_WIDTH, height=IMAGE_HEIGHT)
                    elements.append(im)
                    elements.append(Spacer(1, 10))
                else:
                    print(f"File not found. Tried: {candidates}")
                    elements.append(Paragraph("Image not found at the provided path.", styles['Italic']))
        except Exception as e:
            print(f"Image error: {e}")
            elements.append(Paragraph("Image could not be rendered.", styles['Italic']))

    # Build PDF with header/footer
    doc.build(
        elements,
        onFirstPage=lambda canv, doc: header_footer(canv, doc, data.company),
        onLaterPages=lambda canv, doc: header_footer(canv, doc, data.company)
    )
    buffer.seek(0)
    return buffer.read()


@app.post("/generate-catalog-pdf/")
async def generate_catalog_pdf(data: ProductData):
    filename = f"Catalog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf_bytes = _build_pdf_bytes(data)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

if __name__ == "__main__":
    import uvicorn
    # Run with: py product.py  or  python product.py
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)