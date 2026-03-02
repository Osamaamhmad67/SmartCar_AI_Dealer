
import os
from fpdf import FPDF
from config import Config

def create_structure_pdf():
    # Setup paths
    md_file_path = r"C:\Users\Osama\.gemini\antigravity\brain\ce027b75-c4fc-4432-80ba-b0dce2a41a1a\Osama_Project_Structure.md"
    output_pdf_path = os.path.join(Config.BASE_DIR, "Project_Structure.pdf")
    
    # Fonts
    font_path = str(Config.FONTS_DIR / Config.FONT_REGULAR)
    font_bold_path = str(Config.FONTS_DIR / Config.FONT_BOLD)

    # Initialize PDF
    pdf = FPDF()
    pdf.add_page()
    
    # Register Arabic-supporting font
    # Note: verify these paths exist, fallback if needed
    if os.path.exists(font_path):
        pdf.add_font('CustomFont', '', font_path, uni=True)
        pdf.add_font('CustomFont', 'B', font_bold_path, uni=True)
        main_font = 'CustomFont'
    else:
        # Fallback to standard font (might not support Arabic well, but prevents crash)
        main_font = 'Arial'

    # Read Markdown content
    with open(md_file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Simple Markdown to PDF Parser
    for line in lines:
        line = line.strip()
        if not line:
            pdf.ln(5)
            continue
            
        if line.startswith('# '):
            # H1
            pdf.set_font(main_font, 'B', 24)
            pdf.set_text_color(33, 150, 243) # Blue
            pdf.cell(0, 15, line[2:], ln=True, align='R') # Arabic is RTL usually, but simpler to align Right
            pdf.ln(5)
        elif line.startswith('## '):
            # H2
            pdf.set_font(main_font, 'B', 18)
            pdf.set_text_color(40, 40, 40)
            pdf.cell(0, 12, line[3:], ln=True, align='R')
            pdf.ln(2)
        elif line.startswith('### '):
            # H3
            pdf.set_font(main_font, 'B', 14)
            pdf.set_text_color(60, 60, 60)
            pdf.cell(0, 10, line[4:], ln=True, align='R')
        elif line.startswith('#### '):
            # H4
            pdf.set_font(main_font, 'B', 12)
            pdf.set_text_color(80, 80, 80)
            pdf.cell(0, 8, line[5:], ln=True, align='R')
        elif line.startswith('* ') or line.startswith('- '):
            # Bullet points
            pdf.set_font(main_font, '', 11)
            pdf.set_text_color(0, 0, 0)
            pdf.cell(0, 7, f"• {line[2:]}", ln=True, align='R')
        elif line.startswith('1. '):
             # Numbered list (simplified)
            pdf.set_font(main_font, '', 11)
            pdf.cell(0, 7, line, ln=True, align='R')
        elif line.startswith('|'):
            # Simple table handling (just print as text for now to avoid complex grid logic)
            pdf.set_font('Courier', '', 9) # Monospace for alignment
            pdf.cell(0, 6, line, ln=True, align='R')
        else:
            # Normal text
            pdf.set_font(main_font, '', 11)
            pdf.set_text_color(0, 0, 0)
            pdf.multi_cell(0, 7, line, align='R')

    pdf.output(output_pdf_path)
    print(f"PDF created at: {output_pdf_path}")

if __name__ == "__main__":
    create_structure_pdf()
