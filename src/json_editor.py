# json_editor.py
from __future__ import annotations

import sys
import os
from pathlib import Path
from textual.app import App, ComposeResult, events
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import DataTable, Footer, Header, Input, Static
from textual.widgets._button import Button  # botón simple
from typing import Any
import orjson

from model import KVPair

# Output directory
OUTPUT_DIR = Path("output")


class JsonEditor(App):
    """JSON editor."""

    CSS = """
    Horizontal {
        height: auto;
        margin: 1;
        padding: 1;
    }

    Input {
        margin: 1 2;
        width: 40%;
    }

    Button {
        margin: 1 2;
    }

    #actions {
        content-align: center middle;
        padding: 1;
    }

    #save-button {
        background: $success;
    }

    #reset-button {
        background: $error;
    }

    DataTable {
        height: 50vh;
        margin: 1;
    }

    #preview {
        height: auto;
        margin: 1;
        background: $surface;
        padding: 1;
        border: solid $primary;
    }
    """

    BINDINGS = [
        Binding("ctrl+s", "save", "Save JSON"),
        Binding("ctrl+q", "quit", "Quit"),
        Binding("tab", "next_input", "Next field"),
        Binding("shift+tab", "previous_input", "Previous field"),
    ]

    kvs: reactive[list[KVPair]] = reactive([])

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical():
            with Horizontal(id="input-container"):
                yield Input(placeholder="Write the key here", id="key")
                yield Input(placeholder="Write the value here", id="value")
                yield Button("Agregar", id="add", variant="primary")
            with Horizontal(id="actions"):
                yield Button("Save JSON (Ctrl+S)", id="save-button", variant="success")
                yield Button("Reset", id="reset-button", variant="error")
            self.table = DataTable(zebra_stripes=True)
            self.table.add_columns("Key", "Value")
            yield self.table
            self.preview = Static("", id="preview", expand=True, markup=False)
            yield self.preview
        yield Footer()

    def on_mount(self) -> None:
        """When the app starts."""
        self.key_in = self.query_one("#key", Input)
        self.val_in = self.query_one("#value", Input)
        self.preview.update(
            "[blue]Editor ready. Enter a key and a value.[/]")
        self.key_in.focus()

    # --------------------- Eventos -----------------------------------------

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "add":
            self.preview.update("[blue]Add button pressed[/]")
            await self.action_add_kv()
        elif event.button.id == "save-button":
            self.preview.update("[blue]Save button pressed[/]")
            await self.action_save()
        elif event.button.id == "reset-button":
            self.preview.update("[blue]Reset button pressed[/]")
            await self.action_reset()

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        if event.input.id == "key":
            self.preview.update("[blue]Enter pressed in key field[/]")
            self.val_in.focus()
        elif event.input.id == "value":
            self.preview.update("[blue]Enter pressed in value field[/]")
            await self.action_add_kv()

    def action_next_input(self) -> None:
        if self.key_in.has_focus:
            self.val_in.focus()
        else:
            self.key_in.focus()

    def action_previous_input(self) -> None:
        if self.val_in.has_focus:
            self.key_in.focus()
        else:
            self.val_in.focus()

    # --------------------- Acciones ----------------------------------------

    async def action_add_kv(self) -> None:
        key = self.key_in.value.strip()
        val_raw = self.val_in.value.strip()

        self.preview.update(
            f"[blue]Trying to add - Key: {key}, Value: {val_raw}[/]")

        if not key:
            self.preview.update("[b red]The key cannot be empty[/]")
            return
        if any(kv.key == key for kv in self.kvs):
            self.preview.update(f"[b yellow]Duplicate key: {key}[/]")
            return

        # intenta castear value
        val: Any
        try:
            # Primero intentamos números
            if val_raw.replace(".", "").isdigit():
                if "." in val_raw:
                    val = float(val_raw)
                else:
                    val = int(val_raw)
            # Luego booleanos
            elif val_raw.lower() == "true":
                val = True
            elif val_raw.lower() == "false":
                val = False
            # Luego null
            elif val_raw.lower() == "null":
                val = None
            # Por defecto, es string
            else:
                val = val_raw
        except ValueError:
            val = val_raw

        self.kvs.append(KVPair(key, val))
        self.table.add_row(key, str(val))
        self.key_in.value = self.val_in.value = ""
        self.key_in.focus()
        self.refresh_preview()
        self.preview.update("[green]Pair added correctly[/]")

    async def action_save(self) -> None:
        """Save the JSON to a file."""
        self.preview.update("[blue]Trying to save JSON...[/]")

        if not self.kvs:
            self.preview.update("[b red]No data to save[/]")
            return

        try:
            # Create directory if it doesn't exist
            OUTPUT_DIR.mkdir(exist_ok=True)

            # Generate file name with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = OUTPUT_DIR / f"data_{timestamp}.json"

            # Prepare data
            data = {kv.key: kv.value for kv in self.kvs}
            json_bytes = orjson.dumps(data, option=orjson.OPT_INDENT_2)

            # Write file
            with open(output_file, "wb") as f:
                f.write(json_bytes)

            self.preview.update(f"[green]JSON saved in: {output_file}[/]")
        except Exception as e:
            self.preview.update(f"[b red]Error saving: {str(e)}[/]")

    def refresh_preview(self) -> None:
        """Update the JSON preview."""
        if not self.kvs:
            self.preview.update("[dim]No data yet[/]")
            return

        try:
            data = {kv.key: kv.value for kv in self.kvs}
            pretty = orjson.dumps(data, option=orjson.OPT_INDENT_2).decode()
            self.preview.update(f"[white on black]\n{pretty}\n[/]")
        except Exception as e:
            self.preview.update(f"[b red]Error in preview: {str(e)}[/]")

    async def action_reset(self) -> None:
        """Reset all fields and the table."""
        self.key_in.value = ""
        self.val_in.value = ""
        self.kvs.clear()
        self.table.clear()
        self.preview.update("[yellow]All data has been deleted[/]")
        self.key_in.focus()

    # Allow to quit with ESC as well as Ctrl+Q
    async def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            await self.action_quit()


if __name__ == "__main__":
    JsonEditor().run()
