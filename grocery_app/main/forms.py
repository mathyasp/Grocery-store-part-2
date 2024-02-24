from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SelectField, SubmitField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, NumberRange
from grocery_app.models import ItemCategory, GroceryStore, GroceryItem

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""

    # TODO: Add the following fields to the form class:
    # - title - StringField
    # - address - StringField
    # - submit button
    title = StringField('Store Name',
        validators=[
            DataRequired(),
            Length(min=3, max=80, message="Your message needs to be between 3 and 80 characters long.")
        ])
    address = StringField('Address',
        validators=[
            DataRequired(),
            Length(min=3, max=200, message="Your message needs to be between 3 and 200 characters long.")
        ])
    submit = SubmitField('Submit')

class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""

    # TODO: Add the following fields to the form class:
    # - name - StringField
    # - price - FloatField
    # - category - SelectField (specify the 'choices' param)
    # - photo_url - StringField
    # - store - QuerySelectField (specify the `query_factory` param)
    # - submit button
    name = StringField('Grocery Name',
        validators=[
            DataRequired(),
            Length(min=3, max=80, message="Your message needs to be between 3 and 80 characters long.")
        ])
    price = FloatField('Price',
        validators=[
            DataRequired()
        ])
    category = SelectField('Category', choices=ItemCategory.choices())
    photo_url = StringField('Photo URL',
        validators=[
            DataRequired(),
            Length(min=3, max=200, message="Your message needs to be between 3 and 200 characters long.")
        ])
    store = QuerySelectField('Store', query_factory=lambda: GroceryStore.query.all(), get_label='title')
    submit = SubmitField('Submit') 
