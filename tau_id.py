
from sys import argv, stdout, stderr
import ROOT
import sys

##Style##
ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)
if len(argv) < 2:
	print "usage: python tau_id variable"
	sys.exit()
var = argv[1]
shape_norm = True
if shape_norm:
	ynormlabel = "Normalized to 1"
	yoffset = 0.1
else:
	ynormlabel = "Normalized to \sqrt{8} TeV Data"
	yoffset = 10.0
## axis labels
binwidth = 5
datadir = "tau_id_oct3/"
channel = "gg"
savedir = "tau_id_oct3/"
if var == "tDecayMode":
	xlabel = "#tau Decay Mode"
	binwidth = 1
	legend =ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel
elif var == "tPt":
	xlabel = "#tau P_{T} (GeV)"
	legend =ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel + "      5 GeV Binning"
elif var == "tEta":
	xlabel = "#tau #eta"
	legend =ROOT.TLegend(0.67,0.6,0.99,0.88,'','brNDC')
	binwidth = 10
	ylabel = ynormlabel
elif var == "tMtToPfMet_Ty1":
	xlabel = "#tau M_{T} Ty1 (GeV)"
	legend =ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel + "     5 GeV Binning"
elif var == "mCharge":
	xlabel = "#mu Charge"
	legend =ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel
	binwidth = 1
elif var == "tCharge":
	xlabel = "#tau Charge"
	legend =ROOT.TLegend(0.15,0.6,0.45,0.8,'','brNDC')
	ylabel = ynormlabel
	binwidth = 1
else:
	xlabel = var
	binwidth = 5
	legend =ROOT.TLegend(0.45,0.6,0.8,0.8,'','brNDC')
	ylabel = ynormlabel

canvas = ROOT.TCanvas("canvas","canvas",800,800)
hgglfv_ntuple_file_str = 'LFV_GluGlu_H2Tau_M-126.root'
hvbflfv_ntuple_file_str = 'LFV_VBF_H2Tau_M-126.root'
hvbflfv_pm_ntuple_file_str ='LFV_VBF_HMuPlusTauMinus.root'
hvbflfv_mp_ntuple_file_str ='LFV_VBF_HMuMinusTauPlus.root'
hgglfv_pm_ntuple_file_str = 'LFV_GGH_HMuPlusTauMinus.root'
hgglfv_mp_ntuple_file_str = 'LFV_GGH_HMuMinusTauPlus.root'
suvadeep_vbf_ntuple_file_str = 'SuvadeepVBF.root'
suvadeep_gg_ntuple_file_str = 'SuvadeepGG.root'

hgglfv_ntuple_file = ROOT.TFile(datadir+hgglfv_ntuple_file_str)
hvbflfv_ntuple_file = ROOT.TFile(datadir+hvbflfv_ntuple_file_str)
hvbflfv_pm_ntuple_file = ROOT.TFile(datadir+hvbflfv_pm_ntuple_file_str)
hvbflfv_mp_ntuple_file = ROOT.TFile(datadir+hvbflfv_mp_ntuple_file_str)
hgglfv_pm_ntuple_file = ROOT.TFile(datadir+hgglfv_pm_ntuple_file_str)
hgglfv_mp_ntuple_file = ROOT.TFile(datadir+hgglfv_mp_ntuple_file_str)
suvadeep_vbf_ntuple_file = ROOT.TFile(datadir+suvadeep_vbf_ntuple_file_str)
suvadeep_gg_ntuple_file = ROOT.TFile(datadir+suvadeep_gg_ntuple_file_str)

ntuple_spot = channel
hgglfv = hgglfv_ntuple_file.Get(channel+"/"+var).Clone()
hvbflfv = hvbflfv_ntuple_file.Get(channel+"/"+var).Clone()
hvbflfv_pm = hvbflfv_pm_ntuple_file.Get(channel+"/"+var).Clone()
hvbflfv_mp = hvbflfv_mp_ntuple_file.Get(channel+"/"+var).Clone()
hgglfv_pm = hgglfv_pm_ntuple_file.Get(channel+"/"+var).Clone()
hgglfv_mp = hgglfv_mp_ntuple_file.Get(channel+"/"+var).Clone()
suvadeep_vbf = suvadeep_vbf_ntuple_file.Get(channel+"/"+var).Clone()
suvadeep_gg = suvadeep_gg_ntuple_file.Get(channel+"/"+var).Clone()

hgglfv_lumifile = 'lumicalc/LFV_GluGlu_H2Tau_M-126.lumicalc.sum'
hvbflfv_lumifile = 'lumicalc/LFV_VBF_H2Tau_M-126.lumicalc.sum'
hgglfv_pm_lumifile = 'lumicalc/LFV_GGH_HMuPlusTauMinus_M-126.lumicalc.sum'
hvbflfv_pm_lumifile = 'lumicalc/LFV_VBF_HMuPlusTauMinus_M-126.lumicalc.sum'
hgglfv_mp_lumifile = 'lumicalc/LFV_GGH_HMuMinusTauPlus_M-126.lumicalc.sum'
hvbflfv_mp_lumifile = 'lumicalc/LFV_VBF_HMuMinusTauPlus_M-126.lumicalc.sum'

f = open(hgglfv_lumifile).read().splitlines()
hgglfv_efflumi = float(f[0])

f = open(hvbflfv_lumifile).read().splitlines()
hvbflfv_efflumi = float(f[0])

f = open(hgglfv_pm_lumifile).read().splitlines()
hgglfv_pm_efflumi = float(f[0])

f = open(hvbflfv_pm_lumifile).read().splitlines()
hvbflfv_pm_efflumi = float(f[0])

f = open(hgglfv_mp_lumifile).read().splitlines()
hgglfv_mp_efflumi = float(f[0])

f = open(hvbflfv_mp_lumifile).read().splitlines()
hvbflfv_mp_efflumi = float(f[0])

lumi = 18025.9 #inverse picobarns
#hgglfv_efflumi= 509885.536 #1.922 pb xsection
#hgglfv_pm_efflumi = 101041.666667
#hgglfv_mp_efflumi = 157291.666667
#hvbflfv_efflumi = 6369426.75159  #0.157 pb xsection
#hvbflfv_pm_efflumi = 1242038.21656
#hvbflfv_mp_efflumi = 1242038.21656

if shape_norm == False:
	hvbflfv_pm_norm = lumi/hvbflfv_pm_efflumi
	hvbflfv_mp_norm = lumi/hvbflfv_mp_efflumi
	hgglfv_pm_norm = lumi/hgglfv_pm_efflumi
	hgglfv_mp_norm = lumi/hgglfv_mp_efflumi
	hgglfv_norm = lumi/hgglfv_efflumi
	hvbflfv_norm = lumi/hvbflfv_efflumi

else:
#	if var == 'mCharge':
		
	hgglfv_norm = 1/(hgglfv.Integral())
	hvbflfv_norm = 1/(hvbflfv.Integral())
	hgglfv_pm_norm = 1/(hgglfv_pm.Integral())
	hgglfv_mp_norm = 1/(hgglfv_mp.Integral())
	hvbflfv_pm_norm = 1/(hvbflfv_pm.Integral())
	hvbflfv_mp_norm = 1/(hvbflfv_mp.Integral())
	suvadeep_vbf_norm = 1/(suvadeep_vbf.Integral())
	suvadeep_gg_norm = 1/(suvadeep_gg.Integral())

hgglfv.Scale(hgglfv_norm)
hvbflfv.Scale(hvbflfv_norm)
hgglfv_pm.Scale(hgglfv_pm_norm)
hvbflfv_pm.Scale(hvbflfv_pm_norm)
hgglfv_mp.Scale(hgglfv_mp_norm)
hvbflfv_mp.Scale(hvbflfv_mp_norm)
suvadeep_vbf.Scale(suvadeep_vbf_norm)
suvadeep_gg.Scale(suvadeep_gg_norm)

hgglfv.SetLineColor(ROOT.EColor.kBlue+1)
hvbflfv.SetLineColor(ROOT.EColor.kBlue+1)
hgglfv.SetMarkerSize(0)
hvbflfv.SetMarkerSize(0)
hgglfv.SetLineWidth(3)
hvbflfv.SetLineWidth(3)
hgglfv_pm.SetLineColor(ROOT.EColor.kGreen+3)
hvbflfv_pm.SetLineColor(ROOT.EColor.kGreen+3)
hgglfv_pm.SetMarkerSize(0)
hvbflfv_pm.SetMarkerSize(0)
hgglfv_pm.SetLineWidth(3)
hvbflfv_pm.SetLineWidth(3)
hgglfv_mp.SetLineColor(ROOT.EColor.kRed+1)
hvbflfv_mp.SetLineColor(ROOT.EColor.kRed+1)
hgglfv_mp.SetMarkerSize(0)
hvbflfv_mp.SetMarkerSize(0)
hgglfv_mp.SetLineWidth(3)
hvbflfv_mp.SetLineWidth(3)
suvadeep_gg.SetLineColor(ROOT.EColor.kCyan+1)
suvadeep_vbf.SetLineColor(ROOT.EColor.kCyan+1)
suvadeep_gg.SetMarkerSize(0)
suvadeep_vbf.SetMarkerSize(0)
suvadeep_gg.SetLineWidth(3)
suvadeep_vbf.SetLineWidth(3)
#print binwidth
hgglfv.Rebin(binwidth)
hvbflfv.Rebin(binwidth)
hgglfv_pm.Rebin(binwidth)
hvbflfv_pm.Rebin(binwidth)
hgglfv_mp.Rebin(binwidth)
hvbflfv_mp.Rebin(binwidth)
suvadeep_gg.Rebin(binwidth)
suvadeep_vbf.Rebin(binwidth)

##maximum y value for plotting
hgglfv_ymax = hgglfv.GetMaximum()
hgglfv_pm_ymax = hgglfv_pm.GetMaximum()
hgglfv_mp_ymax = hgglfv_mp.GetMaximum()
suvadeep_gg_ymax = suvadeep_gg.GetMaximum()

hvbflfv_ymax = hvbflfv.GetMaximum()
hvbflfv_pm_ymax = hvbflfv_pm.GetMaximum()
hvbflfv_mp_ymax = hvbflfv_mp.GetMaximum()
suvadeep_vbf_ymax = suvadeep_vbf.GetMaximum()


if channel == "gg":
	legend.AddEntry(hgglfv,'GG LFV Higgs')
	legend.AddEntry(hgglfv_pm,'GG LFV Higgs #mu+ #tau-')
	legend.AddEntry(hgglfv_mp,'GG LFV Higgs #tau+ #mu-')
	legend.AddEntry(suvadeep_gg,'New October GG Ntuples') 
	print hgglfv.Integral()
	hgglfv.Draw('hist')
	print hgglfv_pm.Integral()
	hgglfv_pm.Draw('sameshist')
	print hgglfv_mp.Integral()
	hgglfv_mp.Draw('sameshist')
	suvadeep_gg.Draw('sameshist')
        print hgglfv.Integral()
        print hgglfv_pm.Integral()
        print hgglfv_mp.Integral()	
        hgglfv.SetTitle("#tau ID Comparison in " + channel + " channel  "+ ylabel )
        hgglfv.GetXaxis().SetTitle(xlabel)
	hgglfv.GetXaxis().SetTitleOffset(0.8)
	ymax = max(hgglfv_ymax, hgglfv_pm_ymax, hgglfv_mp_ymax,suvadeep_gg_ymax) + yoffset
        hgglfv.SetMaximum(ymax)
if channel == "vbf":
	print hvbflfv.Integral()
	hvbflfv.Draw('hist')
	print hvbflfv_pm.Integral()
	if var == 'mCharge' or var == "tCharge":
        	hvbflfv_pm.SetMarkerSize(5)
        	hvbflfv_pm.SetMarkerStyle(2)
		hvbflfv_pm.Draw('sames')
	else:
		hvbflfv_pm.Draw('sameshist')
        legend.AddEntry(hvbflfv, 'VBF LFV Higgs')
        legend.AddEntry(hvbflfv_pm,'VBF LFV Higgs #mu+ #tau-')
        legend.AddEntry(hvbflfv_mp,'VBF LFV Higgs #tau+ #mu-')
	legend.AddEntry(suvadeep_vbf,'New October VBF Ntuples')
	print hvbflfv_mp.Integral()
	hvbflfv_mp.Draw('sameshist')
	suvadeep_vbf.Draw('sameshist')
	print hvbflfv.Integral()
	print hvbflfv_pm.Integral()
	print hvbflfv_mp.Integral()
	hvbflfv.SetTitle("#tau ID Comparison in " + channel + " channel  "+ylabel)
        ymax = max(hvbflfv_ymax,hvbflfv_pm_ymax,hvbflfv_mp_ymax,suvadeep_vbf_ymax) + yoffset
	hvbflfv.GetXaxis().SetTitle(xlabel)
	hvbflfv.SetMaximum(ymax)
	hvbflfv.GetXaxis().SetTitleOffset(0.8)

legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.Draw('sames')
if shape_norm == False:
	canvas.SaveAs(savedir+"TauID"+var+channel+".png")
else:
	canvas.SaveAs(savedir+"TauID"+var+channel+"_shape.png")

