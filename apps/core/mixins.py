
class BaseHasPermsMixin:

    @property
    def has_perms(self):
        user = self.request.user
        if user.is_authenticated:
            if hasattr(self, 'form_class'):
                form_class = getattr(self, 'form_class')
                if hasattr(form_class, '_meta') and hasattr(form_class._meta, 'model'):
                    opts = form_class._meta.model._meta
                else:
                    return True  # form without model, check permissions elsewhere
            elif hasattr(self, 'object'):
                obj = getattr(self, 'object')
                opts = obj._meta
            elif hasattr(self, 'model'):
                model = getattr(self, 'model')
                opts = model._meta
            perm_list = ['view', 'change']
            return user.has_perms([f'{opts.app_label}.{perm}_{opts.model_name}' for perm in perm_list])
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_perms'] = self.has_perms
        return context


class HasPermsMixin(BaseHasPermsMixin):
    pass
