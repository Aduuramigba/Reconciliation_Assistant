from dotenv import load_dotenv
import logging
import asyncio

from livekit import agents
from livekit.agents import AgentSession, Agent, RoomInputOptions
from livekit.plugins import openai, silero
from livekit.agents.metrics import LLMMetrics, STTMetrics, TTSMetrics, EOUMetrics
from livekit.agents import function_tool

from prompt import WELCOME_MESSAGE, INSTRUCTIONS
from my_tool import conversation_chain

logger = logging.getLogger("dlai-agent")
logger.setLevel(logging.INFO)

load_dotenv(override=True)

class Assistant(Agent):
    def __init__(self) -> None:
        stt = openai.STT(model="whisper-1")
        tts = openai.TTS(model="gpt-4o-mini-tts", voice="sage")
        llm = openai.LLM(model="gpt-4o-mini")
        vad = silero.VAD.load()

        # Initialize parent class with the query_documents tool
        super().__init__(
            instructions=INSTRUCTIONS,
            stt=stt,
            llm=llm,
            tts=tts,
            vad=vad,
            
        )

        # Metrics hooks
        llm.on("metrics_collected", lambda m: asyncio.create_task(self.on_llm_metrics_collected(m)))
        stt.on("metrics_collected", lambda m: asyncio.create_task(self.on_stt_metrics_collected(m)))
        stt.on("eou_metrics_collected", lambda m: asyncio.create_task(self.on_eou_metrics_collected(m)))
        tts.on("metrics_collected", lambda m: asyncio.create_task(self.on_tts_metrics_collected(m)))

    @function_tool()
    async def query_documents(self, user_input: str) -> str:
        """Query your Chroma + LangChain retrieval chain."""
        try:
            return conversation_chain.run(user_input)
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"

    # Metrics handlers
    async def on_llm_metrics_collected(self, metrics: LLMMetrics) -> None:
        print(f"[LLM] Prompt Tokens: {metrics.prompt_tokens}, Completion Tokens: {metrics.completion_tokens}")

    async def on_stt_metrics_collected(self, metrics: STTMetrics) -> None:
        print(f"[STT] Duration: {metrics.duration:.4f}s, Streamed: {'Yes' if metrics.streamed else 'No'}")

    async def on_eou_metrics_collected(self, metrics: EOUMetrics) -> None:
        print(f"[EOU] End of Utterance Delay: {metrics.end_of_utterance_delay:.4f}s")

    async def on_tts_metrics_collected(self, metrics: TTSMetrics) -> None:
        print(f"[TTS] Duration: {metrics.duration:.4f}s, Streamed: {'Yes' if metrics.streamed else 'No'}")


async def entrypoint(ctx: agents.JobContext):
    assistant = Assistant()
    session = AgentSession()

    await session.start(agent=assistant, room=ctx.room)
    await session.start(room=ctx.room, agent=assistant, room_input_options=RoomInputOptions())
    await session.generate_reply(instructions=WELCOME_MESSAGE)


if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))
