from reportlab.platypus import SimpleDocTemplate ,Paragraph , Spacer , Table ,TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
def generate_pdf_report(
    filename,
    ats_score,
    matched_skills,
    missing_skills,
    ai_feedback
):
    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    story = []

    # ------------------------
    # Title
    # ------------------------

    title = Paragraph(
        "<font size=22><b>AI Resume Analysis Report</b></font>",
        styles["Title"]
    )

    story.append(title)
    story.append(Spacer(1, 15))

    # ------------------------
    # Date
    # ------------------------

    date = datetime.now().strftime("%d %B %Y")

    story.append(
        Paragraph(
            f"<b>Generated:</b> {date}",
            styles["Normal"]
        )
    )

    story.append(Spacer(1, 15))

    # ------------------------
    # ATS Table
    # ------------------------

    ats_table = Table([
        ["ATS Match Score", f"{ats_score}%"]
    ])

    ats_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.darkblue),
        ("TEXTCOLOR",(0,0),(-1,-1),colors.white),
        ("ALIGN",(0,0),(-1,-1),"CENTER"),
        ("FONTNAME",(0,0),(-1,-1),"Helvetica-Bold"),
        ("FONTSIZE",(0,0),(-1,-1),16),
        ("BOTTOMPADDING",(0,0),(-1,-1),12),
        ("GRID",(0,0),(-1,-1),1,colors.white)
    ]))

    story.append(ats_table)

    story.append(Spacer(1,20))

    # ------------------------
    # Matching Skills
    # ------------------------

    story.append(
        Paragraph(
            "<b>Matching Skills</b>",
            styles["Heading2"]
        )
    )

    if matched_skills:

        data = [["Skill"]]

        for skill in matched_skills:
            data.append([skill])

        table = Table(data)

        table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.green),   # Header only
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),

    ("BACKGROUND", (0,1), (-1,-1), colors.beige),  # Data rows
    ("TEXTCOLOR", (0,1), (-1,-1), colors.black),

    ("GRID", (0,0), (-1,-1), 1, colors.black),
    ("BOTTOMPADDING", (0,0), (-1,0), 8),
]))
        story.append(table)

    else:

        story.append(
            Paragraph(
                "No Matching Skills",
                styles["Normal"]
            )
        )

    story.append(Spacer(1,15))

    # ------------------------
    # Missing Skills
    # ------------------------

    story.append(
        Paragraph(
            "<b>Missing Skills</b>",
            styles["Heading2"]
        )
    )

    if missing_skills:

        data = [["Skill"]]

        for skill in missing_skills:
            data.append([skill])

        table = Table(data)

        table.setStyle(TableStyle([
    ("BACKGROUND", (0,0), (-1,0), colors.green),   # Header only
    ("TEXTCOLOR", (0,0), (-1,0), colors.white),

    ("BACKGROUND", (0,1), (-1,-1), colors.beige),  # Data rows
    ("TEXTCOLOR", (0,1), (-1,-1), colors.black),

    ("GRID", (0,0), (-1,-1), 1, colors.black),
    ("BOTTOMPADDING", (0,0), (-1,0), 8),
]))
        story.append(table)

    else:

        story.append(
            Paragraph(
                "No Missing Skills",
                styles["Normal"]
            )
        )

    story.append(Spacer(1,20))

    # ------------------------
    # AI Feedback
    # ------------------------

    story.append(
        Paragraph(
            "<b>AI Feedback</b>",
            styles["Heading2"]
        )
    )

    feedback = ai_feedback.replace("\n","<br/>")

    story.append(
        Paragraph(
            feedback,
            styles["BodyText"]
        )
    )

    story.append(Spacer(1,25))

    # ------------------------
    # Footer
    # ------------------------

    story.append(
        Paragraph(
            "<font color='grey'>Generated using AI Resume Analyzer by Gurmeet Punia</font>",
            styles["Italic"]
        )
    )

    try:
        doc.build(story)
        return True
    except Exception as e:
        print(e)
        return False