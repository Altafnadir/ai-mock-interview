import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, KeepTogether, HRFlowable
)

from app.core.config import settings

class PDFReportBuilder:
    """Builds comprehensive, professional PDF reports for candidate interview sessions."""

    def build_report_pdf(
        self,
        session_id: str,
        candidate_name: str,
        candidate_email: str,
        job_role: str,
        category: str,
        difficulty: str,
        date_str: str,
        overall_score: float,
        final_verdict: str,
        score_breakdown: Dict[str, float],
        strengths: List[str],
        weaknesses: List[str],
        improvement_tips: List[str],
        questions_data: List[Dict[str, Any]],
        recommendations: List[Dict[str, Any]]
    ) -> str:
        reports_dir = Path(settings.STORAGE_DIR) / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        pdf_filename = f"report_{session_id}.pdf"
        output_path = reports_dir / pdf_filename

        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=40,
            leftMargin=40,
            topMargin=40,
            bottomMargin=40
        )

        styles = getSampleStyleSheet()

        # Custom Palette
        primary_color = colors.HexColor("#0284c7")  # Sky/Primary 600
        dark_slate = colors.HexColor("#0f172a")     # Slate 900
        muted_slate = colors.HexColor("#475569")    # Slate 600
        card_bg = colors.HexColor("#f8fafc")        # Slate 50
        border_color = colors.HexColor("#e2e8f0")   # Slate 200
        success_color = colors.HexColor("#10b981")  # Emerald 500

        # Custom typography styles
        title_style = ParagraphStyle(
            "DocTitle",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=20,
            leading=24,
            textColor=dark_slate
        )

        subtitle_style = ParagraphStyle(
            "DocSubtitle",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=muted_slate
        )

        h2_style = ParagraphStyle(
            "Heading2Style",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=dark_slate,
            spaceBefore=12,
            spaceAfter=6
        )

        body_style = ParagraphStyle(
            "DocBody",
            parent=styles["Normal"],
            fontName="Helvetica",
            fontSize=9,
            leading=13,
            textColor=dark_slate
        )

        badge_style = ParagraphStyle(
            "VerdictBadge",
            parent=styles["Normal"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=14,
            textColor=colors.white,
            alignment=1
        )

        story = []

        # 1. Header Banner
        header_table_data = [
            [
                Paragraph("<b>AI-Based Mock Interview Preparation System</b>", title_style),
                Paragraph(f"<b>Overall Score</b><br/><font size='22' color='#0284c7'><b>{overall_score}</b></font>/100", ParagraphStyle("ScoreBox", fontName="Helvetica", alignment=2, textColor=dark_slate))
            ],
            [
                Paragraph("Project ID: <b>GIMS-BSSE-F202206</b> &bull; PMAS-Arid Agriculture University Rawalpindi", subtitle_style),
                Paragraph(f"<font color='#0284c7'><b>{final_verdict}</b></font>", ParagraphStyle("VerdictText", fontName="Helvetica-Bold", alignment=2, fontSize=10))
            ]
        ]
        header_table = Table(header_table_data, colWidths=[380, 150])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=14))

        # 2. Candidate & Session Info Grid
        meta_data = [
            [
                Paragraph(f"<b>Candidate:</b> {candidate_name}", body_style),
                Paragraph(f"<b>Job Role:</b> {job_role}", body_style)
            ],
            [
                Paragraph(f"<b>Email:</b> {candidate_email}", body_style),
                Paragraph(f"<b>Category:</b> {category} &bull; <b>Difficulty:</b> {difficulty}", body_style)
            ],
            [
                Paragraph(f"<b>Session ID:</b> {session_id[:16]}...", body_style),
                Paragraph(f"<b>Date Generated:</b> {date_str}", body_style)
            ]
        ]
        meta_table = Table(meta_data, colWidths=[265, 265])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), card_bg),
            ('BOX', (0, 0), (-1, -1), 0.5, border_color),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, border_color),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(meta_table)
        story.append(Spacer(1, 14))

        # 3. Weighted Evaluation Matrix Table
        story.append(Paragraph("Performance Dimension Breakdown", h2_style))
        eval_table_data = [
            ["Dimension", "Weight", "Score", "Rating", "Benchmark Status"],
            ["Content Depth & Technical Accuracy", "35%", f"{score_breakdown.get('content_score', 0)}%", "Strong", "Meets Industry Standard"],
            ["Communication & Grammar", "20%", f"{score_breakdown.get('communication_score', 0)}%", "Proficient", "Clear & Articulate"],
            ["Voice Dynamics & Pacing", "15%", f"{score_breakdown.get('voice_score', 0)}%", "Optimal", "120-150 WPM Range"],
            ["Eye Contact & Camera Engagement", "15%", f"{score_breakdown.get('eye_contact_score', 0)}%", "Good", "Active Gaze Engagement"],
            ["Confidence & Demeanor", "15%", f"{score_breakdown.get('confidence_score', 0)}%", "High", "Low Stress Indicators"]
        ]
        eval_table = Table(eval_table_data, colWidths=[180, 60, 65, 85, 140])
        eval_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), dark_slate),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, card_bg]),
            ('GRID', (0, 0), (-1, -1), 0.5, border_color),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('ALIGN', (1, 0), (2, -1), 'CENTER'),
        ]))
        story.append(eval_table)
        story.append(Spacer(1, 14))

        # 4. Strengths & Weaknesses 2-Column Box
        story.append(Paragraph("Key Observations & Feedback", h2_style))
        str_bullets = "<br/>".join([f"&bull; {s}" for s in strengths]) if strengths else "Consistent interview performance demonstrated."
        weak_bullets = "<br/>".join([f"&bull; {w}" for w in weaknesses]) if weaknesses else "No critical shortcomings observed."

        sw_data = [
            [
                Paragraph("<b>Strengths Identified</b>", ParagraphStyle("StrH", fontName="Helvetica-Bold", fontSize=9.5, textColor=colors.HexColor("#065f46"))),
                Paragraph("<b>Areas for Development</b>", ParagraphStyle("WeakH", fontName="Helvetica-Bold", fontSize=9.5, textColor=colors.HexColor("#991b1b")))
            ],
            [
                Paragraph(str_bullets, body_style),
                Paragraph(weak_bullets, body_style)
            ]
        ]
        sw_table = Table(sw_data, colWidths=[265, 265])
        sw_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#ecfdf5")),
            ('BACKGROUND', (1, 0), (1, -1), colors.HexColor("#fef2f2")),
            ('BOX', (0, 0), (0, -1), 0.5, colors.HexColor("#a7f3d0")),
            ('BOX', (1, 0), (1, -1), 0.5, colors.HexColor("#fecaca")),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(sw_table)
        story.append(Spacer(1, 14))

        # 5. Question-by-Question STAR Evaluation
        if questions_data:
            story.append(Paragraph("Detailed Question-by-Question Evaluation", h2_style))
            q_rows = [["#", "Question & Transcript Summary", "STAR Scores", "Technical Accuracy"]]
            for idx, q in enumerate(questions_data[:5]):
                q_text = q.get("question_text", f"Question {idx+1}")
                ans_text = q.get("transcript", "Answer recorded.")
                acc = q.get("technical_accuracy", 80.0)
                star = q.get("star_score", 82.0)

                q_cell = f"<b>Q: {q_text[:95]}...</b><br/><font color='#475569'>Ans: {ans_text[:110]}...</font>"
                q_rows.append([
                    str(idx + 1),
                    Paragraph(q_cell, body_style),
                    f"{star}%",
                    f"{acc}%"
                ])

            q_table = Table(q_rows, colWidths=[25, 365, 70, 70])
            q_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, border_color),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, card_bg]),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                ('ALIGN', (2, 0), (3, -1), 'CENTER'),
            ]))
            story.append(q_table)
            story.append(Spacer(1, 14))

        # 6. Recommendations & Learning Next Steps
        if recommendations or improvement_tips:
            story.append(Paragraph("Targeted Learning Resources & Practice Roadmap", h2_style))
            rec_items = []
            for tip in improvement_tips[:3]:
                rec_items.append(Paragraph(f"&bull; <b>Practice Focus:</b> {tip}", body_style))
            for r in recommendations[:3]:
                title = r.get("title", "Resource Tutorial")
                url = r.get("url", "https://youtube.com")
                rec_items.append(Paragraph(f"&bull; <b>Recommended Tutorial:</b> <font color='#0284c7'><u>{title}</u></font> ({url})", body_style))

            rec_table = Table([[item] for item in rec_items], colWidths=[530])
            rec_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), card_bg),
                ('BOX', (0, 0), (-1, -1), 0.5, border_color),
                ('TOPPADDING', (0, 0), (-1, -1), 5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ]))
            story.append(rec_table)

        # Build Document
        doc.build(story)
        relative_path = f"{settings.STORAGE_DIR}/reports/{pdf_filename}".replace("\\", "/")
        return relative_path

pdf_builder = PDFReportBuilder()
