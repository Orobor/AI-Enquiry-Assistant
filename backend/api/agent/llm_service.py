import os, multiprocessing

from typing import List, Optional

from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    BaseMessage,
)

from langchain_community.chat_models import ChatLlamaCpp
from langchain_openai import ChatOpenAI

from decouple import config

class LLMService:
    """
    Service responsible for LLM initialisation,
    message construction, and response generation.
    """

    def __init__(
        self,
        model_path=None,
        temperature=None,
        max_tokens=None,
        n_ctx=None,
        n_gpu_layers=None,
        verbose=None,
    ):

        # Load configuration
        
        self.model_path = (
            model_path or config("MODEL_PATH")
        )

        self.temperature = (
            temperature if temperature is not None
            else config("LLM_TEMPERATURE", cast=float, default=0.2)
        )

        self.max_tokens = (
            max_tokens if max_tokens is not None
            else config("LLM_MAX_TOKENS", cast=int, default=2048)
        )

        self.n_ctx = (
            n_ctx if n_ctx is not None
            else config("LLM_N_CTX", cast=int, default=4096)
        )

        self.n_gpu_layers = (
            n_gpu_layers if n_gpu_layers is not None
            else config("LLM_N_GPU_LAYERS", cast=int, default=0)
        )

        self.verbose = (
            verbose if verbose is not None
            else config("LLM_VERBOSE", cast=bool, default=False)
        )

        # Initialize LLM 

        # self.llm = ChatLlamaCpp(
        #     model_path=self.model_path,
        #     temperature=self.temperature,
        #     max_tokens=self.max_tokens,
        #     n_ctx=self.n_ctx,
        #     n_gpu_layers=self.n_gpu_layers,
        #     verbose=self.verbose,
        # )

        self.llm = ChatOpenAI(
            model="gpt-4.1",
            temperature=0.1,
            max_tokens=512,
            api_key=config("API_KEY"),
        )

    # ---------------------
    # Build message
    # ---------------------

    def build_messages(self, system_prompt: str, question: str, context: Optional[List[str]] = None) -> List[BaseMessage]:
        """
        Construct messages for the LLM.

        Args:
            system_prompt: Instructions for the LLM.
            question: User question.
            context: Retrieved reference documents.

        Returns:
            List of LangChain messages.
        """

        context_text = "\n\n".join(context or [])

        human_message = f"""
            Retrieved reference material:

            {context_text}

            User question:

            {question}

            Provide a clear and relevant answer using the
            retrieved reference material.
        """

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=human_message),
        ]

        return messages

    # ---------------------
    # Generate response
    # ---------------------

    def generate(self, messages: List[BaseMessage]) -> str:
        """
        Invoke the LLM and return its response.
        """

        response = self.llm.invoke(messages)

        content = response.content

        if not isinstance(content, str):
            content = str(content)

        return content

    # ---------------------
    # Generate answer
    # ---------------------

    def generate_answer(self, system_prompt: str, question: str, context: Optional[List[str]] = None) -> str:
        """
        Build messages and generate an answer.

        This is the main public generation method used by AgentWorkflow.
        """

        messages = self.build_messages(
            system_prompt=system_prompt,
            question=question,
            context=context,
        )

        return self.generate(messages)
