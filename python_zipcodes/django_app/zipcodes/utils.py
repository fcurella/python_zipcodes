from django.contrib.localflavor.us.forms import USZipCodeField

country_flavor = {
    'US': USZipCodeField,
}
