import reflex as rx

config = rx.Config(
    app_name="guest_management",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)