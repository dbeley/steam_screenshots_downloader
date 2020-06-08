"""
Download every public screenshots of a steam user.
"""
import logging
import time
import argparse
import requests
import re
from bs4 import BeautifulSoup
from pathlib import Path
from tqdm import tqdm

logger = logging.getLogger()
temps_debut = time.time()


def download_image(url, export_folder):
    try:
        response = requests.get(url)
        additional_infos = response.headers["content-disposition"]
        filename = (
            export_folder
            + "/"
            + re.sub(
                "'|\"|;|=",
                "",
                re.findall("filename(.+)", additional_infos)[0].split("'")[-1],
            )
        )
        logger.debug(f"Downloading image {url} at {filename}")
        with open(filename, "wb") as f:
            f.write(response.content)
    except Exception as e:
        logger.error(f"Error for url {url}: {e}")


def extract_direct_link(url):
    soup = BeautifulSoup(requests.get(url).content, "lxml")
    image_link = soup.find("div", {"class": "actualmediactn"}).find("a")["href"]
    logger.debug(f"Found image: {image_link}")
    return image_link


def main():
    args = parse_args()
    page_id = 1
    all_screenshots_links = []
    export_folder = "Exports"
    Path(export_folder).mkdir(parents=True, exist_ok=True)

    while True:
        url = f"https://steamcommunity.com/id/{args.user}/screenshots/?p={page_id}&sort=newestfirst&browsefilter=myfiles&view=grid&privacy=30"
        logger.debug(f"Extracting content of {url}.")
        soup = BeautifulSoup(requests.get(url).content, "lxml")

        all_screenshots_links_partial = [
            x["href"] for x in soup.find_all("a", {"class": "profile_media_item"})
        ]
        if len(all_screenshots_links_partial) == 0:
            break
        all_screenshots_links += all_screenshots_links_partial
        logger.info(
            f"{len(all_screenshots_links_partial)} new screenshots found. {len(all_screenshots_links)} total."
        )
        page_id += 1

    direct_links = []
    logger.info("Extracting Screenshots URLs.")
    for link in tqdm(all_screenshots_links, dynamic_ncols=True):
        direct_links.append(extract_direct_link(link))

    logger.info("Downloading Screenshots.")
    for link in tqdm(direct_links, dynamic_ncols=True):
        download_image(link, export_folder)

    logger.info("Runtime : %.2f seconds." % (time.time() - temps_debut))


def parse_args():
    format = "%(levelname)s :: %(message)s"
    parser = argparse.ArgumentParser(
        description="Download every public screenshots of a steam user."
    )
    parser.add_argument(
        "--debug",
        help="Display debugging information.",
        action="store_const",
        dest="loglevel",
        const=logging.DEBUG,
        default=logging.INFO,
    )
    parser.add_argument(
        "-u",
        "--user",
        help="Steam username (you can put the username in between quotes if it contains some special characters).",
        required=True,
    )
    args = parser.parse_args()

    logging.basicConfig(level=args.loglevel, format=format)
    return args


if __name__ == "__main__":
    main()
