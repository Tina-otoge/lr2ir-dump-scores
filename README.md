# LR2IR dump scores

Dumb and simple Python script to dump all scores from a given LR2IR player ID.

Can also download replay data.

This was hastily wrote after the announcement that LR2IR will shutdown on
2026-05-31 (https://x.com/kenjidct/status/2059644318596661391), as I don't have
access to my old LR2IR accounts anymore, but want to preserve my old play
history.

:warning: I strongly advise against attempting to scrape the entirety of LR2IR.
Whether its by using this script, or any other mean. There are numerous other
projects that already try to be all encompassing in preserving the data of the
website.

:warning: **DO NOT ATTEMPT TO SCRAPE THE ENTIRETY OF LR2IR**

:warning: **DO NOT TRY TO REMOVE THE SELF-IMPOSED RATE-LIMITING**

The motivation behind this script was that I wanted a backup of MY personal
LR2IR data. Something I always wanted, whether the site was going to shut down
or not. This announce only added an ultimatum and forced me to complete this
project before the 31st of May.

If you are also interested into dumping your own PBs and replay data, then this
script can be useful to you. Otherwise, you should probably look elsewhere.

## Rate-limiting

The script has an hardcoded self-rate limiting of 1 req/s. If a response is
obtained from LR2IR in less time than that, the script will throttle itself, as
to not overload the website.

When requests are dropped, the script will retry infinitely with an exponential
backoff timeout (wait 2s, then 4, 8, 16, 32, then cap at 60).


## Usage

```bash
pip install requests

python main.py <PLAYER ID>

# Example
python main.py 117388

# Include replays
python main.py 117388 --include-replays
```

## Example output

The script will create a file named <PLAYER_ID>\_<PLAYER_NAME>\_rivalinfo.xml
with the output of the LR2IR API route for
`getplayerxml.cgi?id={PLAYER_ID}&lastupdate`, and a file named
<PLAYER_ID>\_<PLAYER_NAME>\_mypage.html with the output of the LR2IR website
route for `search.cgi?mode=mypage&playerid={PLAYER_ID}`.

The former contains all of your PBs, the other contains your userpage, which has
some useful content such as bio, dan rank, amount of plays, and rival names and
IDs.

Example `117388_SKIEL_rivalinfo.xml`:

```xml
#<?xml version="1.0" encoding="shift_jis"?>
<scorelist>
	<score>
		<hash>4054870e58b6f497edfe027f5e5a638f</hash>
		<clear>3</clear>
		<notes>689</notes>
		<combo>211</combo>
		<pg>429</pg>
		<gr>220</gr>
		<gd>23</gd>
		<bd>9</bd>
		<pr>15</pr>
		<minbp>24</minbp>
		<option>0</option>
		<lastupdate>1779714184</lastupdate>
	</score>
	<score>
		<hash>3302469a5576fe17d30a32ccdd0a193f</hash>
		<clear>3</clear>
		<notes>930</notes>
		<combo>178</combo>
		<pg>486</pg>
		<gr>380</gr>
		<gd>49</gd>
		<bd>7</bd>
		<pr>18</pr>
		<minbp>25</minbp>
		<option>0</option>
		<lastupdate>1778408985</lastupdate>
	</score>
	<score>
		<hash>0f9cec1771ab8d40b562de5dec4ebff9</hash>
		<clear>3</clear>
		<notes>813</notes>
...
	</score>
</scorelist>
<rivalname>SKIEL</rivalname>
```

If you add `--include-replays`, the script will create individual files in
`replays/<PLAYER_ID>_<PLAYER_NAME>/<SONG_HASH_MD5>.csv` with the output of the
LR2IR API route `getghost.cgi?songmd5={HASH}&targetid={PLAYER_ID}`.

Example:

`replays/117388_SKIEL/0a8bfce9f46a82e19a9e775fa6ad08b5.csv`

```csv
#SKIEL,0,11434,m2@hGSGC@GmlPPETh2PETItqSKq12X@Itvq4tvXSGXTETETEsXScHSHS@GvTITIr0tqSF1wuSEaG@2q11D@HsxswUgzsuh3MtSMusswD7GUEqSBG@Q@GsTGhNBE@Kn7TESJSGSEq4XTGVGxaqvqBE@sg2h@Hvssr8n3r2SKTEXmGr2UGuTNwSn5SGytyvshEr0tq2qXSGSHwXSC@Rw@m6ESEXUETMXSIqSGg5VGq4q10X@XmPMTGg2sSEq3SH@P2GSESE@Xh@2tXSGD8ESHsSGggvBD@EsSESHghEsSESISEsSGtg2SGhh2mGtsSEug2gsD7GVGYESHTgSEThLXbXD8h2gSgSLTGTHa2Y@Xh2h2@SEUEXgcSC@Y2BXgYD@BaEagC@ahi2SZZ,
```

## Tested on

- Python 3.14.4, Linux
- Python 3.12.7, Windows

## Resource used

- https://git.sr.ht/~showy_fence/new-lr2ir/tree/master/item/src/routes/lr2ir/api/getghost.rs

## License

MIT.
