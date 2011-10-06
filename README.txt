Introduction
============

collective.wtforms is plone integration with the WTForms form library.


Basic Complete Form Example
---------------------------

The basic form is constructed like so::

    from wtforms import Form, TextField
    from wtforms import validators
    class MyForm(Form):
        one = TextField("Field One", [validators.required()])
        two = TextField("Field Two")
        three = TextField("Field Three")

    from collective.wtforms.views import WTFormView
    class MyFormView(WTFormView):
        formClass = MyForm
        buttons = ('Create', 'Cancel')

        def submit(self, button):
            if button == 'Create' and self.validate():
                # do fun stuff here
                self.context.value = self.form.one.data

Then wire up the form with zcml::
    
    <browser:page
        name="my-form"
        for="*"
        class=".pathto.MyFormView"
        permission="zope2.View"
    />


You can also override the template used and then do::

    <form tal:replace="structure view/renderForm" />

To render the form anywhere in your view.


Fieldsets
---------

You can specific which fields go with which fieldsets
easily also::

    class MyFormView(WTFormView):
        formClass = MyForm
        buttons = ('Create', 'Cancel')
        fieldsets = (
            ('Fieldset One', ('one', 'two')),
            ('Fieldset Two', ('three',))
        )

        def submit(self, button):
            if button == 'Create' and self.validate():
                # do fun stuff here
                self.context.value = self.form.one.data

This will render the form in the standard plone feildsets.


Control Panel
-------------

It's also possible to easily construct a control panel form::

    from collective.wtforms.views import WTFormControlPanelView
    class MyFormView(WTFormControlPanelView):
        formClass = MyForm
        buttons = ('Save', 'Cancel')

        def submit(self, button):
            if button == 'Save' and self.validate():
                # do fun stuff here
                self.context.value = self.form.one.data

WTFormView Class Properties
---------------------------

formClass
    The WTForm class used. `Required`

label
    The form label that shows up in the h1 tag

description
    form description

prefix
    The prefix of the form input name values. Defaults to `wtform`

buttonPrefix
    The prefix of the button names. Defaults to `form.actions.`

wrapWithFieldset
    A boolean that decides if it should wrap the fields in a fieldset. Defaults to True

csrfProtect
    Protect the form against csrf attacks. Defaults to True

buttons
    An iterable of button names. Defaults to ('Save', 'Cancel')

fieldsets
    An iterable of (fieldset name, (field names, ...)). Defaults to empty

form
    The instance of the WTForm form that is created on rendering the form.

data
    Override this property to specify default values to populate the form with. This must return a dictionary.

submitted
    Boolean if the form was submitted or not.

renderField(field)
    Method to render a specific field.

renderForm()
    Method to render the entire form.

validate()
    Check csrf protection and validates the form.

submit(button)
    The method you must override to handle the form sumission and run validation. Return a value to override rendering the template(self.index()). For instance, if you do a redirect, there is no need to render the page also::

        def submit(self, button):
            if button == 'Save' and self.validate():
                self.context.value = self.form.one.data
                self.request.response.redirect(self.context.absolute_url())
                return 1
mungeForm(form)
    A method to mess with the form after it is created. This is what can be used to apply dynamic choices.
