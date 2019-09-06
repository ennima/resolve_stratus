import string
from ctypes import windll
import time
import os, sys
from os import walk
import subprocess
import ftplib
import json



def ftpSend(host,user,passs,destFolder,newFile):
	#Login FTP to Summit
	#host = "192.168.196.92"
	#user = "mxfmovie"
	print("New File",newFile)
	passs = ""
	ftp = ftplib.FTP(host)
	ftp.login(user,passs)
	ftp.cwd(destFolder)
	#print ftp.pwd()
	print ("Enviando ",os.path.basename(newFile) ," a ftp Dest...")
	ftp.storbinary('STOR '+os.path.basename(newFile),open(newFile,'rb'))
	ftp.quit()
	print ("Listo.")
	
# def muxer(video,unidad,channels,ffmpeg_path,temp_dir,ingest_folder,stratus_ftp,stratus_ftp_user,stratus_ftp_pass,ftp_material_name):
# 	#video = '00014M'
# 	#unidad = 'I:\\'
# 	FinalVideo = ftp_material_name +"_"+ video

# 	print(FinalVideo)
# 	print("Channels: ",channels)
# 	if(channels == 4):
# 		audio = ffmpeg_path+'ffmpeg -i '+unidad+':\\CONTENTS\\AUDIO\\'+video+'00.mxf -i '+unidad+':\\CONTENTS\\AUDIO\\'+video+'01.mxf -i '+unidad+':\\CONTENTS\\AUDIO\\'+video+'02.mxf -i '+unidad+':\\CONTENTS\\AUDIO\\'+video+'03.mxf -filter_complex [0:a][1:a][2:a][3:a]amerge=inputs=4[aout] -map [aout] -ac 4 '+temp_dir+video+'.flac'
# 	else:
# 		audio = ffmpeg_path+'ffmpeg -i '+unidad+':\\CONTENTS\\AUDIO\\'+video+'00.mxf -i '+unidad+':\\CONTENTS\\AUDIO\\'+video+'01.mxf -filter_complex [0:a][1:a]amerge=inputs=2[aout] -map [aout] -ac 2 '+temp_dir+video+'.flac'
# 	print("Muxing audio " + audio)
# 	audio2 = audio.split(" ")
# 	print(audio2)

# 	print("CDW: ", os.getcwd(), "tmp: ", temp_dir)
	

# 	p = subprocess.Popen(audio2)
# 	p.wait()

# 	print("ingest_folder: ",ingest_folder,"stratus_ftp: ",stratus_ftp," stratus_ftp_user: ",stratus_ftp_user," stratus_ftp_pass:",stratus_ftp_pass)
	
# 	videoMerge = ffmpeg_path+'ffmpeg -i '+unidad+':\\CONTENTS\\VIDEO\\'+video+'.mxf -i '+temp_dir+video+'.flac -vcodec mpeg2video -vtag xd5b -s 1920x1080 -pix_fmt yuv420p -rtbufsize 50000k -b:v 50000k -dc 9 -flags +ilme+ildct -top 1 -acodec pcm_s16le -ac 4 -f mxf '+temp_dir+FinalVideo+'.mxf'
# 	print("Muxing Video" + videoMerge)
# 	videoMerge2 = videoMerge.split(' ')
# 	print(videoMerge2)
	

# 	p = subprocess.Popen(videoMerge2)
# 	p.wait()
# 	print("Sending: "+temp_dir+FinalVideo)
# 	ftpSend(stratus_ftp,stratus_ftp_user,stratus_ftp_pass,ingest_folder,temp_dir+FinalVideo+'.mxf')
# 	drive =""
# 	print(FinalVideo,' ingestado.')
	


# def ingesta(drive,channels,ffmpeg_path,temp_dir,ingest_folder,stratus_ftp,stratus_ftp_user,stratus_ftp_pass):
# 	drivePath = drive+":\\"

# 	pathClips = "CONTENTS\\CLIP\\"
# 	pathThumbnail = "CONTENTS\\ICON\\"
# 	pathAudio = "CONTENTS\\AUDIO\\"
# 	pathVideo = "CONTENTS\\VIDEO\\"

# 	dirClipsPath = drivePath + pathClips

# 	#print(dirClipsPath)
# 	# f = []
# 	# material = ["0092T4","01590J","0075EE"]
   
# 	# for clip in material:
# 	#     muxer(clip,drive,channels,ffmpeg_path,temp_dir,ingest_folder,stratus_ftp,stratus_ftp_user,stratus_ftp_pass,"PIEDRAS_NEGRAS_4")

   

# 	# f = []
# 	# material = ["0092T4","01590J","0075EE","0071XU"]
# 	# for (dirpath, dirnames, filenames) in walk(dirClipsPath):
# 	#     f.extend(filenames)
# 	#     #print("Number of files: ",len(f))
# 	#     #print(f)
# 	#     for clip in f:
# 	#         #print("muxing ",clip.replace(".XML",""))
# 	#         if(clip.replace(".XML","") in material):
# 	#             print("-----------No ingestar "+clip.replace(".XML",""))
# 	#         else:
# 	#             print(" Ingestando: "+clip.replace(".XML",""))
# 	#             muxer(clip.replace(".XML",""),drive,channels,ffmpeg_path,temp_dir,ingest_folder,stratus_ftp,stratus_ftp_user,stratus_ftp_pass,"PIEDRAS_NEGRAS_ULTIMO")
# 	#             print(" Listo "+clip.replace(".XML",""))
# 	#     break

# def ingestaCompleto(drive,channels,ffmpeg_path,temp_dir,ingest_folder,stratus_ftp,stratus_ftp_user,stratus_ftp_pass,material_name_final):
# 	drivePath = drive+":\\"

# 	pathClips = "CONTENTS\\CLIP\\"
# 	pathThumbnail = "CONTENTS\\ICON\\"
# 	pathAudio = "CONTENTS\\AUDIO\\"
# 	pathVideo = "CONTENTS\\VIDEO\\"

# 	dirClipsPath = drivePath + pathClips

# 	#print(dirClipsPath)
# 	f = []
# 	for (dirpath, dirnames, filenames) in walk(dirClipsPath):
# 		f.extend(filenames)
# 		print("Number of files: ",len(f), "   FINAL NAME:",material_name_final)
# 		print(f)
# 		for clip in f:
# 			print("muxing ",clip.replace(".XML",""))
# 			muxer(clip.replace(".XML",""),drive,channels,ffmpeg_path,temp_dir,ingest_folder,stratus_ftp,stratus_ftp_user,stratus_ftp_pass,material_name_final)
# 		break


def read_folder(folder):
	print("folder: ",folder)
	for (dirpath, dirnames, filenames) in walk(folder):
		print(filenames)
		pass
	
	return filenames



def transcode_media(clip,path,FinalVideo):
	print(FinalVideo)
	print(path)
	if(not "._" in clip) and (not ".textClipping" in clip):
		name_split = clip.strip().split(".")
		test = 0
		print(len(name_split))
		print(len(name_split[0].strip()))
		
		if(len(name_split[0].strip()) == 0):
			print("No lo hago ")
		else:
			print("#Transcodificando: ",clip.strip())
			
			if(os.path.exists(temp_dir)) and (test == 0):
				print("Existe el directorio de cache")
				videoMerge = ffmpeg_path+'ffmpeg -y -i "'+path+clip+'" -vcodec mpeg2video -vtag xd5b -s 1920x1080 -pix_fmt yuv420p -r 29.97 -rtbufsize 50000k -b:v 50000k -dc 9 -flags +ilme+ildct -top 1 -acodec pcm_s16le -ac 4 -f mxf "'+temp_dir+FinalVideo+'".mxf'
				print(videoMerge)
			   
				p = subprocess.Popen(videoMerge)
				p.wait()
				print("Sending: "+temp_dir+FinalVideo)
				test += 1

				ftpSend(stratus_ftp,stratus_ftp_user,stratus_ftp_pass,ingest_folder,temp_dir+FinalVideo+'.mxf')
				drive =""
				
				print(FinalVideo,' ingestado.')
			else:
				print("no esta: ",temp_dir)
	 			

def loadJson(path):
	with open(path,"r") as f:
		data = f.read()
	return json.loads(data) 


ingestado_msg = r""" ___                       _            _              ____  
|_ _|_ __   __ _  ___  ___| |_ __ _  __| | ___     _  |  _ \ 
 | || '_ \ / _` |/ _ \/ __| __/ _` |/ _` |/ _ \   (_) | | | |
 | || | | | (_| |  __/\__ \ || (_| | (_| | (_) |   _  | |_| |
|___|_| |_|\__, |\___||___/\__\__,_|\__,_|\___/   (_) |____/ 
           |___/                                             
"""



conf = loadJson("conf.json")
print(conf)

folders = [""]

drives = ["E"]                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        
final_clip = conf["final_clip"]
ingest_folder = conf["ingest_folder"]
inferior = conf["inferior"]
superior = conf["superior"]

delay_time_seconds = conf["delay_time"]

# Nombre de la ingesta
final_clip = final_clip.replace(" ","_") 

channels = 4
ffmpeg_path = ""
temp_dir = conf["render_path"]


stratus_ftp = conf["ftp"]["host"]
stratus_ftp_user = conf["ftp"]["user"]
stratus_ftp_pass = conf["ftp"]["pass"]



for drive in drives:
	counter = 0
	origin_path = ".\\videos\\"

	print("----------------------------------------------------------",origin_path)
	for folder in folders:
		print("Leyendo: ",folder)
	   # read_folder(origin_path+folder)
		
		clips = read_folder(origin_path+folder)
		
		for clip in clips:
			print("Clip "+str(counter)+" de "+str(len(clips)))
			print("\n \ncounter:"+str(counter)+" Transcoding: ",clip)
			print("")
			if(counter > (inferior - 1)) and (counter < (superior + 1) ):
				# pass
				print(counter,"-------------------------------------",)
				transcode_media(clip,origin_path+folder+"",folder+final_clip+conf["clip_separator"]+clip.replace(".mxf","")+"")
				# counter=counter + 1
				time.sleep(delay_time_seconds)

			counter=counter + 1
print(ingestado_msg)


