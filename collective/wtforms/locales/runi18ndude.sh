#!/bin/sh

DOMAIN='collective.wtforms'

i18ndude rebuild-pot --pot ${DOMAIN}.pot --merge wtforms.pot --create ${DOMAIN} ..
i18ndude sync --pot ${DOMAIN}.pot ./*/LC_MESSAGES/${DOMAIN}.po
