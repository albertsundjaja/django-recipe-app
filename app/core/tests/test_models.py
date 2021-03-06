from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

from core import models


def sample_user(email='test@test.com', password='testpass'):
    """ Helper function to create a sample user """
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creaing a new user with an email"""
        email = 'something@test.com'
        password = 'test123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_with_email_normalized(self):
        """ Test that email for a new user is normalized
            (all lowercase for the domain)
        """
        email = 'something@TEST.com'
        user = get_user_model().objects.create_user(
            email=email,
            password='test123'
        )

        self.assertEqual(user.email, email.lower())

    def test_create_user_with_none_email(self):
        """ Test creating user with no email raises error """

        # anything we run must raise a ValueError
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """ Test create a new superuser """

        user = get_user_model().objects.create_superuser(
            email='test@test.com', password='test123')
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """
            Test the tag string representation
            i.e. the returned string
            from str(tag)
            this is a way to test our model is created
            successfully
        """
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag), tag.name)

    def test_ingredient_str(self):
        """Test the ingredient string representation"""
        ingredient = models.Ingredient.objects.create(
            user=sample_user(),
            name='Cucumber'
        )

        self.assertEqual(str(ingredient), ingredient.name)

    def test_recipe_str(self):
        """Test the recipe string representation"""
        recipe = models.Recipe.objects.create(
            user=sample_user(),
            title='Steak and mushroom sauce',
            time_minutes=5,
            price=5.00
        )

        self.assertEqual(str(recipe), recipe.title)

    @patch('uuid.uuid4')
    # the patch will pass the mocked function
    def test_recipe_file_name_uuid(self, mock_uuid):
        """Test that image is saved in the correct location"""
        # make the mock function return our arbitrary uuid value
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid

        file_path = models.recipe_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/recipe/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
