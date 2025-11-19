import reflex as rx
from app.states.state import State


def nav_item(item: dict) -> rx.Component:
    """A navigation item component."""
    return rx.el.a(
        rx.icon(
            item["icon"],
            class_name="h-5 w-5 text-gray-400 group-hover:text-violet-400 transition-colors",
        ),
        rx.el.span(
            item["label"],
            class_name="text-sm font-medium text-gray-300 group-hover:text-white transition-colors",
        ),
        href=item["href"],
        class_name="group flex items-center gap-3 rounded-lg px-3 py-2 transition-all hover:bg-[#252a41]",
    )


def recording_indicator() -> rx.Component:
    return rx.el.div(
        rx.el.div(class_name="h-2.5 w-2.5 rounded-full bg-current"),
        class_name="flex items-center justify-center text-red-500 animate-pulse",
    )


def microphone_button() -> rx.Component:
    return rx.el.button(
        rx.cond(
            State.is_recording,
            recording_indicator(),
            rx.icon("mic", class_name="h-6 w-6"),
        ),
        on_click=rx.cond(
            State.is_recording, State.stop_recording, State.start_recording
        ),
        disabled=State.is_processing,
        class_name="flex items-center justify-center h-14 w-14 rounded-full bg-violet-600 text-white hover:bg-violet-700 disabled:bg-gray-500 transition-all",
    )


def pdf_dropzone() -> rx.Component:
    return rx.el.div(
        rx.upload.root(
            rx.el.div(
                rx.el.div(
                    rx.icon("cloud_upload", class_name="h-8 w-8 text-gray-400"),
                    rx.el.h3("Drop PDF here", class_name="font-semibold text-gray-300"),
                    rx.el.p("or click to upload", class_name="text-sm text-gray-500"),
                ),
                class_name="flex flex-col items-center justify-center gap-2 text-center",
            ),
            id="pdf-upload",
            class_name="flex h-32 w-full cursor-pointer items-center justify-center rounded-lg border-2 border-dashed border-gray-600 bg-[#252a41] p-4 hover:border-violet-500 transition-colors",
            accept={"application/pdf": [".pdf"]},
            max_files=1,
            multiple=False,
            on_click=rx.window_alert("Click the 'Upload PDF' button to upload."),
        ),
        rx.el.button(
            "Upload PDF",
            on_click=State.handle_upload(rx.upload_files(upload_id="pdf-upload")),
            class_name="w-full mt-2 rounded-md bg-violet-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-violet-500",
        ),
        class_name="flex flex-col items-center justify-center",
    )


def sidebar() -> rx.Component:
    """The sidebar component for the app."""
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.a(
                    rx.image(src="/q.png", class_name="h-8 w-8", size="large"),
                    rx.el.span("Welcome", class_name="sr-only"),
                    href="#",
                    class_name="flex items-center gap-2",
                ),
                class_name="flex h-16 shrink-0 items-center border-b border-gray-700 px-6",
            ),
            rx.el.nav(
                rx.foreach(State.nav_items, nav_item), class_name="flex-1 space-y-1 p-4"
            ),
            rx.el.div(
                rx.el.div(
                    pdf_dropzone(), class_name="flex items-center justify-center gap-8"
                ),
                class_name="p-6 border-t border-gray-800",
            ),
            rx.el.div(
                rx.el.div(
                    microphone_button(),
                    class_name="flex items-center justify-center gap-8",
                ),
                class_name="p-6 border-t border-gray-800",
            ),
        ),
        class_name="hidden lg:flex lg:flex-col lg:w-64 bg-[#1a1d2e] border-r border-gray-800",
    )