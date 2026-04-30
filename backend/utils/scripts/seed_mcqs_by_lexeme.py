#!/usr/bin/env python3
"""
Seed MCQ data with Lexeme foreign keys.
Questions are tied to Lexeme, can be searched by word.

Usage:
  cd backend
  python manage.py shell < utils/scripts/seed_mcqs_by_lexeme.py
"""

import json
from pathlib import Path
from django.db import transaction

from quiz.models import Question, Option
from words.models import Lexeme


def load_mcq_files():
    """Load all MCQ JSON files."""
    backend_dir = Path("/home/ariz/repos/lexiQ/backend")
    all_mcqs = {}
    
    for i in range(1, 6):
        mcq_file = backend_dir / f"mcq_json{i}.json"
        if not mcq_file.exists():
            print(f"⚠️  {mcq_file.name} not found")
            continue
        
        with open(mcq_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        words_mcqs = data.get("words_mcqs", {})
        all_mcqs.update(words_mcqs)
        print(f"✓ Loaded {mcq_file.name}: {len(words_mcqs)} words")
    
    return all_mcqs


def seed_mcqs_to_db(all_mcqs, dry_run=False):
    """Seed MCQ data into database with Lexeme foreign keys."""
    
    total_questions = 0
    total_options = 0
    words_not_found = []
    
    try:
        with transaction.atomic():
            for word, word_data in all_mcqs.items():
                # Find lexeme for this word
                lexeme = Lexeme.objects.filter(word=word.lower()).first()
                if not lexeme:
                    words_not_found.append(word)
                    continue
                
                mcqs = word_data.get("mcqs", [])
                
                for mcq in mcqs:
                    if dry_run:
                        print(f"[{word}] Would create question: {mcq.get('question')[:50]}...")
                        continue
                    
                    # Create question tied to lexeme
                    question = Question.objects.create(
                        lexeme=lexeme,
                        text=mcq.get("question", "")
                    )
                    total_questions += 1
                    
                    # Create 4 options
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
            print(f"\n📋 DRY RUN: Would create {total_questions} questions, {total_options} options")
        else:
            print(f"\n✅ Seeded {total_questions} questions, {total_options} options")
        
        if words_not_found:
            print(f"⚠️  Words not found in database: {', '.join(words_not_found[:5])}")
            if len(words_not_found) > 5:
                print(f"   ... and {len(words_not_found) - 5} more")
    
    except Exception as e:
        print(f"❌ Error seeding: {e}")
        if not dry_run:
            raise


# Main execution
print("📖 Loading MCQ files...\n")
all_mcqs = load_mcq_files()
print(f"\nTotal words with MCQs: {len(all_mcqs)}")

if all_mcqs:
    dry_run = False  # Set to True for preview
    seed_mcqs_to_db(all_mcqs, dry_run=dry_run)
else:
    print("❌ No MCQ data loaded")
