import json
from pathlib import Path
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from words.models import Lexeme, WordSense


class Command(BaseCommand):
    help = "Seed database with reviewed gift_words JSON data (reviewed_1.json through reviewed_6.json)"

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be seeded without committing to database',
        )
        parser.add_argument(
            '--replace-senses',
            action='store_true',
            help='Delete existing senses for words before inserting new ones',
        )

    def load_reviewed_files(self):
        """Load and merge reviewed_1.json through reviewed_6.json files."""
        scripts_dir = Path(__file__).parent.parent.parent.parent / "utils" / "scripts"
        reviewed_files = sorted([
            scripts_dir / f"reviewed_{i}.json"
            for i in range(1, 7)
            if (scripts_dir / f"reviewed_{i}.json").exists()
        ])
        
        if not reviewed_files:
            raise CommandError(
                "No reviewed JSON files found in utils/scripts/. "
                "Expected: reviewed_1.json through reviewed_6.json"
            )
        
        self.stdout.write(self.style.SUCCESS(f"📚 Found {len(reviewed_files)} reviewed files"))
        
        merged_lexemes = []
        merged_failures = []
        
        for reviewed_path in reviewed_files:
            with open(reviewed_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                lex_count = len(data.get("lexemes", []))
                fail_count = len(data.get("failures", []))
                merged_lexemes.extend(data.get("lexemes", []))
                merged_failures.extend(data.get("failures", []))
                self.stdout.write(f"  ✓ {reviewed_path.name}: {lex_count} lexemes, {fail_count} failures")
        
        return merged_lexemes, merged_failures

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        replace_senses = options['replace_senses']
        
        # Load data
        try:
            merged_lexemes, merged_failures = self.load_reviewed_files()
        except CommandError as e:
            self.stdout.write(self.style.ERROR(f"❌ {e}"))
            raise
        
        total_lexemes = len(merged_lexemes)
        total_failures = len(merged_failures)
        
        self.stdout.write(
            self.style.SUCCESS(
                f"\n📖 Seeding {total_lexemes} lexemes ({total_failures} failures)"
            )
        )
        
        created_lexemes = 0
        created_senses = 0
        updated_lexemes = 0
        skipped_senses = 0
        
        try:
            with transaction.atomic():
                for i, lexeme_entry in enumerate(merged_lexemes, 1):
                    word = lexeme_entry.get("word")
                    senses = lexeme_entry.get("senses", [])
                    
                    # Progress indicator
                    print(f"[{i}/{total_lexemes}] {word}: ", end="", flush=True)
                    
                    if dry_run:
                        lexeme_exists = Lexeme.objects.filter(word=word).exists()
                        action = "UPDATE" if lexeme_exists else "CREATE"
                        print(f"{action} lexeme + {len(senses)} sense(s)")
                        continue
                    
                    # Get or create lexeme
                    lexeme, lexeme_created = Lexeme.objects.get_or_create(word=word)
                    
                    if lexeme_created:
                        created_lexemes += 1
                    else:
                        updated_lexemes += 1
                    
                    # If replace_senses, delete old senses
                    if replace_senses and not lexeme_created:
                        old_count = WordSense.objects.filter(lexeme=lexeme).count()
                        WordSense.objects.filter(lexeme=lexeme).delete()
                        print(f"DELETE {old_count} old sense(s), ", end="", flush=True)
                    
                    # Create new senses
                    for sense_data in senses:
                        WordSense.objects.create(
                            lexeme=lexeme,
                            definition=sense_data.get("definition", ""),
                            example=sense_data.get("example", ""),
                            part_of_speech=sense_data.get("part_of_speech", ""),
                            synonyms=sense_data.get("synonyms", []),
                            antonyms=sense_data.get("antonyms", []),
                            usage=sense_data.get("usage", ""),
                            examples=sense_data.get("examples", []),
                            register=sense_data.get("register", ""),
                            connotation=sense_data.get("connotation", ""),
                            collocations=sense_data.get("collocations", []),
                            word_forms=sense_data.get("word_forms", {}),
                        )
                        created_senses += 1
                    
                    print(f"✓ (+{len(senses)} sense(s))")
            
            # Summary
            self.stdout.write("")
            if dry_run:
                self.stdout.write(
                    self.style.WARNING(
                        f"📋 DRY RUN: Would create {created_lexemes} new lexemes, "
                        f"update {updated_lexemes} existing, and add {created_senses} total senses"
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ Successfully seeded!\n"
                        f"   Created: {created_lexemes} lexemes\n"
                        f"   Updated: {updated_lexemes} lexemes\n"
                        f"   Senses: {created_senses} total"
                    )
                )
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error: {e}"))
            if not dry_run:
                raise
