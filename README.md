# steam_screenshots_downloader

Download every public screenshots of a steam user.

The user needs to have publicly available screenshots on his profile page (`https://steamcommunity.com/id/USERNAME/screenshots/`).

## Dependencies

- requests
- beautifulsoup
- tqdm

## Installation

### Regular installation

```
git clone https://github.com/dbeley/steam_screenshots_downloader
cd steam_screenshots_downloader
pip install -r requirements.txt
```

### Installation with pipenv

```
git clone https://github.com/dbeley/steam_screenshots_downloader
cd steam_screenshots_downloader
pipenv install
```

## Usage

```
python steam_screenshots_downloader.py -u USERNAME
```

## Help

```
python steam_screenshots_downloader -h
```
