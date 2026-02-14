import reflex as rx
GOLD = "#D4AF37"
BLACK = "#111111"
DARK_GRAY = "#1A1A1A"
TEXT_WHITE = "#FFFFFF"

def success_page():
    return rx.box(
        rx.script("""
            setTimeout(() => {
                const script = document.createElement('script');
                script.src = "https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js";
                script.onload = () => {
                    confetti({
                        particleCount: 200,
                        spread: 90,
                        origin: { y: 0.6 }
                    });
                };
                document.body.appendChild(script);
            }, 200);
        """),

        rx.center(
            rx.vstack(
                rx.heading("🎉 Check-In Successful!", size="8", color="green"),
                rx.text("Welcome to the event"),
                spacing="4",
                align="center"
            ),
            height="100vh"
        )
    )
