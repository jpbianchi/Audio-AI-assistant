import reflex as rx
from app.states.state import State, Message
from app.components.sidebar import sidebar


# def recording_indicator() -> rx.Component:
#     return rx.el.div(
#         rx.el.div(class_name="h-2.5 w-2.5 rounded-full bg-current"),
#         class_name="flex items-center justify-center text-red-500 animate-pulse",
#     )


# def microphone_button() -> rx.Component:
#     return rx.el.button(
#         rx.cond(
#             State.is_recording,
#             recording_indicator(),
#             rx.icon("mic", class_name="h-6 w-6"),
#         ),
#         on_click=rx.cond(
#             State.is_recording, State.stop_recording, State.start_recording
#         ),
#         disabled=State.is_processing,
#         class_name="flex items-center justify-center h-14 w-14 rounded-full bg-violet-600 text-white hover:bg-violet-700 disabled:bg-gray-500 transition-all",
#     )


# def pdf_dropzone() -> rx.Component:
#     return rx.el.div(
#         rx.upload.root(
#             rx.el.div(
#                 rx.el.div(
#                     rx.icon("cloud_upload", class_name="h-8 w-8 text-gray-400"),
#                     rx.el.h3("Drop PDF here", class_name="font-semibold text-gray-300"),
#                     rx.el.p("or click to upload", class_name="text-sm text-gray-500"),
#                 ),
#                 class_name="flex flex-col items-center justify-center gap-2 text-center",
#             ),
#             id="pdf-upload",
#             class_name="flex h-32 w-full cursor-pointer items-center justify-center rounded-lg border-2 border-dashed border-gray-600 bg-[#252a41] p-4 hover:border-violet-500 transition-colors",
#             accept={"application/pdf": [".pdf"]},
#             max_files=1,
#             multiple=False,
#             on_click=rx.window_alert("Click the 'Upload PDF' button to upload."),
#         ),
#         rx.el.button(
#             "Upload PDF",
#             on_click=State.handle_upload(rx.upload_files(upload_id="pdf-upload")),
#             class_name="w-full mt-2 rounded-md bg-violet-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-violet-500",
#         ),
#         class_name="flex flex-col items-center justify-center",
#     )


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
            rx.el.h1("Board meetings AI Assistant", class_name="text-2xl font-semibold text-white"),
            class_name="bg-[#1a1d2e] p-6 sticky top-0 z-10 border-b border-gray-800",
        ),
        rx.el.main(
            rx.el.div(
                rx.el.div(
                    rx.foreach(State.chat_history, chat_message),
                    id="chat-container",
                    class_name="flex-1 overflow-y-auto p-6",
                ),
                # rx.el.div(
                #     rx.el.div(
                #         microphone_button(),
                #         pdf_dropzone(),
                #         class_name="flex items-center justify-center gap-8",
                #     ),
                #     class_name="p-6 border-t border-gray-800",
                # ),
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