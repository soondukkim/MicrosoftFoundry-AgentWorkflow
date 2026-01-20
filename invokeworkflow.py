# Microsoft Foundry Workflow Invocation using Foundry SDK
# Before running: pip install --pre azure-ai-projects>=2.0.0b1
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import ResponseStreamEventType

# Project configuration
PROJECT_ENDPOINT = "<project_endpoint>"
WORKFLOW_NAME = "<workflow_name>"
WORKFLOW_VERSION = "1"  # 게시된 버전으로 업데이트

# Create AI Project client
project_client = AIProjectClient(
    endpoint=PROJECT_ENDPOINT,
    credential=DefaultAzureCredential(),
)

with project_client:
    workflow = {
        "name": WORKFLOW_NAME,
        "version": WORKFLOW_VERSION,
    }
    
    # Get OpenAI client from project
    openai_client = project_client.get_openai_client()

    # Create a conversation
    conversation = openai_client.conversations.create()
    print(f"Created conversation (id: {conversation.id})")

    # Call the workflow with streaming
    print(f"\nCalling workflow: {WORKFLOW_NAME}...\n")
    stream = openai_client.responses.create(
        conversation=conversation.id,
        extra_body={"agent": {"name": workflow["name"], "type": "agent_reference"}},
        input="제주도 2박 3일 여행 일정 짜줘",
        stream=True,
        metadata={"x-ms-debug-mode-enabled": "1"},
    )

    # Process streaming events
    for event in stream:
        if event.type == ResponseStreamEventType.RESPONSE_OUTPUT_TEXT_DONE:
            print("\t", event.text)
        elif event.type == ResponseStreamEventType.RESPONSE_OUTPUT_ITEM_ADDED and event.item.type == "workflow_action":
            print(f"\n{'='*60}")
            print(f"Actor - '{event.item.action_id}':")
            print(f"{'='*60}")
        elif event.type == ResponseStreamEventType.RESPONSE_OUTPUT_ITEM_DONE and event.item.type == "workflow_action":
            print(f"\n✓ Workflow Item '{event.item.action_id}' is '{event.item.status}'")
            print(f"  (previous item was: '{event.item.previous_action_id}')")
        elif event.type == ResponseStreamEventType.RESPONSE_OUTPUT_TEXT_DELTA:
            print(event.delta, end="", flush=True)

    # Clean up
    print("\n\n✅ Workflow completed!")
    openai_client.conversations.delete(conversation_id=conversation.id)
    print("Conversation deleted")