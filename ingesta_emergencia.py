import string
from ctypes import windll
import time
import os, sys
from os import walk


import subprocess
import ftplib
#print (sys.argv)


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
    
def muxer(video,unidad,channels,ffmpeg_path,temp_dir,ingest_folder,stratus_ftp,stratus_ftp_user,stratus_ftp_pass,ftp_material_name):
    #video = '00014M'
    #unidad = 'I:\\'
    FinalVideo = ftp_material_name +"_"+ video
    print("muxing",video)
    print(FinalVideo)
    print("Channels: ",channels)
    audio_channels_string = ""
    filter_complex_string = "-filter_complex "
    audio_merge_string = ffmpeg_path+'ffmpeg '
    end_line = " "
    for channel in range(0,channels):
        
        if(channel<10):
            channel_num = "0"+str(channel)
        else:
            channel_num = str(channel)

        # print('-i '+unidad+':\\CONTENTS\\AUDIO\\'+video+channel_num+'.mxf')
        # print('['+str(channel)+':a]')

        filter_complex_string += '['+str(channel)+':a]'
        audio_channels_string += '-y -i '+unidad+':\\CONTENTS\\AUDIO\\'+video+channel_num+'.mxf' + end_line

    audio_filter = filter_complex_string+'amerge=inputs='+str(channels)+'[aout] -map [aout] -ac '+str(channels)+' '
    audio = audio_merge_string+audio_channels_string+audio_filter+temp_dir+video+'.flac'
    # if(channels == 4):
    #     audio = ffmpeg_path+'ffmpeg -i '+unidad+':\\CONTENTS\\AUDIO\\'+video+'00.mxf -i '+unidad+':\\CONTENTS\\AUDIO\\'+video+'01.mxf -i '+unidad+':\\CONTENTS\\AUDIO\\'+video+'02.mxf -i '+unidad+':\\CONTENTS\\AUDIO\\'+video+'03.mxf -filter_complex [0:a][1:a][2:a][3:a]amerge=inputs=4[aout] -map [aout] -ac 4 '+temp_dir+video+'.flac'
    # else:
    #     audio = ffmpeg_path+'ffmpeg -i '+unidad+':\\CONTENTS\\AUDIO\\'+video+'00.mxf -i '+unidad+':\\CONTENTS\\AUDIO\\'+video+'01.mxf -filter_complex [0:a][1:a]amerge=inputs=2[aout] -map [aout] -ac 2 '+temp_dir+video+'.flac'
    print("Muxing audio " + audio + "\n")
    audio2 = audio.split(" ")
    print(audio2)

    print("CDW: ", os.getcwd(), "tmp: ", temp_dir)
    

    p = subprocess.Popen(audio2)
    p.wait()

    print("ingest_folder: ",ingest_folder,"stratus_ftp: ",stratus_ftp," stratus_ftp_user: ",stratus_ftp_user," stratus_ftp_pass:",stratus_ftp_pass)
    
    videoMerge = ffmpeg_path+'ffmpeg -y -i '+unidad+':\\CONTENTS\\VIDEO\\'+video+'.mxf -i '+temp_dir+video+'.flac -vcodec mpeg2video -vtag xd5b -s 1920x1080 -pix_fmt yuv420p -rtbufsize 50000k -b:v 50000k -dc 9 -flags +ilme+ildct -top 1 -r 29.97 -acodec pcm_s16le -ac 4 -f mxf '+temp_dir+FinalVideo+'.mxf'
    print("Muxing Video" + videoMerge)
    videoMerge2 = videoMerge.split(' ')
    print(videoMerge2)
    

    p = subprocess.Popen(videoMerge2)
    p.wait()
    print("Sending: "+temp_dir+FinalVideo)
    ftpSend(stratus_ftp,stratus_ftp_user,stratus_ftp_pass,ingest_folder,temp_dir+FinalVideo+'.mxf')
    drive =""
    print(FinalVideo,' ingestado.')
    


def ingestaAdd(drive,channels,ffmpeg_path,temp_dir,ingest_folder,stratus_ftp,stratus_ftp_user,stratus_ftp_pass,material_name_final):
    drivePath = drive+":\\"

    pathClips = "CONTENTS\\CLIP\\"
    pathThumbnail = "CONTENTS\\ICON\\"
    pathAudio = "CONTENTS\\AUDIO\\"
    pathVideo = "CONTENTS\\VIDEO\\"

    dirClipsPath = drivePath + pathClips

    print(dirClipsPath)
    f = []
   
    material = ['152458']
   
    for clip in material:
        muxer(clip,drive,channels,ffmpeg_path,temp_dir,ingest_folder,stratus_ftp,stratus_ftp_user,stratus_ftp_pass,material_name_final)
        # print(clip)
def ingestaAdd2(drive,channels,ffmpeg_path,temp_dir,ingest_folder,stratus_ftp,stratus_ftp_user,stratus_ftp_pass,material_name_final,material):
    drivePath = drive+":\\"

    pathClips = "CONTENTS\\CLIP\\"
    pathThumbnail = "CONTENTS\\ICON\\"
    pathAudio = "CONTENTS\\AUDIO\\"
    pathVideo = "CONTENTS\\VIDEO\\"

    dirClipsPath = drivePath + pathClips

    print(dirClipsPath)
    f = []
   
    # material = ['0001C5', '0002PK', '0003V0', '0004BH', '00052R', '0006XX', '0007GY', '0008GP', '00098E', '001038', '0011LN', '00129U', '00136N', '0014XP', '0015V5', '0016Z2', '0017T7', '0018BJ', '00198T', '0020QS', '0021C3', '0022BP', '00237B', '0024F6', '00251Q', '0026AD', '0027P5', '00280X', '0029G0', '0030DJ', '0031G5', '00321Z', '0033RY', '00345J', '00355L', '0036H4', '0037HU', '003831', '0039FC', '0040H7', '0041JY', '00425X', '004363', '004491', '00450A', '00463I', '0047B5', '0048PN', '0049JZ', '0050SI', '0051YB', '00523Y', '00532C', '00547M', '0055CM', '005689', '0057SN', '00584J', '0059QO', '00605X', '0061FB', '0062JM']
   
    for clip in material:
        muxer(clip,drive,channels,ffmpeg_path,temp_dir,ingest_folder,stratus_ftp,stratus_ftp_user,stratus_ftp_pass,material_name_final)
        



def ingestaDiscard(drive,channels,ffmpeg_path,temp_dir,ingest_folder,stratus_ftp,stratus_ftp_user,stratus_ftp_pass,material_name_final):
    drivePath = drive+":\\"

    pathClips = "CONTENTS\\CLIP\\"
    pathThumbnail = "CONTENTS\\ICON\\"
    pathAudio = "CONTENTS\\AUDIO\\"
    pathVideo = "CONTENTS\\VIDEO\\"

    dirClipsPath = drivePath + pathClips

    print(dirClipsPath)
      
    f = []
    material = ["08898L"]
    for (dirpath, dirnames, filenames) in walk(dirClipsPath):
        f.extend(filenames)
        #print("Number of files: ",len(f))
        #print(f)
        for clip in f:
            #print("muxing ",clip.replace(".XML",""))
            if(clip.replace(".XML","") in material):
                print("-----------No ingestar "+clip.replace(".XML",""))
            else:
                print(" Ingestando: "+clip.replace(".XML",""))
                muxer(clip.replace(".XML",""),drive,channels,ffmpeg_path,temp_dir,ingest_folder,stratus_ftp,stratus_ftp_user,stratus_ftp_pass,material_name_final)
                print(" Listo "+clip.replace(".XML",""))
        break




def ingestaCompleto(drive,channels,ffmpeg_path,temp_dir,ingest_folder,stratus_ftp,stratus_ftp_user,stratus_ftp_pass,material_name_final):
    drivePath = drive+":\\"

    pathClips = "CONTENTS\\CLIP\\"
    pathThumbnail = "CONTENTS\\ICON\\"
    pathAudio = "CONTENTS\\AUDIO\\"
    pathVideo = "CONTENTS\\VIDEO\\"

    dirClipsPath = drivePath + pathClips

    #print(dirClipsPath)
    f = []
    count = 0
    for (dirpath, dirnames, filenames) in walk(dirClipsPath):
        f.extend(filenames)
        print("Number of files: ",len(f), "   FINAL NAME:",material_name_final)
        print(f)
        
        for clip in f:
            # print(count,"muxing ",clip.replace(".XML",""))
            
            # count+=1
            # muxer(clip.replace(".XML",""),drive,channels,ffmpeg_path,temp_dir,ingest_folder,stratus_ftp,stratus_ftp_user,stratus_ftp_pass,material_name_final)
            
        
            count+=1
        

            # if(drive == "E"):
            #     if(count> 16) and (count<3000):
            #         print(count,"muxing ",clip.replace(".XML",""))
            #         muxer(clip.replace(".XML",""),drive,channels,ffmpeg_path,temp_dir,ingest_folder,stratus_ftp,stratus_ftp_user,stratus_ftp_pass,material_name_final)
            # else:
            #     if(count>-1) and (count<3000):
            #         print(count,"muxing ",clip.replace(".XML",""))
            #         muxer(clip.replace(".XML",""),drive,channels,ffmpeg_path,temp_dir,ingest_folder,stratus_ftp,stratus_ftp_user,stratus_ftp_pass,material_name_final)
            
            if(count> 0) and (count<1000):

                print(count,"muxing ",clip.replace(".XML",""))
                if("0127QG" in clip):
                    print("No ingesta")
                else:
                    pass
                    muxer(clip.replace(".XML",""),drive,channels,ffmpeg_path,temp_dir,ingest_folder,stratus_ftp,stratus_ftp_user,stratus_ftp_pass,material_name_final)
                    # print(count,"muxing ",clip.replace(".XML",""))

        break

# 08898L
###################  Datos a editar en la ingesta ####################
drives = ["I"]
channels = 4

# V:/Camarografos/Daniel R/EDIFICIOS AUTISMO
# ingest_folder = "\\Especiales Noticias\\ESCUELA ALBANILES\\"
# V:/Camarografos/Isaac
# V:/Camarografos/JAIR/TLAHUE 4
nombre_ingesta = "ARTURO HERRERA"
ingest_folder = "\\Camarografos\\Daniel R\\"+nombre_ingesta+"\\"
nombre_ingesta = nombre_ingesta.replace(" ","_")
delay_time_seconds = 0

################### FIN Datos a editar en la ingesta ####################

ffmpeg_path = ""
temp_dir = "C:\\Users\\gvadmin\\Desktop\\ingestapy_\\temp\\"  

stratus_ftp = "192.168.196.139"
stratus_ftp_user = "mxfmovie"
stratus_ftp_pass = ""


#for drive in drives:
#    print("ingestando Drive> ", drive)
#    ingestaDiscard(drive,channels,ffmpeg_path,temp_dir,ingest_folder,stratus_ftp,stratus_ftp_user,stratus_ftp_pass,"RECORIDO_BAREZZITO_OKEY")





for drive in drives:
    print("ingestando Drive> ", drive)

    # ingestaCompleto(drive,channels,ffmpeg_path,temp_dir,ingest_folder,stratus_ftp,stratus_ftp_user,stratus_ftp_pass,nombre_ingesta)
    



    ingestaAdd(drive,channels,ffmpeg_path,temp_dir,ingest_folder,stratus_ftp,stratus_ftp_user,stratus_ftp_pass,nombre_ingesta)
    # ingestaDiscard(drive,channels,ffmpeg_path,temp_dir,ingest_folder,stratus_ftp,stratus_ftp_user,stratus_ftp_pass,nombre_ingesta)
    time.sleep(delay_time_seconds)




# to_add = [{'nombre_ingesta': 'MANIFESTACION_A_FAVOR_DE_AEROPUERTO', 'ingest_folder': '\\Camarografos\\Mario P\\MANIFESTACION A FAVOR DE AEROPUERTO\\', 'clips': ['0001F7', '00020G', '00038V', '00047V', '0005HD', '00062L', '000773', '00087I', '0009VV', '0010P0', '0011ES', '0012IN', '001387', '0014MA', '0015C5', '00164I', '0017KN', '0018N0', '0019WJ', '00204M', '0021I9', '00220X', '002374', '0024N5', '0025UY', '00269G', '00272V', '0028C8', '0029FT', '0030NC', '0031FS', '0032HN', '0033VO', '003429', '0035VZ', '00364Y', '0037LE'], 'drive': 'E'}, {'nombre_ingesta': 'REAVIVA_FUEGO_FABRICA', 'ingest_folder': '\\Camarografos\\Mario P\\REAVIVA FUEGO FABRICA\\', 'clips': ['0038MT', '0039DJ', '0040C0', '004190', '0042O8', '0043RL', '0044WO', '00457F', '0046LU', '00479S', '0048KQ', '0049CU', '00502G', '0051JE', '005299', '00530C', '0054TW', '0055ME', '0056RW'], 'drive': 'E'}]

# for add in to_add:
#    print(add)
#    ingestaAdd2(add["drive"],channels,ffmpeg_path,temp_dir,add["ingest_folder"],stratus_ftp,stratus_ftp_user,stratus_ftp_pass,add["nombre_ingesta"],add["clips"])
