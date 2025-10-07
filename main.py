import os
import logging
from dotenv import load_dotenv
from livekit.agents import JobContext, WorkerOptions, cli, Agent, AgentSession
from livekit.plugins import deepgram, silero, openai, cartesia

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(".env")

# Verify keys are loaded
logger.info(f"GROQ_API_KEY loaded: {os.getenv('GROQ_API_KEY')[:20]}..." if os.getenv('GROQ_API_KEY') else "GROQ_API_KEY not found!")
logger.info(f"CARTESIA_API_KEY loaded: {os.getenv('CARTESIA_API_KEY')[:20]}..." if os.getenv('CARTESIA_API_KEY') else "CARTESIA_API_KEY not found!")


async def entrypoint(ctx: JobContext):
    """Entry point for the agent."""
    
    logger.info(f"🎯 Job request received for room: {ctx.job.room.name}")
    
    # Wait for the first participant to connect
    await ctx.connect()
    logger.info(f"✓ Room connected: {ctx.room.name}")
    logger.info(f"Participants in room: {len(ctx.room.remote_participants)}")
    
    # Wait for participant if none yet
    if len(ctx.room.remote_participants) == 0:
        logger.info("Waiting for participant to join...")
        participant = await ctx.wait_for_participant()
        logger.info(f"✓ Participant joined: {participant.identity}")
    
    try:
        # Create the agent session with plugins
        logger.info("Creating agent session...")
        session = AgentSession(
            vad=silero.VAD.load(),
            stt=deepgram.STT(model="nova-2"),
            llm=openai.LLM(
                model="llama-3.3-70b-versatile",
                base_url="https://api.groq.com/openai/v1",
                api_key=os.getenv("GROQ_API_KEY")
            ),
            tts=cartesia.TTS(
                model="sonic-english",
                voice="f786b574-daa5-4673-aa0c-cbe3e8534c02",
                api_key=os.getenv("CARTESIA_API_KEY")
            ),
        )
        logger.info("✓ Agent session created")
        
        # Create the agent with instructions
        agent = Agent(
            instructions="""You are a helpful and friendly voice assistant.
            Keep your responses concise and natural, as if having a conversation.
            Be warm and engaging. Keep responses under 3 sentences unless asked for more detail."""
        )
        logger.info("✓ Agent created")
        
        # Start the session
        logger.info("Starting agent session...")
        await session.start(room=ctx.room, agent=agent)
        logger.info(f"✓ Agent session started in room: {ctx.room.name}")
        
        # Generate initial greeting
        logger.info("Generating initial greeting...")
        await session.generate_reply(
            instructions="Greet the user warmly and briefly ask how you can help them today. Keep it under 2 sentences."
        )
        logger.info("✓ Initial greeting sent")
        
    except Exception as e:
        logger.error(f"❌ Error in agent entrypoint: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    # Run the agent worker
    logger.info("Starting LiveKit agent worker...")
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))