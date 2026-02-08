from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from PIL import Image as PILImage

PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN = 2 * cm
LINE_HEIGHT = 14  # line height for code and text

def create_assignment_pdf(filename, cover_info, blocks):
    """
    Generate a PDF assignment with cover page and content blocks.
    Args:
        filename (str): Output PDF file path.
        cover_info (dict): Cover page information (university, student info, logo, etc.).
        blocks (list): List of content blocks (dicts with type=text/code/image).
    """
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = PAGE_WIDTH, PAGE_HEIGHT

    # ---------------- COVER PAGE ----------------
    draw_cover_page(c, cover_info)
    c.showPage()

    # ---------------- CONTENT BLOCKS ----------------
    y = height - MARGIN
    for block in blocks:
        try:
            block_type = block.get("type")
            if block_type == "text" and block.get("content"):
                y = draw_text_block(c, block["content"], y)
            elif block_type == "code" and block.get("content"):
                y = draw_code_block(c, block["content"], y)
            elif block_type == "image" and block.get("file"):
                y = draw_image_block(c, block["file"], y)
        except Exception as e:
            print(f"[Warning] Skipping block due to error: {e}")

    c.save()


# ---------------- COVER PAGE ----------------
def draw_cover_page(c, info):
    width, height = PAGE_WIDTH, PAGE_HEIGHT

    # Draw logo if exists
    if info.get("logo"):
        try:
            logo_file = info["logo"]
            if hasattr(logo_file, "seek"):
                logo_file.seek(0)
            logo = PILImage.open(logo_file)
            logo_width = 6 * cm
            aspect = logo.height / logo.width
            logo_height = logo_width * aspect
            c.drawInlineImage(logo, (width - logo_width)/2, height - 8*cm, logo_width, logo_height)
        except Exception as e:
            print(f"[Warning] Could not load logo: {e}")

    # University name
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width/2, height-10*cm, info.get("university", "University Name"))

    # Assignment title
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width/2, height-12*cm, info.get("assignment_title", "Assignment Title"))

    # Student info
    c.setFont("Helvetica", 14)
    y = height - 14*cm
    info_items = ["student_name", "roll_number", "department", "course", "professor", "submission_date"]
    for item in info_items:
        c.drawString(MARGIN, y, f"{item.replace('_',' ').title()}: {info.get(item,'')}")
        y -= 1*cm


# ---------------- CONTENT BLOCKS ----------------
def draw_text_block(c, text, y_start):
    width, height = PAGE_WIDTH, PAGE_HEIGHT
    c.setFont("Helvetica", 12)
    y = y_start
    lines = text.split("\n")
    for line in lines:
        c.drawString(MARGIN, y, line)
        y -= LINE_HEIGHT
        if y < MARGIN:
            c.showPage()
            y = height - MARGIN
            c.setFont("Helvetica", 12)
    return y - 14  # spacing after block


def draw_code_block(c, code, y_start):
    width, height = PAGE_WIDTH, PAGE_HEIGHT
    c.setFont("Courier", 10)
    y = y_start
    lines = code.split("\n")
    for line in lines:
        wrapped_lines = [line[i:i+90] for i in range(0, len(line), 90)]  # wrap long lines
        for wline in wrapped_lines:
            c.drawString(MARGIN, y, wline)
            y -= LINE_HEIGHT
            if y < MARGIN:
                c.showPage()
                y = height - MARGIN
                c.setFont("Courier", 10)
    return y - 14


def draw_image_block(c,img_file, y_start):
    width, height = PAGE_WIDTH, PAGE_HEIGHT
    y = y_start

    if img_file is None:
        return y

    if hasattr(img_file, "seek"):
        img_file.seek(0)

    try:
        img = PILImage.open(img_file)
    except Exception as e:
        print(f"[Warning] Skipping invalid image: {e}")
        return y

    max_width = width - 2*MARGIN
    max_height = y - MARGIN
    aspect = img.height / img.width

    if max_width * aspect > max_height:
        img_height = max_height
        img_width = img_height / aspect
    else:
        img_width = max_width
        img_height = img_width * aspect

    if y - img_height < MARGIN:
        c.showPage()
        y = height - MARGIN
        max_height = y - MARGIN
        if max_width * aspect > max_height:
            img_height = max_height
            img_width = img_height / aspect
        else:
            img_width = max_width
            img_height = img_width * aspect

    c.drawInlineImage(img, (width - img_width)/2, y - img_height, img_width, img_height)
    y -= img_height + 14
    return y

