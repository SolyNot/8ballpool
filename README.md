# 8Ball Pool AI

## Requirements

- Windows OS (uses win32api)
- Python 3.7+

## Installation

1. Clone the repository:
```bash
git clone https://github.com/SolyNot/8ballpool.git
cd 8ballpool
```

2. Install dependencies:
```bash
pip install opencv-python numpy mss pygetwindow pygame pywin32
```

## Usage

1. Open Roblox and join this [game](https://www.roblox.com/games/5523851880/8-Ball-Pool-Classic#!/game-instances)
2. Run the script:
```bash
python 8_bit.py
```

3. The overlay will appear and draw aim lines on detected winning balls

## Troubleshooting

- **No window detected**: Ensure Roblox is running and the window title matches `WINDOW_TITLE`
- **No lines detected**: Try adjusting `MIN_AREA` or `HOUGH_THRESHOLD`
- **Overlay not visible**: Check if Windows allows transparent overlay apps
- **Performance issues**: Reduce `fps` in [`overlay.display()`](8_bit.py:102) call

## Disclaimer

This tool is for educational purposes. Use at your own risk and respect Roblox's terms of service.