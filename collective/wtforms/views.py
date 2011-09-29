from zope.component import getMultiAdapter
from AccessControl import Unauthorized
from Products.Five import BrowserView
from plone.memoize.view import memoize
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class PostData(dict):
    """
    The form wants the getlist method - no problem.
    """
    def getlist(self, key):
        v = self[key]
        if not isinstance(v, (list, tuple)):
            v = [v]
        return v


class WTFormView(BrowserView):
    formClass = None
    label = 'Form Title'
    description = 'Form Description'
    prefix = 'wtform'
    buttonPrefix = 'form.actions.'
    wrapWithFieldset = True
    csrfProtect = True
    buttons = (
        'Save',
        'Cancel'
    )

    fieldsets = ()

    index = ViewPageTemplateFile('basicform.pt')
    fieldTemplate = ViewPageTemplateFile('field.pt')
    formTemplate = ViewPageTemplateFile('form.pt')

    def viewname(self):
        return self.__name__

    def fixName(self, name):
        return name.replace(' ', '').replace(',', '')

    @property
    @memoize
    def form(self):
        return self.formClass(PostData(self.request.form), prefix=self.prefix)

    def renderField(self, field):
        return self.fieldTemplate(field=field)

    def renderForm(self):
        return self.formTemplate()

    def validate(self):
        if self.csrfProtect:
            authenticator = getMultiAdapter((self.context, self.request),
                                            name=u"authenticator")
            if not authenticator.verify():
                raise Unauthorized
        return self.form.validate()

    def submit(self, button=None):
        if button == 'Save':
            if self.validate():
                self.request.response.redirect(self.context.absolute_url())
                return 1
        elif button == 'Cancel':
            self.request.response.redirect(self.context.absolute_url())
            return 1

    def __call__(self):
        if self.request.get('REQUEST_METHOD') == 'POST':
            for button in self.buttons:
                if button == self.request.get('%s%s' % (self.buttonPrefix,
                                                        self.fixName(button))):
                    result = self.submit(button)
                    if result:
                        return result
                    else:
                        break
        return self.index()

    def iterfieldsets(self):
        form = self.form
        if self.fieldsets:
            for fieldset, fieldnames in self.fieldsets:
                fields = []
                for name in fieldnames:
                    field = getattr(form, name, None)
                    if field:
                        fields.append(field)
                yield fieldset, fields
        else:
            yield self.label, [f for f in form]


class WTFormControlPanelView(WTFormView):
    index = ViewPageTemplateFile('controlpanelform.pt')
