# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

from typing import TYPE_CHECKING, Any

from azure.core.tracing.decorator import distributed_trace
from ._generated.aio.operations import ServerCallsOperations
from ._shared.models import CommunicationIdentifier
from ._generated.models import (
    RemoveParticipantByIdRequest,
    GetParticipantByIdRequest,
    StartHoldMusicResult,
    StopHoldMusicResult,
    StartHoldMusicRequest,
    PlayAudioRequest,
    PlayAudioResult
)
from ._models import (
    CallParticipant
)
from ._communication_identifier_serializer import serialize_identifier

if TYPE_CHECKING:
    # pylint: disable=unused-import,ungrouped-imports
    from typing import Any, List, Optional
    
class ServerCall(object):

    def __init__(
        self,
        server_call_id: str,  # type: str
        server_call_client: ServerCallsOperations,  # type: AsyncTokenCredential
        **kwargs  # type: Any
    ):
        # type: (...) -> None
        self.server_call_id = server_call_id
        self.server_call_client = server_call_client

    @distributed_trace()
    def play_audio(
        self,
        audio_file_uri: str,
        audio_File_id: str,
        callback_uri: str,
        operation_context: str,
        **kwargs: Any
    ):
        # type: (...) -> PlayAudioResult
        try:
            if not audio_file_uri.lower().startswith('http'):
                audio_file_uri = "https://" + audio_file_uri
        except AttributeError:
            raise ValueError("URL must be a string.")

        if not audio_File_id:
            raise ValueError("audio_File_id can not be None")

        try:
            if not callback_uri.lower().startswith('http'):
                callback_uri = "https://" + callback_uri
        except AttributeError:
            raise ValueError("URL must be a string.")

        if not operation_context:
            raise ValueError("operation_context can not be None")

        request = PlayAudioRequest(
            audio_file_uri=audio_file_uri,
            loop = kwargs.get('loop', False),
            operation_context=operation_context,
            audio_file_id=audio_File_id,
            callback_uri=callback_uri
            **kwargs
        )

        play_audio_result = self.server_call_client.play_audio(
            server_call_id=self.server_call_id,
            request=request,
        )

        return PlayAudioResult._from_generated(play_audio_result)

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
        return self.server_call_client.remove_participant_by_id(
            server_call_id=self.server_call_id,
            remove_participant_by_id_request=removeParticipantByIdRequest,
            **kwargs
        )

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

        call_participants = self.server_call_client.get_participants(server_call_id=self.server_call_id, **kwargs)
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

        call_participant = self.server_call_client.get_participant(
            server_call_id=self.server_call_id, 
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

        call_participants = self.server_call_client.get_participant_by_id(
            server_call_id=self.server_call_id, 
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

        return self.server_call_client.start_hold_music(
            server_call_id=self.server_call_id, 
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

        return self.server_call_client.start_hold_music(
            server_call_id=self.server_call_id, 
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

        return self.server_call_client.stop_hold_music(
            server_call_id=self.server_call_id, 
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

        return self.server_call_client.participant_play_audio(
            server_call_id=self.server_call_id, 
            participant_id=participant_id,
            request=PlayAudioRequest(
                audio_file_uri=audio_file_uri, 
                loop=loop, 
                audio_file_id=audio_file_id, 
                callback_uri=callback_uri, operation_context=operation_context),
             **kwargs)

    def close(self):
        # type: () -> None
        self.server_call_client.close()

    def __enter__(self):
        # type: () -> ServerCall
        self.server_call_client.__enter__()  # pylint:disable=no-member
        return self

    def __exit__(self, *args):
        # type: (*Any) -> None
        self.server_call_client.__exit__(*args)  # pylint:disable=no-member
