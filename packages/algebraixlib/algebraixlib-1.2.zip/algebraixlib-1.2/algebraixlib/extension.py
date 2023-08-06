"""Facilities for extending operations from one :term:`algebra` to another."""

# $Id: extension.py 22754 2015-08-06 22:27:31Z gfiedler $
# Copyright Algebraix Data Corporation 2015 - $Date: 2015-08-06 17:27:31 -0500 (Thu, 06 Aug 2015) $
#
# This file is part of algebraixlib <http://github.com/AlgebraixData/algebraixlib>.
#
# algebraixlib is free software: you can redistribute it and/or modify it under the terms of version
# 3 of the GNU Lesser General Public License as published by the Free Software Foundation.
#
# algebraixlib is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with algebraixlib.
# If not, see <http://www.gnu.org/licenses/>.
# --------------------------------------------------------------------------------------------------
import collections as _collections

import algebraixlib.mathobjects as _mo
import algebraixlib.undef as _ud


def binary_extend(set1: 'P( M )', set2: 'P( M )', op, _checked=True) -> 'P( M )':
    r"""Return the :term:`binary extension` of ``op`` from one :term:`algebra` to another algebra.

    For this extension, the elements of the extended algebra must be :term:`set`\s of the
    elements of the original algebra.

    :param set1: A :term:`set` with elements on which ``op`` operates.
    :param set2: A set with elements on which ``op`` operates.
    :param op: A :term:`binary operation` that operates on the elements of ``set1`` and ``set2``.
    :return: A set that consists of the defined results of ``op`` when executed on all combinations
        of the elements of ``set1`` and ``set2``, or `Undef()` if either set is not a
        :class:`~.Set`.
    """
    if _checked:
        if not isinstance(set1, _mo.Set):
            return _ud.make_or_raise_undef()
        if not isinstance(set2, _mo.Set):
            return _ud.make_or_raise_undef()
    else:
        assert set1.is_set
        assert set2.is_set

    def _get_values(_set1, _set2):
        for e1 in _set1:
            for e2 in _set2:
                result = op(e1, e2)
                if result is not _ud.Undef():
                    yield result

    return _mo.Set(_get_values(set1, set2), direct_load=True)


def binary_multi_extend(multiset1: 'P( M x N )', multiset2: 'P( M x N )', op,
                        _checked=True) -> 'P( M x N )':
    r"""Return the :term:`binary extension` of ``op`` from one :term:`algebra` to another algebra.

    For this extension, the elements of the extended algebra must be :term:`multiset`\s of the
    elements of the original algebra.

    :param multiset1: A :term:`multiset` with elements on which ``op`` operates.
    :param multiset2: A multiset with elements on which ``op`` operates.
    :param op: A :term:`binary operation` that operates on the elements of ``multiset1`` and
        ``multiset2``.
    :return: A multiset that consists of the defined results of ``op`` when executed on all
        combinations of the elements of ``multiset1`` and ``multiset2``, or `Undef()` if either
        set is not a :class:`~.Multiset`.
    """
    if _checked:
        if not isinstance(multiset1, _mo.Multiset):
            return _ud.make_or_raise_undef()
        if not isinstance(multiset2, _mo.Multiset):
            return _ud.make_or_raise_undef()
    else:
        assert multiset1.is_multiset
        assert multiset2.is_multiset

    def _get_values(_set1, _set2):
        return_count = _collections.Counter()
        for elem1, multi1 in _set1.data.items():
            for elem2, multi2 in _set2.data.items():
                result = op(elem1, elem2)
                if result is not _ud.Undef():
                    return_count[result] += multi1 * multi2

        return return_count

    return _mo.Multiset(_get_values(multiset1, multiset2), direct_load=True)


def unary_extend(set_: 'P( M )', op, _checked=True) -> 'P( M )':
    r"""Return the :term:`unary extension` of ``op`` from one :term:`algebra` to another algebra.

    For this extension, the elements of the extended algebra must be :term:`set`\s of the elements
    of the original algebra.

    :param set_: A :term:`set` with elements on which ``op`` operates.
    :param op: A :term:`unary operation` that operates on the elements of ``set_``.
    :return: A set that consists of the defined results of ``op`` when executed on the elements of
        ``set_``, or `Undef()` if ``set_`` is not a :class:`~.Set`.
    """
    if _checked:
        if not isinstance(set_, _mo.Set):
            return _ud.make_or_raise_undef()
    else:
        assert set_.is_set

    def _get_values(_set):
        for e in _set:
            result = op(e)
            if result is not _ud.Undef():
                yield result

    return _mo.Set(_get_values(set_), direct_load=True)


def unary_multi_extend(multiset: 'P( M x N )', op, _checked=True) -> 'P( M x N )':
    r"""Return the :term:`unary extension` of ``op`` from one :term:`algebra` to another algebra.

    For this extension, the elements of the extended algebra must be :term:`multiset`\s of the
    elements of the original algebra.

    :param multiset: A :term:`multiset` with elements on which ``op`` operates.
    :param op: A :term:`unary operation` that operates on the elements of ``multiset``.
    :return: A set that consists of the defined results of ``op`` when executed on the elements of
        ``multiset``, or `Undef()` if ``set1`` is not a :class:`~.Multiset`.
    """
    if _checked:
        if not isinstance(multiset, _mo.Multiset):
            return _ud.make_or_raise_undef()
    else:
        assert multiset.is_multiset

    def _get_values(_multiset):
        return_count = _collections.Counter()
        for elem, multi in _multiset.data.items():
            result = op(elem)
            if result is not _ud.Undef():
                return_count[result] += multi

        return return_count

    return _mo.Multiset(_get_values(multiset))
