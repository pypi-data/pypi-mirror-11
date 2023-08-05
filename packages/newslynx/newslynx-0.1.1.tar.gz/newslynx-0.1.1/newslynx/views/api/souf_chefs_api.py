from collections import defaultdict, Counter

from flask import Blueprint

from newslynx.core import db
from newslynx.models import SousChef
from newslynx.models import sous_chef_schema
from newslynx.lib.serialize import jsonify
from newslynx.views.decorators import load_user, load_org
from newslynx.models.util import fetch_by_id_or_field
from newslynx.views.util import *


# blueprint
bp = Blueprint('sous_chefs', __name__, )


# utils

@bp.route('/api/v1/sous-chefs', methods=['GET'])
@load_user
def list_sous_chefs(user):

    # optionally filter by type/level/category
    creates = arg_str('creates', default='all')
    is_command = arg_bool('is_command', default=None)
    include_sous_chefs, exclude_sous_chefs = \
        arg_list('sous_chefs', default=[], typ=str, exclusions=True)
    sort_field, direction = arg_sort('sort', default='slug')

    # base query
    sous_chef_query = db.session.query(SousChef)

    # apply filters
    if creates != "all":
        sous_chef_query = sous_chef_query\
            .filter_by(creates=creates)

    if is_command is not None:
        sous_chef_query = sous_chef_query\
            .filter_by(is_command=is_command)

    # include sous chefs
    if len(include_sous_chefs):
        sous_chef_query = sous_chef_query\
            .filter(SousChef.slug.in_(include_sous_chefs))

    # exclude sous chefs
    if len(exclude_sous_chefs):
        sous_chef_query = sous_chef_query\
            .filter(~SousChef.slug.in_(exclude_sous_chefs))

    # sort
    if sort_field:
        validate_fields(SousChef, fields=[sort_field], suffix='to sort by')
        sort_obj = eval('SousChef.{}.{}'.format(sort_field, direction))
        sous_chef_query = sous_chef_query.order_by(sort_obj())

    # process query, compute facets.
    clean_sous_chefs = []
    facets = defaultdict(Counter)
    for sc in sous_chef_query.all():
        facets['creates'][sc.creates] += 1
        if not sc.is_command:
            facets['runners']['python'] += 1
        else:
            facets['runners']['command'] += 1
        clean_sous_chefs.append(sc)

    resp = {
        'facets': facets,
        'sous_chefs': clean_sous_chefs
    }
    return jsonify(resp)


@bp.route('/api/v1/sous-chefs', methods=['POST'])
@load_user
def create_sous_chef(user):

    req_data = request_data()

    # validate the sous chef
    sc = sous_chef_schema.validate(req_data)

    # add it to the database
    sc = SousChef(**sc)
    db.session.add(sc)
    try:
        db.session.commit()
    except Exception as e:
        raise RequestError(e.message)

    return jsonify(sc)


@bp.route('/api/v1/sous-chefs/<sous_chef>', methods=['GET'])
@load_user
def get_sous_chef(user, sous_chef):

    sc = fetch_by_id_or_field(SousChef, 'slug', sous_chef)
    if not sc:
        raise NotFoundError(
            'A SousChef does not exist with ID/slug {}'
            .format(sous_chef))

    return jsonify(sc)


@bp.route('/api/v1/sous-chefs/<sous_chef>', methods=['PUT', 'PATCH'])
@load_user
def update_sous_chef(user, sous_chef):

    sc = fetch_by_id_or_field(SousChef, 'slug', sous_chef)
    if not sc:
        raise NotFoundError(
            'A SousChef does not exist with ID/slug {}'
            .format(sous_chef))

    req_data = request_data()

    # validate the schema
    new_sous_chef = sous_chef_schema.update(sc, req_data)

    # udpate
    for name, value in new_sous_chef.items():
        setattr(sc, name, value)
    db.session.add(sc)

    try:
        db.session.commit()

    except Exception as e:
        raise RequestError(
            "An error occurred while updating SousChef '{}'. "
            "Here's the error message: {}"
            .format(sc.slug, e.message))
    return jsonify(sc)


@bp.route('/api/v1/sous-chefs/<sous_chef>', methods=['DELETE'])
@load_user
def delete_sous_chef(user, sous_chef):

    sc = fetch_by_id_or_field(SousChef, 'slug', sous_chef)
    if not sc:
        raise NotFoundError(
            'A SousChef does not exist with ID/slug {}'
            .format(sous_chef))

    db.session.delete(sc)
    db.session.commit()
    return delete_response()
