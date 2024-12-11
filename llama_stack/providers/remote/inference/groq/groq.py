from typing import AsyncIterator, List, Optional, Union, AsyncGenerator
from llama_models.llama3.api.datatypes import (
    InterleavedTextMedia,
    Message,
    ToolChoice,
    ToolDefinition,
    ToolPromptFormat,
)
from llama_models.datatypes import SamplingParams
from llama_stack.apis.inference import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionResponseEvent,
    ChatCompletionResponseStreamChunk,
    ChatCompletionResponseEventType,
    CompletionResponse,
    CompletionMessage,
    CompletionResponseStreamChunk,
    EmbeddingsResponse,
    Inference,
    LogProbConfig,
    ResponseFormat,
)
from llama_stack.providers.utils.inference.model_registry import (
    build_model_alias,
    ModelRegistryHelper,
)
from llama_stack.providers.remote.inference.groq.config import GroqConfig
from llama_models.sku_list import CoreModelId
from llama_models.llama3.api.datatypes import StopReason
from groq import Groq

_MODEL_ALIASES = [
    build_model_alias(
        "llama3-8b-8192",
        CoreModelId.llama3_2_3b_instruct.value,
    ),
]

class GroqInferenceAdapter(Inference, ModelRegistryHelper):
    client: Groq
    def __init__(self, config: GroqConfig) -> None:
        ModelRegistryHelper.__init__(self, model_aliases=_MODEL_ALIASES)
        self.client = Groq(api_key=config.api_key)

    def completion(
        self,
        model_id: str,
        content: InterleavedTextMedia,
        sampling_params: Optional[SamplingParams] = SamplingParams(),
        response_format: Optional[ResponseFormat] = None,
        stream: Optional[bool] = False,
        logprobs: Optional[LogProbConfig] = None,
    ) -> Union[CompletionResponse, AsyncIterator[CompletionResponseStreamChunk]]:
        raise NotImplementedError()

    async def embeddings(
        self,
        model_id: str,
        contents: List[InterleavedTextMedia],
    ) -> EmbeddingsResponse:
        raise NotImplementedError()

    async def chat_completion(
        self,
        model_id: str,
        messages: List[Message],
        sampling_params: Optional[SamplingParams] = SamplingParams(),
        response_format: Optional[ResponseFormat] = None,
        tools: Optional[List[ToolDefinition]] = None,
        tool_choice: Optional[ToolChoice] = ToolChoice.auto,
        tool_prompt_format: Optional[
            ToolPromptFormat
        ] = None,  # API default is ToolPromptFormat.json, we default to None to detect user input
        stream: Optional[bool] = False,
        logprobs: Optional[LogProbConfig] = None,
    ) -> Union[
        ChatCompletionResponse, AsyncGenerator
    ]:
        if stream:
            response = self.client.chat.completions.create(
                model=self.get_provider_model_id(model_id),
                messages=messages,
                stream=True,
            )
            async def stream_response():
                for chunk in response:
                    # TODO(aidand): Is this 
                    if chunk.choices[0].delta.content == None:
                        yield ChatCompletionResponseStreamChunk(
                            event=ChatCompletionResponseEvent(
                                event_type=ChatCompletionResponseEventType.complete,
                                delta=chunk.choices[0].delta.content,
                            )
                        )
                        return
                    yield ChatCompletionResponseStreamChunk(
                        event=ChatCompletionResponseEvent(
                        event_type=ChatCompletionResponseEventType.progress,
                        delta=chunk.choices[0].delta.content,
                    )
                )
            return stream_response()

        print(self.get_provider_model_id(model_id))
        response = self.client.chat.completions.create(
            model=self.get_provider_model_id(model_id),
            messages=messages,
        )
        return ChatCompletionResponse(
            completion_message=CompletionMessage(
                content=response.choices[0].message.content,
                stop_reason=StopReason.end_of_turn,
            ),
            logprobs=None,
        )
        # async def generate_alphabet():
        #     for letter in 'abcdefghijklmnopqrstuvwxyz':
        #         await asyncio.sleep(1)
        #         if letter == 'a':
        #             event_type = ChatCompletionResponseEventType.start
        #         elif letter == 'z':
        #             event_type = ChatCompletionResponseEventType.complete
        #         else:
        #             event_type = ChatCompletionResponseEventType.progress
        #         yield ChatCompletionResponseStreamChunk(
        #             event=ChatCompletionResponseEvent(
        #                 event_type=event_type,
        #                 delta=letter,
        #                 stop_reason=StopReason.end_of_turn if letter == 'z' else None
        #             )
        #         )
        # return generate_alphabet()