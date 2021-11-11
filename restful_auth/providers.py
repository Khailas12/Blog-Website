from allauth.socialaccount.providers.google.provider import GoogleProvider


class GoogleProviderMod(GoogleProvider):
    def exact_uid(self, data):
        return str(data['sub'])