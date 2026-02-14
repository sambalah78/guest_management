import reflex as rx

config = rx.Config(
    app_name="guest_management",
    db_url="postgresql+psycopg://postgres.gzhgzsorwihydufypymq:Sambalah086211@aws-1-ap-southeast-1.pooler.supabase.com:6543/postgres",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
