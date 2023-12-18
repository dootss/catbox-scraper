# Catbox Scraper

An extremely fast python script for scraping and downloading random files from [Catbox](https://catbox.moe), a file-hosting site.

The script takes from file extensions specified under config.yaml, generates random urls and checks to see if they are valid. If they are, it downloads them and stores them in extension-sorted folders.

`https://files.catbox.moe/[a-z0-9]{6}.(extension)` is the format for URL generation.

## Demonstration
https://github.com/dootss/catbox-scraper/assets/126783585/c0213d13-01ec-4a55-80cd-1e877b081530

## Installation and Usage
You will need:
- Python
- Git
```
git clone https://github.com/dootss/catbox-scraper.git
cd catbox-scraper
pip install -r requirements.txt
python main.py
```
and the script will handle everything else from there!

Press CTRL+C to stop the script.

## Configuration
If you wish to change the extensions the script attempts to check for, simply edit `config.yaml`'s `file_extensions` field with the extensions you wish to check for:

![image](https://github.com/dootss/catbox-scraper/assets/126783585/726ebad4-9fa9-4807-bafe-28f3867c6949)

By default, the script checks for the following: `png, gif, jpg, jpeg, webm, mp4`

## NOTICE
*I am not responsible for any consequences that come from using this script! Catbox is a file hosting site, and files found on it can be unpredictable. You'll definitely find a LOT of NSFW images as a result of running this; Catbox is used a fair amount by anonymous communities like 4chan.*


