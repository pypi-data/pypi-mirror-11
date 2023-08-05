import unittest
import os
from kafka_influxdb.kafka_influxdb import parse_configfile, overwrite_config_values

class Config:
    def __init__(self, configfile):
        self.configfile = configfile

class ParsedConfig:
    def __init__(self, kafka):
        self.kafka_host = "defaulthost"

class TestConfig(unittest.TestCase):

    def setUp(self):
        path = os.path.dirname(os.path.abspath(__file__))
        self.configfile = "{}/fixtures/config.yaml".format(path)

    def test_load_config(self):
        parsed_config = parse_configfile(self.configfile)
        self.assertEqual(parsed_config["kafka"]["host"], "kafkahost")
        self.assertEqual(parsed_config["kafka"]["port"], 1234)
        self.assertEqual(parsed_config["kafka"]["topic"], "kafkatopic")
        self.assertEqual(parsed_config["influxdb"]["host"], "influxdbhost")
        self.assertEqual(parsed_config["influxdb"]["port"], 9999)
        self.assertEqual(parsed_config["influxdb"]["user"], "hans")
        self.assertEqual(parsed_config["influxdb"]["password"], "hans")
        self.assertEqual(parsed_config["influxdb"]["dbname"], "influxdbname")
        self.assertEqual(parsed_config["influxdb"]["version"], 0.9)
        self.assertEqual(parsed_config["influxdb"]["retention_policy"], "my_rp")
        self.assertEqual(parsed_config["input_format"], "graphite")
        self.assertEqual(parsed_config["output_format"], "influxdb")
        self.assertEqual(parsed_config["buffer_size"], 1000)
        self.assertEqual(parsed_config["verbose"], False)
        self.assertEqual(parsed_config["statistics"], True)

    def test_override_config(self):
        parsed_config = ParsedConfig("defaulthost")
        self.assertEqual(parsed_config.kafka_host, "defaulthost")
        overwrite_config_values(parsed_config, {"kafka": {"host": "otherhost"}})
        self.assertEqual(parsed_config.kafka_host, "otherhost")

if __name__ == '__main__':
    unittest.main()
