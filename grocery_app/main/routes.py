from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from flask_login import login_required, current_user
from grocery_app.models import GroceryStore, GroceryItem, User
from grocery_app.main.forms import GroceryStoreForm, GroceryItemForm

# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    print(current_user)
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    # TODO: Create a GroceryStoreForm
    form = GroceryStoreForm()
    # TODO: If form was submitted and was valid:
    # - create a new GroceryStore object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the store detail page.
    if form.validate_on_submit():
        new_store = GroceryStore(
            title=form.title.data,
            address=form.address.data,
            created_by_id=current_user.id
        )
        db.session.add(new_store)
        db.session.commit()

        flash('New store was created successfully.')
        return redirect(url_for('main.store_detail', store_id=new_store.id))
    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_store.html', form=form)

@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    # TODO: Create a GroceryItemForm
    form = GroceryItemForm()
    # TODO: If form was submitted and was valid:
    # - create a new GroceryItem object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the item detail page.
    if form.validate_on_submit():
        new_item = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            photo_url=form.photo_url.data,
            store=form.store.data,
            created_by_id=current_user.id
        )
        db.session.add(new_item)
        db.session.commit()

        flash('New item was created successfully.')
        return redirect(url_for('main.item_detail', item_id=new_item.id))
    # TODO: Send the form to the template and use it to render the form fields
    return render_template('new_item.html', form=form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    # TODO: Create a GroceryStoreForm and pass in `obj=store`
    form = GroceryStoreForm(obj=store)
    # TODO: If form was submitted and was valid:
    # - update the GroceryStore object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the store detail page.
    if form.validate_on_submit():
        store.title = form.title.data
        store.address = form.address.data
        db.session.commit()

        flash('Store was updated successfully.')
        return redirect(url_for('main.store_detail', store_id=store.id))
    # TODO: Send the form to the template and use it to render the form fields
    return render_template('store_detail.html', store=store, form=form)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    # TODO: Create a GroceryItemForm and pass in `obj=item`
    form = GroceryItemForm(obj=item)
    # TODO: If form was submitted and was valid:
    # - update the GroceryItem object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the item detail page.
    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        item.category = form.category.data
        item.photo_url = form.photo_url.data
        item.store = form.store.data
        db.session.commit()

        flash('Item was updated successfully.')
        return redirect(url_for('main.item_detail', item_id=item.id))
    # TODO: Send the form to the template and use it to render the form fields
    return render_template('item_detail.html', item=item, form=form)

@main.route('/add_to_shopping_list/<item_id>', methods=['POST'])
@login_required
def add_to_shopping_list(item_id):
    """Add item to user list"""
    item = GroceryItem.query.get(item_id)
    if item in current_user.shopping_list_items:
        flash("Item already in shopping list.")
        return redirect(url_for('main.item_detail', item_id=item.id))
    current_user.shopping_list_items.append(item)
    db.session.commit()
    flash("Item added to shopping list successfully.")
    return redirect(url_for('main.item_detail', item_id=item.id))

@main.route('/delete_from_shopping_list/<item_id>', methods=['POST'])
@login_required
def delete_from_shopping_list(item_id):
    """Remove item from user list"""
    item = GroceryItem.query.get(item_id)
    if item in current_user.shopping_list_items:
        current_user.shopping_list_items.remove(item)
        db.session.commit()
        flash("Item removed from shopping list successfully.")
    return redirect(url_for('main.shopping_list'))

@main.route('/shopping_list')
@login_required
def shopping_list():
    user_shopping_list = current_user.shopping_list_items
    return render_template('shopping_list.html', shopping_list=user_shopping_list)

# @main.route('/reset_db')
# def reset_db():
#     db.drop_all()
#     db.create_all()
#     flash('Database has been reset.')
#     return redirect(url_for('main.homepage'))