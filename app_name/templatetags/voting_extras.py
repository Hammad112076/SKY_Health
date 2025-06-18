# Importing Django's template library to create custom template filters
from django import template

# Registering the custom filters with Django's template system
register = template.Library()

@register.filter
def get_card_field(form, card):
    """
    Custom template filter to safely retrieve a form field corresponding to a specific card.
    
    Args:
        form: The form object containing input fields.
        card: The HealthCard object, expected to have an 'id' attribute.

    Returns:
        The form field corresponding to the card's ID if it exists; otherwise, returns None.
    """
    if not form or not hasattr(form, '__getitem__') or not hasattr(card, 'id'):
        return None
    key = f'card_{card.id}'  # Construct the field name, e.g., 'card_1'
    return form[key] if key in form.fields else None


@register.filter
def get_vote_status(existing_votes, card_id):
    """
    Retrieves the current vote status for a specific card ID.
    
    Args:
        existing_votes: A dictionary with card_id as key and vote status (e.g., 'green') as value.
        card_id: The ID of the card to check.

    Returns:
        The vote status for the given card ID, or None if not found.
    """
    return existing_votes.get(card_id)


@register.filter
def vote_percentage(vote_counts, color):
    """
    Calculates the percentage of votes for a specific color (green, amber, or red).
    
    Args:
        vote_counts: A dictionary with color as keys and number of votes as values.
        color: The specific color to calculate percentage for.

    Returns:
        An integer percentage of the selected color out of total votes, or 0 if invalid.
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
    """
    Subtracts one integer value from another.

    Args:
        value: The initial number.
        arg: The number to subtract.

    Returns:
        The result of the subtraction or 0 on error.
    """
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def multiply(value, arg):
    """
    Multiplies two integer values.

    Args:
        value: First integer.
        arg: Second integer.

    Returns:
        The product of the two integers or 0 on error.
    """
    try:
        return int(value) * int(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def mul(value, arg):
    """
    Multiplies two floating point values (used where decimals are involved).

    Args:
        value: First float.
        arg: Second float.

    Returns:
        The product of the two floats or 0 on error.
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.filter
def divide(value, arg):
    """
    Performs integer division (floor division) between two numbers.

    Args:
        value: Numerator.
        arg: Denominator.

    Returns:
        The integer result of the division or 0 on error (e.g., divide by zero).
    """
    try:
        return int(value) // int(arg)
    except (ZeroDivisionError, ValueError, TypeError):
        return 0
