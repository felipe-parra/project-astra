# Project Astra

A modern Text User Interface (TUI) JSON editor built with Python. Create and edit JSON files interactively with a beautiful terminal interface.

![Project Status: Active](https://img.shields.io/badge/Project%20Status-Active-green)
![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

![Project Astra screenshot](https://raw.githubusercontent.com/felipe-parra/project-astra/main/screenshot_project_astra.png)

## Features

- 🎨 Beautiful terminal user interface
- ⌨️ Keyboard shortcuts for quick actions
- 📝 Interactive key-value pair editing
- 🔄 Real-time JSON preview
- 💾 Automatic type inference for values
- 📂 Timestamped output files
- 🎯 Input validation and error handling

## Installation

1. Clone the repository:

```bash
git clone https://github.com/felipe-parra/project-astra.git
cd project-astra
```

2. Create a virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the JSON editor using the CLI:

```bash
python -m src.json_editor
```

### Keyboard Shortcuts

- `Ctrl+S`: Save JSON file
- `Ctrl+Q`: Quit application
- `Tab`: Navigate to next input field
- `Shift+Tab`: Navigate to previous input field
- `Enter`: Submit current input field

## Project Structure

```
src/
├── cli.py           # Command-line interface
├── json_editor.py   # Main TUI application
├── model.py         # Data models
└── output/          # Generated JSON files directory
```

## Dependencies

- [Textual](https://github.com/Textualize/textual) - TUI framework
- [Typer](https://github.com/tiangolo/typer) - CLI builder
- [orjson](https://github.com/ijl/orjson) - Fast JSON parsing/serialization

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Textual](https://github.com/Textualize/textual)
- Inspired by modern JSON editors
