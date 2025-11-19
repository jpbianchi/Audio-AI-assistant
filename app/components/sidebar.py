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
        ),
        class_name="hidden lg:flex lg:flex-col lg:w-64 bg-[#1a1d2e] border-r border-gray-800",
    )