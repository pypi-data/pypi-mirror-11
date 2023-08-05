import json

from twisted.internet.defer import Deferred, inlineCallbacks, returnValue
from twisted.web.server import NOT_DONE_YET
from twisted.web import http, resource, util

from vumi.config import ConfigContext
from vumi.message import TransportUserMessage
from vumi import errors


class BaseResource(resource.Resource):

    def __init__(self, worker, conversation_key):
        resource.Resource.__init__(self)
        self.worker = worker
        self.conversation_key = conversation_key

    def finish_response(self, request, body, code, status=None):
        request.setHeader('Content-Type', 'application/json; charset=utf-8')
        request.setResponseCode(code, status)
        request.write(body)
        request.finish()

    def client_error_response(self, request, reason, code=http.BAD_REQUEST):
        msg = json.dumps({
            "success": False,
            "reason": reason,
        })
        self.finish_response(request, msg, code=code, status=reason)

    def successful_send_response(self, request, msg, code=http.OK):
        self.finish_response(request, msg.to_json(), code=code)


class InvalidAggregate(errors.VumiError):
    pass


class MsgOptions(object):
    """Helper for sanitizing msg options from clients."""

    WHITELIST = {}
    VALIDATION = ()

    def __init__(self, payload, api_config):
        self.errors = []
        for key, checker in sorted(self.WHITELIST.iteritems()):
            value = payload.get(key)
            if not checker(value):
                self.errors.append(
                    "Invalid or missing value for payload key %r" % (key,))
            else:
                setattr(self, key, value)

        for checker in self.VALIDATION:
            error = checker(payload, api_config)
            if error is not None:
                self.errors.append(error)

    @property
    def as_dict(self):
        ret = {}
        for field in self.WHITELIST:
            value = getattr(self, field)
            if value:
                ret[field] = value
        return ret

    @property
    def is_valid(self):
        return not bool(self.errors)

    @property
    def error_msg(self):
        if not self.errors:
            return None
        elif len(self.errors) == 1:
            return self.errors[0]
        else:
            return "Errors:\n* %s" % ("\n* ".join(self.errors))


class MsgCheckHelpers(object):
    @staticmethod
    def is_unicode(value):
        return isinstance(value, unicode)

    @staticmethod
    def is_unicode_or_none(value):
        return (value is None) or (isinstance(value, unicode))

    @staticmethod
    def is_session_event(value):
        return value in TransportUserMessage.SESSION_EVENTS

    @staticmethod
    def is_dict_or_none(value):
        return (value is None) or (isinstance(value, dict))

    # The following checkers perform more complex validation based on the
    # entire payload and the API config.

    @staticmethod
    def is_within_content_length_limit(payload, api_config):
        """
        Check that the message content is within the configured length limit.
        """
        length_limit = api_config.get('content_length_limit')
        if (length_limit is not None) and (payload["content"] is not None):
            content_length = len(payload["content"])
            if content_length > length_limit:
                return "Payload content too long: %s > %s" % (
                    content_length, length_limit)
        return None


class HelperMetadataOptions(MsgOptions):
    """`helper_metadata` parameter for messages"""

    WHITELIST = {
        'voice': MsgCheckHelpers.is_dict_or_none,
    }


class SendToOptions(MsgOptions):
    """Payload options for messages sent with `.send_to(...)`."""

    WHITELIST = {
        'content': MsgCheckHelpers.is_unicode_or_none,
        'to_addr': MsgCheckHelpers.is_unicode,
        'helper_metadata': MsgCheckHelpers.is_dict_or_none,
        'session_event': MsgCheckHelpers.is_session_event,
    }

    VALIDATION = (
        MsgCheckHelpers.is_within_content_length_limit,
    )


class ReplyToOptions(MsgOptions):
    """Payload options for messages sent with `.reply_to(...)`."""

    WHITELIST = {
        'content': MsgCheckHelpers.is_unicode_or_none,
        'session_event': MsgCheckHelpers.is_session_event,
    }

    VALIDATION = (
        MsgCheckHelpers.is_within_content_length_limit,
    )


class MessageResource(BaseResource):

    routing_key = '%(transport_name)s.stream.message.%(conversation_key)s'

    def render_PUT(self, request):
        d = Deferred()
        d.addCallback(self.handle_PUT)
        d.callback(request)
        return NOT_DONE_YET

    @inlineCallbacks
    def handle_PUT(self, request):
        try:
            payload = json.loads(request.content.read())
        except ValueError:
            self.client_error_response(request, 'Invalid Message')
            return

        user_account = request.getUser()
        d = self.worker.concurrency_limiter.start(user_account)
        try:
            yield d  # Wait for our concurrency limiter to let us move on.
            yield self.handle_PUT_send_to(request, payload)
        finally:
            self.worker.concurrency_limiter.stop(user_account)

    @inlineCallbacks
    def handle_PUT_send_to(self, request, payload):
        msg_options = SendToOptions(
            payload, self.worker.get_static_config()._config_data)
        if not msg_options.is_valid:
            self.client_error_response(request, msg_options.error_msg)
            return

        helper_metadata_checker = HelperMetadataOptions(
            msg_options.helper_metadata or {},
            self.worker.get_static_config()._config_data)
        if not helper_metadata_checker.is_valid:
            self.client_error_response(
                request, helper_metadata_checker.error_msg)
            return

        helper_metadata = helper_metadata_checker.as_dict

        msg = yield self.worker.send_to(
            msg_options.to_addr, msg_options.content,
            endpoint='default', session_event=msg_options.session_event,
            helper_metadata=helper_metadata)

        self.successful_send_response(request, msg)


class ConversationResource(resource.Resource):

    def __init__(self, worker, conversation_key):
        resource.Resource.__init__(self)
        self.worker = worker
        self.redis = worker.redis
        self.conversation_key = conversation_key

    def get_worker_config(self, user_account_key):
        ctxt = ConfigContext(user_account=user_account_key)
        return self.worker.get_config(msg=None, ctxt=ctxt)

    def key(self, *args):
        return ':'.join(['concurrency'] + map(unicode, args))

    @inlineCallbacks
    def is_allowed(self, config, user_id):
        if config.concurrency_limit < 0:
            returnValue(True)
        count = int((yield self.redis.get(self.key(user_id))) or 0)
        returnValue(count < config.concurrency_limit)

    def track_request(self, user_id):
        return self.redis.incr(self.key(user_id))

    def release_request(self, err, user_id):
        return self.redis.decr(self.key(user_id))

    def render(self, request):
        return resource.NoResource().render(request)

    def getChild(self, path, request):
        return util.DeferredResource(self.getDeferredChild(path, request))

    @inlineCallbacks
    def getDeferredChild(self, path, request):
        resource_class = self.get_child_resource(path)

        if resource_class is None:
            returnValue(resource.NoResource())

        user_id = request.getUser()
        config = yield self.get_worker_config(user_id)
        if (yield self.is_allowed(config, user_id)):

            # remove track when request is closed
            finished = request.notifyFinish()
            finished.addBoth(self.release_request, user_id)

            yield self.track_request(user_id)
            returnValue(resource_class(self.worker, self.conversation_key))
        returnValue(resource.ErrorPage(http.FORBIDDEN, 'Forbidden',
                                       'Too many concurrent connections'))

    def get_child_resource(self, path):
        return {
            'messages.json': MessageResource,
        }.get(path)
