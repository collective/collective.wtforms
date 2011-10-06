from zope.component import getMultiAdapter
import unittest2 as unittest
from collective.wtforms.testing import WTForms_FUNCTIONAL_TESTING
from collective.wtforms.views import WTFormView


class TestForm(unittest.TestCase):

    layer = WTForms_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']

    def getView(self, name):
        return getMultiAdapter((self.portal, self.request), name=name)

    def getButtonName(self, name):
        return '%s%s' % (WTFormView.buttonPrefix, name)

    def getFieldName(self, name):
        return '%s-%s' % (WTFormView.prefix, name)

    def test_basic_form_renders(self):
        view = self.getView('test-form')
        view()

    def test_basic_form_submit(self):
        self.request.environ['REQUEST_METHOD'] = 'POST'
        self.request.form[self.getButtonName('Create')] = 'Create'
        self.request.form[self.getFieldName('one')] = 'Foobar'
        self.request.form['form.submitted'] = 'true'
        view = self.getView('test-form')
        view()
        self.assertEquals(view.buttonClicked, 'Create')
        self.assertEquals(view.valid, True)
        self.assertEquals(view.form.one.data, 'Foobar')

    def test_basic_form_submit_not_valid(self):
        self.request.environ['REQUEST_METHOD'] = 'POST'
        self.request.form[self.getButtonName('Create')] = 'Create'
        self.request.form['form.submitted'] = 'true'
        view = self.getView('test-form')
        result = view()
        self.assertTrue('<div class="field error">' in result)
        self.assertEquals(view.buttonClicked, 'Create')
        self.assertEquals(view.valid, False)

    def test_basic_form_submit_cancel_clicked(self):
        self.request.environ['REQUEST_METHOD'] = 'POST'
        self.request.form[self.getButtonName('Cancel')] = 'Cancel'
        self.request.form['form.submitted'] = 'true'
        view = self.getView('test-form')
        view.valid = True
        view()
        self.assertEquals(view.buttonClicked, 'Cancel')
        self.assertEquals(view.valid, True)

    def test_basic_form_only_works_on_post(self):
        self.request.form[self.getButtonName('Create')] = 'Create'
        self.request.form['form.submitted'] = 'true'
        view = self.getView('test-form')
        view()
        self.assertEquals(view.buttonClicked, None)
        self.assertEquals(view.valid, False)

    def test_fieldset_form_renders(self):
        view = self.getView('test-fieldset')
        view()

    def test_fieldset_form_submit(self):
        self.request.environ['REQUEST_METHOD'] = 'POST'
        self.request.form[self.getButtonName('Yes')] = 'Yes'
        self.request.form[self.getFieldName('one')] = 'Foo'
        self.request.form[self.getFieldName('four')] = 'bar'
        self.request.form['form.submitted'] = 'true'
        view = self.getView('test-fieldset')
        view()
        self.assertEquals(view.buttonClicked, 'Yes')
        self.assertEquals(view.valid, True)
        self.assertEquals(view.form.one.data, 'Foo')
        self.assertEquals(view.form.four.data, 'bar')

    def test_fieldset_form_submit_not_valid(self):
        self.request.environ['REQUEST_METHOD'] = 'POST'
        self.request.form[self.getButtonName('Yes')] = 'Yes'
        self.request.form['form.submitted'] = 'true'
        view = self.getView('test-fieldset')
        result = view()
        self.assertTrue('<div class="field error">' in result)
        self.assertEquals(view.buttonClicked, 'Yes')
        self.assertEquals(view.valid, False)

    def test_fieldset_form_submit_cancel_clicked(self):
        self.request.environ['REQUEST_METHOD'] = 'POST'
        self.request.form[self.getButtonName('No')] = 'No'
        self.request.form['form.submitted'] = 'true'
        view = self.getView('test-fieldset')
        view.valid = True
        view()
        self.assertEquals(view.buttonClicked, 'No')
        self.assertEquals(view.valid, True)

    def test_fieldset_form_only_works_on_post(self):
        self.request.form[self.getButtonName('Yes')] = 'Yes'
        self.request.form['form.submitted'] = 'true'
        view = self.getView('test-fieldset')
        view()
        self.assertEquals(view.buttonClicked, None)
        self.assertEquals(view.valid, False)

    def test_controlpanel_form_renders(self):
        view = self.getView('test-controlpanel-form')
        view()

    def test_controlpanel_form_submit(self):
        self.request.environ['REQUEST_METHOD'] = 'POST'
        self.request.form[self.getButtonName('Save')] = 'Save'
        self.request.form[self.getFieldName('one')] = 'Foobar'
        self.request.form['form.submitted'] = 'true'
        view = self.getView('test-controlpanel-form')
        view()
        self.assertEquals(view.buttonClicked, 'Save')
        self.assertEquals(view.valid, True)
        self.assertEquals(view.form.one.data, 'Foobar')

    def test_controlpanel_form_submit_not_valid(self):
        self.request.environ['REQUEST_METHOD'] = 'POST'
        self.request.form[self.getButtonName('Save')] = 'Save'
        self.request.form['form.submitted'] = 'true'
        view = self.getView('test-controlpanel-form')
        result = view()
        self.assertTrue('<div class="field error">' in result)
        self.assertEquals(view.buttonClicked, 'Save')
        self.assertEquals(view.valid, False)

    def test_controlpanel_form_submit_cancel_clicked(self):
        self.request.environ['REQUEST_METHOD'] = 'POST'
        self.request.form[self.getButtonName('Cancel')] = 'Cancel'
        self.request.form['form.submitted'] = 'true'
        view = self.getView('test-controlpanel-form')
        view.valid = True
        view()
        self.assertEquals(view.buttonClicked, 'Cancel')
        self.assertEquals(view.valid, True)

    def test_controlpanel_form_only_works_on_post(self):
        self.request.form[self.getButtonName('Save')] = 'Save'
        self.request.form['form.submitted'] = 'true'
        view = self.getView('test-controlpanel-form')
        view()
        self.assertEquals(view.buttonClicked, None)
        self.assertEquals(view.valid, False)
