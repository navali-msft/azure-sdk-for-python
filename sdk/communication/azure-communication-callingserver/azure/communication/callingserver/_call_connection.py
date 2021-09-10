# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from typing import TYPE_CHECKING, Any

from azure.core.tracing.decorator import distributed_trace
from ._shared.models import CommunicationIdentifier
from ._generated.models import (
    RemoveParticipantByIdRequest,
    TransferCallRequest,
    GetParticipantByIdRequest,
    StartHoldMusicResult,
    StopHoldMusicResult,
    StartHoldMusicRequest,
    PlayAudioRequest,
    PlayAudioResult
)
from ._models import (
    CallConnectionProperties,
    CallParticipant
)
from ._generated.aio.operations import CallConnectionsOperations
from ._communication_identifier_serializer import serialize_identifier

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from typing import Any, List, Optional
    
class CallConnection(object):
    def __init__(
        self,
        call_connection_id: str,  # type: str
        call_connection_client: CallConnectionsOperations,  # type: AsyncTokenCredential
        **kwargs  # type: Any
    ):
        # type: (...) -> None
        self.call_connection_id = call_connection_id
        self.call_connection_client = call_connection_client

    @distributed_trace()
    def hang_up(
        self,
        **kwargs: Any
    ):
        # type: (...) -> None

        return self.call_connection_client.hangup_call(
            call_connection_id=self.call_connection_id,
            **kwargs
        )

    @distributed_trace
    def remove_participant_by_id(
        self,
        participant,  # type: CommunicationIdentifier
        **kwargs: Any
    ):
        #type: (...) -> None
        """Remove a participant from the call using CommunicationIdentifier

        :param participant: The identity of participant to be removed from the call.
        :type participant: CommunicationIdentifier.
        :return: None
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """

        if not participant:
            raise ValueError("participant cannot be None.")

        removeParticipantByIdRequest=RemoveParticipantByIdRequest(identifier=serialize_identifier(participant))
        return self.call_connection_client.remove_participant_by_id(
            call_connection_id=self.call_connection_id,
            remove_participant_by_id_request=removeParticipantByIdRequest,
            **kwargs
        )

    @distributed_trace
    def transfer_to_participant(
        self,
        target_participant,  # type: CommunicationIdentifier
        user_to_user_information=None, # type: Optional[str]
        **kwargs: Any
    ):
        #type: (...) -> None
        """Transfer the call to a participant.

        :param target_participant: The target participant.
        :type target_participant: CommunicationIdentifier.
        :param user_to_user_information: The user to user information payload.
        :type user_to_user_information: str.
        :return: None
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """

        if not target_participant:
            raise ValueError("target_participant cannot be None.")

        transferCallRequest=TransferCallRequest(
            target_participant=serialize_identifier(target_participant), 
            user_to_user_information=user_to_user_information)
        return self.call_connection_client.transfer(
            call_connection_id=self.call_connection_id,
            transfer_call_request=transferCallRequest,
            **kwargs
        )

    @distributed_trace
    def get(
        self,
        **kwargs: Any
    ):
        # type: (...) -> CallConnectionProperties
        """Get call connection properties.

        :return: CallConnectionProperties
        :rtype: ~azure.communication.callingServer.CallConnectionProperties
        :raises: ~azure.core.exceptions.HttpResponseError
        """

        call_connection_properties = self.call_connection_client.get_call(call_connection_id=self.call_connection_id, **kwargs)
        return CallConnectionProperties._from_generated(call_connection_properties)  # pylint:disable=protected-access

    @distributed_trace
    def get_participants(
        self,
        **kwargs: Any
    ):
        # type: (...) -> List[CallParticipant]
        """Get participants of the call.

        :return: List[CallParticipant]
        :rtype: List[~azure.communication.callingserver.CallParticipant]
        :raises: ~azure.core.exceptions.HttpResponseError
        """

        call_participants = self.call_connection_client.get_participants(call_connection_id=self.call_connection_id, **kwargs)
        return [
                CallParticipant._from_generated(call_participant) for call_participant in  # pylint:disable=protected-access
                call_participants
            ]

    @distributed_trace
    def get_participant(
        self,
        participant_id, # type: str
        **kwargs: Any
    ):
        # type: (...) -> CallParticipant
        """Get participant of the call using participant id.

        :param participant_id: The participant id.
        :type participant_id: str.
        :return: CallParticipant
        :rtype: ~azure.communication.callingserver.CallParticipant
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """

        if not participant_id:
            raise ValueError("participant_id cannot be None.")

        call_participant = self.call_connection_client.get_participant(
            call_connection_id=self.call_connection_id, 
            participant_id=participant_id,

             **kwargs)
        return CallParticipant._from_generated(call_participant)

    @distributed_trace
    def get_participant_by_id(
        self,
        participant,  # type: CommunicationIdentifier
        **kwargs: Any
    ):
        # type: (...) -> List[CallParticipant]
        """Get participants of the call using identifier

        :param participant: The identifier of the participant.
        :type participant: CommunicationIdentifier.
        :return: List[CallParticipant]
        :rtype: List[~azure.communication.callingserver.CallParticipant]
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """

        call_participants = self.call_connection_client.get_participant_by_id(
            call_connection_id=self.call_connection_id, 
            get_participant_by_id_request=GetParticipantByIdRequest(identifier=serialize_identifier(participant))
            **kwargs)

        return [
                CallParticipant._from_generated(call_participant) for call_participant in  # pylint:disable=protected-access
                call_participants
            ]

    @distributed_trace
    def start_hold_music(
        self,
        participant_id, # type: str
        audio_file_uri, # type: str
        audio_file_id, # type: str
        callback_uri, # type: str
        **kwargs: Any
    ):
        # type: (...) -> StartHoldMusicResult
        """Hold the participant and play the custom music.

        :param participant_id: The participant id.
        :type participant_id: str.
        :param audio_file_uri: The uri of the audio file.
        :type audio_file_uri: str.
        :param audio_file_id: Tne id for the media in the AudioFileUri, using which we cache the media resource.
        :type audio_file_id: str.
        :param callback_uri: The callback Uri to receive PlayAudio status notifications.
        :type callback_uri: str.
        :return: StartHoldMusicResult
        :rtype: ~azure.communication.callingserver.models.StartHoldMusicResult
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """

        if not participant_id:
            raise ValueError("participant_id cannot be None.")

        return self.call_connection_client.start_hold_music(
            call_connection_id=self.call_connection_id, 
            participant_id=participant_id,
            request=StartHoldMusicRequest(audio_file_uri=audio_file_uri, audio_file_id=audio_file_id, callback_uri=callback_uri)
             **kwargs)

    @distributed_trace
    def start_hold_music(
        self,
        participant_id, # type: str
        **kwargs: Any
    ):
        # type: (...) -> StartHoldMusicResult
        """Hold the participant and play default music.

        :return: StartHoldMusicResult
        :rtype: ~azure.communication.callingserver.models.StartHoldMusicResult
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """

        audio_file_uri = kwargs.pop('audio_file_uri', None)
        audio_file_id = kwargs.pop('audio_file_id', None)
        callback_uri = kwargs.pop('callback_uri', None)

        if not participant_id:
            raise ValueError("participant_id cannot be None.")

        return self.call_connection_client.start_hold_music(
            call_connection_id=self.call_connection_id, 
            participant_id=participant_id,
            request=StartHoldMusicRequest(audio_file_uri=audio_file_uri, audio_file_id=audio_file_id, callback_uri=callback_uri)
             **kwargs)

    @distributed_trace
    def stop_hold_music(
        self,
        participant_id, # type: str
        **kwargs: Any
    ):
        # type: (...) -> StopHoldMusicResult
        """Remove participant from the hold and stop playing audio.

        :return: StopHoldMusicResult
        :rtype: ~azure.communication.callingserver.models.StopHoldMusicResult
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """

        if not participant_id:
            raise ValueError("participant_id cannot be None.")

        return self.call_connection_client.stop_hold_music(
            call_connection_id=self.call_connection_id, 
            participant_id=participant_id,
             **kwargs)

    def play_audio_to_participant(
        self,
        participant_id, # type: str
        audio_file_uri, # type: str
        loop, # type: bool
        audio_file_id, # type: str
        callback_uri, # type: str
        operation_context, # type: str
        **kwargs: Any
    ):
        # type: (...) -> PlayAudioResult
        """Play audio to a participant.

        :param participant_id: The participant id.
        :type participant_id: str.
        :param audio_file_uri: The uri of the audio file.
        :type audio_file_uri: str.
        :param loop: The flag indicating whether audio file needs to be played in loop or not.
        :type loop: bool.
        :param audio_file_id: Tne id for the media in the AudioFileUri, using which we cache the media resource.
        :type audio_file_id: str.
        :param callback_uri: The callback Uri to receive PlayAudio status notifications.
        :type callback_uri: str.
        :param operation_context: The operation context.
        :type operation_context: str.
        :return: PlayAudioResult
        :rtype: ~azure.communication.callingserver.models.PlayAudioResult
        :raises: ~azure.core.exceptions.HttpResponseError, ValueError
        """

        if not participant_id:
            raise ValueError("participant_id cannot be None.")

        return self.call_connection_client.participant_play_audio(
            call_connection_id=self.call_connection_id, 
            participant_id=participant_id,
            request=PlayAudioRequest(
                audio_file_uri=audio_file_uri, 
                loop=loop, 
                audio_file_id=audio_file_id, 
                callback_uri=callback_uri, operation_context=operation_context),
             **kwargs)

    @distributed_trace()
    def keep_alive(
        self,
        **kwargs: Any
    ):
        # type: (...) -> None
        """Keep call connection alive.

        :return: None
        :rtype: None
        :raises: ~azure.core.exceptions.HttpResponseError
        """
        return self.call_connection_client.keep_alive(
            call_connection_id=self.call_connection_id,
            **kwargs
        )

    def close(self):
        # type: () -> None
        self.call_connection_client.close()

    def __enter__(self):
        # type: () -> CallConnection
        self.call_connection_client.__enter__()  # pylint:disable=no-member
        return self

    def __exit__(self, *args):
        # type: (*Any) -> None
        self.call_connection_client.__exit__(*args)  # pylint:disable=no-member
