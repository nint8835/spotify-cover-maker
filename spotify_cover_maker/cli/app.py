import typer

from .generate import generate_app

app = typer.Typer(
    help="Utility for automatically generating cover images for Spotify playlists."
)

app.add_typer(generate_app, name="generate")
