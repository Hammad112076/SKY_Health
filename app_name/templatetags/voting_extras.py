from django import template

register = template.Library()

@register.filter
def get_card_field(form, card):
    """
    Safely returns the form field corresponding to a card.
    """
    if not form or not hasattr(form, '__getitem__') or not hasattr(card, 'id'):
        return None
    key = f'card_{card.id}'
    return form[key] if key in form.fields else None

@register.filter
def get_vote_status(existing_votes, card_id):
    """
    Retrieves the vote status (color) for a specific card_id.
    """
    return existing_votes.get(card_id)

@register.filter
def vote_percentage(vote_counts, color):
    """
    Calculates percentage of a specific color out of total votes.
    """
    try:
        total = sum(vote_counts.values())
        if total == 0:
            return 0
        return round((vote_counts.get(color, 0) / total) * 100)
    except:
        return 0

@register.filter
def subtract(value, arg):
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def multiply(value, arg):
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def mul(value, arg):
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    try:
        return int(value) // int(arg)
    except (ZeroDivisionError, ValueError, TypeError):
        return 0
