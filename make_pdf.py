import re
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    KeepTogether,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


SOURCE_FILE = "实验报告.md"
OUTPUT_FILE = "实验报告.pdf"
REPOSITORY_URL = (
    "https://github.com/shixuhui-ops/AI-Search-Experiment-2"
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
    raise FileNotFoundError("未找到可用的中文字体")

pdfmetrics.registerFont(TTFont("ChineseFont", font_path))

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "ChineseTitle",
    parent=styles["Title"],
    fontName="ChineseFont",
    fontSize=18,
    leading=24,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#111827"),
    spaceAfter=6,
)

repo_style = ParagraphStyle(
    "Repository",
    parent=styles["BodyText"],
    fontName="ChineseFont",
    fontSize=8,
    leading=11,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#374151"),
    spaceAfter=8,
)

section_style = ParagraphStyle(
    "Section",
    parent=styles["Heading2"],
    fontName="ChineseFont",
    fontSize=13,
    leading=18,
    textColor=colors.HexColor("#111827"),
    spaceBefore=8,
    spaceAfter=4,
    keepWithNext=True,
)

subsection_style = ParagraphStyle(
    "Subsection",
    parent=styles["Heading3"],
    fontName="ChineseFont",
    fontSize=11,
    leading=15,
    textColor=colors.HexColor("#1f2937"),
    spaceBefore=6,
    spaceAfter=3,
    keepWithNext=True,
)

body_style = ParagraphStyle(
    "ChineseBody",
    parent=styles["BodyText"],
    fontName="ChineseFont",
    fontSize=10,
    leading=14.5,
    textColor=colors.HexColor("#111827"),
    spaceAfter=4,
    wordWrap="CJK",
)

bullet_style = ParagraphStyle(
    "ChineseBullet",
    parent=body_style,
    leftIndent=5 * mm,
    firstLineIndent=-3 * mm,
    bulletIndent=1.5 * mm,
    spaceAfter=1.5,
)

code_style = ParagraphStyle(
    "ChineseCode",
    parent=styles["Code"],
    fontName="ChineseFont",
    fontSize=8.8,
    leading=12,
    leftIndent=3 * mm,
    rightIndent=3 * mm,
    borderColor=colors.HexColor("#d1d5db"),
    borderWidth=0.4,
    borderPadding=4,
    backColor=colors.HexColor("#f8fafc"),
    textColor=colors.HexColor("#111827"),
    spaceBefore=2,
    spaceAfter=3,
)

table_header_style = ParagraphStyle(
    "TableHeader",
    parent=body_style,
    fontSize=8.5,
    leading=11,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#111827"),
)

table_cell_style = ParagraphStyle(
    "TableCell",
    parent=body_style,
    fontSize=8.3,
    leading=10.5,
    alignment=TA_CENTER,
    spaceAfter=0,
)


def inline_markdown(text):
    result = escape(text.strip())

    result = re.sub(
        r"`([^`]+)`",
        r"<font color='#1f4e79'>\1</font>",
        result,
    )
    result = re.sub(
        r"\*\*([^*]+)\*\*",
        r"<b>\1</b>",
        result,
    )

    return result


def split_table_row(line):
    return [
        cell.strip()
        for cell in line.strip().strip("|").split("|")
    ]


def is_table_separator(line):
    cells = split_table_row(line)

    return bool(cells) and all(
        re.fullmatch(r":?-{3,}:?", cell) is not None
        for cell in cells
    )


def table_widths(column_count):
    available = A4[0] - 30 * mm

    if column_count == 4:
        return [25 * mm, 25 * mm, 100 * mm, 30 * mm]

    if column_count == 5:
        return [
            31 * mm,
            31 * mm,
            38 * mm,
            40 * mm,
            40 * mm,
        ]

    return [available / column_count] * column_count


def build_table(rows):
    column_count = max(len(row) for row in rows)
    normalized = [
        row + [""] * (column_count - len(row))
        for row in rows
    ]

    data = []

    for row_index, row in enumerate(normalized):
        style = (
            table_header_style
            if row_index == 0
            else table_cell_style
        )
        data.append([
            Paragraph(inline_markdown(cell), style)
            for cell in row
        ])

    table = Table(
        data,
        colWidths=table_widths(column_count),
        repeatRows=1,
        hAlign="LEFT",
    )

    table.setStyle(TableStyle([
        (
            "BACKGROUND",
            (0, 0),
            (-1, 0),
            colors.HexColor("#e5e7eb"),
        ),
        (
            "GRID",
            (0, 0),
            (-1, -1),
            0.35,
            colors.HexColor("#9ca3af"),
        ),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3),
        ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ]))

    return table


lines = Path(SOURCE_FILE).read_text(
    encoding="utf-8-sig"
).splitlines()

# 标题和仓库链接由生成器统一添加，跳过 Markdown 中重复的开头。
start_index = next(
    (
        index
        for index, line in enumerate(lines)
        if line.strip().startswith("## 一、实验目标")
    ),
    0,
)
lines = lines[start_index:]

story = [
    Paragraph("实验二：搜索算法实验报告", title_style),
    Paragraph(
        "GitHub 仓库："
        f'<link href="{REPOSITORY_URL}" color="#1d4ed8">'
        f"{REPOSITORY_URL}</link>",
        repo_style,
    ),
    Spacer(1, 1.5 * mm),
]

index = 0

while index < len(lines):
    raw_line = lines[index]
    line = raw_line.strip()

    if not line:
        index += 1
        continue

    if line.startswith("```"):
        code_lines = []
        index += 1

        while (
            index < len(lines)
            and not lines[index].strip().startswith("```")
        ):
            code_lines.append(lines[index])
            index += 1

        story.append(
            KeepTogether([
                Preformatted(
                    escape("\n".join(code_lines)),
                    code_style,
                )
            ])
        )
        index += 1
        continue

    if (
        line.startswith("|")
        and index + 1 < len(lines)
        and is_table_separator(lines[index + 1])
    ):
        rows = [split_table_row(line)]
        index += 2

        while (
            index < len(lines)
            and lines[index].strip().startswith("|")
        ):
            rows.append(split_table_row(lines[index]))
            index += 1

        story.append(build_table(rows))
        story.append(Spacer(1, 1.5 * mm))
        continue

    if raw_line.startswith("    "):
        code_lines = []

        while (
            index < len(lines)
            and lines[index].startswith("    ")
        ):
            code_lines.append(lines[index][4:])
            index += 1

        story.append(
            KeepTogether([
                Preformatted(
                    escape("\n".join(code_lines)),
                    code_style,
                )
            ])
        )
        continue

    if line.startswith("## "):
        story.append(
            Paragraph(
                inline_markdown(line[3:]),
                section_style,
            )
        )
    elif line.startswith("### "):
        story.append(
            Paragraph(
                inline_markdown(line[4:]),
                subsection_style,
            )
        )
    elif line.startswith("- "):
        story.append(
            Paragraph(
                inline_markdown(line[2:]),
                bullet_style,
                bulletText="-",
            )
        )
    else:
        story.append(
            Paragraph(
                inline_markdown(line),
                body_style,
            )
        )

    index += 1


def decorate_page(canvas, document):
    canvas.saveState()

    canvas.setFillColor(colors.white)
    canvas.rect(
        0,
        0,
        A4[0],
        A4[1],
        stroke=0,
        fill=1,
    )

    canvas.setTitle("实验二：搜索算法实验报告")
    canvas.setAuthor("师旭辉")

    canvas.setStrokeColor(colors.HexColor("#d1d5db"))
    canvas.setLineWidth(0.3)
    canvas.line(
        15 * mm,
        13 * mm,
        A4[0] - 15 * mm,
        13 * mm,
    )

    canvas.setFillColor(colors.HexColor("#4b5563"))
    canvas.setFont("ChineseFont", 7.5)
    canvas.drawCentredString(
        A4[0] / 2,
        8.5 * mm,
        f"第 {document.page} 页",
    )

    canvas.restoreState()


document = SimpleDocTemplate(
    OUTPUT_FILE,
    pagesize=A4,
    rightMargin=15 * mm,
    leftMargin=15 * mm,
    topMargin=12 * mm,
    bottomMargin=17 * mm,
    title="实验二：搜索算法实验报告",
    author="师旭辉",
)

document.build(
    story,
    onFirstPage=decorate_page,
    onLaterPages=decorate_page,
)

print(f"{OUTPUT_FILE} 已生成")