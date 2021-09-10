# coding=utf-8
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

from ._generated.models import EventSubscriptionType, MediaType
from ._shared.models import PhoneNumberIdentifier
from ._communication_identifier_serializer import serialize_identifier, deserialize_identifier

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse # type: ignore

from typing import Any


class CreateCallOptions(object):

    def __init__(
        self,
        *,
        callback_uri: str,
        requested_media_types: MediaType,
        requested_call_events: EventSubscriptionType,
    ):
        try:
            if not callback_uri.lower().startswith('http'):
                callback_uri = "https://" + callback_uri
        except AttributeError:
            raise ValueError("Host URL must be a string")

        parsed_url = urlparse(callback_uri.rstrip('/'))
        if not parsed_url.netloc:
            raise ValueError("Invalid URL: {}".format(callback_uri))

        if not requested_media_types:
            raise ValueError("requestedMediaTypes can not be None or empty")

        if not requested_call_events:
            raise ValueError("requestedCallEvents can not be None or empty")

        self.callback_uri = callback_uri
        self.requested_media_types = requested_media_types
        self.requested_call_events = requested_call_events
        self.subject = None

    @property
    def alternate_Caller_Id(self):
        return self._alternate_Caller_Id
    @alternate_Caller_Id.setter
    def alternate_Caller_Id(self, value: PhoneNumberIdentifier):
        self._alternate_Caller_Id = value

    @property
    def subject(self):
        return self._subject
    @subject.setter
    def subject(self, value: str):
        self._subject = value

class JoinCallOptions(object):

    def __init__(
        self,
        *,
        callback_uri: str,
        requested_media_types: MediaType,
        requested_call_events: EventSubscriptionType,
    ):
        try:
            if not callback_uri.lower().startswith('http'):
                callback_uri = "https://" + callback_uri
        except AttributeError:
            raise ValueError("Host URL must be a string")

        parsed_url = urlparse(callback_uri.rstrip('/'))
        if not parsed_url.netloc:
            raise ValueError("Invalid URL: {}".format(callback_uri))

        if not requested_media_types:
            raise ValueError("requestedMediaTypes can not be None or empty")

        if not requested_call_events:
            raise ValueError("requestedCallEvents can not be None or empty")

        self._callback_uri = callback_uri
        self._requested_media_types = requested_media_types
        self._requested_call_events = requested_call_events

    @property
    def subject(self):
        return self._subject
    @subject.setter
    def subject(self, value: str):
        self._subject = value

class PlayAudioResult(object):

    def __init__(
        self,
        **kwargs # type: Any
    ):
        # type: (...) -> None
        self.operation_id = kwargs['operation_id']
        self.status = kwargs['status']
        self.operation_context = kwargs['operation_context']
        self.result_info = kwargs['result_info']

    @classmethod
    def _from_generated(cls, play_audio_result):
        if play_audio_result is None:
            return None

        return cls(
            operation_id=play_audio_result.operation_id,
            status=play_audio_result.status,
            operation_context=play_audio_result.operation_context,
            result_info=ResultInfo._from_generated(play_audio_result.result_info)
        )

class ResultInfo(object):
    def __init__(
        self,
        **kwargs # type: Any
    ):
        # type: (...) -> None
        self.code = kwargs['code']
        self.subcode = kwargs['subcode']
        self.message = kwargs['message']

    @classmethod
    def _from_generated(cls, result_info):
        if result_info is None:
            return None

        return cls(
            code=result_info.code,
            subcode=result_info.subcode,
            message=result_info.message,
        )

class CallConnectionProperties(object):
    """The call connection properties.

    :ivar call_connection_id: The call connection id.
    :type call_connection_id: str
    :ivar source: The source of the call.
    :type source: ~azure.communication.CommunicationIdentifier
    :ivar alternate_caller_id: The alternate identity of the source of the call if dialing out to
     a pstn number.
    :type alternate_caller_id: ~azure.communication.PhoneNumberIdentifier
    :ivar targets: The targets of the call.
    :type targets: list[~azure.communication.CommunicationIdentifier]
    :ivar call_connection_state: The state of the call connection. Possible values include:
     "connecting", "connected", "transferring", "transferAccepted", "disconnecting", "disconnected".
    :type call_connection_state: str or
     ~azure.communication.callingserver.models.CallConnectionState
    :ivar subject: The subject.
    :type subject: str
    :ivar callback_uri: The callback URI.
    :type callback_uri: str
    :ivar requested_media_types: The requested modalities.
    :type requested_media_types: list[str or ~azure.communication.callingserver.models.MediaType]
    :ivar requested_call_events: The requested call events to subscribe to.
    :type requested_call_events: list[str or
     ~azure.communication.callingserver.models.EventSubscriptionType]
    :ivar server_call_id: The server call id.
    :type server_call_id: str
    """

    # pylint:disable=protected-access

    def __init__(
        self,
        **kwargs # type: Any
    ):
        # type: (...) -> None
        self.call_connection_id = kwargs.get('call_connection_id', None)
        self.source = kwargs.get('source', None)
        self.alternate_caller_id = kwargs.get('alternate_caller_id', None)
        self.targets = kwargs.get('targets', None)
        self.call_connection_state = kwargs.get('call_connection_state', None)
        self.subject = kwargs.get('subject', None)
        self.callback_uri = kwargs.get('callback_uri', None)
        self.requested_media_types = kwargs.get('requested_media_types', None)
        self.requested_call_events = kwargs.get('requested_call_events', None)
        self.server_call_id = kwargs.get('server_call_id', None)

    @classmethod
    def _from_generated(cls, call_connection_properties):

        if call_connection_properties is None:
            return None

        targets = call_connection_properties.targets
        if targets is not None and len(targets) > 0:
            target_participants = [
                deserialize_identifier(participant) for participant in  # pylint:disable=protected-access
                targets
            ]
        else:
            target_participants = []

        alternate_caller_id = call_connection_properties.alternate_caller_id
        if alternate_caller_id is not None:
            alternate_caller_id = PhoneNumberIdentifier(alternate_caller_id.value)
        else:
            alternate_caller_id = None

        return cls(
            call_connection_id=call_connection_properties.call_connection_id,
            source=deserialize_identifier(call_connection_properties.source),
            targets=target_participants,
            alternate_caller_id=alternate_caller_id,
            call_connection_state=call_connection_properties.call_connection_state,
            subject=call_connection_properties.subject,
            callback_uri=call_connection_properties.callback_uri,
            requested_media_types=call_connection_properties.requested_media_types,
            requested_call_events=call_connection_properties.requested_call_events,
            server_call_id=call_connection_properties.server_call_id
        )

class CallParticipant(object):
    """A participant in a call.

    :ivar identifier: Required. Communication identifier of the participant.
    :type identifier: ~azure.communication.callingserver.models.CommunicationIdentifierModel
    :ivar participant_id: Participant id.
    :type participant_id: str
    :ivar is_muted: Required. Is participant muted.
    :type is_muted: bool
    """

    def __init__(
        self,
        **kwargs
    ):
        self.identifier = kwargs['identifier']
        self.participant_id = kwargs.get('participant_id', None)
        self.is_muted = kwargs['is_muted']

    @classmethod
    def _from_generated(cls, call_participant):

        if call_participant is None:
            return None

        return cls(
            identifier=deserialize_identifier(call_participant.identifier),
            participant_id=call_participant.participant_id,
            is_muted=call_participant.is_muted
        )