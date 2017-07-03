# Planet Earth Engine Pipeline: From Assets to Analysis
# Planet, People and Pixels: Assets to Analysis
# Planet, People and Pipelines: Assets to Analysis

One of the most powerful afterthought that came when Planet Labs decided to capture the whole world using a collection of satellites was the capability of analysis which was unprecedented. With the need to handle such datasets which are global and often massive Google was already building and hosting a platform called Google Earth Engine(GEE) designed to analyze massive datasets. As Planet opened up its data using the Open California program[link], the Ambassador program[link]  and now the educational access program[link] there was a need for platforms capable of handling this analyis. I found the connection between Planet API and GEE was an easy one to make. As a researcher and novice developer my question was a simpler one, would it be possible to build a pipeline that allows users to batch download dataasets and upload to GEE for analysis.The following is a tool developed as a result of that and steps on using it 

## Getting the Tool
If you ever hear the word CLI in relationship to a program you can assume that it refers to a command line interface and I will be using this throughout the article. It is basically a program I can use on a unix or osx based terminal or windows command prompt. Anyways let us get started

The things you need first (Housekeeping)
* You need a planet account which gives you access to your very own shiny API key. It also defines the area you have access to globally and you can sign up
 [here](https://www.planet.com/explorer/) 
 You also need a Google Earth Engine account with access to the [API](https://signup.earthengine.google.com/#!/)

* You need the planet API and the Google Earth Engine API installed on your system
		To install planet API you can simply type
			pip install planet
		Since google earth engine API has a slightly longer install process and it gets updated frequently you might want to install using [instructions](https://developers.google.com/earth-engine/python_install)
* The only dependecy that does not install automatically using requirements.txt is GDAL.For installing GDAL in Ubuntu
		sudo add-apt-repository ppa:ubuntugis/ppa && sudo apt-get update
		sudo apt-get install gdal-bin
		For Windows I found this [guide](https://sandbox.idre.ucla.edu/sandbox/tutorials/installing-gdal-for-windows) from UCLA
*  To install the Planet-GEE-Pipeline-CLI. As always two of my favorite operating systems are windows and linux to install on linux
	```
	git clone https://github.com/samapriya/Planet-GEE-Pipeline-CLI.git
	cd Planet-GEE-Pipeline-CLI && sudo python setup.py install
	pip install -r requirements.txt
	```
*for windows download the zip and after extraction go to the folder containing "setup.py" and open command prompt at that location and type
```
	python setup.py install
	pip install -r requirements.txt
```

You can use the tool without any installation by typing python ppipe.py
		
For the rest of the tutorial I will be working on a windows system because this is the most common operating system I use within my lab and in the university setting of which I am currently a part. If you have installed everything and your dependencies are met you should be able to type ppipe-h in command prompt and you should be able to get the following readout. Since I have designed the tool to be powerful addon tools to earth engine as well I will only deal with the ones responsible for processing and uploading Planet assets but feel free to explore the other tools included in the toolset

![CLI](http://i.imgur.com/mRUcPtq.gif)

## Registering your Planet API
The tool is designed to save your API key so that you don't have to do this again and again, this also means that a new users API key overrides yours. This also assumes you have registered your google earthengine api by running "earthengine authenticate"

With everything set up lets get started, You only need to provide your planetkey one since it is saved for future use.
aoijson-Is a powerful tool, as it allows you to bring any existing KML, Zipped Shapefile, GeoJSON, WKT or even Landsat Tiles to a structured geojson file, this is so that the Planet API can read the structured geojson which has additional filters such as cloud cover and range of dates. The tool allows you to bring your own area of interest geospatial file or create one. Incase you are interested in creating a initial area of interest file you can simply go to geojson.io and once you have defined your area of interest click on save as GeoJson(A map.geojson file is created). For the ease of use I am choosing and working on an area within Californias since this is convered under the Open California license and should be easily accesible to anyone

![GEO](http://i.imgur.com/vmBGedl.gif)

The tool can then allow you to convert the geojson file to include filters to be used with the Planet Data API.

Let us say we want to convert this map.geojson to a structured aoi.json from June 1 2017 to June 30th 2017 with 15% cloud cover as our maximum. We would pass the following command
ppipe.py aoijson --start "2017-06-01" --end "2017-06-30" --cloud "0.15" --inputfile "GJSON"  --geo "local path to map.geojson file" --loc "path where aoi.json output file will be created"

![aoijson](http://i.imgur.com/5Pr0iqp.png)

I am providing the [map.geojson](https://filebin.ca/3S3EeDlgNzmj/map.geojson) and the [aoi.json](https://filebin.ca/3S3CzV90x72d/aoi.json) file so that you can compare th file structures and can replicate the same process. It is a great idea to go into the planet explorer first and toggle your available area, that way you can be sure that you have access to the area you are trying to download.

The data API activates assets only when requested by a user rather than keeping all assets activated all the time. So for the area of interest we created the next tool we use is the activatepl tool which allows you to activate or check the activation status of the assets within our area of interest. You can request activation for any planet asset and for now I am interested in just PSOrthoTile analytic.

The setup for asset activation for aoi.json will be

```
ppipe activatepl --aoi "local path where you create aoi.json file " --action activate --asst "PSOrthoTile analytic"
```

![activate](http://i.imgur.com/glkDz4K.png)

You can then periodically check the progress on activation

```
ppipe activatepl --aoi "local path where you create aoi.json file " --action check --asst "PSOrthoTile analytic"
```

![activating](http://i.imgur.com/KO8yTq8.png)

![activated](http://i.imgur.com/jIajFfE.png)

The next step pertaining to the Data API is to download the assets

![downloader](http://i.imgur.com/KItCGPK.png)

Download the metadata

![downmeta](http://i.imgur.com/zgZYmEy.png)

Parse the metadata

![parse](http://i.imgur.com/WUvFZNU.gif)

Upload the Files to Earth Engine

![ee](http://i.imgur.com/hkykXOo.gif)
 
 
Future projects and plans

![auto](http://i.imgur.com/VaDrNTH.gif)


From the readme file the instructions included
You can choose from multiple input files types such as KML, Zipped Shapefile, GeoJSON, WKT or even Landsat Tiles based on PathRow numbers. The geo option asks you to select existing files which will be converted into formatted JSON file called aoi.json. If using WRS as an option just type in the 6 digit PathRow combination and it will create a json file for you.

This was unique not just because it meant you had backups and control of your datasets but also because your analysis and storage could be made free.
```
 			planetkey           Enter your planet API Key
			aoijson             Tool to convert KML, Shapefile,WKT,GeoJSON or Landsat
								WRS PathRow file to AreaOfInterest.JSON file with
								structured query for use with Planet API 1.0
			activatepl          Tool to query and/or activate Planet Assets
			downloadpl          Tool to download Planet Assets
			metadata            Tool to tabulate and convert all metadata files from
								Planet or Digital Globe Assets
								-------------------------------------------
								----Choose from Earth Engine Tools Below----
								-------------------------------------------
			ee_user             Get Earth Engine API Key & Paste it back to Command
								line/shell to change user
			create              Allows the user to create an asset collection or
								folder in Google Earth Engine
			upload              Batch Asset Uploader to Earth Engine.
```
