# coding: utf-8
"""Utility/high-level functions for interacting with suggestions."""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import django.db.models
from django.contrib.contenttypes import models as ct_models


def __user_from_request(req):
    """Get either the User object or session key from a request.

    Returns None for anonymous users with no session keys.
    """
    try:  # Requests have a .user object
        req.user
    except AttributeError:  # Probably not a request, maybe a string
        return req
    if req.user.is_authenticated():
        return req.user
    return req.session.session_key


def set_score(request_or_user, obj, score):
    """Set the score for the given obj.

    Will attribute it to the user, if request has an authenticated user, or to
    a session.

    """
    from . import models
    user = __user_from_request(request_or_user)
    return models.UserScore.set(user, obj, score)


def setdefault_score(request_or_user, obj, score):
    """Set the score for the given obj if it doesn't exist.

    Will attribute it to the user, if request has an authenticated user, or to
    a session.

    """
    from . import models
    user = __user_from_request(request_or_user)
    return models.UserScore.setdefault(user, obj, score)


def scores_for(obj):
    """Get all scores for the given object."""
    from . import models
    return models.UserScore.scores_for(obj)


def get_score(request_or_user, obj):
    """Get a user's score for the given object."""
    from . import models
    user = __user_from_request(request_or_user)
    return models.UserScore.get(user, obj)


def similar_objects(obj):
    """Get objects most similar to obj.

    Returns an iterator, not a collection.

    """
    return similar_to(obj).get_instances_for(obj)


def similar_to(obj):
    """Get a queryset of similarity scores most similar to obj.

    This can allow you to use methods of the ObjectSimilarityQueryset, such as
    exclude_objects, as well as normal queryset slicing.

    """
    from . import models
    obj_qset = type(obj).objects.filter(pk=obj.pk)
    high_similarity = models.ObjectSimilarity.objects.filter_objects(obj_qset)
    high_similarity = high_similarity.order_by('-score')
    return high_similarity
