from django.db import models

EXCLUDED_FOR_FILTERING = (models.TextField,)  # 6.5
AUTO_FIELDS = {'created_at', 'updated_at'}


def build_filterset_fields(model):
    """Return a list of concrete, filterable field names for a model.

    Includes scalar fields (char/choice, bool, date/datetime, numeric) and
    foreign keys (filtered by related pk). Excludes TextField columns and
    auto-managed timestamps. (Requirements 6.4, 6.5)
    """
    fields = []
    for field in model._meta.get_fields():
        if not getattr(field, 'concrete', False):
            continue                      # skip reverse relations / m2m accessors
        if field.many_to_many or field.one_to_many:
            continue
        if field.name in AUTO_FIELDS:
            continue
        if isinstance(field, EXCLUDED_FOR_FILTERING):
            continue                      # 6.5: exclude large text fields
        fields.append(field.name)         # FK stored as <name>, filtered by pk
    return fields
