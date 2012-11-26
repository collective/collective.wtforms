from zope.component import getMultiAdapter
from AccessControl import Unauthorized
from Products.Five import BrowserView
from plone.memoize.view import memoize
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.wtforms import messageFactory as _
from unidecode import unidecode


def convertStr(v):
    if type(v) == str:
        try:
            v = unicode(v, 'utf8')
        except:
            v = unidecode(v)
    return v


class PostData(dict):
    """
    The form wants the getlist method - no problem.
    """
    def getlist(self, key):
        v = self[key]
        if not isinstance(v, (list, tuple)):
            v = [convertStr(v)]
        else:
            # is a list...
            v = [convertStr(v2) for v2 in v]
        return v


class WTFormView(BrowserView):
    formClass = None
    label = ''
    description = ''
    prefix = 'wtform'
    buttonPrefix = 'form.actions.'
    wrapWithFieldset = True
    csrfProtect = True
    buttons = (
        _(u'Save'),
        _(u'Cancel')
    )

    fieldsets = ()

    index = ViewPageTemplateFile('basicform.pt')
    fieldTemplate = ViewPageTemplateFile('field.pt')
    formTemplate = ViewPageTemplateFile('form.pt')

    def viewname(self):
        return self.__name__

    def fixName(self, name):
        return name.replace(' ', '').replace(',', '')

    def mungeForm(self, form):
        pass

    def getButtonName(self, button):
        return '%s%s' % (self.buttonPrefix, self.fixName(button))

    @property
    def submitted(self):
        return self.request.get('REQUEST_METHOD') == 'POST' and \
            self.request.get('form.submitted', 'false') == 'true'

    @property
    def data(self):
        return {}

    @property
    @memoize
    def form(self):
        if not self.submitted:
            data = self.data
            formdata = PostData({})
        else:
            data = {}
            formdata = PostData(self.request.form)

        data.update(self.request.form)
        for key, value in data.items():
            data[key] = convertStr(value)
        form = self.formClass(formdata, prefix=self.prefix, **data)
        self.mungeForm(form)
        return form

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

    @memoize
    def hasButtonSubmitted(self):
        for button in self.buttons:
            btnname = "%s%s" % (self.buttonPrefix, button)
            if btnname in self.request.form or btnname.replace(' ', '') in self.request.form:
                return button

    def __call__(self):
        if self.submitted:
            button = self.hasButtonSubmitted()
            if button:
                result = self.submit(button)
                if result:
                    return result
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
    status = None
