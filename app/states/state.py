import reflex as rx
from typing import TypedDict
import httpx
import os
import logging


class NavItem(TypedDict):
    label: str
    icon: str
    href: str


class Message(TypedDict):
    role: str
    content: str


BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
WEBSOCKET_URL = os.getenv("WEBSOCKET_URL", "ws://localhost:8000/ws/audio")


class State(rx.State):
    """The base state for the app."""

    nav_items: list[NavItem] = [
        {"label": "System health check", "icon": "activity", "href": "#"},
        {"label": "Logout", "icon": "log-out", "href": "#"},
    ]
    is_recording: bool = False
    is_processing: bool = False
    chat_history: list[Message] = []

    @rx.event
    def start_recording(self):
        """Start the audio recording."""
        self.is_recording = True
        self.is_processing = False
        return rx.call_script(f"startRecording('{WEBSOCKET_URL}')")

    @rx.event
    def stop_recording(self):
        """Stop the audio recording and start processing."""
        self.is_recording = False
        self.is_processing = True
        self.chat_history.append({"role": "user", "content": "..."})
        return rx.call_script("stopRecording()")

    @rx.event
    def add_transcription(self, transcribed_text: str):
        """Add the transcribed text to the chat history as a user message."""
        if self.chat_history and self.chat_history[-1]["content"] == "...":
            self.chat_history[-1]["content"] = transcribed_text
        else:
            self.chat_history.append({"role": "user", "content": transcribed_text})
        yield State.add_assistant_response(
            "I received your message. I am still learning to respond."
        )

    @rx.event
    def add_assistant_response(self, response: str):
        """Add the assistant's response to the chat history."""
        if self.chat_history and self.chat_history[-1]["role"] == "user":
            self.chat_history.append({"role": "assistant", "content": ""})
        if self.chat_history and self.chat_history[-1]["role"] == "assistant":
            self.chat_history[-1]["content"] += response
        self.is_processing = False

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        """Handle PDF uploads."""
        if not files:
            return rx.toast.error("No file selected.")
        file = files[0]
        upload_data = await file.read()
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{BACKEND_URL}/process_doc",
                    files={"file": (file.filename, upload_data, file.content_type)},
                )
                response.raise_for_status()
                self.chat_history.append(
                    {
                        "role": "assistant",
                        "content": f"Successfully uploaded and processed {file.filename}.",
                    }
                )
                return rx.clear_selected_files("pdf-upload")
        except httpx.RequestError as e:
            logging.exception(f"Error uploading file: {e}")
            self.chat_history.append(
                {
                    "role": "assistant",
                    "content": f"Error uploading {file.filename}: {e}",
                }
            )
            return rx.toast.error(f"Upload failed: {e}")