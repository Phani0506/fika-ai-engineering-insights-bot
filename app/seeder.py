import datetime
import random
from app.data_store import get_session, Commit, PullRequest

def seed_database():
    """Populates the database with realistic fake data for demo purposes."""
    session = get_session()

    # Check if data already exists to prevent re-seeding
    if session.query(Commit).count() > 0:
        print("Database already seeded. Skipping.")
        session.close()
        return

    print("Seeding database with fake data...")

    authors = ['dev1@example.com', 'dev2@example.com', 'dev3@example.com']
    
    # Seed Commits
    for i in range(100):
        author = random.choice(authors)
        days_ago = random.randint(1, 30)
        commit = Commit(
            commit_hash=f'fake_hash_{i}',
            author=author,
            timestamp=datetime.datetime.now() - datetime.timedelta(days=days_ago),
            additions=random.randint(5, 200),
            deletions=random.randint(0, 100),
            files_changed=random.randint(1, 10)
        )
        session.add(commit)

    # Add one outlier commit to test the analyst agent
    outlier_commit = Commit(
        commit_hash='outlier_hash',
        author='dev1@example.com',
        timestamp=datetime.datetime.now() - datetime.timedelta(days=3),
        additions=1500,
        deletions=700,
        files_changed=50
    )
    session.add(outlier_commit)

    # Seed Pull Requests
    for i in range(20):
        created_days_ago = random.randint(2, 20)
        merged_days_ago = created_days_ago - random.randint(1, 2)
        created_at = datetime.datetime.now() - datetime.timedelta(days=created_days_ago)
        merged_at = datetime.datetime.now() - datetime.timedelta(days=merged_days_ago)
        cycle_time = (merged_at - created_at).total_seconds() / 3600
        
        pr = PullRequest(
            pr_id=100 + i,
            author=random.choice(authors),
            created_at=created_at,
            merged_at=merged_at,
            cycle_time_hours=cycle_time
        )
        session.add(pr)

    session.commit()
    session.close()
    print("✅ Database seeding complete.")

# This allows running the seeder directly from the command line
if __name__ == '__main__':
    seed_database()