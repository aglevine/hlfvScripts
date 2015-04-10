from sys import argv, stdout, stderr
import ROOT
import sys
import math
import array
import numpy

nonedir = "jesnonesignalFeb26_01JetFix/"
updir = "jesplussignalFeb26_01JetFix/"
downdir = "jesminussignalFeb26_01JetFix/"

channel = "vbf"

if channel == "vbf":
        dirname = "vbfmutau"
elif channel == "gg1":
        dirname = "boostmutau"
elif channel == "gg0":
        dirname = "gg0mutau"

nonefile_str = "LFV_" + channel+"_collMass_type1_fakeRate_zjetsEmbed_newSignal_jesnone.root"
upfile_str = "LFV_" + channel+"_collMass_jes_plus_fakeRate_zjetsEmbed_newSignal_jesplus.root"
downfile_str = "LFV_" + channel+"_collMass_jes_minus_fakeRate_zjetsEmbed_newSignal_jesminus.root"

nonefile = ROOT.TFile(nonedir+nonefile_str)
upfile = ROOT.TFile(updir+upfile_str)
downfile = ROOT.TFile(downdir+downfile_str)

fakes = nonefile.Get("vbfmutau/fakes")
ztautau = nonefile.Get("vbfmutau/ztautau")
zjetsother = nonefile.Get("vbfmutau/zjetsother")
ttbar = nonefile.Get("vbfmutau/ttbar")
ww = nonefile.Get("vbfmutau/ww")
singlet = nonefile.Get("vbfmutau/singlet")
data_obs = nonefile.Get("vbfmutau/data_obs")
LFVVBF126 = nonefile.Get("vbfmutau/LFVVBF126")
LFVGG126 = nonefile.Get("vbfmutau/LFVGG126")
SMVBF126 = nonefile.Get("vbfmutau/SMVBF126")
SMGG126 = nonefile.Get("vbfmutau/SMGG126")
LFVVBF = nonefile.Get("vbfmutau/LFVVBF")
LFVGG = nonefile.Get("vbfmutau/LFVGG")
SMVBF = nonefile.Get("vbfmutau/SMVBF")
SMGG = nonefile.Get("vbfmutau/SMGG")

LFVVBF126.Scale(10)
LFVGG126.Scale(10)
LFVVBF.Scale(10)
LFVGG.Scale(10)

ztautau_JES_Up = upfile.Get("vbfmutau/ztautau")
zjetsother_JES_Up = upfile.Get("vbfmutau/zjetsother")
ttbar_JES_Up = upfile.Get("vbfmutau/ttbar")
ww_JES_Up = upfile.Get("vbfmutau/ww")
LFVVBF126_JES_Up = upfile.Get("vbfmutau/LFVVBF126")
LFVGG126_JES_Up = upfile.Get("vbfmutau/LFVGG126")
SMVBF126_JES_Up = upfile.Get("vbfmutau/SMVBF126")
SMGG126_JES_Up = upfile.Get("vbfmutau/SMGG126")
LFVVBF_JES_Up = upfile.Get("vbfmutau/LFVVBF")
LFVGG_JES_Up = upfile.Get("vbfmutau/LFVGG")
SMVBF_JES_Up = upfile.Get("vbfmutau/SMVBF")
SMGG_JES_Up = upfile.Get("vbfmutau/SMGG")

LFVVBF126_JES_Up.Scale(10)
LFVGG126_JES_Up.Scale(10)
LFVVBF_JES_Up.Scale(10)
LFVGG_JES_Up.Scale(10)

ztautau_JES_Down = downfile.Get("vbfmutau/ztautau")
zjetsother_JES_Down = downfile.Get("vbfmutau/zjetsother")
ttbar_JES_Down = downfile.Get("vbfmutau/ttbar")
ww_JES_Down = downfile.Get("vbfmutau/ww")
LFVVBF126_JES_Down = downfile.Get("vbfmutau/LFVVBF126")
LFVGG126_JES_Down = downfile.Get("vbfmutau/LFVGG126")
SMVBF126_JES_Down = downfile.Get("vbfmutau/SMVBF126")
SMGG126_JES_Down = downfile.Get("vbfmutau/SMGG126")
LFVVBF_JES_Down = downfile.Get("vbfmutau/LFVVBF")
LFVGG_JES_Down = downfile.Get("vbfmutau/LFVGG")
SMVBF_JES_Down = downfile.Get("vbfmutau/SMVBF")
SMGG_JES_Down = downfile.Get("vbfmutau/SMGG")

LFVVBF126_JES_Down.Scale(10)
LFVGG126_JES_Down.Scale(10)
LFVVBF_JES_Down.Scale(10)
LFVGG_JES_Down.Scale(10)

##create root file with yields for datacards
outfile = ROOT.TFile("LFV_"+channel+"_jesshape.root","RECREATE")
outfile.mkdir(dirname)
outfile.cd(dirname+"/")

fakes.Write("fakes")
ztautau.Write("ztautau")
zjetsother.Write("zjetsother")
ttbar.Write("ttbar")
ww.Write("ww")
singlet.Write("singlet")
data_obs.Write("data_obs")
LFVVBF126.Write("LFVVBF126")
LFVGG126.Write("LFVGG126")
SMVBF126.Write("SMVBF126")
SMGG126.Write("SMGG126")
LFVVBF.Write("LFVVBF")
LFVGG.Write("LFVGG")
SMVBF.Write("SMVBF")
SMGG.Write("SMGG")

ztautau_JES_Up.Write("ztautau_JESUp")
zjetsother_JES_Up.Write("zjetsother_JESUp")
ttbar_JES_Up.Write("ttbar_JESUp")
ww_JES_Up.Write("ww_JESUp")
LFVVBF126_JES_Up.Write("LFVVBF126_JESUp")
LFVGG126_JES_Up.Write("LFVGG126_JESUp")
SMVBF126_JES_Up.Write("SMVBF126_JESUp")
SMGG126_JES_Up.Write("SMGG126_JESUp")
LFVVBF_JES_Up.Write("LFVVBF_JESUp")
LFVGG_JES_Up.Write("LFVGG_JESUp")
SMVBF_JES_Up.Write("SMVBF_JESUp")
SMGG_JES_Up.Write("SMGG_JESUp")

ztautau_JES_Down.Write("ztautau_JESDown")
zjetsother_JES_Down.Write("zjetsother_JESDown")
ttbar_JES_Down.Write("ttbar_JESDown")
ww_JES_Down.Write("ww_JESDown")
LFVVBF126_JES_Down.Write("LFVVBF126_JESDown")
LFVGG126_JES_Down.Write("LFVGG126_JESDown")
SMVBF126_JES_Down.Write("SMVBF126_JESDown")
SMGG126_JES_Down.Write("SMGG126_JESDown")
LFVVBF_JES_Down.Write("LFVVBF_JESDown")
LFVGG_JES_Down.Write("LFVGG_JESDown")
SMVBF_JES_Down.Write("SMVBF_JESDown")
SMGG_JES_Down.Write("SMGG_JESDown")

print "channel: " + channel
print "ztautau jes difference up: " + str((ztautau_JES_Up.Integral()-ztautau.Integral())/ztautau.Integral()*100)+" %"
print "ztautau jes difference down: " + str((ztautau_JES_Down.Integral()-ztautau.Integral())/ztautau.Integral()*100)+" %"
print "zjetsother jes difference up: " + str((zjetsother_JES_Up.Integral()-zjetsother.Integral())/zjetsother.Integral()*100)+" %"
print "zjetsother jes difference down: " + str((zjetsother_JES_Down.Integral()-zjetsother.Integral())/zjetsother.Integral()*100)+" %"
print "ttbar jes difference up: " + str((ttbar_JES_Up.Integral()-ttbar.Integral())/ttbar.Integral()*100)+" %"
print "ttbar jes difference down: " + str((ttbar_JES_Down.Integral()-ttbar.Integral())/ttbar.Integral()*100)+" %"
print "ww jes difference up: " + str((ww_JES_Up.Integral()-ww.Integral())/ww.Integral()*100)+" %"
print "ww jes difference down: " + str((ww_JES_Down.Integral()-ww.Integral())/ww.Integral()*100)+" %"
print "LFVVBF jes difference up: " + str((LFVVBF_JES_Up.Integral()-LFVVBF.Integral())/LFVVBF.Integral()*100)+" %"
print "LFVVBF jes difference down: " + str((LFVVBF_JES_Down.Integral()-LFVVBF.Integral())/LFVVBF.Integral()*100)+" %"
print "LFVGG jes difference up: " + str((LFVGG_JES_Up.Integral()-LFVGG.Integral())/LFVGG.Integral()*100)+" %"
print "LFVGG jes difference down: " + str((LFVGG_JES_Down.Integral()-LFVGG.Integral())/LFVGG.Integral()*100)+" %"
print "SMVBF jes difference up: " + str((SMVBF_JES_Up.Integral()-SMVBF.Integral())/SMVBF.Integral()*100)+" %"
print "SMVBF jes difference down: " + str((SMVBF_JES_Down.Integral()-SMVBF.Integral())/SMVBF.Integral()*100)+" %"
print "SMGG jes difference up: " + str((SMGG_JES_Up.Integral()-SMGG.Integral())/SMGG.Integral()*100)+" %"
print "SMGG jes difference down: " + str((SMGG_JES_Down.Integral()-SMGG.Integral())/SMGG.Integral()*100)+" %"

#print "zjetsother jes difference: " + str(zjetsother_JES_Up.Integral()-zjetsother_JES_Down.Integral())
#print "ttbar jes difference: " + str(ttbar_JES_Up.Integral()-ttbar_JES_Down.Integral())
#print "ww jes difference: " + str(ww_JES_Up.Integral()-ww_JES_Down.Integral())
#print "LFVVBF jes difference: " + str(LFVVBF_JES_Up.Integral()-LFVVBF_JES_Down.Integral())
#print "LFVGG jes difference: " + str(LFVGG_JES_Up.Integral()-LFVGG_JES_Down.Integral())
#print "SMVBF jes difference: " + str(SMVBF_JES_Up.Integral()-SMVBF_JES_Down.Integral())
#print "SMGG jes difference: " + str(SMGG_JES_Up.Integral()-SMGG_JES_Down.Integral())

outfile.Write()

