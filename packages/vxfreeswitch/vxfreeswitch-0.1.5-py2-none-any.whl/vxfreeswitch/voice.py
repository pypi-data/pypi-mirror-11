# -*- test-case-name: vxfreeswitch.tests.test_voice -*-

"""A Vumi transport for connecting to SIP gateways via FreeSWITCH's ESL
interfaces.

If outbound messages provide a URL to a pre-recorded audio message,
that is played via SIP. Otherwise sound is generated using a
text-to-speech engine.

DTMF digits dialed on the phone are collected by the transport and
sent as inbound messages. Digits may either be sent through individually
(the default) or collected until a specified character is pressed.
"""

import md5
import os

from twisted.internet.protocol import ServerFactory
from twisted.internet.defer import (
    inlineCallbacks, returnValue, Deferred, gatherResults)
from twisted.internet.utils import getProcessOutput

from eventsocket import EventProtocol

from confmodel.errors import ConfigError
from confmodel.fields import ConfigText, ConfigDict

from vumi.transports import Transport
from vumi.message import TransportUserMessage
from vumi.config import ConfigClientEndpoint, ConfigServerEndpoint
from vumi.errors import VumiError
from vumi import log

from vxfreeswitch.originate import (
    OriginateFormatter, OriginateMissingParameter)
from vxfreeswitch.client import FreeSwitchClient, FreeSwitchClientError


class VoiceError(VumiError):
    """Raised when errors occur while processing voice messages."""


class FreeSwitchESLProtocol(EventProtocol):

    def __init__(self, vumi_transport):
        EventProtocol.__init__(self)
        self.vumi_transport = vumi_transport
        self.request_hang_up = False
        self.current_input = ''
        self.input_type = None
        self.uniquecallid = None

    @inlineCallbacks
    def connectionMade(self):
        yield self.connect().addCallback(self.on_connect)
        yield self.myevents()
        yield self.answer()
        yield self.vumi_transport.register_client(self)

    def on_connect(self, ctx):
        self.uniquecallid = ctx.variable_call_uuid

    def onDtmf(self, ev):
        if self.input_type is None:
            return self.vumi_transport.handle_input(self, ev.DTMF_Digit)
        else:
            if ev.DTMF_Digit == self.input_type:
                ret_value = self.current_input
                self.current_input = ''
                return self.vumi_transport.handle_input(self, ret_value)
            else:
                self.current_input += ev.DTMF_Digit

    def create_tts_command(self, command_template, filename, message):
        params = {"filename": filename, "text": message}
        args = command_template.strip().split()
        cmd, args = args[0], args[1:]
        args = [arg.format(**params) for arg in args]
        return cmd, args

    @inlineCallbacks
    def create_and_stream_text_as_speech(self, folder, command, ext, message):
        key = md5.md5(message).hexdigest()
        filename = os.path.join(folder, "voice-%s.%s" % (key, ext))
        if not os.path.exists(filename):
            log.msg("Generating voice file %r" % (filename,))
            cmd, args = self.create_tts_command(command, filename, message)
            yield getProcessOutput(cmd, args=args)
        else:
            log.msg("Using cached voice file %r" % (filename,))

        yield self.playback(filename)

    @inlineCallbacks
    def send_text_as_speech(self, engine, voice, message):
        yield self.set("tts_engine=" + engine)
        yield self.set("tts_voice=" + voice)
        yield self.execute("speak", message)

    @inlineCallbacks
    def stream_text_as_speech(self, message):
        finalmessage = message.replace("\n", " . ")
        log.msg("TTS: " + finalmessage)
        cfg = self.vumi_transport.config
        if cfg.tts_type == "local":
            yield self.create_and_stream_text_as_speech(
                cfg.tts_local_cache, cfg.tts_local_command,
                cfg.tts_local_ext, finalmessage)
        elif cfg.tts_type == "freeswitch":
            yield self.send_text_as_speech(
                cfg.tts_fs_engine, cfg.tts_fs_voice, finalmessage)
        else:
            raise VoiceError("Unknown tts_type %r" % (
                cfg.tts_type,))

    def get_address(self):
        return self.uniquecallid

    def output_message(self, text):
        return self.stream_text_as_speech(text)

    def output_stream(self, url):
        return self.playback(url)

    def set_input_type(self, input_type):
        self.input_type = input_type

    def close_call(self):
        self.request_hang_up = True

    def onChannelExecuteComplete(self, ev):
        log.msg("execute complete " + ev.variable_call_uuid)
        if self.request_hang_up:
            return self.hangup()

    def onChannelHangupComplete(self, ev):
        log.msg("Channel HangUp")
        try:
            answered_time = int(ev.get('Caller_Channel_Answered_Time'))
            hangup_time = int(ev.get('Caller_Channel_Hangup_Time'))
            duration = hangup_time - answered_time
        except (TypeError, ValueError):
            log.warning(
                "Unable to get call duration for %r" % self.get_address())
            duration = None
        self.vumi_transport.deregister_client(self, duration)

    def onDisconnect(self, ev):
        log.msg("Channel disconnect received")
        self.vumi_transport.deregister_client(self)

    def unboundEvent(self, evdata, evname):
        log.msg("Unbound event %r" % (evname,))


class FreeSwitchESLFactory(ServerFactory):
    """ FreeSwitch ESL server factory. """
    def __init__(self, vumi_transport):
        self.vumi_transport = vumi_transport

    def protocol(self):
        return FreeSwitchESLProtocol(self.vumi_transport)


class VoiceServerTransportConfig(Transport.CONFIG_CLASS):
    """
    Configuration parameters for the voice transport
    """

    to_addr = ConfigText(
        "The ``to_addr`` to use for inbound messages.",
        default="freeswitchvoice", static=True)

    tts_type = ConfigText(
        "Either 'freeswitch' or 'local' to specify where TTS is executed.",
        default="freeswitch", static=True)

    tts_fs_engine = ConfigText(
        "Specify Freeswitch TTS engine to use (only affects tts_type"
        " 'freeswitch').",
        default="flite", static=True)

    tts_fs_voice = ConfigText(
        "Specify Freeswitch TTS voice to use (only affects tts_type"
        " 'freeswitch').",
        default="kal", static=True)

    tts_local_command = ConfigText(
        "Specify command template to use for generating voice files (only"
        " affects tts_type 'local'). E.g. 'flite -o {filename} -t {text}'."
        " Command parameters are split on whitespace (no shell-like escape"
        " processing is performed on the command).",
        default=None, static=True)

    tts_local_cache = ConfigText(
        "Specify folder to cache voice files (only affects tts_type"
        " 'local').", default=".", static=True)

    tts_local_ext = ConfigText(
        "Specify the file extension used for cached voice files (only affects"
        " tts_type 'local').", default="wav", static=True)

    twisted_endpoint = ConfigServerEndpoint(
        "The endpoint the voice transport will listen on (and that Freeswitch"
        " will connect to).",
        required=True, default="tcp:port=8084", static=True)

    freeswitch_endpoint = ConfigClientEndpoint(
        "The endpoint the voice transport will send originate commands"
        "to (and that Freeswitch listens on).",
        default=None, static=True)

    freeswitch_auth = ConfigText(
        "Password for connecting to the Freeswitch endpoint."
        " None means no authentication credentials are offered.",
        default=None, static=True)

    originate_parameters = ConfigDict(
        "The parameters to pass to the originate command when initiating"
        " outbound calls. This dictionary of parameters is passed to the"
        " originate call template:\n\n"
        "  %(template)r\n\n"
        "All call parameters are required but the following defaults are"
        " supplied:\n\n"
        "  %(defaults)r" % {
            'template': OriginateFormatter.PROTO_TEMPLATE,
            'defaults': OriginateFormatter.DEFAULT_PARAMS,
        },
        default=None, static=True)

    @property
    def supports_outbound(self):
        return self.freeswitch_endpoint is not None

    def post_validate(self):
        super(VoiceServerTransportConfig, self).post_validate()
        required_outbound = (
            self.freeswitch_endpoint is not None,
            self.originate_parameters is not None)
        if self.supports_outbound and not all(required_outbound):
            raise ConfigError(
                "If any outbound message parameters are supplied"
                " (freeswitch_endpoint or originate_params), all must be"
                " given.")
        if self.originate_parameters is not None:
            try:
                OriginateFormatter(**self.originate_parameters)
            except OriginateMissingParameter as err:
                raise ConfigError(str(err))


class VoiceServerTransport(Transport):
    """
    Transport for Freeswitch Voice Service.

    Voice transports may receive additional hints for how to handle
    outbound messages the ``voice`` section of ``helper_metadata``.
    The ``voice`` section may contain the following keys:

    * ``speech_url``: An HTTP URL from which a custom sound file to
      use for this message. If absent or ``None`` a text-to-speech
      engine will be used to generate suitable sound to play.
      Sound formats supported are: ``.wav``, ``.ogg`` and ``.mp3``.
      The format will be determined by the ``Content-Type`` returned
      by the URL, or by the file extension if the ``Content-Type``
      header is absent. The preferred format is ``.ogg``.

    * ``wait_for``: Gather response characters until the given
      DTMF character is encountered. Commonly either ``#`` or ``*``.
      If absent or ``None``, an inbound message is sent as soon as
      a single DTMF character arrives.

      If no input is seen for some time (configurable in the
      transport config) the voice transport will timeout the wait
      and send the characters entered so far.

    Example ``helper_metadata``::

      "helper_metadata": {
          "voice": {
              "speech_url": "http://www.example.com/voice/ab34f611cdee.ogg",
              "wait_for": "#",
          },
      }
    """

    CONFIG_CLASS = VoiceServerTransportConfig

    @inlineCallbacks
    def setup_transport(self):
        self._clients = {}
        self._originated_calls = {}

        self.config = self.get_static_config()
        self._to_addr = self.config.to_addr
        self._transport_type = "voice"

        if self.config.supports_outbound:
            self.voice_client = FreeSwitchClient(
                self.config.freeswitch_endpoint, self.config.freeswitch_auth)
            self.originate_formatter = OriginateFormatter(
                **self.config.originate_parameters)
        else:
            self.voice_client = None
            self.originate_formatter = None

        self.voice_server = yield self.config.twisted_endpoint.listen(
            FreeSwitchESLFactory(self))

    @inlineCallbacks
    def teardown_transport(self):
        if hasattr(self, 'voice_server'):
            # We need to wait for all the client connections to be closed (and
            # their deregistration messages sent) before tearing down the rest
            # of the transport.
            log.info("Shutting down %d clients." % len(self._clients))
            self.voice_server.loseConnection()
            yield gatherResults([
                client.registration_d for client in self._clients.values()])

    @inlineCallbacks
    def register_client(self, client):
        # We add our own Deferred to the client here because we only want to
        # fire it after we're finished with our own deregistration process.
        client.registration_d = Deferred()
        client_addr = client.get_address()
        log.info("Registering client connected from %r" % (client_addr,))
        self._clients[client_addr] = client
        originated_msg = self._originated_calls.pop(client_addr, None)
        if originated_msg is not None:
            yield self.send_outbound_message(client, originated_msg)
        else:
            self.send_inbound_message(
                client, None, TransportUserMessage.SESSION_NEW)
        log.info("Registration complete.")

    def deregister_client(self, client, duration=None):
        client_addr = client.get_address()
        if client_addr not in self._clients:
            return
        log.info("Deregistering client connected from %r" % (client_addr,))
        del self._clients[client_addr]
        self.send_inbound_message(
            client, None, TransportUserMessage.SESSION_CLOSE, duration)
        client.registration_d.callback(None)
        log.info("Deregistration complete.")

    def handle_input(self, client, text):
        self.send_inbound_message(
            client, text, TransportUserMessage.SESSION_RESUME)

    def send_inbound_message(self, client, text, session_event, duration=None):
        helper_metadata = {}
        if duration:
            if not helper_metadata.get('voice'):
                helper_metadata['voice'] = voice = {}
            voice['call_duration'] = duration

        self.publish_message(
            from_addr=client.get_address(),
            to_addr=self._to_addr,
            session_event=session_event,
            content=text,
            transport_name=self.transport_name,
            transport_type=self._transport_type,
            helper_metadata=helper_metadata,
        )

    @inlineCallbacks
    def send_outbound_message(self, client, message):
        content = message['content']
        if content is None:
            content = u''
        content = u"\n".join(content.splitlines())
        content = content.encode('utf-8')

        overrideURL = None
        client.set_input_type(None)
        if 'helper_metadata' in message:
            meta = message['helper_metadata']
            if 'voice' in meta:
                voicemeta = meta['voice']
                client.set_input_type(voicemeta.get('wait_for', None))
                overrideURL = voicemeta.get('speech_url', None)

        if overrideURL is None:
            yield client.output_message("%s\n" % content)
        elif isinstance(overrideURL, basestring):
            yield client.output_stream(overrideURL)
        elif isinstance(overrideURL, list):
            for url in overrideURL:
                if isinstance(url, basestring):
                    yield client.output_stream(url)
                else:
                    log.warning("Invalid URL %r" % url)
        else:
            log.warning("Invalid URL %r" % overrideURL)


        if message['session_event'] == TransportUserMessage.SESSION_CLOSE:
            client.close_call()

        yield self.publish_ack(message["message_id"], message["message_id"])

    @inlineCallbacks
    def dial_outbound(self, to_addr):
        reply = yield self.voice_client.api(
            self.originate_formatter.format_call(self._to_addr, to_addr))
        call_uuid = reply.args[1]
        returnValue(call_uuid)

    @inlineCallbacks
    def handle_outbound_message(self, message):

        client_addr = message['to_addr']
        client = self._clients.get(client_addr)

        if (self.config.supports_outbound and
            client is None and
            message.get('session_event') ==
                TransportUserMessage.SESSION_NEW):
            try:
                call_uuid = yield self.dial_outbound(client_addr)
            except FreeSwitchClientError as e:
                log.msg("Error connecting to client %r: %s" % (
                    client_addr, e))
                yield self.publish_nack(
                    message["message_id"],
                    "Could not make call to client %r" % (client_addr,))
            else:
                self._originated_calls[call_uuid] = message
            return

        if client is None:
            yield self.publish_nack(
                message["message_id"],
                "Client %r no longer connected" % (client_addr,))
            return

        yield self.send_outbound_message(client, message)
