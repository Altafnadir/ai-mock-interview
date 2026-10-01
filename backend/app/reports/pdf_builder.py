import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List, Optional

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, KeepTogether, HRFlowable
)

from app.core.config import settings

class PDFReportBuilder:
    """Builds official ReportLab PDF documents:
    1. Full Multi-Page Comprehensive Report
    2. 1-Page Condensed AI Performance Summary
    3. Visual Performance Poster
    """

    def _get_storage_dir(self) -> Path:
        reports_dir = Path(settings.STORAGE_DIR) / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        return reports_dir

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
        """Generates comprehensive multi-page PDF evaluation report."""
        reports_dir = self._get_storage_dir()
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

        primary_color = colors.HexColor("#0284c7")  # Sky/Primary 600
        dark_slate = colors.HexColor("#0f172a")     # Slate 900
        muted_slate = colors.HexColor("#475569")    # Slate 600
        card_bg = colors.HexColor("#f8fafc")        # Slate 50
        border_color = colors.HexColor("#e2e8f0")   # Slate 200
        success_color = colors.HexColor("#10b981")  # Emerald 500

        title_style = ParagraphStyle(
            "DocTitle", parent=styles["Normal"],
            fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=dark_slate
        )
        subtitle_style = ParagraphStyle(
            "DocSubtitle", parent=styles["Normal"],
            fontName="Helvetica", fontSize=9, leading=13, textColor=muted_slate
        )
        h2_style = ParagraphStyle(
            "Heading2Style", parent=styles["Normal"],
            fontName="Helvetica-Bold", fontSize=13, leading=17, textColor=dark_slate,
            spaceBefore=12, spaceAfter=6
        )
        body_style = ParagraphStyle(
            "DocBody", parent=styles["Normal"],
            fontName="Helvetica", fontSize=9, leading=13, textColor=dark_slate
        )

        story = []

        # 1. Header
        header_table = Table([
            [
                Paragraph("<b>AI Mock Interview Preparation System</b><br/><font size='8' color='#64748b'>Gujrat Institute of Management Sciences (PMAS-AAUR)</font>", title_style),
                Paragraph(f"<b>Session ID:</b> {session_id[:8]}<br/><b>Date:</b> {date_str}", subtitle_style)
            ]
        ], colWidths=[380, 150])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ]))
        story.append(header_table)
        story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=8, spaceAfter=12))

        # 2. Candidate Overview & Overall Score Box
        score_box = Table([
            [Paragraph(f"<font size='26' color='#0284c7'><b>{overall_score:.1f}%</b></font><br/><b>Overall Score</b>", ParagraphStyle('Score', alignment=1)),
             Paragraph(f"<b>Candidate:</b> {candidate_name}<br/><b>Email:</b> {candidate_email}<br/><b>Target Role:</b> {job_role}<br/><b>Category:</b> {category} ({difficulty})<br/><b>Hiring Verdict:</b> <font color='#10b981'><b>{final_verdict}</b></font>", body_style)]
        ], colWidths=[150, 380])
        score_box.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), card_bg),
            ('BOX', (0, 0), (-1, -1), 1, border_color),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ]))
        story.append(score_box)
        story.append(Spacer(1, 14))

        # 3. 7-Dimensional Core Metrics
        story.append(Paragraph("Multimodal Competency Breakdown", h2_style))
        scores_matrix = [
            ["Content / Technical", "Communication", "Voice Dynamics", "Confidence", "Eye Contact", "Body Language", "Grammar"],
            [
                f"{score_breakdown.get('content_score', overall_score):.1f}%",
                f"{score_breakdown.get('communication_score', overall_score):.1f}%",
                f"{score_breakdown.get('voice_score', overall_score):.1f}%",
                f"{score_breakdown.get('confidence_score', overall_score):.1f}%",
                f"{score_breakdown.get('eye_contact_score', overall_score):.1f}%",
                f"{score_breakdown.get('body_language_score', overall_score):.1f}%",
                f"{score_breakdown.get('grammar_score', overall_score):.1f}%",
            ]
        ]
        breakdown_table = Table(scores_matrix, colWidths=[75, 75, 75, 75, 75, 78, 77])
        breakdown_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#0284c7")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, border_color),
            ('BACKGROUND', (0, 1), (-1, 1), colors.white),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(breakdown_table)
        story.append(Spacer(1, 14))

        # 4. Strengths & Areas for Improvement
        story.append(Paragraph("Evaluator Feedback: Strengths & Weaknesses", h2_style))
        str_content = "<br/>".join([f"&bull; {s}" for s in (strengths or ["Demonstrated solid preparation and clarity."])[:4]])
        weak_content = "<br/>".join([f"&bull; {w}" for w in (weaknesses or ["Could provide more quantified impact metrics."])[:4]])

        sw_data = [
            [Paragraph(f"<b>Key Strengths</b><br/>{str_content}", body_style),
             Paragraph(f"<b>Areas for Growth</b><br/>{weak_content}", body_style)]
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
                    f"{star:.1f}%",
                    f"{acc:.1f}%"
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

        doc.build(story)
        relative_path = f"{settings.STORAGE_DIR}/reports/{pdf_filename}".replace("\\", "/")
        return relative_path

    def build_summary_pdf(
        self,
        session_id: str,
        candidate_name: str,
        job_role: str,
        date_str: str,
        overall_score: float,
        final_verdict: str,
        score_breakdown: Dict[str, float],
        strengths: List[str],
        weaknesses: List[str],
        top_tips: List[str]
    ) -> str:
        """Generates a concise, high-density 1-page executive performance summary."""
        reports_dir = self._get_storage_dir()
        pdf_filename = f"summary_{session_id}.pdf"
        output_path = reports_dir / pdf_filename

        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        dark_slate = colors.HexColor("#0f172a")
        primary_color = colors.HexColor("#0284c7")
        card_bg = colors.HexColor("#f8fafc")
        border_color = colors.HexColor("#e2e8f0")

        title_style = ParagraphStyle(
            "SummaryTitle", parent=styles["Normal"],
            fontName="Helvetica-Bold", fontSize=18, leading=22, textColor=dark_slate
        )
        body_style = ParagraphStyle(
            "SummaryBody", parent=styles["Normal"],
            fontName="Helvetica", fontSize=8.5, leading=12, textColor=dark_slate
        )
        h2_style = ParagraphStyle(
            "SummaryH2", parent=styles["Normal"],
            fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=dark_slate,
            spaceBefore=8, spaceAfter=4
        )

        story = []

        # Header
        header = Table([
            [Paragraph("<b>AI Mock Interview — Executive Performance Summary</b>", title_style),
             Paragraph(f"<b>Date:</b> {date_str}<br/><b>Target:</b> {job_role}", body_style)]
        ], colWidths=[380, 160])
        story.append(header)
        story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceBefore=6, spaceAfter=10))

        # Hero Banner
        hero = Table([
            [
                Paragraph(f"<font size='28' color='#0284c7'><b>{overall_score:.1f}%</b></font><br/><b>Overall Readiness</b>", ParagraphStyle('H1', alignment=1)),
                Paragraph(f"<b>Candidate:</b> {candidate_name}<br/><b>Role Evaluated:</b> {job_role}<br/><b>Verdict Band:</b> <font color='#10b981'><b>{final_verdict}</b></font><br/><b>Session Reference:</b> {session_id[:8]}", body_style)
            ]
        ], colWidths=[150, 390])
        hero.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), card_bg),
            ('BOX', (0, 0), (-1, -1), 0.5, border_color),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(hero)
        story.append(Spacer(1, 10))

        # Core Matrix
        story.append(Paragraph("Core Competency Summary (0-100)", h2_style))
        matrix_data = [
            ["Technical / Content", "Communication", "Voice Dynamics", "Confidence", "Eye Contact", "Body Language", "Grammar"],
            [
                f"{score_breakdown.get('content_score', overall_score):.1f}%",
                f"{score_breakdown.get('communication_score', overall_score):.1f}%",
                f"{score_breakdown.get('voice_score', overall_score):.1f}%",
                f"{score_breakdown.get('confidence_score', overall_score):.1f}%",
                f"{score_breakdown.get('eye_contact_score', overall_score):.1f}%",
                f"{score_breakdown.get('body_language_score', overall_score):.1f}%",
                f"{score_breakdown.get('grammar_score', overall_score):.1f}%",
            ]
        ]
        matrix_table = Table(matrix_data, colWidths=[77, 77, 77, 77, 77, 78, 77])
        matrix_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7.5),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, border_color),
            ('PADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(matrix_table)
        story.append(Spacer(1, 10))

        # Strengths & Opportunities
        story.append(Paragraph("Key Strengths & Growth Areas", h2_style))
        s_bullets = "<br/>".join([f"&bull; {s}" for s in (strengths or ["Solid domain knowledge."])[:3]])
        w_bullets = "<br/>".join([f"&bull; {w}" for w in (weaknesses or ["Provide more quantified metrics."])[:3]])
        sw_box = Table([
            [Paragraph(f"<b>Key Strengths:</b><br/>{s_bullets}", body_style),
             Paragraph(f"<b>Targeted Growth Areas:</b><br/>{w_bullets}", body_style)]
        ], colWidths=[270, 270])
        sw_box.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#ecfdf5")),
            ('BACKGROUND', (1, 0), (1, -1), colors.HexColor("#fef2f2")),
            ('BOX', (0, 0), (-1, -1), 0.5, border_color),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(sw_box)
        story.append(Spacer(1, 10))

        # Top Coaching Action Items
        story.append(Paragraph("Recommended Action Plan", h2_style))
        tips_bullets = "<br/>".join([f"<b>{i+1}.</b> {t}" for i, t in enumerate((top_tips or ["Practice STAR behavioral framework.", "Maintain steady eye contact with webcam."])[:3])])
        tips_box = Table([[Paragraph(tips_bullets, body_style)]], colWidths=[540])
        tips_box.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), card_bg),
            ('BOX', (0, 0), (-1, -1), 0.5, border_color),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(tips_box)

        doc.build(story)
        relative_path = f"{settings.STORAGE_DIR}/reports/{pdf_filename}".replace("\\", "/")
        return relative_path

    def build_poster_pdf(
        self,
        session_id: str,
        candidate_name: str,
        job_role: str,
        overall_score: float,
        final_verdict: str,
        score_breakdown: Dict[str, float],
        strengths: List[str]
    ) -> str:
        """Generates an aesthetic portrait Performance Poster showcasing candidate achievements."""
        reports_dir = self._get_storage_dir()
        pdf_filename = f"poster_{session_id}.pdf"
        output_path = reports_dir / pdf_filename

        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()
        primary_color = colors.HexColor("#0284c7")
        dark_slate = colors.HexColor("#0f172a")
        emerald = colors.HexColor("#10b981")
        card_bg = colors.HexColor("#0f172a")

        poster_title = ParagraphStyle(
            "PosterTitle", parent=styles["Normal"],
            fontName="Helvetica-Bold", fontSize=24, leading=28, textColor=colors.HexColor("#38bdf8"),
            alignment=1
        )
        poster_sub = ParagraphStyle(
            "PosterSub", parent=styles["Normal"],
            fontName="Helvetica", fontSize=11, leading=15, textColor=colors.HexColor("#94a3b8"),
            alignment=1
        )
        badge_style = ParagraphStyle(
            "PosterBadge", parent=styles["Normal"],
            fontName="Helvetica-Bold", fontSize=13, leading=17, textColor=emerald,
            alignment=1
        )
        white_body = ParagraphStyle(
            "WhiteBody", parent=styles["Normal"],
            fontName="Helvetica", fontSize=9.5, leading=14, textColor=colors.HexColor("#e2e8f0")
        )

        story = []

        # Dark theme poster container
        poster_content = [
            Paragraph("AI INTERVIEW PERFORMANCE POSTER", poster_title),
            Spacer(1, 4),
            Paragraph(f"Official Candidate Evaluation &bull; {job_role}", poster_sub),
            Spacer(1, 16),
            Paragraph(f"<font size='48' color='#38bdf8'><b>{overall_score:.1f}%</b></font>", ParagraphStyle('PBig', alignment=1)),
            Paragraph(f"OVERALL READINESS SCORE &bull; <b>{final_verdict.upper()}</b>", badge_style),
            Spacer(1, 16),
        ]

        # 6 Competency bars
        comp_rows = [
            ["Pillar", "Score Rating"],
            ["Technical / Content Depth", f"{score_breakdown.get('content_score', overall_score):.1f}%"],
            ["Communication Effectiveness", f"{score_breakdown.get('communication_score', overall_score):.1f}%"],
            ["Voice Modulation & Tempo", f"{score_breakdown.get('voice_score', overall_score):.1f}%"],
            ["Candidate Poise & Confidence", f"{score_breakdown.get('confidence_score', overall_score):.1f}%"],
            ["Eye Contact Engagement", f"{score_breakdown.get('eye_contact_score', overall_score):.1f}%"],
            ["Body Posture & Stability", f"{score_breakdown.get('body_language_score', overall_score):.1f}%"],
            ["Grammar & Language Quality", f"{score_breakdown.get('grammar_score', overall_score):.1f}%"],
        ]
        ctable = Table(comp_rows, colWidths=[320, 160])
        ctable.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#38bdf8")),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#334155")),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.white),
            ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#1e293b")),
            ('PADDING', (0, 0), (-1, -1), 6),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ]))
        poster_content.append(ctable)
        poster_content.append(Spacer(1, 16))

        # Verified Candidate Signature footer
        foot_text = (
            f"<b>Candidate:</b> {candidate_name} &nbsp;|&nbsp; "
            f"<b>Role:</b> {job_role} &nbsp;|&nbsp; "
            f"<b>Verification:</b> GIMS-BSSE-F202206 &nbsp;|&nbsp; "
            f"<b>Session:</b> {session_id[:8]}"
        )
        poster_content.append(Paragraph(foot_text, ParagraphStyle('PFoots', alignment=1, textColor=colors.HexColor("#94a3b8"), fontSize=8)))

        poster_table = Table([[item] for item in poster_content], colWidths=[540])
        poster_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#090d16")),
            ('BOX', (0, 0), (-1, -1), 2, colors.HexColor("#0284c7")),
            ('TOPPADDING', (0, 0), (-1, -1), 20),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 20),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
        ]))
        story.append(poster_table)

        doc.build(story)
        relative_path = f"{settings.STORAGE_DIR}/reports/{pdf_filename}".replace("\\", "/")
        return relative_path

pdf_builder = PDFReportBuilder()
