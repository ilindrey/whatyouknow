from rest_framework.serializers import JSONField


class IsNullSetDefaultJSONField(JSONField):

    def to_internal_value(self, data):
        if not data:
            data = self.get_default()
        return super().to_internal_value(data)