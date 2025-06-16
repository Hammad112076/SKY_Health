from django import template

register = template.Library()

@register.filter
def get_card_field(form, card):
    return form[f'card_{card.id}']

@register.filter
def subtract(value, arg):
    """Subtracts arg from value."""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def percentage(value, total):
    """Returns percentage of value out of total."""
    try:
        return round((int(value) / int(total)) * 100)
    except (ZeroDivisionError, ValueError, TypeError):
        return 0

@register.filter
def multiply(value, arg):
    """Multiplies two integers."""
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    """Divides two integers (floor division)."""
    try:
        return int(value) // int(arg)
    except (ZeroDivisionError, ValueError, TypeError):
        return 0

@register.filter
def get_vote_status(votes, card_id):
    """Returns vote color for a given card."""
    for vote in votes:
        if vote.card.id == card_id:
            return vote.color
    return None

@register.filter
def get_vote_comment(vote_comments, card_id):
    """Returns vote comment for a given card."""
    return vote_comments.get(card_id, "")
