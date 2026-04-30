#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Checking if data exists..."
LEXEME_COUNT=$(python manage.py shell -c "from words.models import Lexeme; print(Lexeme.objects.count())" 2>/dev/null || echo "0")

if [ "$LEXEME_COUNT" -eq 0 ]; then
    echo "No lexemes found. Seeding initial data..."
    python manage.py seed_gift_words
    echo "Lexeme data seeded successfully."
else
    echo "Lexemes already exist ($LEXEME_COUNT). Skipping seed_gift_words."
fi

echo "Checking if questions exist..."
QUESTION_COUNT=$(python manage.py shell -c "from quiz.models import Question; print(Question.objects.count())" 2>/dev/null || echo "0")

if [ "$QUESTION_COUNT" -eq 0 ]; then
    echo "No questions found. Loading MCQ data..."
    if [ -f "data-seeding/mcq_json1.json" ]; then
        python utils/scripts/seed_mcqs_by_lexeme.py
        echo "MCQ data seeded successfully."
    else
        echo "MCQ JSON files not found in data-seeding/. Skipping MCQ seed."
    fi
else
    echo "Questions already exist ($QUESTION_COUNT). Skipping MCQ seed."
fi

echo "Deployment complete!"
