# coding: utf8

# Copyright 2014-2015 Vincent Jacques <vincent@vincent-jacques.net>

"""
When given a :class:`Query`, the connection will return a :class:`QueryResponse`:

>>> connection(Query(table2).key_eq("h", 42))
<LowVoltage.actions.query.QueryResponse ...>

Items are accessed like this:

>>> connection(Query(table2).key_eq("h", 42)).items
[{u'h': 42, u'r1': 0, u'r2': 10}, {u'h': 42, u'r1': 1, u'r2': 9}, {u'h': 42, u'r1': 2, u'r2': 8}, {u'h': 42, u'r1': 3, u'r2': 7}, {u'h': 42, u'r1': 4, u'r2': 6}, {u'h': 42, u'r1': 5, u'r2': 5}, {u'h': 42, u'r1': 6}, {u'h': 42, u'r1': 7}, {u'h': 42, u'r1': 8}, {u'h': 42, u'r1': 9}]

See also the :func:`.iterate_query` compound. And :ref:`actions-vs-compounds` in the user guide.
"""

import LowVoltage as _lv
import LowVoltage.testing as _tst
from .action import Action
from .conversion import _convert_value_to_db, _convert_db_to_dict
from .next_gen_mixins import proxy
from .next_gen_mixins import OptionalBoolParameter, OptionalDictParameter
from .next_gen_mixins import (
    ConsistentRead,
    ExclusiveStartKey,
    ExpressionAttributeNames,
    ExpressionAttributeValues,
    FilterExpression,
    IndexName,
    Limit,
    ProjectionExpression,
    ReturnConsumedCapacity,
    Select,
    TableName,
)
from .return_types import ConsumedCapacity, _is_dict, _is_int, _is_list_of_dict


class QueryResponse(object):
    """
    QueryResponse()

    The `Query response <http://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Query.html#API_Query_ResponseElements>`__.
    """

    def __init__(
        self,
        ConsumedCapacity=None,
        Count=None,
        Items=None,
        LastEvaluatedKey=None,
        ScannedCount=None,
        **dummy
    ):
        self.__consumed_capacity = ConsumedCapacity
        self.__count = Count
        self.__items = Items
        self.__last_evaluated_key = LastEvaluatedKey
        self.__scanned_count = ScannedCount

    @property
    def consumed_capacity(self):
        """
        The capacity consumed by the request. If you used :meth:`~Query.return_consumed_capacity_total` or :meth:`~Query.return_consumed_capacity_indexes`.

        :type: ``None`` or :class:`.ConsumedCapacity`
        """
        if _is_dict(self.__consumed_capacity):
            return ConsumedCapacity(**self.__consumed_capacity)

    @property
    def count(self):
        """
        The number of items matching the query.

        :type: ``None`` or long
        """
        if _is_int(self.__count):
            return long(self.__count)

    @property
    def items(self):
        """
        The items matching the query. Unless you used :meth:`~Query.select_count`.

        :type: ``None`` or list of dict
        """
        if _is_list_of_dict(self.__items):
            return [_convert_db_to_dict(i) for i in self.__items]

    @property
    def last_evaluated_key(self):
        """
        The key of the last item evaluated by the query. If not None, it should be given to :meth:`~Query.exclusive_start_key` is a subsequent :class:`Query`.

        The :func:`.iterate_query` compound does that for you.

        :type: ``None`` or dict
        """
        if _is_dict(self.__last_evaluated_key):
            return _convert_db_to_dict(self.__last_evaluated_key)

    @property
    def scanned_count(self):
        """
        The number of item scanned during the query. This can be different from :attr:`count` when using :meth:`~Query.filter_expression`.

        :type: ``None`` or long
        """
        if _is_int(self.__scanned_count):
            return long(self.__scanned_count)


class KeyConditions(OptionalDictParameter):
    def __init__(self, parent):
        super(KeyConditions, self).__init__("KeyConditions", parent)

    def _convert(self, (operator, values)):
        return {
            "ComparisonOperator": operator,
            "AttributeValueList": [_convert_value_to_db(value) for value in values]
        }


class Query(Action):
    """
    The `Query request <http://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Query.html#API_Query_RequestParameters>`__.
    """

    def __init__(self, table_name=None):
        """
        Passing ``table_name`` to the constructor is like calling :meth:`table_name` on the new instance.
        """
        super(Query, self).__init__("Query", QueryResponse)
        self.__consistent_read = ConsistentRead(self)
        self.__exclusive_start_key = ExclusiveStartKey(self)
        self.__expression_attribute_names = ExpressionAttributeNames(self)
        self.__expression_attribute_values = ExpressionAttributeValues(self)
        self.__filter_expression = FilterExpression(self)
        self.__index_name = IndexName(self)
        self.__key_conditions = KeyConditions(self)
        self.__limit = Limit(self)
        self.__projection_expression = ProjectionExpression(self)
        self.__return_consumed_capacity = ReturnConsumedCapacity(self)
        self.__scan_index_forward = OptionalBoolParameter("ScanIndexForward", self)
        self.__select = Select(self)
        self.__table_name = TableName(self, table_name)

    @property
    def payload(self):
        data = {}
        data.update(self.__consistent_read.payload)
        data.update(self.__exclusive_start_key.payload)
        data.update(self.__expression_attribute_names.payload)
        data.update(self.__expression_attribute_values.payload)
        data.update(self.__filter_expression.payload)
        data.update(self.__index_name.payload)
        data.update(self.__key_conditions.payload)
        data.update(self.__limit.payload)
        data.update(self.__projection_expression.payload)
        data.update(self.__return_consumed_capacity.payload)
        data.update(self.__scan_index_forward.payload)
        data.update(self.__select.payload)
        data.update(self.__table_name.payload)
        return data

    @proxy
    def table_name(self, table_name):
        """
        >>> connection(
        ...   Query()
        ...     .table_name(table2)
        ...     .key_eq("h", 42)
        ... )
        <LowVoltage.actions.query.QueryResponse ...>
        """
        return self.__table_name.set(table_name)

    def key_eq(self, name, value):
        """
        Add a EQ condition to KeyConditions. Usable on both the hash key and the range key.
        The response will contain items whose key attribute ``name`` is equal to ``value``.

        >>> connection(
        ...   Query(table2)
        ...     .key_eq("h", 42)
        ... ).items
        [{u'h': 42, u'r1': 0, u'r2': 10}, {u'h': 42, u'r1': 1, u'r2': 9}, {u'h': 42, u'r1': 2, u'r2': 8}, ...]
        """
        return self.__key_conditions.add(name, ("EQ", [value]))

    def key_le(self, name, value):
        """
        Add a LE condition to KeyConditions. Usable only on the range key.
        The response will contain items whose key attribute ``name`` is less than or equal to ``value``.

        >>> connection(
        ...   Query(table2)
        ...     .key_eq("h", 42)
        ...     .key_le("r1", 1)
        ... ).items
        [{u'h': 42, u'r1': 0, u'r2': 10}, {u'h': 42, u'r1': 1, u'r2': 9}]
        """
        return self.__key_conditions.add(name, ("LE", [value]))

    def key_lt(self, name, value):
        """
        Add a LT condition to KeyConditions. Usable only on the range key.
        The response will contain items whose key attribute ``name`` is strictly less than ``value``.

        >>> connection(
        ...   Query(table2)
        ...     .key_eq("h", 42)
        ...     .key_lt("r1", 2)
        ... ).items
        [{u'h': 42, u'r1': 0, u'r2': 10}, {u'h': 42, u'r1': 1, u'r2': 9}]
        """
        return self.__key_conditions.add(name, ("LT", [value]))

    def key_ge(self, name, value):
        """
        Add a GE condition to KeyConditions. Usable only on the range key.
        The response will contain items whose key attribute ``name`` is greater than or equal to ``value``.

        >>> connection(
        ...   Query(table2)
        ...     .key_eq("h", 42)
        ...     .key_ge("r1", 7)
        ... ).items
        [{u'h': 42, u'r1': 7}, {u'h': 42, u'r1': 8}, {u'h': 42, u'r1': 9}]
        """
        return self.__key_conditions.add(name, ("GE", [value]))

    def key_gt(self, name, value):
        """
        Add a GT condition to KeyConditions. Usable only on the range key.
        The response will contain items whose key attribute ``name`` is strictly greater than ``value``.

        >>> connection(
        ...   Query(table2)
        ...     .key_eq("h", 42)
        ...     .key_gt("r1", 6)
        ... ).items
        [{u'h': 42, u'r1': 7}, {u'h': 42, u'r1': 8}, {u'h': 42, u'r1': 9}]
        """
        return self.__key_conditions.add(name, ("GT", [value]))

    def key_begins_with(self, name, value):
        """
        Add a BEGINS_WITH condition to KeyConditions. Usable only on the range key if it is a string.
        The response will contain items whose key attribute ``name`` begins with ``value``.
        """
        return self.__key_conditions.add(name, ("BEGINS_WITH", [value]))

    def key_between(self, name, lo, hi):
        """
        Add a BETWEEN condition to KeyConditions. Usable only on the range key.
        The response will contain items whose key attribute ``name`` is greater than or equal to ``lo`` and less than or equal to ``hi``.

        >>> connection(
        ...   Query(table2)
        ...     .key_eq("h", 42)
        ...     .key_between("r1", 4, 6)
        ... ).items
        [{u'h': 42, u'r1': 4, u'r2': 6}, {u'h': 42, u'r1': 5, u'r2': 5}, {u'h': 42, u'r1': 6}]
        """
        return self.__key_conditions.add(name, ("BETWEEN", [lo, hi]))

    @proxy("Query")
    def exclusive_start_key(self, key):
        """
        The :func:`.iterate_query` compound does that for you.

        >>> r = connection(
        ...   Query(table2)
        ...     .key_eq("h", 42)
        ...     .limit(2)
        ... )
        >>> r.items
        [{u'h': 42, u'r1': 0, u'r2': 10}, {u'h': 42, u'r1': 1, u'r2': 9}]
        >>> r.last_evaluated_key
        {u'h': 42, u'r1': 1}
        >>> connection(
        ...   Query(table2)
        ...     .key_eq("h", 42)
        ...     .limit(2)
        ...     .exclusive_start_key({u'h': 42, u'r1': 1})
        ... ).items
        [{u'h': 42, u'r1': 2, u'r2': 8}, {u'h': 42, u'r1': 3, u'r2': 7}]
        """
        return self.__exclusive_start_key.set(key)

    @proxy
    def limit(self, limit):
        """
        See :meth:`exclusive_start_key` for an example.
        """
        return self.__limit.set(limit)

    @proxy
    def select_count(self):
        """
        >>> r = connection(
        ...   Query(table2)
        ...     .key_eq("h", 42)
        ...     .select_count()
        ... )
        >>> r.count
        10L
        >>> print r.items
        None
        """
        return self.__select.count()

    @proxy
    def select_all_attributes(self):
        """
        >>> connection(
        ...   Query(table2)
        ...     .key_eq("h", 42)
        ...     .index_name("lsi")
        ...     .select_all_attributes()
        ...     .limit(2)
        ... ).items
        [{u'h': 42, u'r1': 5, u'r2': 5}, {u'h': 42, u'r1': 4, u'r2': 6}]
        """
        return self.__select.all_attributes()

    @proxy
    def select_all_projected_attributes(self):
        """
        >>> connection(
        ...   Query(table2)
        ...     .key_eq("h", 42)
        ...     .index_name("lsi")
        ...     .select_all_projected_attributes()
        ...     .limit(2)
        ... ).items
        [{u'h': 42, u'r1': 5, u'r2': 5}, {u'h': 42, u'r1': 4, u'r2': 6}]
        """
        return self.__select.all_projected_attributes()

    @proxy
    def index_name(self, index_name):
        """
        >>> connection(
        ...   Query(table2)
        ...     .key_eq("h", 42)
        ...     .index_name("lsi")
        ... ).items
        [{u'h': 42, u'r1': 5, u'r2': 5}, {u'h': 42, u'r1': 4, u'r2': 6}, {u'h': 42, u'r1': 3, u'r2': 7}, {u'h': 42, u'r1': 2, u'r2': 8}, {u'h': 42, u'r1': 1, u'r2': 9}, {u'h': 42, u'r1': 0, u'r2': 10}]
        """
        return self.__index_name.set(index_name)

    def scan_index_forward_true(self):
        """
        Set ScanIndexForward to true. Items in the response will be sorted with ascending range keys.

        >>> connection(
        ...   Query(table2)
        ...     .key_eq("h", 42)
        ...     .project("r1")
        ...     .scan_index_forward_true()
        ... ).items
        [{u'r1': 0}, {u'r1': 1}, {u'r1': 2}, {u'r1': 3}, {u'r1': 4}, {u'r1': 5}, {u'r1': 6}, {u'r1': 7}, {u'r1': 8}, {u'r1': 9}]
        """
        return self.__scan_index_forward.set(True)

    def scan_index_forward_false(self):
        """
        Set ScanIndexForward to false. Items in the response will be sorted with descending range keys.

        >>> connection(
        ...   Query(table2)
        ...     .key_eq("h", 42)
        ...     .project("r1")
        ...     .scan_index_forward_false()
        ... ).items
        [{u'r1': 9}, {u'r1': 8}, {u'r1': 7}, {u'r1': 6}, {u'r1': 5}, {u'r1': 4}, {u'r1': 3}, {u'r1': 2}, {u'r1': 1}, {u'r1': 0}]
        """
        return self.__scan_index_forward.set(False)

    @proxy
    def project(self, *names):
        """
        >>> connection(
        ...   Query(table2)
        ...     .key_eq("h", 42)
        ...     .project("r2")
        ... ).items
        [{u'r2': 10}, {u'r2': 9}, {u'r2': 8}, {u'r2': 7}, {u'r2': 6}, {u'r2': 5}, {}, {}, {}, {}]
        """
        return self.__projection_expression.add(*names)

    @proxy
    def filter_expression(self, expression):
        """
        >>> connection(
        ...   Query(table2)
        ...     .key_eq("h", 42)
        ...     .key_ge("r1", 2)
        ...     .filter_expression("#syn IN (:val1, :val2)")
        ...     .expression_attribute_name("syn", "r2")
        ...     .expression_attribute_value("val1", 5)
        ...     .expression_attribute_value("val2", 7)
        ... ).items
        [{u'h': 42, u'r1': 3, u'r2': 7}, {u'h': 42, u'r1': 5, u'r2': 5}]
        """
        return self.__filter_expression.set(expression)

    @proxy
    def expression_attribute_name(self, synonym, name):
        """
        See :meth:`filter_expression` for an example.
        """
        return self.__expression_attribute_names.add(synonym, name)

    @proxy
    def expression_attribute_value(self, name, value):
        """
        See :meth:`filter_expression` for an example.
        """
        return self.__expression_attribute_values.add(name, value)

    @proxy
    def consistent_read_true(self):
        """
        >>> connection(
        ...   Query(table)
        ...     .key_eq("h", 0)
        ...     .consistent_read_true()
        ...     .return_consumed_capacity_total()
        ... ).consumed_capacity.capacity_units
        1.0
        """
        return self.__consistent_read.true()

    @proxy
    def consistent_read_false(self):
        """
        >>> connection(
        ...   Query(table)
        ...     .key_eq("h", 0)
        ...     .consistent_read_false()
        ...     .return_consumed_capacity_total()
        ... ).consumed_capacity.capacity_units
        0.5
        """
        return self.__consistent_read.false()

    @proxy
    def return_consumed_capacity_total(self):
        """
        >>> connection(
        ...   Query(table)
        ...     .key_eq("h", 0)
        ...     .return_consumed_capacity_total()
        ... ).consumed_capacity.capacity_units
        0.5
        """
        return self.__return_consumed_capacity.total()

    @proxy
    def return_consumed_capacity_indexes(self):
        """
        >>> c1 = connection(
        ...   Query(table)
        ...     .key_eq("h", 0)
        ...     .return_consumed_capacity_indexes()
        ... ).consumed_capacity
        >>> c1.capacity_units
        0.5
        >>> c1.table.capacity_units
        0.5
        >>> print c1.global_secondary_indexes
        None

        >>> c2 = connection(
        ...   Query(table)
        ...     .index_name("gsi")
        ...     .key_eq("gh", 0)
        ...     .return_consumed_capacity_indexes()
        ... ).consumed_capacity
        >>> c2.capacity_units
        0.5
        >>> c2.table.capacity_units
        0.0
        >>> c2.global_secondary_indexes["gsi"].capacity_units
        0.5
        """
        return self.__return_consumed_capacity.indexes()

    @proxy
    def return_consumed_capacity_none(self):
        """
        >>> print connection(
        ...   Query(table)
        ...     .key_eq("h", 0)
        ...     .return_consumed_capacity_none()
        ... ).consumed_capacity
        None
        """
        return self.__return_consumed_capacity.none()


class QueryUnitTests(_tst.UnitTests):
    def test_name(self):
        self.assertEqual(Query("Aaa").name, "Query")

    def test_table_name(self):
        self.assertEqual(Query().table_name("Aaa").payload, {"TableName": "Aaa"})

    def test_constructor(self):
        self.assertEqual(Query("Aaa").payload, {"TableName": "Aaa"})

    def test_key_eq(self):
        self.assertEqual(
            Query("Aaa").key_eq("name", 42).payload,
            {
                "TableName": "Aaa",
                "KeyConditions": {"name": {"ComparisonOperator": "EQ", "AttributeValueList": [{"N": "42"}]}},
            }
        )

    def test_key_le(self):
        self.assertEqual(
            Query("Aaa").key_le("name", 42).payload,
            {
                "TableName": "Aaa",
                "KeyConditions": {"name": {"ComparisonOperator": "LE", "AttributeValueList": [{"N": "42"}]}},
            }
        )

    def test_key_lt(self):
        self.assertEqual(
            Query("Aaa").key_lt("name", 42).payload,
            {
                "TableName": "Aaa",
                "KeyConditions": {"name": {"ComparisonOperator": "LT", "AttributeValueList": [{"N": "42"}]}},
            }
        )

    def test_key_ge(self):
        self.assertEqual(
            Query("Aaa").key_ge("name", 42).payload,
            {
                "TableName": "Aaa",
                "KeyConditions": {"name": {"ComparisonOperator": "GE", "AttributeValueList": [{"N": "42"}]}},
            }
        )

    def test_key_gt(self):
        self.assertEqual(
            Query("Aaa").key_gt("name", 42).payload,
            {
                "TableName": "Aaa",
                "KeyConditions": {"name": {"ComparisonOperator": "GT", "AttributeValueList": [{"N": "42"}]}},
            }
        )

    def test_key_begins_with(self):
        self.assertEqual(
            Query("Aaa").key_begins_with("name", u"prefix").payload,
            {
                "TableName": "Aaa",
                "KeyConditions": {"name": {"ComparisonOperator": "BEGINS_WITH", "AttributeValueList": [{"S": "prefix"}]}},
            }
        )

    def test_key_between(self):
        self.assertEqual(
            Query("Aaa").key_between("name", 42, 44).payload,
            {
                "TableName": "Aaa",
                "KeyConditions": {"name": {"ComparisonOperator": "BETWEEN", "AttributeValueList": [{"N": "42"}, {"N": "44"}]}},
            }
        )

    def test_exclusive_start_key(self):
        self.assertEqual(Query("Aaa").exclusive_start_key({"h": u"v"}).payload, {"TableName": "Aaa", "ExclusiveStartKey": {"h": {"S": "v"}}})

    def test_limit(self):
        self.assertEqual(Query("Aaa").limit(4).payload, {"TableName": "Aaa", "Limit": 4})

    def test_select_all_attributes(self):
        self.assertEqual(Query("Aaa").select_all_attributes().payload, {"TableName": "Aaa", "Select": "ALL_ATTRIBUTES"})

    def test_select_all_projected_attributes(self):
        self.assertEqual(Query("Aaa").select_all_projected_attributes().payload, {"TableName": "Aaa", "Select": "ALL_PROJECTED_ATTRIBUTES"})

    def test_select_count(self):
        self.assertEqual(Query("Aaa").select_count().payload, {"TableName": "Aaa", "Select": "COUNT"})

    def test_expression_attribute_name(self):
        self.assertEqual(Query("Aaa").expression_attribute_name("n", "p").payload, {"TableName": "Aaa", "ExpressionAttributeNames": {"#n": "p"}})

    def test_expression_attribute_value(self):
        self.assertEqual(Query("Aaa").expression_attribute_value("n", u"p").payload, {"TableName": "Aaa", "ExpressionAttributeValues": {":n": {"S": "p"}}})

    def test_project(self):
        self.assertEqual(Query("Aaa").project("a").payload, {"TableName": "Aaa", "ProjectionExpression": "a"})

    def test_return_consumed_capacity_total(self):
        self.assertEqual(Query("Aaa").return_consumed_capacity_total().payload, {"TableName": "Aaa", "ReturnConsumedCapacity": "TOTAL"})

    def test_return_consumed_capacity_indexes(self):
        self.assertEqual(Query("Aaa").return_consumed_capacity_indexes().payload, {"TableName": "Aaa", "ReturnConsumedCapacity": "INDEXES"})

    def test_return_consumed_capacity_none(self):
        self.assertEqual(Query("Aaa").return_consumed_capacity_none().payload, {"TableName": "Aaa", "ReturnConsumedCapacity": "NONE"})

    def test_filter_expression(self):
        self.assertEqual(Query("Aaa").filter_expression("a=b").payload, {"TableName": "Aaa", "FilterExpression": "a=b"})

    def test_consistent_read_true(self):
        self.assertEqual(Query("Aaa").consistent_read_true().payload, {"TableName": "Aaa", "ConsistentRead": True})

    def test_consistent_read_false(self):
        self.assertEqual(Query("Aaa").consistent_read_false().payload, {"TableName": "Aaa", "ConsistentRead": False})

    def test_index_name(self):
        self.assertEqual(Query("Aaa").index_name("foo").payload, {"TableName": "Aaa", "IndexName": "foo"})

    def test_scan_index_forward_true(self):
        self.assertEqual(Query("Aaa").scan_index_forward_true().payload, {"TableName": "Aaa", "ScanIndexForward": True})

    def test_scan_index_forward_false(self):
        self.assertEqual(Query("Aaa").scan_index_forward_false().payload, {"TableName": "Aaa", "ScanIndexForward": False})


class QueryResponseUnitTests(_tst.UnitTests):
    def test_all_none(self):
        r = QueryResponse()
        self.assertIsNone(r.consumed_capacity)
        self.assertIsNone(r.count)
        self.assertIsNone(r.items)
        self.assertIsNone(r.last_evaluated_key)
        self.assertIsNone(r.scanned_count)

    def test_all_set(self):
        unprocessed_keys = object()
        r = QueryResponse(ConsumedCapacity={}, Count=1, Items=[{"h": {"S": "a"}}], LastEvaluatedKey={"h": {"S": "b"}}, ScannedCount=2)
        self.assertIsInstance(r.consumed_capacity, ConsumedCapacity)
        self.assertEqual(r.count, 1)
        self.assertEqual(r.items, [{"h": "a"}])
        self.assertEqual(r.last_evaluated_key, {"h": "b"})
        self.assertEqual(r.scanned_count, 2)
