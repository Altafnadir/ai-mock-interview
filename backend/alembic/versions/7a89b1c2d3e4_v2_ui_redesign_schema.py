"""v2_ui_redesign_schema

Revision ID: 7a89b1c2d3e4
Revises: 47602d1e9233
Create Date: 2026-10-04 03:59:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '7a89b1c2d3e4'
down_revision = '47602d1e9233'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # 1. New Tables
    op.create_table(
        'coach_conversations',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('user_id', sa.String(length=36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_table(
        'coach_messages',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('conversation_id', sa.String(length=36), sa.ForeignKey('coach_conversations.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', sa.String(length=20), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_table(
        'badges',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('code', sa.String(length=50), unique=True, nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=False),
        sa.Column('icon', sa.String(length=50), nullable=False),
        sa.Column('criteria_json', sa.JSON(), nullable=False),
        sa.Column('points', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_table(
        'user_badges',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('user_id', sa.String(length=36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('badge_id', sa.String(length=36), sa.ForeignKey('badges.id', ondelete='CASCADE'), nullable=False),
        sa.Column('earned_at', sa.DateTime(), nullable=False),
    )
    op.create_table(
        'points_ledger',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('user_id', sa.String(length=36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('points', sa.Integer(), nullable=False),
        sa.Column('reason', sa.String(length=255), nullable=False),
        sa.Column('session_id', sa.String(length=36), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
    )
    op.create_table(
        'practice_goals',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('user_id', sa.String(length=36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('target', sa.Integer(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_table(
        'notification_preferences',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('user_id', sa.String(length=36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('type', sa.String(length=50), nullable=False),
        sa.Column('in_app', sa.Boolean(), nullable=False),
        sa.Column('email', sa.Boolean(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
    )
    op.create_table(
        'learning_progress',
        sa.Column('id', sa.String(length=36), primary_key=True),
        sa.Column('user_id', sa.String(length=36), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('resource_id', sa.String(length=36), sa.ForeignKey('learning_resources.id', ondelete='CASCADE'), nullable=False),
        sa.Column('watched_at', sa.DateTime(), nullable=False),
    )

    # 2. Add columns with batch_alter_table for SQLite compatibility
    with op.batch_alter_table('resume_analyses') as batch_op:
        batch_op.add_column(sa.Column('resume_score', sa.Float(), server_default='85.0', nullable=False))
        batch_op.add_column(sa.Column('top_skills', sa.JSON(), server_default='[]', nullable=False))
        batch_op.add_column(sa.Column('years_experience', sa.Float(), server_default='2.0', nullable=False))
        batch_op.add_column(sa.Column('projects_count', sa.Integer(), server_default='3', nullable=False))
        batch_op.add_column(sa.Column('strengths', sa.JSON(), server_default='[]', nullable=False))
        batch_op.add_column(sa.Column('areas_to_improve', sa.JSON(), server_default='[]', nullable=False))

    with op.batch_alter_table('analysis_voice') as batch_op:
        batch_op.add_column(sa.Column('volume_score', sa.Float(), server_default='85.0', nullable=False))
        batch_op.add_column(sa.Column('pitch_score', sa.Float(), server_default='82.0', nullable=False))
        batch_op.add_column(sa.Column('pace_score', sa.Float(), server_default='85.0', nullable=False))
        batch_op.add_column(sa.Column('pronunciation_score', sa.Float(), server_default='84.0', nullable=False))
        batch_op.add_column(sa.Column('filler_score', sa.Float(), server_default='92.0', nullable=False))
        batch_op.add_column(sa.Column('clarity_label', sa.String(length=50), server_default='Optimal', nullable=False))

    with op.batch_alter_table('analysis_vision') as batch_op:
        batch_op.add_column(sa.Column('shoulder_position_score', sa.Float(), server_default='82.0', nullable=False))
        batch_op.add_column(sa.Column('head_position_score', sa.Float(), server_default='80.0', nullable=False))
        batch_op.add_column(sa.Column('hand_gesture_score', sa.Float(), server_default='78.0', nullable=False))
        batch_op.add_column(sa.Column('gaze_consistency_score', sa.Float(), server_default='80.0', nullable=False))
        batch_op.add_column(sa.Column('blink_rate_per_min', sa.Float(), server_default='18.0', nullable=False))
        batch_op.add_column(sa.Column('blink_label', sa.String(length=20), server_default='Normal', nullable=False))
        batch_op.add_column(sa.Column('distraction_score', sa.Float(), server_default='85.0', nullable=False))

    with op.batch_alter_table('learning_resources') as batch_op:
        batch_op.add_column(sa.Column('level', sa.String(length=20), server_default='Beginner', nullable=False))
        batch_op.add_column(sa.Column('thumbnail_url', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('duration_seconds', sa.Integer(), server_default='600', nullable=False))
        batch_op.add_column(sa.Column('is_featured', sa.Boolean(), server_default='0', nullable=False))
        batch_op.add_column(sa.Column('view_count', sa.Integer(), server_default='0', nullable=False))

    with op.batch_alter_table('candidate_profiles') as batch_op:
        batch_op.add_column(sa.Column('location', sa.String(length=100), nullable=True))

def downgrade() -> None:
    pass
