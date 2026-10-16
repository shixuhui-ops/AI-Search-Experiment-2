from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
)


font_candidates = [
    r"C:\Windows\Fonts\msyh.ttf",
    r"C:\Windows\Fonts\simhei.ttf",
    r"C:\Windows\Fonts\simsun.ttc",
]

font_path = next(
    (path for path in font_candidates if Path(path).exists()),
    None,
)

if font_path is None:
    raise FileNotFoundError("未找到中文字体文件")

pdfmetrics.registerFont(TTFont("ChineseFont", font_path))

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleChinese",
    parent=styles["Title"],
    fontName="ChineseFont",
    fontSize=15,
    leading=19,
    alignment=TA_CENTER,
    spaceAfter=8,
)

heading_style = ParagraphStyle(
    "HeadingChinese",
    parent=styles["Heading2"],
    fontName="ChineseFont",
    fontSize=11,
    leading=14,
    spaceBefore=5,
    spaceAfter=3,
)

body_style = ParagraphStyle(
    "BodyChinese",
    parent=styles["BodyText"],
    fontName="ChineseFont",
    fontSize=8.5,
    leading=11,
    spaceAfter=2,
)

code_style = ParagraphStyle(
    "CodeChinese",
    parent=styles["Code"],
    fontName="ChineseFont",
    fontSize=7.5,
    leading=9,
)

output_file = "实验报告.pdf"
source_file = "实验报告.md"

story = []

story.append(Paragraph("实验二：搜索算法实验报告", title_style))
story.append(
    Paragraph(
        "GitHub 仓库："
        '<link href="https://github.com/shixuhui-ops/AI-Search-Experiment-2">'
        "https://github.com/shixuhui-ops/AI-Search-Experiment-2"
        "</link>",
        body_style,
    )
)

in_code_block = False
code_lines = []

for raw_line in Path(source_file).read_text(
    encoding="utf-8"
).splitlines():

    line = raw_line.strip()

    if line.startswith("```"):
        if in_code_block:
            story.append(
                Preformatted(
                    "\n".join(code_lines),
                    code_style,
                )
            )
            code_lines = []
            in_code_block = False
        else:
            in_code_block = True
        continue

    if in_code_block:
        code_lines.append(raw_line)
        continue

    if not line:
        continue

    if line.startswith("# "):
        story.append(
            Paragraph(
                escape(line[2:]),
                title_style,
            )
        )
    elif line.startswith("## "):
        story.append(
            Paragraph(
                escape(line[3:]),
                heading_style,
            )
        )
    elif line.startswith("### "):
        story.append(
            Paragraph(
                escape(line[4:]),
                heading_style,
            )
        )
    elif line.startswith("- "):
        story.append(
            Paragraph(
                "• " + escape(line[2:]),
                body_style,
            )
        )
    else:
        story.append(
            Paragraph(
                escape(line),
                body_style,
            )
        )


def add_page_number(canvas, document):
    canvas.saveState()
    canvas.setFont("ChineseFont", 8)
    canvas.drawCentredString(
        A4[0] / 2,
        10 * mm,
        f"第 {document.page} 页",
    )
    canvas.restoreState()


document = SimpleDocTemplate(
    output_file,
    pagesize=A4,
    rightMargin=15 * mm,
    leftMargin=15 * mm,
    topMargin=13 * mm,
    bottomMargin=15 * mm,
)

document.build(
    story,
    onFirstPage=add_page_number,
    onLaterPages=add_page_number,
)

print(f"{output_file} 已生成")