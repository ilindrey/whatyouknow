
def _edit_string_for_tags(tags):
    """
    Given list of ``Tag`` instances or list of dictionaries with a similar
    model "Tag" structure, creates a string representation of the list
    suitable for editing by the user, such that submitting the given
    string representation back without changing it will give the
    same list of tags.

    Tag names which contain commas will be double quoted.

    If any tag name which isn't being quoted contains whitespace, the
    resulting string of tag names will be comma-delimited, otherwise
    it will be space-delimited.

    Ported from Jonathan Buchanan's `django-tagging
    <http://django-tagging.googlecode.com/>`_
    """
    names = []
    for tag in tags:
        if isinstance(tag, dict):
            name = tag['name']
        else:
            name = tag.name
        if "," in name or " " in name:
            names.append('"%s"' % name)
        else:
            names.append(name)
    return ", ".join(sorted(names))