import reflex as rx
from app.states.state import State, Message
from app.components.sidebar import sidebar


def user_message(message: Message) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.text(message["content"], class_name="text-white"),
            class_name="rounded-xl bg-violet-600 p-3 max-w-lg",
        ),
        class_name="flex justify-end my-4",
    )


def assistant_message(message: Message) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.text(message["content"], class_name="text-gray-300"),
            class_name="rounded-xl bg-[#252a41] p-3 max-w-lg",
        ),
        class_name="flex justify-start my-4",
    )


def chat_message(message: Message) -> rx.Component:
    return rx.cond(
        message["role"] == "user", user_message(message), assistant_message(message)
    )


def main_content() -> rx.Component:
    """The main content area of the app."""
    return rx.el.div(
        rx.el.header(
            rx.el.h1(
                "Board meetings AI Assistant",
                class_name="text-2xl font-semibold text-white",
            ),
            class_name="bg-[#1a1d2e] p-6 sticky top-0 z-10 border-b border-gray-800",
        ),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.foreach(State.chat_history, chat_message),
                    id="chat-container",
                    class_name="flex-1 overflow-y-auto p-6",
                ),
                class_name="flex flex-col flex-1 h-full",
            ),
            class_name="flex-1 flex flex-col h-[calc(100vh-89px)]",
        ),
        class_name="flex flex-col flex-1",
    )


def index() -> rx.Component:
    return rx.el.div(
        sidebar(),
        main_content(),
        class_name="flex min-h-screen w-full bg-[#1a1d2e] font-['Inter']",
    )


app = rx.App(
    theme=rx.theme(appearance="light", accent_color="violet"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
        rx.el.script(src="/js/audio.js"),
    ],
)
app.add_page(index, route="/")