##----------------------------------------------------------------------------------------
##  Unity Texture Extractor
##----------------------------------------------------------------------------------------
##  Platform: macOS Catalina + Python 3.7.4
##  Written by Pacess HO
##  Copyright Pacess Studio, 2020.  All rights reserved.
##----------------------------------------------------------------------------------------

import os
from os import path
import struct
import sys

##  pip install UnityPy
from UnityPy import AssetsManager

##----------------------------------------------------------------------------------------
##  Main extraction routine
def extractAssets(sourcePath: str, targetPath: str):
	for root, directories, files in os.walk(sourcePath):
		for filename in files:

			filePath = os.path.join(root, filename)
			print("Reading "+filePath+"...")
			try:

				manager = AssetsManager(filePath)
				for asset in manager.assets.values():
					for obj in asset.objects.values():

						##  Extract texture
						if obj.type in ["Texture2D", "Sprite"]:

							outputPath = root.replace(sourcePath, targetPath)
							if not os.path.exists(outputPath):
								os.makedirs(outputPath)

							data = obj.read()
							outputPath = os.path.join(outputPath, data.name)
							outputPath, extension = os.path.splitext(outputPath)
							outputPath = outputPath+".png"

							if path.exists(outputPath):
								continue

							print("  Saving "+outputPath+"...")
							image = data.image
							image.save(outputPath)
							continue

						##----------------------------------------------------------------------------------------
						##  Extract text
						if obj.type in ["TextAsset"]:

							outputPath = root.replace(sourcePath, targetPath)
							if not os.path.exists(outputPath):
								os.makedirs(outputPath)

							data = obj.read()
							outputPath = os.path.join(outputPath, data.name)
							outputPath, extension = os.path.splitext(outputPath)
							outputPath = outputPath+".txt"

							if path.exists(outputPath):
								continue

							print("  Saving "+outputPath+"...")
							with open(outputPath, "wb") as file:
								file.write(data.script)

							continue

						##----------------------------------------------------------------------------------------
						if obj.type in ["AudioClip"]:

							filePath = root.replace(sourcePath, targetPath)
							if not os.path.exists(filePath):
								os.makedirs(filePath)

							data = obj.read()
							for key in data.samples:

								outputPath = os.path.join(filePath, key)
								outputPath, extension = os.path.splitext(outputPath)
								outputPath = outputPath+".wav"

								if path.exists(outputPath):
									continue

								print("  Saving "+outputPath+"...")
								sampleData = data.samples[key]
								with open(outputPath, "wb") as file:
									file.write(sampleData)

						##----------------------------------------------------------------------------------------
						##  Any other format are not support yet
						print("  ### Asset type '"+str(obj.type)+"' not support yet...")

			except KeyboardInterrupt:
				sys.exit()

			except struct.error as err:
				print("### "+str(err))

			except:
				print("### Unknown error...")

##----------------------------------------------------------------------------------------
##  Main program
extractAssets("../ROM/", "../Extracted/")