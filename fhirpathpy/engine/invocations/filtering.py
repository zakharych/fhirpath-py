import numbers
import fhirpathpy.engine.util as util

# Contains the FHIRPath Filtering and Projection functions.
# (Section 5.2 of the FHIRPath 1.0.0 specification).

"""
 Adds the filtering and projection functions to the given FHIRPath engine.
"""


def where_macro(ctx, data, expr):
    if not isinstance(data, list):
        return []

    return util.flatten([x for x in data if expr(x)[0]])


def select_macro(ctx, data, expr):
    if not isinstance(data, list):
        return []

    return util.flatten([x for x in data if expr(x)])


def repeat_macro(ctx, data, expr):
    if not isinstance(data, list):
        return []

    res = []
    items = data

    next = None
    lres = None

    while len(items) != 0:
        next = items[0]
        items = items[1:]
        lres = expr(next)
        if lres:
            res = res + lres
            items = items + lres

    return res


# TODO: behavior on object?
def single_fn(ctx, x):
    if len(x) == 1:
        return x

    if len(x) == 0:
        return []

    # TODO: should throw error?
    return {"$status": "error", "$error": "Expected single"}


def first_fn(ctx, x):
    return x[0]


def last_fn(ctx, x):
    return x[-1]


def tail_fn(ctx, x):
    return x[1:]


def take_fn(ctx, x, n):
    return x[: int(n)]


def skip_fn(ctx, x, n):
    return x[int(n) :]


# TODO test
def check_fhir_type(ctx, x, tp):
    if type(x) == tp:
        return True

    if tp == "integer":
        return int(x) == x

    if tp == "decimal":
        return isinstance(x, numbers.Number)

    return False


def of_type_fn(ctx, coll, type):
    return list(filter(lambda x: check_fhir_type(util.get_data(x), type), coll))  # TODO
