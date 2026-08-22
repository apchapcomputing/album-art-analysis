---
title: Album Art Analysis
emoji: 🎙️
colorFrom: purple
colorTo: blue
sdk: gradio
sdk_version: "6.24.0"
python_version: "3.10.21"
app_file: app.py
pinned: false
---

## Thesis

Art styles on album covers have changed over time — and that change is tied to the medium. What was once a 12×12 inch vinyl canvas is now a digital postage stamp at best, a pinky nail at worst. As music shifted from vinyl → cassette → CD → digital download → streaming, the role of album art shrank with it. People no longer listen to albums in their entirety; we consume songs on playlists where the artwork is an afterthought.

This project collects album art from the most popular albums of each year (1940–2024) and analyzes visual trends over time, grouped by the dominant music format of the era.

## Format Eras

| Format | Years |
| --- | --- |
| Pre-vinyl | 1940–1949 |
| Vinyl | 1950–1987 |
| Cassette Tape | 1983–1990 |
| CD | 1988–2010 |
| Digital Download | 2003–2014 |
| Streaming | 2015–2026 |

## Project Structure

```text
collect_data.py     # Fetches album art from Spotify by year and saves to dataset/
analysis.ipynb      # Exploratory analysis and model training
formats.csv         # Format era definitions
dataset/
    pre_vinyl/      # 1940–1949
    vinyl/          # 1950–1987
    cassette_tape/  # 1983–1990
    cd/             # 1988–2010
    digital_download/ # 2003–2014
    streaming/      # 2015–2026
```

## Setup

1. Clone the repo and create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your Spotify API credentials:

   ```env
   CLIENT_SECRET=your_spotify_client_secret
   ```

3. Collect data:

   ```bash
   python collect_data.py
   ```

## Tools

- **Spotify API** — album metadata and art collection
- **fastai / PyTorch** — model training and transfer learning
- **CLIP** — zero-shot image classification
- **timm** — pretrained vision models
- **OpenCV / scikit-image** — image feature extraction
- **Gradio** — interactive demo interface
