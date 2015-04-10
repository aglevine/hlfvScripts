from sys import argv, stdout, stderr
import ROOT
import sys
import math
import array
import numpy

nonedir = "jesnonesignalFeb26_01JetFix/"
jesupdir = "jesplussignalFeb26_01JetFix/"
jesdowndir = "jesminussignalFeb26_01JetFix/"
tesupdir = "tesup_signal_March9/"
tesdowndir = "tesdown_signal_March9/"

channel = "gg0"

nonefile_str = "LFV_" + channel+"_collMass_type1_fakeRate_zjetsEmbed_newSignal_jesnone.root"
jesupfile_str = "LFV_" + channel+"_collMass_jes_plus_fakeRate_zjetsEmbed_newSignal_jesplus.root"
jesdownfile_str = "LFV_" + channel+"_collMass_jes_minus_fakeRate_zjetsEmbed_newSignal_jesminus.root"
tesupfile_str = "LFV_" + channel+"_collMass_type1_fakeRate_zjetsEmbed_newSignal.root"
tesdownfile_str = "LFV_" + channel+"_collMass_type1_fakeRate_zjetsEmbed_newSignal.root"

nonefile = ROOT.TFile(nonedir+nonefile_str)
jesupfile = ROOT.TFile(jesupdir+jesupfile_str)
jesdownfile = ROOT.TFile(jesdowndir+jesdownfile_str)
tesupfile = ROOT.TFile(tesupdir+tesupfile_str)
tesdownfile = ROOT.TFile(tesdowndir+tesdownfile_str)

if channel == "vbf":
	dirname = "vbfmutau"
elif channel == "gg1":
	dirname = "boostmutau"
elif channel == "gg0":
	dirname = "gg0mutau"

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

ztautau_shape_JES_Up = jesupfile.Get("vbfmutau/ztautau")
zjetsother_shape_JES_Up = jesupfile.Get("vbfmutau/zjetsother")
ttbar_shape_JES_Up = jesupfile.Get("vbfmutau/ttbar")
ww_shape_JES_Up = jesupfile.Get("vbfmutau/ww")
singlet_shape_JES_Up = jesupfile.Get("vbfmutau/singlet")
LFVVBF126_shape_JES_Up = jesupfile.Get("vbfmutau/LFVVBF126")
LFVGG126_shape_JES_Up = jesupfile.Get("vbfmutau/LFVGG126")
SMVBF126_shape_JES_Up = jesupfile.Get("vbfmutau/SMVBF126")
SMGG126_shape_JES_Up = jesupfile.Get("vbfmutau/SMGG126")
LFVVBF_shape_JES_Up = jesupfile.Get("vbfmutau/LFVVBF")
LFVGG_shape_JES_Up = jesupfile.Get("vbfmutau/LFVGG")
SMVBF_shape_JES_Up = jesupfile.Get("vbfmutau/SMVBF")
SMGG_shape_JES_Up = jesupfile.Get("vbfmutau/SMGG")

LFVVBF126_shape_JES_Up.Scale(10)
LFVGG126_shape_JES_Up.Scale(10)
LFVVBF_shape_JES_Up.Scale(10)
LFVGG_shape_JES_Up.Scale(10)

ztautau_shape_JES_Down = jesdownfile.Get("vbfmutau/ztautau")
zjetsother_shape_JES_Down = jesdownfile.Get("vbfmutau/zjetsother")
ttbar_shape_JES_Down = jesdownfile.Get("vbfmutau/ttbar")
ww_shape_JES_Down = jesdownfile.Get("vbfmutau/ww")
singlet_shape_JES_Down = jesdownfile.Get("vbfmutau/singlet")
LFVVBF126_shape_JES_Down = jesdownfile.Get("vbfmutau/LFVVBF126")
LFVGG126_shape_JES_Down = jesdownfile.Get("vbfmutau/LFVGG126")
SMVBF126_shape_JES_Down = jesdownfile.Get("vbfmutau/SMVBF126")
SMGG126_shape_JES_Down = jesdownfile.Get("vbfmutau/SMGG126")
LFVVBF_shape_JES_Down = jesdownfile.Get("vbfmutau/LFVVBF")
LFVGG_shape_JES_Down = jesdownfile.Get("vbfmutau/LFVGG")
SMVBF_shape_JES_Down = jesdownfile.Get("vbfmutau/SMVBF")
SMGG_shape_JES_Down = jesdownfile.Get("vbfmutau/SMGG")

LFVVBF126_shape_JES_Down.Scale(10)
LFVGG126_shape_JES_Down.Scale(10)
LFVVBF_shape_JES_Down.Scale(10)
LFVGG_shape_JES_Down.Scale(10)

ztautau_shape_TES_Up = tesupfile.Get("vbfmutau/ztautau")
zjetsother_shape_TES_Up = tesupfile.Get("vbfmutau/zjetsother")
ttbar_shape_TES_Up = tesupfile.Get("vbfmutau/ttbar")
ww_shape_TES_Up = tesupfile.Get("vbfmutau/ww")
singlet_shape_TES_Up = tesupfile.Get("vbfmutau/singlet")
LFVVBF126_shape_TES_Up = tesupfile.Get("vbfmutau/LFVVBF126")
LFVGG126_shape_TES_Up = tesupfile.Get("vbfmutau/LFVGG126")
SMVBF126_shape_TES_Up = tesupfile.Get("vbfmutau/SMVBF126")
SMGG126_shape_TES_Up = tesupfile.Get("vbfmutau/SMGG126")
LFVVBF_shape_TES_Up = tesupfile.Get("vbfmutau/LFVVBF")
LFVGG_shape_TES_Up = tesupfile.Get("vbfmutau/LFVGG")
SMVBF_shape_TES_Up = tesupfile.Get("vbfmutau/SMVBF")
SMGG_shape_TES_Up = tesupfile.Get("vbfmutau/SMGG")

LFVVBF126_shape_TES_Up.Scale(10)
LFVGG126_shape_TES_Up.Scale(10)
LFVVBF_shape_TES_Up.Scale(10)
LFVGG_shape_TES_Up.Scale(10)

ztautau_shape_TES_Down = tesdownfile.Get("vbfmutau/ztautau")
zjetsother_shape_TES_Down = tesdownfile.Get("vbfmutau/zjetsother")
ttbar_shape_TES_Down = tesdownfile.Get("vbfmutau/ttbar")
ww_shape_TES_Down = tesdownfile.Get("vbfmutau/ww")
singlet_shape_TES_Down = tesdownfile.Get("vbfmutau/singlet")
LFVVBF126_shape_TES_Down = tesdownfile.Get("vbfmutau/LFVVBF126")
LFVGG126_shape_TES_Down = tesdownfile.Get("vbfmutau/LFVGG126")
SMVBF126_shape_TES_Down = tesdownfile.Get("vbfmutau/SMVBF126")
SMGG126_shape_TES_Down = tesdownfile.Get("vbfmutau/SMGG126")
LFVVBF_shape_TES_Down = tesdownfile.Get("vbfmutau/LFVVBF")
LFVGG_shape_TES_Down = tesdownfile.Get("vbfmutau/LFVGG")
SMVBF_shape_TES_Down = tesdownfile.Get("vbfmutau/SMVBF")
SMGG_shape_TES_Down = tesdownfile.Get("vbfmutau/SMGG")

LFVVBF126_shape_TES_Down.Scale(10)
LFVGG126_shape_TES_Down.Scale(10)
LFVVBF_shape_TES_Down.Scale(10)
LFVGG_shape_TES_Down.Scale(10)



##create root file with yields for datacards
outfile = ROOT.TFile("LFV_"+channel+"_jesshape_tesshape.root","RECREATE")
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

ztautau_shape_JES_Up.Write("ztautau_shape_JESUp")
zjetsother_shape_JES_Up.Write("zjetsother_shape_JESUp")
ttbar_shape_JES_Up.Write("ttbar_shape_JESUp")
ww_shape_JES_Up.Write("ww_shape_JESUp")
singlet_shape_JES_Up.Write("singlet_shape_JESUp")
LFVVBF126_shape_JES_Up.Write("LFVVBF126_shape_JESUp")
LFVGG126_shape_JES_Up.Write("LFVGG126_shape_JESUp")
SMVBF126_shape_JES_Up.Write("SMVBF126_shape_JESUp")
SMGG126_shape_JES_Up.Write("SMGG126_shape_JESUp")
LFVVBF_shape_JES_Up.Write("LFVVBF_shape_JESUp")
LFVGG_shape_JES_Up.Write("LFVGG_shape_JESUp")
SMVBF_shape_JES_Up.Write("SMVBF_shape_JESUp")
SMGG_shape_JES_Up.Write("SMGG_shape_JESUp")

ztautau_shape_JES_Down.Write("ztautau_shape_JESDown")
zjetsother_shape_JES_Down.Write("zjetsother_shape_JESDown")
ttbar_shape_JES_Down.Write("ttbar_shape_JESDown")
ww_shape_JES_Down.Write("ww_shape_JESDown")
singlet_shape_JES_Down.Write("singlet_shape_JESDown")
LFVVBF126_shape_JES_Down.Write("LFVVBF126_shape_JESDown")
LFVGG126_shape_JES_Down.Write("LFVGG126_shape_JESDown")
SMVBF126_shape_JES_Down.Write("SMVBF126_shape_JESDown")
SMGG126_shape_JES_Down.Write("SMGG126_shape_JESDown")
LFVVBF_shape_JES_Down.Write("LFVVBF_shape_JESDown")
LFVGG_shape_JES_Down.Write("LFVGG_shape_JESDown")
SMVBF_shape_JES_Down.Write("SMVBF_shape_JESDown")
SMGG_shape_JES_Down.Write("SMGG_shape_JESDown")


ztautau_shape_TES_Up.Write("ztautau_shape_TESUp")
zjetsother_shape_TES_Up.Write("zjetsother_shape_TESUp")
ttbar_shape_TES_Up.Write("ttbar_shape_TESUp")
ww_shape_TES_Up.Write("ww_shape_TESUp")
singlet_shape_TES_Up.Write("singlet_shape_TESUp")
LFVVBF126_shape_TES_Up.Write("LFVVBF126_shape_TESUp")
LFVGG126_shape_TES_Up.Write("LFVGG126_shape_TESUp")
SMVBF126_shape_TES_Up.Write("SMVBF126_shape_TESUp")
SMGG126_shape_TES_Up.Write("SMGG126_shape_TESUp")
LFVVBF_shape_TES_Up.Write("LFVVBF_shape_TESUp")
LFVGG_shape_TES_Up.Write("LFVGG_shape_TESUp")
SMVBF_shape_TES_Up.Write("SMVBF_shape_TESUp")
SMGG_shape_TES_Up.Write("SMGG_shape_TESUp")

ztautau_shape_TES_Down.Write("ztautau_shape_TESDown")
zjetsother_shape_TES_Down.Write("zjetsother_shape_TESDown")
ttbar_shape_TES_Down.Write("ttbar_shape_TESDown")
ww_shape_TES_Down.Write("ww_shape_TESDown")
singlet_shape_TES_Down.Write("singlet_shape_TESDown")
LFVVBF126_shape_TES_Down.Write("LFVVBF126_shape_TESDown")
LFVGG126_shape_TES_Down.Write("LFVGG126_shape_TESDown")
SMVBF126_shape_TES_Down.Write("SMVBF126_shape_TESDown")
SMGG126_shape_TES_Down.Write("SMGG126_shape_TESDown")
LFVVBF_shape_TES_Down.Write("LFVVBF_shape_TESDown")
LFVGG_shape_TES_Down.Write("LFVGG_shape_TESDown")
SMVBF_shape_TES_Down.Write("SMVBF_shape_TESDown")
SMGG_shape_TES_Down.Write("SMGG_shape_TESDown")
'''
fakes_shape_Bin_Up.Write("fakes_shape_BinUp")
ztautau_shape_Bin_Up.Write("ztautau_shape_BinUp")
zjetsother_shape_Bin_Up.Write("zjetsother_shape_BinUp")
ttbar_shape_Bin_Up.Write("ttbar_shape_BinUp")
ww_shape_Bin_Up.Write("ww_shape_BinUp")
singlet_shape_Bin_Up.Write("singlet_shape_BinUp")
LFVVBF126_shape_Bin_Up.Write("LFVVBF126_shape_BinUp")
LFVGG126_shape_Bin_Up.Write("LFVGG126_shape_BinUp")
SMVBF126_shape_Bin_Up.Write("SMVBF126_shape_BinUp")
SMGG126_shape_Bin_Up.Write("SMGG126_shape_BinUp")
LFVVBF_shape_Bin_Up.Write("LFVVBF_shape_BinUp")
LFVGG_shape_Bin_Up.Write("LFVGG_shape_BinUp")
SMVBF_shape_Bin_Up.Write("SMVBF_shape_BinUp")
SMGG_shape_Bin_Up.Write("SMGG_shape_BinUp")

fakes_shape_Bin_Down.Write("fakes_shape_BinDown")
ztautau_shape_Bin_Down.Write("ztautau_shape_BinDown")
zjetsother_shape_Bin_Down.Write("zjetsother_shape_BinDown")
ttbar_shape_Bin_Down.Write("ttbar_shape_BinDown")
ww_shape_Bin_Down.Write("ww_shape_BinDown")
singlet_shape_Bin_Up.Write("singlet_shape_BinUp")
LFVVBF126_shape_Bin_Down.Write("LFVVBF126_shape_BinDown")
LFVGG126_shape_Bin_Down.Write("LFVGG126_shape_BinDown")
SMVBF126_shape_Bin_Down.Write("SMVBF126_shape_BinDown")
SMGG126_shape_Bin_Down.Write("SMGG126_shape_BinDown")
LFVVBF_shape_Bin_Down.Write("LFVVBF_shape_BinDown")
LFVGG_shape_Bin_Down.Write("LFVGG_shape_BinDown")
SMVBF_shape_Bin_Down.Write("SMVBF_shape_BinDown")
SMGG_shape_Bin_Down.Write("SMGG_shape_BinDown")
'''
outfile.Write()

