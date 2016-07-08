# coding=UTF-8
import subprocess
import pandas as pd
import numpy as np
import mongoConnect
from preprocessing import label_reduce
from preprocessing import key_estimate
from evaluatefunction import evaluate_function

collection = mongoConnect.db.ACE_Results

def justDownload(SongName, ArtistName, YoutubeURL):
    song = SongName
    artist = ArtistName
    youtube_url = YoutubeURL

    command = "youtube-dl -o /Users/PonShane/Dropbox/Research/ImplementCode/AudioRecords/" + song + ".%(ext)s --extract-audio --audio-format mp3  --audio-quality  0  " + youtube_url
    print command
    #command = "youtube-dl -o Layla.%(ext)s --extract-audio --audio-format mp3  --audio-quality  0  https://www.youtube.com/watch?v=Q_L-0Ryhmic"
    subprocess.call(command.split(), shell=False)

    sonic_command = "sonic-annotator -d vamp:nnls-chroma:chordino:simplechord /Users/PonShane/Dropbox/Research/ImplementCode/AudioRecords/" + song + ".mp3 -w csv"
    #sonic_command = "sonic-annotator -d vamp:nnls-chroma:chordino:simplechord Layla.mp3 -w csv"
    print sonic_command
    subprocess.call(sonic_command.split(),shell=False)

    csv_path = "/Users/PonShane/Dropbox/Research/ImplementCode/AudioRecords/"+song+"_vamp_nnls-chroma_chordino_simplechord.csv"
    #ground_true_lab_path = GroundTruthLab

    df = pd.read_csv(csv_path, header=None)
    est_label = np.squeeze((df.iloc[:-1,1:2])).values.tolist()
    for i in range(len(est_label)):
        est_label[i] = label_reduce(str(est_label[i]))
    print est_label

    est_beat_interval = np.asarray(zip(np.squeeze((df.iloc[:-1,:1]).as_matrix()),np.squeeze((df.iloc[1:,:1]).as_matrix())))
    ace_est_key = key_estimate(est_label)
    print ace_est_key

    InsertData = dict()
    InsertData["chord_list"] = est_label
    InsertData["estimate_key"] = ace_est_key["estimate_key"]
    InsertData["estimate_key_profile"] = ace_est_key["estimate_key_profile"]
    InsertData["song"] = song
    InsertData["artist"] = artist
    InsertData["youtube_url"] = youtube_url
    #InsertData["mir_eval"] = dict()
    #evaluation_result = evaluate_function(csv_path, ground_true_lab_path)
    #for i, (key, value) in enumerate(evaluation_result.iteritems()):
    #    InsertData["mir_eval"][key] = value

    InsertId = collection.insert_one(InsertData).inserted_id
    print InsertId

def downloadPlusAnalysis(SongName, ArtistName, YoutubeURL, GroundTruthLab):
    song = SongName
    artist = ArtistName
    youtube_url = YoutubeURL

    command = "youtube-dl -o /Users/PonShane/Dropbox/Research/ImplementCode/AudioRecords/" + song + ".%(ext)s --extract-audio --audio-format mp3  --audio-quality  0  " + youtube_url
    print command
    #command = "youtube-dl -o Layla.%(ext)s --extract-audio --audio-format mp3  --audio-quality  0  https://www.youtube.com/watch?v=Q_L-0Ryhmic"
    subprocess.call(command.split(), shell=False)

    sonic_command = "sonic-annotator -d vamp:nnls-chroma:chordino:simplechord /Users/PonShane/Dropbox/Research/ImplementCode/AudioRecords/" + song + ".mp3 -w csv"
    #sonic_command = "sonic-annotator -d vamp:nnls-chroma:chordino:simplechord Layla.mp3 -w csv"
    print sonic_command
    subprocess.call(sonic_command.split(),shell=False)

    csv_path = "/Users/PonShane/Dropbox/Research/ImplementCode/AudioRecords/"+song+"_vamp_nnls-chroma_chordino_simplechord.csv"
    ground_true_lab_path = GroundTruthLab

    df = pd.read_csv(csv_path, header=None)
    est_label = np.squeeze((df.iloc[:-1,1:2])).values.tolist()
    for i in range(len(est_label)):
        est_label[i] = label_reduce(str(est_label[i]))
    print est_label

    est_beat_interval = np.asarray(zip(np.squeeze((df.iloc[:-1,:1]).as_matrix()),np.squeeze((df.iloc[1:,:1]).as_matrix())))
    ace_est_key = key_estimate(est_label)
    print ace_est_key

    InsertData = dict()
    InsertData["chord_list"] = est_label
    InsertData["estimate_key"] = ace_est_key["estimate_key"]
    InsertData["estimate_key_profile"] = ace_est_key["estimate_key_profile"]
    InsertData["song"] = song
    InsertData["artist"] = artist
    InsertData["youtube_url"] = youtube_url
    InsertData["mir_eval"] = dict()
    evaluation_result = evaluate_function(csv_path, ground_true_lab_path)
    for i, (key, value) in enumerate(evaluation_result.iteritems()):
        InsertData["mir_eval"][key] = value

    InsertId = collection.insert_one(InsertData).inserted_id
    print InsertId

def main():
    # downloadPlusAnalysis(SongName="You_give_love_a_bad_name", ArtistName="bon_jovi", YoutubeURL="https://www.youtube.com/watch?v=S9tKwSboJeg", GroundTruthLab="/Users/PonShane/Dropbox/Research/ImplementCode/uspopLabels/bon_jovi/Slippery_When_Wet/02-You_Give_Love_a_Bad_Name.lab")
    justDownload(SongName="You_give_love_a_bad_name", ArtistName="bon_jovi", YoutubeURL="https://www.youtube.com/watch?v=S9tKwSboJeg",)

if __name__ == "__main__":
    main()
