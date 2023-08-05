"""
Rejected Consumers for automatic deserialization (and serialization) of
Avro datum in RabbitMQ messages.

"""
import bz2
import base64
import json
import logging
import os
from os import path
import StringIO
import warnings
import zlib

from rejected import consumer
from avro import io
from tornado import httpclient
from avro import schema

LOGGER = logging.getLogger(__name__)

DATUM_MIME_TYPE = 'application/vnd.apache.avro.datum'

__version__ = '0.3.1    '


class _DatumConsumer(consumer.Consumer):
    """Automatically deserialize Avro datum from RabbitMQ messages that have
    the ``content-type`` of ``application/vnd.apache.avro.datum``.

    """
    _schemas = dict()

    @property
    def body(self):
        """Return the message body, deserialized if the content-type is
        set properly.

        :rtype: any

        """
        # Return a materialized view of the body if it has been previously set
        if self._message_body:
            return self._message_body

        # Content Encoding decompression
        elif self.content_encoding == 'bzip2':
            self._message_body = self._decode_bz2(self._message.body)
        elif self.content_encoding == 'gzip':
            self._message_body = self._decode_gzip(self._message.body)
        else:
            self._message_body = self._message.body

        if self.content_type == DATUM_MIME_TYPE:
            schema_json = self._get_schema(self.message_type)
            self._message_body = self._deserialize(schema_json,
                                                   self._message_body)
        elif self.content_type.startswith('application/json'):
            self._message_body = json.loads(self._message_body)

        return self._message_body

    @staticmethod
    def _decode_bz2(value):
        """Return a bz2 decompressed value

        :param str value: Compressed value
        :rtype: str
        """
        return bz2.decompress(value)

    @staticmethod
    def _decode_gzip(value):
        """Return a zlib decompressed value

        :param str value: Compressed value
        :rtype: str
        """
        return zlib.decompress(value)

    @staticmethod
    def _deserialize(avro_schema, data):
        """Deserialize an Avro datum with the specified schema string

        :param str avro_schema: The schema JSON snippet
        :param str data: The Avro datum to deserialize
        :rtype: dict

        """
        datum_reader = io.DatumReader(avro_schema)
        decoder = io.BinaryDecoder(StringIO.StringIO(data))
        return datum_reader.read(decoder)

    @staticmethod
    def _serialize(avro_schema, data):
        """Serialize a data structure into an Avro datum

        :param str savro_schema: The parsed Avro schema
        :param dict data: The value to turn into an Avro datum
        :rtype: str

        """
        str_io = StringIO.StringIO()
        encoder = io.BinaryEncoder(str_io)
        writer = io.DatumWriter(avro_schema)
        try:
            writer.write(data, encoder)
        except io.AvroTypeException as error:
            raise ValueError(error)
        return str_io.getvalue()

    def _get_schema(self, message_type):
        """Fetch the Avro schema file from cache or the filesystem.

        :param str message_type:
        :rtype: str

        """
        if message_type not in self._schemas:
            self._schemas[message_type] = \
                schema.parse(self._load_schema(message_type))
        return self._schemas[message_type]

    def _load_schema(self, message_type):
        """Return the schema file as a str for the specified message_type.
        This method must be implemented by child classes.

        :param str message_type: The message type to load the schema for
        :raises: NotImplementedError
        :type: str

        """
        raise NotImplementedError


class DatumFileSchemaConsumer(_DatumConsumer):
    """Automatically deserialize Avro datum from RabbitMQ messages that have
    the ``content-type`` of ``application/vnd.apache.avro.datum``. Schema
    files are loaded from disk. The schema file path is comprised of the
    ``schema_path`` configuration setting and the message type, appending the
    file type ``.avsc`` to the the end.

    """
    def prepare(self):
        """Ensure the schema_path is set in the settings"""
        if self.settings.get('schema_path') is None:
            raise consumer.ConsumerException('schema_path is not set')
        if not path.exists(path.normpath(self.settings.schema_path)):
            raise consumer.ConsumerException('schema_path is invalid')
        super(DatumFileSchemaConsumer, self).prepare()

    def _load_schema(self, message_type):
        """Load the schema file from the file system, raising a ``ValueError``
        if the the schema file can not be found. The schema file path is
        comprised of the ``schema_path`` configuration setting and the
        message type, appending the file type ``.avsc`` to the the end.

        :param str message_type: The message type to load the schema for
        :type: str

        """
        file_path = path.normpath(path.join(self.settings.schema_path,
                                            '{0}.avsc'.format(message_type)))
        if not path.exists(file_path):
            raise ValueError('Missing schema file: {0}'.format(file_path))

        fp = open(file_path, 'r')
        message_schema = fp.read()
        fp.close()
        return message_schema


class DatumConsumer(DatumFileSchemaConsumer):
    """Deprecated clone of DatumFileSchemaConsumer for 0.1.0 compatibility"""
    def prepare(self):
        warnings.warn("Use DatumFileSchemaConsumer instead of DatumConsumer",
                      DeprecationWarning)
        super(DatumConsumer, self).prepare()


class DatumConsulSchemaConsumer(_DatumConsumer):
    """Automatically deserialize Avro datum from RabbitMQ messages that have
    the ``content-type`` of ``application/vnd.apache.avro.datum``. Schema
    files are loaded from Consul instead of from disk.

    """
    CONSUL_URL_FORMAT = 'http://{0}:{1}/v1/kv/schema/avro/{2}/{3}.avsc'

    def _consul_url(self, schema_name):
        consul_host = os.getenv('CONSUL_HOST', 'localhost')
        consul_port = int(os.getenv('CONSUL_PORT', '8500'))
        schema_type, schema_version = schema_name.rsplit('.', 1)
        return self.CONSUL_URL_FORMAT.format(consul_host, consul_port,
                                             schema_type, schema_version)

    def _load_schema(self, message_type):
        http_client = httpclient.HTTPClient()
        url = self._consul_url(message_type)
        LOGGER.debug('Loading schema for %s from %s', message_type, url)
        print(url)
        try:
            response = http_client.fetch(url)
        except httpclient.HTTPError as error:
            LOGGER.error('Could not fetch Avro schema for %s (%s)',
                         message_type, error)
            raise consumer.ConsumerException('Error fetching avro scema')
        data = json.loads(response.body)
        return base64.b64decode(data[0]['Value'])
