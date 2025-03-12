# UI IMPORTS
from rich.console import Console
console = Console()

# ETC IMPORTS
import requests

# PROGRAM LOGIC
def input_url(url):
    """Responsible for retrieving info from user-inputted URL and parsing character positions."""

    initial_response = requests.get(url)
    parse_type = 0
    character_positions = []  # ✅ Fix: Initialize list to avoid undefined variable error

    try:
        # TRY TO PARSE INFO INTO JSON FORMAT FOR EASIER PARSING
        response = initial_response.json()
        parse_type = 1
        console.print("Information captured, now parsing from JSON format", style="bold green")

        # ✅ Fix: Ensure response is a list before processing
        if isinstance(response, dict):
            response = response.get("data", [])  # Extract list if nested in a dictionary

    except requests.exceptions.JSONDecodeError as e:
        # RAISED ERROR IF FILE CAN'T BE CONVERTED TO JSON
        console.print(f"Error decoding JSON, trying TXT format: {e}", style="yellow")
        parse_type = 2
        response = initial_response.text

    # ✅ Processing JSON format
    if parse_type == 1 and isinstance(response, list):
        try:
            character_positions = [(item["char"], int(item["x"]), int(item["y"])) for item in response]
        except KeyError as e:
            console.print(f"[red]Error: Missing expected key {e} in JSON response.[/red]")
            return

    # ✅ Processing TXT format
    elif parse_type == 2:
        for line in response.split("\n"):
            parts = line.rsplit(" ", 2)  # Split last two as x, y
            print(f"DEBUG: {parts}")  # Debugging output
            if len(parts) == 3:
                try:
                    char, x, y = parts[0], int(parts[1]), int(parts[2])
                    character_positions.append((char, x, y))
                except ValueError as e:
                    print(f"Skipping invalid line: {e} -> {parts}")

    if not character_positions:
        console.print("[red]No valid character positions found.[/red]")
        return

    # FIND GRID SIZE
    max_x = max(x for _, x, _ in character_positions)
    max_y = max(y for _, _, y in character_positions)

    # CREATE GRID FILLED WITH SPACES
    grid = [[" " for _ in range(max_x + 1)] for _ in range(max_y + 1)]

    # PLACE CHARACTERS
    for char, x, y in character_positions:
        grid[y][x] = char

    # PRINT FINAL GRID
    console.print("\n".join("".join(row) for row in grid))


if __name__ == "__main__":
    
    url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"
    input_url(url)
