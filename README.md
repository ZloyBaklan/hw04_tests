# Yatube app tests (hw04_tests)

Tested to see if the value of the __str__ field is displayed correctly in model objects.

Checked accessibility of pages in accordance with user rights

Checking expected templates and passed dictionaries context and URl

It is checked that if you specify a group when creating a post, then this post appears
on the main page of the site,
on the page of the selected group.
Checked that the created post does not fall into a group for which it was not intended.
On the main page, the group page and on the user profile page, the work of the programmer was checked: 10 entries per page are transferred to the context dictionary.

The form for creating a new post (page / new /) has been checked: when the form is submitted, a new record is created in the database.

Checked that when editing a post through the form on the page / <username> / <post_id> / edit /, the corresponding record in the database is changed.
