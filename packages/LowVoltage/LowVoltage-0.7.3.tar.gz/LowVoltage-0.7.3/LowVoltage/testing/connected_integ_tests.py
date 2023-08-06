# coding: utf8

# Copyright 2014-2015 Vincent Jacques <vincent@vincent-jacques.net>

import datetime

try:
    from testresources import TestResourceManager, ResourcedTestCase
except ImportError:  # pragma no cover (Test code)
    class TestResourceManager(object):
        pass

    class ResourcedTestCase(object):
        pass

import LowVoltage as _lv


table_name_prefix = datetime.datetime.now().strftime("LowVoltage.Tests.Integ.%Y-%m-%d.%H-%M-%S.%f")


def make_connection():
    return _lv.Connection("us-west-1", _lv.EnvironmentCredentials())


class ConnectedIntegTests(ResourcedTestCase):
    # Create an IAM user, populate the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables
    # Use the following IAM policy to limit access to specific tables:
    # {
    #     "Version": "2012-10-17",
    #     "Statement": [
    #         {
    #             "Action": [
    #                 "dynamodb:*"
    #             ],
    #             "Effect": "Allow",
    #             "Resource": "arn:aws:dynamodb:*:*:table/LowVoltage.Tests.*"
    #         },
    #         {
    #             "Action": [
    #                 "dynamodb:ListTables"
    #             ],
    #             "Effect": "Allow",
    #             "Resource": "*"
    #         }
    #     ]
    # }
    # Could we refine the policy to ensure the total provisioned throughput is capped?

    def setUp(self):
        super(ConnectedIntegTests, self).setUp()
        self.connection = make_connection()

    @classmethod
    def make_table_name(cls):
        assert cls.__name__.endswith("ConnectedIntegTests")
        return "{}.{}".format(table_name_prefix, cls.__name__[:19])


class DynamoDbResourceManager(TestResourceManager):
    def make(self, dependencies):
        connection = make_connection()

        table = table_name_prefix

        connection(
            _lv.CreateTable(table).hash_key("tab_h", _lv.STRING).range_key("tab_r", _lv.NUMBER).provisioned_throughput(1, 1)
                .global_secondary_index("gsi").hash_key("gsi_h", _lv.STRING).range_key("gsi_r", _lv.NUMBER).project_all().provisioned_throughput(1, 1)
                .local_secondary_index("lsi").hash_key("tab_h").range_key("lsi_r", _lv.NUMBER).project_all().provisioned_throughput(1, 1)
        )
        _lv.wait_for_table_activation(connection, table)

        return table

    def clean(self, table):
        connection = make_connection()
        connection(_lv.DeleteTable(table))
        _lv.wait_for_table_deletion(connection, table)


class ConnectedIntegTestsWithTable(ConnectedIntegTests):
    resources = [("table", DynamoDbResourceManager())]

    item = {"tab_h": u"0", "tab_r": 0, "gsi_h": u"1", "gsi_r": 1, "lsi_r": 2}
    tab_key = {"tab_h": u"0", "tab_r": 0}
    gsi_key = {"gsi_h": u"1", "gsi_r": 1}
    lsi_key = {"tab_h": u"0", "lsi_r": 2}
