"""
Dynamic Resume Builder Module
Generates tailored DOCX and HTML/PDF resumes strictly from verified portfolio records.
"""
import os
from typing import Dict, Any, List
import docx
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls
from docx.shared import Inches, Pt, RGBColor


def build_tailored_docx(
    portfolio: Dict[str, Any],
    selected_ids: Dict[str, Any],
    target_role_title: str,
    custom_summary: str,
    output_path: str,
    primary_hex: str = "0F2942"
) -> str:
    doc = docx.Document()
    for section in doc.sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.85)
        section.right_margin = Inches(0.85)

    text_dark = RGBColor(0x1E, 0x29, 0x3B)
    primary_rgb = RGBColor(int(primary_hex[0:2], 16), int(primary_hex[2:4], 16), int(primary_hex[4:6], 16))
    muted_rgb = RGBColor(0x47, 0x55, 0x69)

    style_normal = doc.styles["Normal"]
    style_normal.font.name = "Calibri"
    style_normal.font.size = Pt(11)
    style_normal.font.color.rgb = text_dark

    p_info = portfolio["personal_info"]

    # Header Name & Target Title
    name_p = doc.add_paragraph()
    name_p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r_name = name_p.add_run(f"{p_info['full_name']}  |  {target_role_title}")
    r_name.font.size = Pt(18)
    r_name.font.bold = True
    r_name.font.color.rgb = primary_rgb
    name_p.paragraph_format.space_after = Pt(3)

    contact_p = doc.add_paragraph()
    r_contact = contact_p.add_run(
        f"{p_info['location']}  •  {p_info['phone']}  •  {p_info['email']}\n"
        f"LinkedIn: {p_info['linkedin_url']}  •  GitHub: {p_info['github_url']}  •  Portfolio: {p_info['portfolio_url']}"
    )
    r_contact.font.size = Pt(10)
    r_contact.font.color.rgb = muted_rgb
    contact_p.paragraph_format.space_after = Pt(8)

    def add_section_header(title: str):
        h = doc.add_paragraph()
        r = h.add_run(title.upper())
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = primary_rgb
        h.paragraph_format.space_before = Pt(8)
        h.paragraph_format.space_after = Pt(3)
        h.paragraph_format.keep_with_next = True
        pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="6" w:space="1" w:color="{primary_hex}"/></w:pBdr>')
        h._p.get_or_add_pPr().append(pBdr)

    # 1. Summary
    add_section_header("Professional Summary")
    sum_p = doc.add_paragraph(custom_summary)
    sum_p.paragraph_format.space_after = Pt(6)
    sum_p.paragraph_format.line_spacing = 1.15
    for r in sum_p.runs:
        r.font.size = Pt(11)

    # 2. Selected Technical & Core Skills (Grouped Table)
    add_section_header("Verified Technical & Core Skills")
    sel_skills = [s for s in portfolio["skills"] if s["id"] in selected_ids.get("skill_ids", [])]
    grouped: Dict[str, List[str]] = {}
    for s in sel_skills:
        grouped.setdefault(s["category"], []).append(f"{s['skill_name']} ({s['proficiency_level']})")

    if grouped:
        table = doc.add_table(rows=1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        hdr = table.rows[0]
        for idx, text in enumerate(["Skill Category", "Verified Portfolio Competencies"]):
            c = hdr.cells[idx]
            c.text = text
            c.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{primary_hex}"/>')
            c._tc.get_or_add_tcPr().append(shd)
            for p in c.paragraphs:
                p.paragraph_format.keep_with_next = True
                for r in p.runs:
                    r.font.bold = True
                    r.font.size = Pt(10.5)
                    r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

        for r_idx, (cat, items) in enumerate(grouped.items()):
            row = table.add_row()
            vals = [cat, ", ".join(items)]
            for c_idx, val in enumerate(vals):
                cell = row.cells[c_idx]
                cell.text = val
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                if r_idx % 2 == 1:
                    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F1F5F9"/>')
                    cell._tc.get_or_add_tcPr().append(shd)
                for p in cell.paragraphs:
                    p.paragraph_format.space_before = Pt(2)
                    p.paragraph_format.space_after = Pt(2)
                    for r in p.runs:
                        r.font.size = Pt(10)
                        if c_idx == 0:
                            r.font.bold = True

    # 3. Work & Internship Experience
    sel_exp = [e for e in portfolio["experience"] if e["id"] in selected_ids.get("experience_ids", [])]
    if sel_exp:
        add_section_header("Professional & Internship Experience")
        for exp in sel_exp:
            ep = doc.add_paragraph()
            ep.paragraph_format.space_before = Pt(4)
            ep.paragraph_format.space_after = Pt(2)
            ep.paragraph_format.keep_with_next = True
            r1 = ep.add_run(f"{exp['role_title']} — {exp['company']} ({exp['employment_type']})")
            r1.font.bold = True
            r1.font.size = Pt(11)
            r2 = ep.add_run(f"  |  {exp['start_date']} – {exp['end_date']}  |  {exp['location']}")
            r2.font.size = Pt(11)
            r2.font.color.rgb = muted_rgb
            for b in exp["achievements_bullets"]:
                bp = doc.add_paragraph(style="List Bullet")
                bp.paragraph_format.space_before = Pt(1)
                bp.paragraph_format.space_after = Pt(2)
                rb = bp.add_run(b)
                rb.font.size = Pt(11)

    # 4. Selected Key Projects
    sel_prj = [p for p in portfolio["projects"] if p["id"] in selected_ids.get("project_ids", [])]
    if sel_prj:
        add_section_header("Selected Key Projects")
        for prj in sel_prj:
            pp = doc.add_paragraph()
            pp.paragraph_format.space_before = Pt(4)
            pp.paragraph_format.space_after = Pt(2)
            pp.paragraph_format.keep_with_next = True
            r1 = pp.add_run(f"{prj['title']} ({prj['role']})")
            r1.font.bold = True
            r1.font.size = Pt(11)
            r2 = pp.add_run(f"  |  {prj['start_date']} – {prj['end_date']}  |  Tech: {prj['tech_stack']}")
            r2.font.size = Pt(11)
            r2.font.color.rgb = muted_rgb
            for b in prj["description_bullets"]:
                bp = doc.add_paragraph(style="List Bullet")
                bp.paragraph_format.space_before = Pt(1)
                bp.paragraph_format.space_after = Pt(2)
                rb = bp.add_run(b)
                rb.font.size = Pt(11)

    # 5. Education & Certifications & Publications
    add_section_header("Education, Certifications & Publications")
    for edu in portfolio["education"]:
        if edu["id"] in selected_ids.get("education_ids", ["EDU-01"]):
            edp = doc.add_paragraph()
            edp.paragraph_format.space_after = Pt(3)
            r_ed = edp.add_run(f"{edu['degree']} in {edu['field_of_study']} — {edu['institution']}")
            r_ed.font.bold = True
            r_ed.font.size = Pt(11)
            r_ed2 = edp.add_run(f" ({edu['start_date']} – {edu['end_date']}) | Grade: {edu['gpa_or_grade']}. {edu['highlights']}")
            r_ed2.font.size = Pt(11)

    sel_crt = [c for c in portfolio["certifications"] if c["id"] in selected_ids.get("certification_ids", [])]
    for crt in sel_crt:
        cp = doc.add_paragraph(style="List Bullet")
        cp.paragraph_format.space_after = Pt(2)
        rc1 = cp.add_run(f"Certification: {crt['name']} — {crt['issuing_organization']} ({crt['issue_date']}, ID: {crt['credential_id']})")
        rc1.font.size = Pt(11)

    sel_pub = [p for p in portfolio["publications_activities"] if p["id"] in selected_ids.get("publication_ids", [])]
    for pub in sel_pub:
        pubp = doc.add_paragraph(style="List Bullet")
        pubp.paragraph_format.space_after = Pt(2)
        rp1 = pubp.add_run(f"{pub['item_type']}: '{pub['title']}' — {pub['venue_or_publisher']} ({pub['publication_date']}). {pub['summary']}")
        rp1.font.size = Pt(11)

    sel_ach = [a for a in portfolio["achievements"] if a["id"] in selected_ids.get("achievement_ids", [])]
    for ach in sel_ach:
        achp = doc.add_paragraph(style="List Bullet")
        achp.paragraph_format.space_after = Pt(2)
        ra1 = achp.add_run(f"Award: {ach['title']} — {ach['issuer_or_event']} ({ach['date_awarded']})")
        ra1.font.size = Pt(11)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    doc.save(output_path)
    return output_path
