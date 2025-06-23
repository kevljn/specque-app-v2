import unittest
from app import create_app, db
from app.models.user import User
from app.models.legislative import LegislativeText, Amendment, Vote

class TestModels(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        user = User(email='test@example.com', role='deputy')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        self.assertIsNotNone(user.id)
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.check_password('wrongpassword'))
        self.assertEqual(user.role, 'deputy')

    def test_legislative_text_creation(self):
        text = LegislativeText(
            title='Test Text',
            content='Test Content',
            status='draft'
        )
        db.session.add(text)
        db.session.commit()
        
        self.assertIsNotNone(text.id)
        self.assertEqual(text.title, 'Test Text')
        self.assertEqual(text.status, 'draft')

    def test_amendment_creation(self):
        user = User(email='test@example.com', role='deputy')
        user.set_password('password123')
        db.session.add(user)
        
        text = LegislativeText(
            title='Test Text',
            content='Test Content',
            status='in_commission'
        )
        db.session.add(text)
        db.session.commit()
        
        amendment = Amendment(
            legislative_text_id=text.id,
            author_id=user.id,
            content='Amendment Content'
        )
        db.session.add(amendment)
        db.session.commit()
        
        self.assertIsNotNone(amendment.id)
        self.assertEqual(amendment.content, 'Amendment Content')
        self.assertEqual(amendment.status, 'proposed')

    def test_vote_creation(self):
        user = User(email='test@example.com', role='deputy')
        user.set_password('password123')
        db.session.add(user)
        
        text = LegislativeText(
            title='Test Text',
            content='Test Content',
            status='in_plenary'
        )
        db.session.add(text)
        db.session.commit()
        
        vote = Vote(
            user_id=user.id,
            legislative_text_id=text.id,
            vote_type='for'
        )
        db.session.add(vote)
        db.session.commit()
        
        self.assertIsNotNone(vote.id)
        self.assertEqual(vote.vote_type, 'for')

if __name__ == '__main__':
    unittest.main() 