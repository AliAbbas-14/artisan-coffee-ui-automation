"""
generate_ppt.py
Generates Project_Phase2_Presentation.pptx using python-pptx.
Professional dark coffee-themed 10-minute class presentation.
Author: Ali Abbas (23F-3037) | Software Testing SE-7A
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import copy

OUTPUT_FILE = r"E:\23F-3037 Ali Abbas ST Presenatation SE-7A\Project_Phase2_Presentation.pptx"

# ─── Colour Palette ────────────────────────────────────────────────────────────
C_DARK_BG   = RGBColor(0x0F, 0x0F, 0x1E)   # dark navy
C_CARD_BG   = RGBColor(0x1A, 0x1A, 0x2E)   # card dark
C_GOLD      = RGBColor(0xD4, 0xA8, 0x43)   # amber gold
C_LIGHT_GOLD= RGBColor(0xF5, 0xD7, 0x8E)   # soft gold
C_CREAM     = RGBColor(0xFA, 0xF7, 0xF0)   # off-white
C_WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
C_GREY      = RGBColor(0x88, 0x88, 0x88)
C_GREEN     = RGBColor(0x4A, 0xD6, 0x6D)   # pass green
C_CODE_BG   = RGBColor(0x1E, 0x1E, 0x2E)
C_CODE_FG   = RGBColor(0xA9, 0xDC, 0x76)

W  = Inches(13.33)   # widescreen 16:9
H  = Inches(7.5)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H

BLANK = prs.slide_layouts[6]  # completely blank layout


# ─── Helpers ───────────────────────────────────────────────────────────────────
def add_rect(slide, l, t, w, h, fill_rgb, border_rgb=None, border_pt=0):
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))  # MSO_SHAPE_TYPE.RECTANGLE = 1
    shape.line.fill.background()
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_rgb
    if border_rgb:
        shape.line.color.rgb = border_rgb
        shape.line.width = Pt(border_pt)
    else:
        shape.line.fill.background()
    return shape


def add_text(slide, text, l, t, w, h,
             font_name='Calibri', font_size=18, bold=False, italic=False,
             color=C_WHITE, align=PP_ALIGN.LEFT, wrap=True):
    txBox = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name = font_name
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox


def add_multiline(slide, lines, l, t, w, h,
                  font_name='Calibri', font_size=14, bold=False,
                  color=C_CREAM, align=PP_ALIGN.LEFT, line_spacing=None):
    txBox = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if line_spacing:
            from pptx.util import Pt as Pt2
            from pptx.oxml.ns import qn
            import lxml.etree as etree
        run = p.add_run()
        run.text = line
        run.font.name = font_name
        run.font.size = Pt(font_size)
        run.font.bold = bold
        run.font.color.rgb = color
    return txBox


def add_code_block(slide, code_lines, l, t, w, h):
    """Dark code block with monospace font."""
    add_rect(slide, l, t, w, h, C_CODE_BG, C_GOLD, 1)
    txBox = slide.shapes.add_textbox(Inches(l+0.1), Inches(t+0.1), Inches(w-0.2), Inches(h-0.2))
    tf = txBox.text_frame
    tf.word_wrap = False
    for i, line in enumerate(code_lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        run = p.add_run()
        run.text = line
        run.font.name = 'Courier New'
        run.font.size = Pt(11)
        run.font.color.rgb = C_CODE_FG
    return txBox


def slide_bg(slide):
    """Apply dark navy background."""
    add_rect(slide, 0, 0, 13.33, 7.5, C_DARK_BG)


def gold_bar_top(slide, height=0.08):
    add_rect(slide, 0, 0, 13.33, height, C_GOLD)


def gold_bar_bottom(slide):
    add_rect(slide, 0, 7.3, 13.33, 0.2, C_GOLD)
    add_text(slide, 'Ali Abbas  |  23F-3037  |  Software Testing SE-7A  |  Artisan Coffee UI Automation',
             0.3, 7.32, 12.7, 0.2, font_size=9, color=C_LIGHT_GOLD, align=PP_ALIGN.CENTER)


def section_title(slide, title, subtitle=None):
    add_text(slide, title, 0.5, 0.15, 12.3, 0.9,
             font_name='Calibri', font_size=32, bold=True,
             color=C_GOLD, align=PP_ALIGN.LEFT)
    add_rect(slide, 0.5, 1.0, 12.3, 0.04, C_GOLD)
    if subtitle:
        add_text(slide, subtitle, 0.5, 1.1, 12.3, 0.5,
                 font_size=14, color=C_LIGHT_GOLD)


def bullet_card(slide, l, t, w, h, title, bullets, title_color=C_GOLD, bullet_color=C_CREAM, font_size=13):
    add_rect(slide, l, t, w, h, C_CARD_BG, C_GOLD, 0.75)
    add_text(slide, title, l+0.15, t+0.1, w-0.3, 0.4,
             font_size=15, bold=True, color=title_color)
    lines = [f'  ▸  {b}' for b in bullets]
    add_multiline(slide, lines, l+0.15, t+0.5, w-0.3, h-0.6,
                  font_size=font_size, color=bullet_color)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — Cover
# ═══════════════════════════════════════════════════════════════════════════════
def slide_cover():
    s = prs.slides.add_slide(BLANK)
    slide_bg(s)
    # accent top strip
    add_rect(s, 0, 0, 13.33, 0.5, C_GOLD)
    add_text(s, '☕  SOFTWARE TESTING  |  SE-7A', 0, 0.05, 13.33, 0.4,
             font_size=14, bold=True, color=C_DARK_BG, align=PP_ALIGN.CENTER)

    # main title
    add_text(s, 'Web UI Test Automation\nFramework', 1, 1.1, 11.33, 2.2,
             font_name='Calibri', font_size=52, bold=True,
             color=C_GOLD, align=PP_ALIGN.CENTER)

    # subtitle
    add_text(s, 'Project Phase 2  —  Playwright • Python • BDD • Allure • CI/CD',
             1, 3.2, 11.33, 0.6,
             font_size=18, color=C_LIGHT_GOLD, align=PP_ALIGN.CENTER)

    add_rect(s, 1.5, 3.9, 10.33, 0.04, C_GOLD)

    # info row
    info = [
        ('👤  Student', 'Ali Abbas'),
        ('🆔  Roll No', '23F-3037'),
        ('📅  Date', '2024'),
    ]
    col_w = 3.5
    for i, (label, val) in enumerate(info):
        x = 1.5 + i * col_w
        add_rect(s, x, 4.1, col_w - 0.2, 0.9, C_CARD_BG, C_GOLD, 0.75)
        add_text(s, label, x+0.1, 4.15, col_w-0.3, 0.3,
                 font_size=10, color=C_LIGHT_GOLD)
        add_text(s, val, x+0.1, 4.45, col_w-0.3, 0.4,
                 font_size=14, bold=True, color=C_WHITE)

    # URLs
    add_text(s, '🌐  coffee-nu-jade.vercel.app', 0, 5.3, 13.33, 0.4,
             font_size=12, color=C_CREAM, align=PP_ALIGN.CENTER)
    add_text(s, '🐙  github.com/AliAbbas-14/artisan-coffee-ui-automation', 0, 5.65, 13.33, 0.4,
             font_size=12, color=C_CREAM, align=PP_ALIGN.CENTER)

    add_rect(s, 0, 7.3, 13.33, 0.2, C_GOLD)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — Agenda
# ═══════════════════════════════════════════════════════════════════════════════
def slide_agenda():
    s = prs.slides.add_slide(BLANK)
    slide_bg(s); gold_bar_top(s); gold_bar_bottom(s)
    section_title(s, 'Agenda', '10-minute presentation roadmap')

    topics = [
        ('01', 'Project Overview & Live Application'),
        ('02', 'Technology Stack'),
        ('03', 'Framework Architecture'),
        ('04', 'Page Object Model (POM)'),
        ('05', 'BDD with Gherkin & Behave'),
        ('06', 'Multi-Source Data Integration'),
        ('07', 'Test Results — 100% Pass Rate'),
        ('08', 'Allure Reporting'),
        ('09', 'GitHub CI/CD Automation'),
        ('10', 'Challenges & Solutions  |  Demo & Q&A'),
    ]

    cols = 2
    per_col = 5
    col_w = 5.9
    for i, (num, text) in enumerate(topics):
        col = i // per_col
        row = i % per_col
        x = 0.4 + col * (col_w + 0.6)
        y = 1.5 + row * 1.1
        add_rect(s, x, y, col_w, 0.9, C_CARD_BG, C_GOLD, 0.5)
        add_text(s, num, x+0.1, y+0.1, 0.6, 0.7,
                 font_size=20, bold=True, color=C_GOLD)
        add_rect(s, x+0.7, y+0.15, 0.03, 0.6, C_GOLD)
        add_text(s, text, x+0.85, y+0.17, col_w-1, 0.6,
                 font_size=14, color=C_CREAM)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — Project Overview
# ═══════════════════════════════════════════════════════════════════════════════
def slide_overview():
    s = prs.slides.add_slide(BLANK)
    slide_bg(s); gold_bar_top(s); gold_bar_bottom(s)
    section_title(s, 'Project Overview', 'What we built and why')

    # Left card
    add_rect(s, 0.4, 1.4, 5.8, 5.6, C_CARD_BG, C_GOLD, 0.75)
    add_text(s, '🎯  Objective', 0.6, 1.5, 5.4, 0.5,
             font_size=16, bold=True, color=C_GOLD)
    add_rect(s, 0.6, 1.95, 5.4, 0.03, C_GOLD)
    desc = [
        'Build a complete Web UI Test',
        'Automation Framework for the',
        'Artisan Coffee e-commerce site.',
        '',
        'Covers all Phase 2 requirements:',
        '• BDD + Gherkin feature files',
        '• Page Object Model (POM)',
        '• Multi-source data integration',
        '• Allure visual reporting',
        '• GitHub CI/CD pipeline',
    ]
    add_multiline(s, desc, 0.6, 2.05, 5.4, 4.6, font_size=14, color=C_CREAM)

    # Right side — app details
    add_rect(s, 6.8, 1.4, 6.1, 2.5, C_CARD_BG, C_GOLD, 0.75)
    add_text(s, '🌐  Live Application', 7.0, 1.5, 5.7, 0.5,
             font_size=16, bold=True, color=C_GOLD)
    app_info = [
        'Artisan Coffee  —  Next.js 14 SPA',
        'Deployed on Vercel',
        '',
        'coffee-nu-jade.vercel.app',
    ]
    add_multiline(s, app_info, 7.0, 2.0, 5.7, 1.7, font_size=13, color=C_CREAM)

    add_rect(s, 6.8, 4.1, 6.1, 2.6, C_CARD_BG, C_GOLD, 0.75)
    add_text(s, '📊  By the Numbers', 7.0, 4.2, 5.7, 0.5,
             font_size=16, bold=True, color=C_GOLD)
    nums = [
        '5   Feature files',
        '21  Scenarios automated',
        '73  Steps passing',
        '9   Page Object classes',
        '3   Data sources (Excel, DB, Redis)',
    ]
    add_multiline(s, nums, 7.0, 4.7, 5.7, 1.8, font_size=13, color=C_CREAM)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — Tech Stack
# ═══════════════════════════════════════════════════════════════════════════════
def slide_tech():
    s = prs.slides.add_slide(BLANK)
    slide_bg(s); gold_bar_top(s); gold_bar_bottom(s)
    section_title(s, 'Technology Stack', 'Tools & libraries powering the framework')

    tech = [
        ('🎭', 'Playwright',      'Python browser automation\nChromium / Firefox / WebKit'),
        ('🐍', 'Python 3.12',    'Core language\nPytest / Behave runtime'),
        ('🥒', 'Behave (BDD)',    'Gherkin feature runner\nScenario Outlines + data tables'),
        ('📊', 'Allure Reports',  'Visual HTML reports\nScreenshots on failure'),
        ('📗', 'OpenPyXL',        'Excel (.xlsx) reader\nMulti-sheet test data'),
        ('🗄️', 'SQLite / Redis',  'Database + cache\nIn-memory Redis fallback'),
        ('⚙️', 'GitHub Actions',  'CI/CD pipeline\nAuto-run on push/PR/merge'),
        ('🌐', 'Next.js + Vercel','Live target application\nProduction deployment'),
    ]

    cols, rows = 4, 2
    card_w, card_h = 2.9, 2.3
    for i, (icon, name, desc) in enumerate(tech):
        col = i % cols
        row = i // cols
        x = 0.35 + col * (card_w + 0.3)
        y = 1.5 + row * (card_h + 0.3)
        add_rect(s, x, y, card_w, card_h, C_CARD_BG, C_GOLD, 0.75)
        add_text(s, icon, x + 0.15, y + 0.15, 0.6, 0.6, font_size=22)
        add_text(s, name, x + 0.75, y + 0.2, card_w-0.9, 0.5,
                 font_size=14, bold=True, color=C_GOLD)
        add_multiline(s, desc.split('\n'), x + 0.15, y + 0.75, card_w-0.3, 1.3,
                      font_size=11, color=C_CREAM)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — Architecture
# ═══════════════════════════════════════════════════════════════════════════════
def slide_architecture():
    s = prs.slides.add_slide(BLANK)
    slide_bg(s); gold_bar_top(s); gold_bar_bottom(s)
    section_title(s, 'Framework Architecture', '4-layer modular design')

    layers = [
        ('⚙️  CONFIG',    'config.py\nBASE_URL, browser, timeouts, headless'),
        ('📄  PAGES',     'BasePage + 8 POM classes\nOne class per UI section'),
        ('🥒  FEATURES',  '5 .feature files + step definitions\nBehave environment hooks'),
        ('📊  DATA',      'DataManager facade\nExcel  •  SQLite  •  Redis'),
    ]

    for i, (layer, desc) in enumerate(layers):
        x = 0.4
        y = 1.6 + i * 1.35
        add_rect(s, x, y, 5.5, 1.1, C_CARD_BG, C_GOLD, 1)
        add_text(s, layer, x+0.15, y+0.1, 5, 0.45,
                 font_size=15, bold=True, color=C_GOLD)
        add_multiline(s, desc.split('\n'), x+0.15, y+0.55, 5, 0.5,
                      font_size=12, color=C_CREAM)
        if i < len(layers) - 1:
            add_text(s, '▼', 0.4+2.5-0.1, y+1.1, 0.4, 0.3,
                     font_size=14, color=C_GOLD, align=PP_ALIGN.CENTER)

    # Right side — directory tree
    add_rect(s, 6.5, 1.4, 6.4, 5.7, C_CODE_BG, C_GOLD, 1)
    tree = [
        'automation_framework/',
        '├── config/',
        '│   └── config.py',
        '├── pages/',
        '│   ├── base_page.py',
        '│   ├── home_page.py',
        '│   ├── menu_page.py',
        '│   └── blend_page.py  ...',
        '├── features/',
        '│   ├── environment.py',
        '│   ├── *.feature  (5 files)',
        '│   └── steps/*.py',
        '├── data/',
        '│   ├── data_manager.py',
        '│   ├── excel_reader.py',
        '│   ├── db_reader.py',
        '│   └── redis_reader.py',
        '├── reports/',
        '│   └── allure-results/',
        '└── run_tests.py',
    ]
    add_code_block(s, tree, 6.6, 1.5, 6.2, 5.5)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — POM
# ═══════════════════════════════════════════════════════════════════════════════
def slide_pom():
    s = prs.slides.add_slide(BLANK)
    slide_bg(s); gold_bar_top(s); gold_bar_bottom(s)
    section_title(s, 'Page Object Model (POM)', 'Encapsulate UI — reuse actions — maintain once')

    # Left — BasePage code
    code = [
        'class BasePage:',
        '  def __init__(self, page):',
        '    self.page = page',
        '    self.timeout = 15000',
        '',
        '  def navigate(self, url):',
        '    self.page.goto(url)',
        '',
        '  def click(self, sel):',
        '    self.page.locator(sel)',
        '             .click()',
        '',
        '  def is_visible(self, sel):',
        '    return self.page.locator(sel)',
        '                    .is_visible()',
    ]
    add_code_block(s, code, 0.4, 1.4, 5.8, 5.6)

    # Right — benefits + hierarchy
    add_rect(s, 6.5, 1.4, 6.4, 2.5, C_CARD_BG, C_GOLD, 0.75)
    add_text(s, '✅  Why POM?', 6.7, 1.5, 6, 0.5,
             font_size=15, bold=True, color=C_GOLD)
    benefits = [
        '▸  Separation of concerns',
        '▸  Reusable page actions',
        '▸  UI changes = 1 file update',
        '▸  Readable step definitions',
    ]
    add_multiline(s, benefits, 6.7, 2.0, 6, 1.7, font_size=13, color=C_CREAM)

    classes = [
        ['HomePage',       '#hero'],
        ['MenuPage',       '#menu'],
        ['BlendPage',      '#blend'],
        ['NewsletterPage', '#newsletter'],
        ['LocationsPage',  '#locations'],
        ['LoginPage',      '/login'],
    ]
    add_rect(s, 6.5, 4.1, 6.4, 2.6, C_CARD_BG, C_GOLD, 0.75)
    add_text(s, '📋  POM Classes', 6.7, 4.2, 6, 0.4,
             font_size=15, bold=True, color=C_GOLD)
    for i, (cls, section) in enumerate(classes):
        y = 4.7 + i * 0.33
        add_text(s, cls, 6.7, y, 3.5, 0.3, font_size=11, bold=True, color=C_LIGHT_GOLD)
        add_text(s, section, 10.3, y, 2.3, 0.3, font_size=11, color=C_GREY)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — BDD / Gherkin
# ═══════════════════════════════════════════════════════════════════════════════
def slide_bdd():
    s = prs.slides.add_slide(BLANK)
    slide_bg(s); gold_bar_top(s); gold_bar_bottom(s)
    section_title(s, 'BDD with Gherkin & Behave', 'Plain-English tests anyone can read')

    # Feature file
    feature = [
        'Feature: Signature Menu Catalog',
        '',
        '  Background:',
        '    Given I navigate to Artisan Coffee',
        '',
        '  Scenario Outline: Verify product',
        '    When I scroll to the menu section',
        '    Then I should see "<product_name>"',
        '    And origin shows "<origin>"',
        '',
        '  Examples:',
        '    | product_name         | origin    |',
        '    | Black Label Espresso | Ethiopia  |',
        '    | Velvet Oat Latte     | Colombia  |',
        '    | Midnight Cold Brew   | Guatemala |',
    ]
    add_code_block(s, feature, 0.4, 1.4, 6.5, 5.6)

    # Right side
    step_code = [
        '@when("I scroll to the menu")',
        'def step_scroll(context):',
        '    context.menu_page',
        '           .scroll_to_menu()',
        '',
        '@then(\'I should see "{product}"\')',
        'def step_see(context, product):',
        '    assert context.menu_page',
        '        .is_product_visible(product)',
    ]
    add_code_block(s, step_code, 7.2, 1.4, 5.7, 3.3)

    add_rect(s, 7.2, 4.9, 5.7, 2.1, C_CARD_BG, C_GOLD, 0.75)
    add_text(s, '5 Feature Files', 7.4, 5.0, 5.3, 0.4,
             font_size=14, bold=True, color=C_GOLD)
    ff = [
        '▸  landing_and_navigation  (4 scenarios)',
        '▸  menu_catalog            (4 scenarios)',
        '▸  blend_lab               (4 scenarios)',
        '▸  newsletter_form         (5 scenarios)',
        '▸  data_sources            (4 scenarios)',
    ]
    add_multiline(s, ff, 7.4, 5.4, 5.3, 1.4, font_size=11, color=C_CREAM)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — Data Integration
# ═══════════════════════════════════════════════════════════════════════════════
def slide_data():
    s = prs.slides.add_slide(BLANK)
    slide_bg(s); gold_bar_top(s); gold_bar_bottom(s)
    section_title(s, 'Multi-Source Data Integration', 'Excel  •  SQLite  •  Redis  →  DataManager')

    # Three source cards
    sources = [
        ('📗', 'Excel (.xlsx)', [
            'Library: OpenPyXL',
            'File: test_data.xlsx',
            'Sheets: MenuProducts,',
            '  BlendData, Newsletter',
        ]),
        ('🗄️', 'SQLite DB', [
            'Library: sqlite3 (stdlib)',
            'File: dev.db',
            'Tables: users, menu,',
            '  blends, newsletter',
        ]),
        ('🔴', 'Redis Cache', [
            'Library: redis-py',
            'Key: cache:menu:signature',
            'Fallback: in-memory dict',
            '  (CI-friendly)',
        ]),
    ]

    card_w = 3.9
    for i, (icon, title, bullets) in enumerate(sources):
        x = 0.4 + i * (card_w + 0.35)
        add_rect(s, x, 1.4, card_w, 2.8, C_CARD_BG, C_GOLD, 0.75)
        add_text(s, f'{icon}  {title}', x+0.15, 1.5, card_w-0.3, 0.5,
                 font_size=15, bold=True, color=C_GOLD)
        add_rect(s, x+0.15, 1.95, card_w-0.3, 0.03, C_GOLD)
        add_multiline(s, bullets, x+0.15, 2.05, card_w-0.3, 2.0, font_size=12, color=C_CREAM)

    # DataManager facade code
    code = [
        'class DataManager:',
        '  def __init__(self):',
        '    self.excel = ExcelReader("test_data.xlsx")',
        '    self.db    = DBReader("dev.db")',
        '    self.redis = RedisReader("localhost")',
        '',
        '  def get_menu_products(self):  # ← Excel',
        '    return self.excel.read_sheet("MenuProducts")',
        '',
        '  def get_blend_profiles(self):  # ← SQLite',
        '    return self.db.query("SELECT * FROM blends")',
        '',
        '  def get_redis_menu(self):  # ← Redis',
        '    return self.redis.get("cache:menu:signature")',
    ]
    add_code_block(s, code, 0.4, 4.4, 12.5, 2.65)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — Test Results
# ═══════════════════════════════════════════════════════════════════════════════
def slide_results():
    s = prs.slides.add_slide(BLANK)
    slide_bg(s); gold_bar_top(s); gold_bar_bottom(s)
    section_title(s, 'Test Results', 'All 21 scenarios — 100% pass rate')

    # Big badge
    add_rect(s, 1.5, 1.4, 10.33, 1.2, C_CARD_BG, C_GOLD, 2)
    add_text(s, '✅  21 Scenarios  |  73 Steps  |  0 Failures  |  0 Skipped',
             1.5, 1.6, 10.33, 0.8,
             font_size=22, bold=True, color=C_GOLD, align=PP_ALIGN.CENTER)

    rows = [
        ('landing_and_navigation', '4',  '14', '~10s'),
        ('menu_catalog',           '4',  '17', '~12s'),
        ('blend_lab',              '4',  '17', '~11s'),
        ('newsletter_form',        '5',  '17', '~10s'),
        ('data_sources',           '4',  '8',  '~8s'),
    ]

    headers = ['Feature', 'Scenarios', 'Steps', 'Duration', 'Result']
    col_x   = [0.4, 5.3, 6.9, 8.5, 10.1]
    col_w   = [4.7, 1.4, 1.4, 1.4,  2.5]

    # header row
    for j, (hdr, cx, cw) in enumerate(zip(headers, col_x, col_w)):
        add_rect(s, cx, 2.8, cw-0.1, 0.5, C_GOLD)
        add_text(s, hdr, cx+0.05, 2.87, cw-0.15, 0.4,
                 font_size=12, bold=True, color=C_DARK_BG, align=PP_ALIGN.CENTER)

    # data rows
    for i, (feat, scen, steps, dur) in enumerate(rows):
        y = 3.35 + i * 0.6
        bg = C_CARD_BG if i % 2 == 0 else C_DARK_BG
        add_rect(s, 0.4, y, 12.1, 0.55, bg, C_GREY, 0.3)
        vals = [feat, scen, steps, dur, '✅ PASSED']
        clrs = [C_CREAM, C_CREAM, C_CREAM, C_CREAM, C_GREEN]
        for j, (v, cx, cw, vc) in enumerate(zip(vals, col_x, col_w, clrs)):
            add_text(s, v, cx+0.05, y+0.1, cw-0.1, 0.4,
                     font_size=12, color=vc,
                     align=PP_ALIGN.CENTER if j > 0 else PP_ALIGN.LEFT)

    # Total
    add_rect(s, 0.4, 6.4, 12.1, 0.55, C_GOLD)
    totals = ['TOTAL', '21', '73', '~51s', '5/5 PASSED']
    for j, (v, cx, cw) in enumerate(zip(totals, col_x, col_w)):
        add_text(s, v, cx+0.05, 6.5, cw-0.1, 0.4,
                 font_size=12, bold=True, color=C_DARK_BG,
                 align=PP_ALIGN.CENTER if j > 0 else PP_ALIGN.LEFT)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — Allure Reporting
# ═══════════════════════════════════════════════════════════════════════════════
def slide_allure():
    s = prs.slides.add_slide(BLANK)
    slide_bg(s); gold_bar_top(s); gold_bar_bottom(s)
    section_title(s, 'Allure Reporting', 'Visual test reports with screenshots')

    # Left — what Allure captures
    bullet_card(s, 0.4, 1.4, 5.8, 5.6,
                '📊  What Allure Captures',
                [
                    'Each scenario with step-level outcomes',
                    'Screenshots on test failure',
                    'Test duration & execution timeline',
                    'Feature-level aggregation view',
                    'JSON artifacts (reports/allure-results/)',
                    'Standalone HTML report (no server)',
                ])

    # Right — environment.py hooks
    code = [
        '# features/environment.py',
        '',
        'def before_scenario(context, scenario):',
        '  pw = sync_playwright().start()',
        '  context.browser = pw.chromium.launch()',
        '  context.page    = context.browser.new_page()',
        '  context.menu_page = MenuPage(context.page)',
        '  # ... other page objects',
        '',
        'def after_scenario(context, scenario):',
        '  if scenario.status == "failed":',
        '    path = f"reports/allure-results/"',
        '           f"{scenario.name}.png"',
        '    context.page.screenshot(path=path)',
        '  context.browser.close()',
    ]
    add_code_block(s, code, 6.5, 1.4, 6.4, 5.6)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — GitHub CI/CD
# ═══════════════════════════════════════════════════════════════════════════════
def slide_cicd():
    s = prs.slides.add_slide(BLANK)
    slide_bg(s); gold_bar_top(s); gold_bar_bottom(s)
    section_title(s, 'GitHub CI/CD Automation', 'Tests run automatically on every push & merge')

    yml = [
        'on:',
        '  push:',
        "    branches: ['**']   # all branches",
        '  pull_request:',
        '    branches: [main]',
        '',
        'jobs:',
        '  ui-tests:',
        '    runs-on: ubuntu-latest',
        '    steps:',
        '      - uses: actions/checkout@v4',
        '      - uses: actions/setup-python@v5',
        '        with: { python-version: "3.12" }',
        '      - run: pip install -r requirements.txt',
        '      - run: playwright install chromium',
        '      - run: python run_tests.py --headless',
        '      - uses: actions/upload-artifact@v4',
        '        with:',
        '          name: allure-results',
        '          path: reports/allure-results/',
    ]
    add_code_block(s, yml, 0.4, 1.4, 6.5, 5.7)

    bullet_card(s, 7.2, 1.4, 5.7, 2.6,
                '⚡  Triggers',
                [
                    'push → any branch (feature/*, fix/*)',
                    'pull_request → main (before merge)',
                    'merge to main (post-merge regression)',
                ])

    bullet_card(s, 7.2, 4.2, 5.7, 2.6,
                '📋  GitHub Practices',
                [
                    'PR template with QA checklist',
                    'Bug report issue template',
                    'Conventional Commits (feat:, fix:, docs:)',
                    'Allure results as CI artifact',
                ])


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — Challenges & Solutions
# ═══════════════════════════════════════════════════════════════════════════════
def slide_challenges():
    s = prs.slides.add_slide(BLANK)
    slide_bg(s); gold_bar_top(s); gold_bar_bottom(s)
    section_title(s, 'Challenges & Solutions', 'Key technical problems resolved during development')

    challenges = [
        ('🔗 SPA Routing',
         '/menu returns 404',
         'Used anchor-based navigation (#menu, #blend) with Playwright scroll helpers'),
        ('📡 Redis in CI',
         'No Redis server in GitHub Actions',
         'Pre-seeded in-memory fallback dict in RedisReader.__init__()'),
        ('🔄 Git Conflict',
         'Push rejected: remote had extra commits',
         'git fetch → git rebase -X theirs origin/main → clean push'),
        ('⚙️ Allure Config',
         'KeyError crash on first run',
         'Removed --outfile format from behave.ini; handled via run_tests.py subprocess'),
        ('🌐 TypeScript Errors',
         'Module not found: react, next, @/components/*',
         'Added declarations.d.ts + tsconfig path mapping + fixed CartProvider types'),
        ('🔍 Selector Issues',
         'text="ARTISANCOFFEE" not visible (strict match)',
         'Changed to :has-text() (broader match); verified against live app DOM'),
    ]

    for i, (icon_title, problem, solution) in enumerate(challenges):
        col = i % 2
        row = i // 2
        x = 0.4 + col * 6.4
        y = 1.6 + row * 1.9
        add_rect(s, x, y, 6.1, 1.7, C_CARD_BG, C_GOLD, 0.75)
        add_text(s, icon_title, x+0.15, y+0.1, 5.7, 0.35,
                 font_size=13, bold=True, color=C_GOLD)
        add_text(s, f'Problem: {problem}', x+0.15, y+0.48, 5.7, 0.3,
                 font_size=11, color=C_LIGHT_GOLD)
        add_text(s, f'Solution: {solution}', x+0.15, y+0.82, 5.7, 0.7,
                 font_size=11, color=C_CREAM)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 13 — Thank You / Q&A
# ═══════════════════════════════════════════════════════════════════════════════
def slide_thankyou():
    s = prs.slides.add_slide(BLANK)
    slide_bg(s)
    add_rect(s, 0, 0, 13.33, 0.8, C_GOLD)
    add_text(s, '☕  ARTISAN COFFEE  |  Web UI Test Automation Framework',
             0, 0.1, 13.33, 0.6,
             font_size=18, bold=True, color=C_DARK_BG, align=PP_ALIGN.CENTER)

    add_text(s, 'Demo & Q&A', 2, 1.2, 9.33, 1.2,
             font_name='Calibri', font_size=48, bold=True,
             color=C_GOLD, align=PP_ALIGN.CENTER)

    add_rect(s, 1.5, 2.3, 10.33, 0.05, C_GOLD)

    # Links
    links = [
        ('🌐  Live Website',  'https://coffee-nu-jade.vercel.app/'),
        ('🐙  GitHub Repo',   'https://github.com/AliAbbas-14/artisan-coffee-ui-automation'),
    ]
    for i, (label, url) in enumerate(links):
        y = 2.7 + i * 1.0
        add_rect(s, 1.5, y, 10.33, 0.8, C_CARD_BG, C_GOLD, 0.75)
        add_text(s, label, 1.7, y+0.08, 3, 0.4, font_size=14, bold=True, color=C_GOLD)
        add_text(s, url, 4.8, y+0.08, 6.8, 0.4, font_size=12, color=C_CREAM)

    # Author
    add_rect(s, 1.5, 4.9, 10.33, 1.6, C_CARD_BG, C_GOLD, 0.75)
    info = [
        'Ali Abbas          Roll No: 23F-3037',
        'Software Testing   Section: SE-7A',
    ]
    add_multiline(s, info, 1.7, 5.1, 10, 1.2,
                  font_size=16, color=C_CREAM, align=PP_ALIGN.CENTER)

    add_text(s, 'Thank You!', 0, 6.5, 13.33, 0.7,
             font_size=24, bold=True, color=C_LIGHT_GOLD, align=PP_ALIGN.CENTER)

    add_rect(s, 0, 7.3, 13.33, 0.2, C_GOLD)


# ─── BUILD ─────────────────────────────────────────────────────────────────────
def build():
    slide_cover()
    slide_agenda()
    slide_overview()
    slide_tech()
    slide_architecture()
    slide_pom()
    slide_bdd()
    slide_data()
    slide_results()
    slide_allure()
    slide_cicd()
    slide_challenges()
    slide_thankyou()

    prs.save(OUTPUT_FILE)
    print(f'✅  PPT saved → {OUTPUT_FILE}')
    print(f'    Total slides: {len(prs.slides)}')


if __name__ == '__main__':
    build()
