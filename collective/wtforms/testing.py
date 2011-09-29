from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing.layers import FunctionalTesting
from plone.app.testing.layers import IntegrationTesting
from zope.configuration import xmlconfig
from plone.testing import z2
from collective.wtforms.views import WTFormView, WTFormControlPanelView
from wtforms import Form, TextField
from wtforms import validators


class WTForms(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # load ZCML
        import collective.wtforms
        xmlconfig.file('configure.zcml', collective.wtforms,
            context=configurationContext)
        xmlconfig.file('test.zcml', collective.wtforms.tests,
            context=configurationContext)
        z2.installProduct(app, 'collective.wtforms')

    def setUpPloneSite(self, portal):
        pass


WTForms_FIXTURE = WTForms()
WTForms_INTEGRATION_TESTING = IntegrationTesting(
    bases=(WTForms_FIXTURE,), name="WTForms:Integration")
WTForms_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(WTForms_FIXTURE,), name="WTForms:Functional")


class TestForm(Form):
    one = TextField("Field One", [validators.required()])
    two = TextField("Field Two")
    three = TextField("Field Three")


class TestFormView(WTFormView):
    formClass = TestForm
    csrfProtect = False
    buttons = ('Create', 'Cancel')
    buttonClicked = None
    valid = False

    def submit(self, button):
        if button == 'Create':
            self.valid = self.validate()
        self.buttonClicked = button


class TestFieldsetForm(Form):
    one = TextField("Field One", [validators.required()])
    two = TextField("Field Two")
    three = TextField("Field Three")

    four = TextField("Field Four", [validators.required()])
    five = TextField("Field Five")
    six = TextField("Field Six")

    seven = TextField("Field Seven")
    eight = TextField("Field Eight")
    nine = TextField("Field Nine")


class TestFieldsetView(WTFormView):
    formClass = TestFieldsetForm
    csrfProtect = False
    fieldsets = (
        ('Fieldset One', ('one', 'two', 'three')),
        ('Fieldset Two', ('four', 'five', 'six')),
        ('Fieldset Three', ('seven', 'eight', 'nine'))
    )
    buttons = ('Yes', 'No')
    buttonClicked = None
    valid = False

    def submit(self, button):
        if button == 'Yes':
            self.valid = self.validate()
        self.buttonClicked = button


class TestControlPanelView(WTFormControlPanelView):
    formClass = TestForm
    csrfProtect = False
    buttons = ('Save', 'Cancel')
    buttonClicked = None
    valid = False

    def submit(self, button):
        if button == 'Save':
            self.valid = self.validate()
        self.buttonClicked = button
