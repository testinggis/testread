import ee
import json
import datetime
import numpy as np
import geojson
from datetime import date

ee.Initialize()


def get_bounding_box(geometry):
    coords = np.array(list(geojson.utils.coords(geometry)))
    return [
        coords[:, 0].min(),
        coords[:, 1].min(),
        coords[:, 0].max(),
        coords[:, 1].max(),
    ]


def stackify(asset):
    binfo = []
    dic = {}
    # Get asset type
    atype = ee.data.getAsset(asset)["type"].lower()
    if atype == "image":
        ee_object = ee.ImageCollection([asset])
        ee_num = 1
    elif atype == "image_collection":
        ee_num = ee.ImageCollection(asset).size().getInfo()
        ee_object = ee.ImageCollection(asset)
    bandlist = ee_object.first().bandNames().getInfo()
    prop = dict(ee_object.first().getInfo()["properties"])
    for key, value in prop.items():
        if not key.startswith("system"):
            dic[key] = value
    for bands in bandlist:
        proj = ee_object.first().select([bands]).projection()
        scale = proj.nominalScale().getInfo()
        for things in ee_object.first().select([bands]).getInfo()["bands"]:
            minima = things["data_type"]["min"]
            maxima = things["data_type"]["max"]
        band_info = {
            "name": bands,
            "gsd": scale,
            "min": minima,
            "max": maxima,
            "gee:estimated_range": True,
        }
        binfo.append(band_info)
    geom = ee_object.geometry()
    ee_bounds = geom.bounds()
    bounding_box = get_bounding_box(ee_bounds.getInfo())
    if ee_num > 1:
        region = ee.Image(ee_object.toList(ee_num).get(ee_num / 2))
    elif ee_num == 1:
        region = ee_object.first()
    img = region.visualize(
        bands=["b4", "b3", "b2"],
        gamma=1.356,
        max=3958,
        min=302,
        opacity=1,
        forceRgbOutput=False,
    )
    thumburl = img.getThumbURL(
        {
            "dimensions": "512x512",
            "region": region.geometry().centroid(0.01).buffer(1000).bounds().getInfo(),
            "format": "png",
        }
    )
    try:
        collect_list = ee_object.toList(
            ee_object.sort("system:time_start").size().getInfo()
        )
        keylist = []
        for key, value in collect_list.get(0).getInfo()["properties"].items():
            keylist.append(key)
            if key.startswith("system:time_start"):
                if len(str(value)) != 10:
                    value = value / (pow(10, len(str(value)) - 10))
                    startdate = str(datetime.datetime.fromtimestamp(value)).split(" ")[
                        0
                    ]
        for key, value in collect_list.get(-1).getInfo()["properties"].items():
            keylist.append(key)
            if key.startswith("system:time_end"):
                if len(str(value)) != 10:
                    value = value / (pow(10, len(str(value)) - 10))
                    enddate = str(datetime.datetime.fromtimestamp(value)).split(" ")[0]
            elif key.startswith("system:time_start"):
                if len(str(value)) != 10:
                    value = value / (pow(10, len(str(value)) - 10))
                    enddate = str(datetime.datetime.fromtimestamp(value)).split(" ")[0]
        if not "system:time_end" in keylist and enddate is None:
            enddate = str(date.today())
        if not "system:time_start" in keylist and startdate is None:
            startdate = str(date.today())
    except Exception as e:
        enddate = str(date.today())
        startdate = str(date.today())
    manifest = {
        "stac_version": "1.0.0-beta.2",
        "stac_extensions": ["scientific"],
        "id": asset,
        "gee:type": atype,
        "links": [
            {
                "rel": "self",
                "href": "https://earthengine-stac.storage.googleapis.com/catalog/USGS_GMTED2010.json",
            },
            {
                "rel": "parent",
                "href": "https://earthengine-stac.storage.googleapis.com/catalog/catalog.json",
            },
            {
                "rel": "root",
                "href": "https://earthengine-stac.storage.googleapis.com/catalog/catalog.json",
            },
            {"rel": "preview", "href": thumburl},
            {
                "rel": "license",
                "href": "https://developers.google.com/earth-engine/datasets/catalog/USGS_GMTED2010#terms-of-use",
            },
        ],
        "extent": {
            "spatial": dict(bbox=bounding_box),
            "temporal": dict(inter=[startdate, enddate]),
        },
        "gee:terms_of_use": "This dataset is made available publicly under the Creative Commons Non Commercial license(CC-BY-NC 4.0).",
        "sci:citation": "copyright: <year> Planet Labs Inc.",
        "keywords": ["midres", "multispectral", "planet"],
        "eo:bands": binfo,
        "eo:properties": dic,
    }
    print(json.dumps(manifest, indent=4, sort_keys=False))


stackify(asset="users/samapriya/open-data/open-ca/ps4bsr")
