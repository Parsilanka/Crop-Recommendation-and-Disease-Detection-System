import os
from fpdf import FPDF

PAGE_W = 190   # usable width with 10mm left+right margins


class WorkDivisionPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'I', 9)
        self.set_text_color(120, 120, 120)
        self.set_left_margin(10)
        self.cell(PAGE_W, 10, 'Group 3 - Presentation Work Division', 0, 0, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 9)
        self.set_text_color(120, 120, 120)
        self.set_left_margin(10)
        self.cell(PAGE_W, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def _reset(self):
        """Reset left margin and x position to standard."""
        self.set_left_margin(10)
        self.set_x(10)

    def hline(self):
        self.set_draw_color(0, 70, 127)
        self.set_line_width(0.5)
        self.line(10, self.get_y(), 200, self.get_y())

    def section_heading(self, text):
        self._reset()
        self.set_font('Arial', 'B', 12)
        self.set_text_color(0, 51, 102)
        self.ln(4)
        self.cell(PAGE_W, 9, text, 0, 1, 'C')
        self.hline()
        self.ln(5)
        self.set_text_color(30, 30, 30)

    def member_block(self, number, name, reg, sections, notes):
        self._reset()
        # Blue header bar
        self.set_fill_color(0, 70, 127)
        self.set_text_color(255, 255, 255)
        self.set_font('Arial', 'B', 11)
        self.cell(PAGE_W, 9, f'  {number}.  {name}  ({reg})', 0, 1, 'L', fill=True)

        # "Sections to Present" label
        self._reset()
        self.set_fill_color(240, 247, 255)
        self.set_text_color(0, 51, 102)
        self.set_font('Arial', 'B', 10)
        self.set_x(14)
        self.cell(PAGE_W - 4, 7, 'Sections to Present:', 0, 1, 'L')

        # Each section line
        self.set_font('Arial', '', 10)
        self.set_text_color(30, 30, 30)
        for sec in sections:
            self._reset()
            self.set_x(16)
            self.multi_cell(PAGE_W - 6, 6, sec)

        # Notes
        if notes:
            self._reset()
            self.set_font('Arial', 'I', 9)
            self.set_text_color(80, 80, 80)
            self.set_x(14)
            self.multi_cell(PAGE_W - 4, 5, f'Note: {notes}')

        self._reset()
        self.ln(5)

    def summary_table(self, assignments):
        self._reset()
        col_w = [8, 58, 52, 72]
        headers = ['#', 'Name', 'Reg. No.', 'Sections']

        # Header row
        self.set_font('Arial', 'B', 10)
        self.set_fill_color(0, 70, 127)
        self.set_text_color(255, 255, 255)
        for i, h in enumerate(headers):
            self.cell(col_w[i], 8, h, 1, 0, 'C', fill=True)
        self.ln()

        # Data rows
        self.set_text_color(30, 30, 30)
        for idx, (name, reg, sections) in enumerate(assignments, 1):
            self.set_fill_color(235, 245, 255) if idx % 2 == 0 else self.set_fill_color(255, 255, 255)
            self.set_font('Arial', '', 9)
            sec_text = '; '.join(sections)
            self.cell(col_w[0], 9, str(idx), 1, 0, 'C', fill=True)
            self.cell(col_w[1], 9, name, 1, 0, 'L', fill=True)
            self.cell(col_w[2], 9, reg, 1, 0, 'C', fill=True)
            self.cell(col_w[3], 9, sec_text, 1, 1, 'L', fill=True)
        self.ln(4)


def generate_work_division():
    pdf = WorkDivisionPDF(format='A4')
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.set_margins(10, 18, 10)
    pdf.add_page()

    # ── COVER PAGE ─────────────────────────────────────────────────────────────
    pdf._reset()
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'must_logo.png')
    if os.path.exists(logo_path):
        img_w = 28
        img_x = (210 - img_w) / 2
        pdf.image(logo_path, x=img_x, y=pdf.get_y(), w=img_w)
        pdf.ln(32)
    else:
        pdf.ln(5)

    pdf._reset()
    pdf.set_font('Arial', 'B', 13)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(PAGE_W, 7, 'MERU UNIVERSITY OF SCIENCE AND TECHNOLOGY', 0, 1, 'C')

    pdf._reset()
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(30, 30, 30)
    pdf.cell(PAGE_W, 6, 'School of Computing and Informatics  |  Department of Information Technology', 0, 1, 'C')
    pdf.ln(6)

    pdf.hline()
    pdf.ln(5)

    pdf._reset()
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(PAGE_W, 7, 'PRESENTATION WORK DIVISION', 0, 1, 'C')
    pdf._reset()
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(PAGE_W, 6,
        'An Intelligent Crop Recommendation and Plant Disease Detection System', 0, 'C')
    pdf.ln(3)
    pdf.hline()
    pdf.ln(6)

    pdf._reset()
    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(50, 50, 50)
    pdf.cell(PAGE_W, 6, 'Research Methodology and Group Project  |  Group 3  |  February 2026', 0, 1, 'C')
    pdf.ln(8)

    # Intro note
    pdf._reset()
    pdf.set_font('Arial', 'I', 10)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(PAGE_W, 6,
        'The following is a fair distribution of presentation responsibilities across all seven '
        'group members. Each member is assigned specific sections from the research proposal to '
        'present. Members are expected to be thoroughly familiar with all sections, not just '
        'their own, to handle questions effectively during the presentation.')
    pdf.ln(6)

    # ── INDIVIDUAL ASSIGNMENTS ─────────────────────────────────────────────────
    pdf.section_heading('INDIVIDUAL PRESENTATION ASSIGNMENTS')

    assignments_detail = [
        (
            'Samuel Lemaiyan', 'CT203/113823/23',
            [
                '1.1 Background of the Study',
                '    - Overview of agriculture challenges in Kenya and globally',
                '    - Role of technology and AI in modern farming',
                '    - Introduction of the proposed system and its context',
            ],
            'Open the presentation. Set the stage and motivate the research problem.',
        ),
        (
            'Faith Chepkorir', 'CT203/113825/23',
            [
                '1.2 Problem Statement',
                '    - Key challenges faced by farmers (no guidance, disease losses)',
                '    - Gap in existing tools and why this system is needed',
            ],
            'Clearly articulate the problem the system solves. Use statistics where possible.',
        ),
        (
            'Clarence Yaa', 'CT203/113803/23',
            [
                '1.3 Research Objectives (all 5)',
                '1.4 Research Questions (all 5)',
                '    - Explain the link between objectives and research questions',
            ],
            'Keep each objective concise. Show how each question aligns with its objective.',
        ),
        (
            'Daisy Chelangat', 'CT203/113827/23',
            [
                '1.5 Significance of the Study',
                '1.6 Scope of the Study',
                '    - Who benefits and how',
                '    - Boundaries and limitations of the system',
            ],
            'Emphasise the real-world impact on smallholder farmers and agricultural extension.',
        ),
        (
            'Kindness Ebenezer', 'CT203/113837/23',
            [
                '2.1 Functions of Existing Systems',
                '2.2 Components of Existing Systems',
                '2.3 Characteristics and Features of Existing Systems',
                '    - Accuracy, accessibility, scalability, security, interpretability',
            ],
            'Use a comparison table or diagram if possible to illustrate components.',
        ),
        (
            'Alfred Musyoki', 'CT203/109347/22',
            [
                '2.4 Types of Existing Systems',
                '    - Standalone crop, standalone disease, integrated, expert systems',
                '2.5 Challenges of Existing Systems',
                '    - Data quality, connectivity, trust, fragmentation, security',
            ],
            'Highlight how the proposed system specifically addresses each challenge.',
        ),
        (
            'Scholar Wamboi', 'CT203/113799/23',
            [
                '2.6 Related Studies and Work',
                '    - Critique of 6 key studies (Mohanty, Ferentinos, Kumar, Sharma, etc.)',
                '2.7 Summary of Literature Review',
                'References (briefly introduce the 5 key citations)',
                'Closing remarks and invitation for Q&A',
            ],
            "Close the presentation. Tie all literature gaps to the proposed system's value.",
        ),
    ]

    for i, (name, reg, sections, notes) in enumerate(assignments_detail, 1):
        pdf.member_block(i, name, reg, sections, notes)

    # ── SUMMARY TABLE ──────────────────────────────────────────────────────────
    pdf.add_page()
    pdf.section_heading('QUICK REFERENCE SUMMARY TABLE')

    summary = [
        ('Samuel Lemaiyan',   'CT203/113823/23', ['1.1 Background']),
        ('Faith Chepkorir',   'CT203/113825/23', ['1.2 Problem Statement']),
        ('Clarence Yaa',      'CT203/113803/23', ['1.3 Objectives', '1.4 Research Questions']),
        ('Daisy Chelangat',   'CT203/113827/23', ['1.5 Significance', '1.6 Scope']),
        ('Kindness Ebenezer', 'CT203/113837/23', ['2.1 Functions', '2.2 Components', '2.3 Characteristics']),
        ('Alfred Musyoki',    'CT203/109347/22', ['2.4 Types', '2.5 Challenges']),
        ('Scholar Wamboi',    'CT203/113799/23', ['2.6 Related Work', '2.7 Summary', 'References', 'Closing']),
    ]
    pdf.summary_table(summary)

    # ── PRESENTATION GUIDELINES ────────────────────────────────────────────────
    pdf._reset()
    pdf.set_font('Arial', 'B', 11)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(PAGE_W, 7, 'General Presentation Guidelines', 0, 1, 'L')
    pdf.hline()
    pdf.ln(4)

    tips = [
        'Time management: Each member should aim for approximately 3-5 minutes.',
        'Preparation: Read and understand all sections of the proposal, not just your own.',
        'Slides: Prepare clear, concise slides with bullet points - avoid reading directly.',
        'Transitions: Smoothly hand over to the next presenter after completing your section.',
        'Q&A: Any member may be asked a question about any section - be prepared.',
        "Dress code: Adhere to the university's formal dress policy during the presentation.",
        'Practice: Conduct at least one full group rehearsal before the actual presentation.',
    ]

    pdf.set_font('Arial', '', 10)
    pdf.set_text_color(30, 30, 30)
    for tip in tips:
        pdf._reset()
        pdf.set_x(14)
        pdf.cell(4, 6, '-', 0, 0)
        pdf.set_x(18)
        pdf.multi_cell(PAGE_W - 8, 6, tip)
        pdf.ln(1)

    # ── OUTPUT ─────────────────────────────────────────────────────────────────
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'Group3_Presentation_Work_Division.pdf'
    )
    pdf.output(output_path)
    print(f'[OK] Work Division PDF generated: {output_path}')
    return output_path


if __name__ == '__main__':
    generate_work_division()
