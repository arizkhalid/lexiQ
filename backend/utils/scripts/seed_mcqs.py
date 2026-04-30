#!/usr/bin/env python3
"""
Convert Python dict MCQ files to valid JSON and seed into database.

Usage:
  cd backend
  python manage.py shell < utils/scripts/seed_mcqs.py
"""

import json
import ast
from pathlib import Path

# Import Django models
from quiz.models import Quiz, Question, Option
from django.contrib.auth.models import User
from django.db import transaction


def load_mcq_files():
    """Load and convert Python dict MCQ files to proper dicts."""
    # Hardcode to backend utils/mcqs
    mcqs_dir = Path("/home/ariz/repos/lexiQ/backend/utils/mcqs")
    print(f"Looking for MCQ files in: {mcqs_dir}")
    
    all_mcqs = []
    
    # Load all 5 files
    for i in range(1, 6):
        mcq_file = mcqs_dir / f"mcq_output{i}.json"
        if not mcq_file.exists():
            print(f"⚠️  {mcq_file.name} not found at {mcq_file}")
            continue
        
        with open(mcq_file, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Convert Python dict string to actual dict
        try:
            data = ast.literal_eval(content)
            all_mcqs.extend(data["words_mcqs"])
            print(f"✓ Loaded {mcq_file.name}: {len(data['words_mcqs'])} word MCQ sets")
        except Exception as e:
            print(f"❌ Error loading {mcq_file.name}: {e}")
            continue
    
    return all_mcqs


def seed_mcqs_to_db(all_mcqs, dry_run=False):
    """Seed MCQ data into database."""
    
    # Get or create default user for quizzes
    user, created = User.objects.get_or_create(username="mcq_seed")
    if created:
        print(f"✓ Created default user for MCQs")
    
    total_quizzes = 0
    total_questions = 0
    total_options = 0
    
    try:
        with transaction.atomic():
            for word_set_idx, word_mcq_set in enumerate(all_mcqs, 1):
                mcqs = word_mcq_set.get("mcqs", [])
                
                if dry_run:
                    print(f"[{word_set_idx}] Would create quiz with {len(mcqs)} questions")
                    continue
                
                # Create quiz for this word's MCQ set
                quiz = Quiz.objects.create(user=user)
                total_quizzes += 1
                
                for mcq in mcqs:
                    # Create question
                    question = Question.objects.create(
                        quiz=quiz,
                        text=mcq.get("question", "")
                    )
                    total_questions += 1
                    
                    # Create options
                    options_data = [
                        (mcq.get("correct_option", ""), True),
                        (mcq.get("wrong_option_1", ""), False),
                        (mcq.get("wrong_option_2", ""), False),
                        (mcq.get("wrong_option_3", ""), False),
                    ]
                    
                    for option_text, is_correct in options_data:
                        if option_text:
                            Option.objects.create(
                                question=question,
                                text=option_text,
                                is_correct=is_correct
                            )
                            total_options += 1
        
        if dry_run:
            print(f"\n📋 DRY RUN: Would create {total_quizzes} quizzes, {total_questions} questions, {total_options} options")
        else:
            print(f"\n✅ Seeded {total_quizzes} quizzes, {total_questions} questions, {total_options} options")
    
    except Exception as e:
        print(f"❌ Error seeding: {e}")
        if not dry_run:
            raise


# Main execution
all_mcqs = load_mcq_files()
print(f"\n📖 Total MCQ sets loaded: {len(all_mcqs)}")

if all_mcqs:
    dry_run = False  # Set to True for preview
    seed_mcqs_to_db(all_mcqs, dry_run=dry_run)
else:
    print("❌ No MCQ data loaded")
