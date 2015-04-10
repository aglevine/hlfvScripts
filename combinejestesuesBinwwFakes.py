from sys import argv
import ROOT
import sys
import math
import array
import numpy
import binFactors

def startUnc(channel):
	if channel == "gg1":
        	channelName = "boost"
		ggScale = 1.10
        else:
        	channelName = channel
		if channel == "vbf":
			ggScale = 1.30
		else:
			ggScale = 1.10
        f = open(channelName+'mutau/unc.vals','w')
	f.write(channelName + 'mutau LFVGG,SMGG126,WWGG126 Theo_PDF_gg 1.08\n')
	f.write(channelName + 'mutau LFVVBF,SMVBF126,WWVBF126 Theo_PDF_vbf 1.08\n')
	f.write('\n')
	f.write(channelName + 'mutau LFVGG, LFVVBF, SMGG126, WWGG126, SMVBF126, WWVBF126 Theo_UE 1.04\n')
	f.write('\n')
	f.write(channelName + 'mutau LFVGG,SMGG126, WWGG126 Theo_Scale_gg ' + str(ggScale)+'\n')
	f.write('\n')
	f.write(channelName + 'mutau LFVVBF,SMVBF126, WWVBF126 Theo_Scale_vbf 1.04\n')
	f.write(channelName + 'mutau signal,ww,ttbar,singlet,ztautau,zjetsother,SMVBF126,SMGG126,WWGG126,WWVBF126  lumi 1.026\n') 
	f.write(channelName + 'mutau signal,ww,ttbar,singlet,ztautau,zjetsother,SMVBF126,SMGG126,WWGG126,WWVBF126  Effi_Mu  1.02\n')
	f.write(channelName + 'mutau signal,ww,ttbar,singlet,ztautau,zjetsother,SMVBF126,SMGG126,WWGG126,WWVBF126  Effi_Tau 1.06\n') 
	f.write('\n')
	f.write('\n')
	f.write('\n')
	f.write(channelName + 'mutau ww        Norm_WW       1.15\n')
	f.write(channelName + 'mutau singlet       Norm_TOP      1.10\n')
	f.write(channelName + 'mutau ttbar        Norm_TT       1.10\n')
	f.write(channelName + 'mutau ztautau   Norm_ZTauTau  1.03\n')
	f.write(channelName + 'mutau zjetsother   Norm_ZJetsOther  1.1\n')
	f.write(channelName + 'mutau fakes     Norm_FAKES  1.30\n')
	f.write('\n')
	f.write('\n')
	f.write('\n')
	if channel == "vbf":
		#f.write(channelName + 'mutau signal,ww,singlet,ttbar, SMVBF126,SMGG126 shape_JES 1\n')
		f.write(channelName + 'mutau signal,ww,singlet,ttbar, SMVBF126,SMGG126 shape_MuTau_JES 1\n')
	else:
		#f.write(channelName + 'mutau signal,ww,singlet,ttbar,zjetsother, SMVBF126,SMGG126 shape_JES 1\n')
		f.write(channelName + 'mutau signal,ww,singlet,ttbar,zjetsother,SMVBF126,SMGG126 shape_MuTau_JES 1\n')
	if channel == "vbf":
		f.write(channelName + 'mutau signal,ww,singlet,ttbar, ztautau, SMVBF126,SMGG126 shape_MuTau_TES 1\n')
	else:
		f.write(channelName + 'mutau signal,ww,singlet,ttbar,zjetsother,ztautau, SMVBF126,SMGG126 shape_MuTau_TES 1\n')
	if channel == "vbf":
		f.write(channelName + 'mutau signal,ww,singlet,ttbar,SMVBF126,SMGG126 shape_MuTau_MET 1\n')
	else:
        	f.write(channelName + 'mutau signal,ww,singlet,ttbar,zjetsother,SMVBF126,SMGG126 shape_MuTau_MET 1\n')
	f.write(channelName + 'mutau fakes shape_FAKES 1\n')
	f.write('\n')
	f.write('\n')

	u = open(channelName+'mutau/unc.conf','w')
	u.write('lumi lnN\n')
	u.write('Effi_Mu lnN\n')
	u.write('Effi_Tau lnN\n')
	u.write('\n')
	u.write('Theo_UE lnN\n')
	u.write('\n')
	u.write('Theo_Scale_gg lnN\n')
	u.write('Theo_PDF_gg lnN\n')
	u.write('\n')
        u.write('Theo_Scale_vbf lnN\n')
        u.write('Theo_PDF_vbf lnN\n')
        u.write('\n')
	u.write('Norm_WW lnN\n')
	u.write('Norm_TT lnN\n')
	u.write('Norm_ZTauTau lnN\n')
	u.write('Norm_ZJetsOther lnN\n')
	u.write('Norm_FAKES lnN\n')
	u.write('Norm_SMGG lnN\n')
	u.write('Norm_SMVBF lnN\n')
        u.write('Norm_WWGG lnN\n')
        u.write('Norm_WWVBF lnN\n')
	u.write('Norm_TOP lnN\n')
	u.write('\n')
	u.write('shape_JES_Norm lnN\n')
        u.write('shape_TES_Norm lnN\n')
        u.write('shape_MET_Norm lnN\n')
	u.write('shape_MuTau_JES shape\n')
	u.write('shape_MuTau_TES shape\n')
	u.write('shape_MuTau_MET shape\n')
	u.write('shape_FAKES shape\n')
	u.write('\n')
	
def NoNegBins(histo,histoname,channel):
	for i in range(1,histo.GetNbinsX()+1):
        	if histo.GetBinContent(i) < 0:
                        getbinFactors = "binFactors."+channel+histoname
                        binFactor = eval(getbinFactors)
                        histo.SetBinContent(i,0.92*binFactor)
                        histo.SetBinError(i,1.8*binFactor)
def NoZeroBins(histo,histoname,channel,minbin,maxbin):
        for i in range(minbin,maxbin+1):
                if histo.GetBinContent(i) == 0:
                        getbinFactors = "binFactors."+channel+histoname
                        binFactor = eval(getbinFactors)
                        histo.SetBinContent(i,0.92*binFactor)
                        histo.SetBinError(i,1.8*binFactor)
def fillEmptyBins(histo,histoname,channel,histojesup=None,histojesdown=None,histometup=None,histometdown=None,histotesup=None,histotesdown=None,histofakesdown=None,histofakesup=None):
	NoNegBins(histo,histoname,channel)
	jes = False
	met = False
	tes = False
	fakes = False
	if histoname == "fakes":
		fakes = True
	if histojesup is not None:
		jes = True
		NoNegBins(histojesup,histoname,channel)
		NoNegBins(histojesdown,histoname,channel)
	if histometup is not None:
		met = True
		NoNegBins(histometup,histoname,channel)
		NoNegBins(histometdown,histoname,channel)
	if histotesup is not None:
		tes = True
		NoNegBins(histotesup,histoname,channel)
		NoNegBins(histotesdown,histoname,channel)
	if fakes == True:
		NoNegBins(histofakesup,"fakes",channel)
		NoNegBins(histofakesdown,"fakes",channel)
	if channel == "vbf":
		minFillBin = 1
                maxSysBin = [histo.GetNbinsX()]
                if jes == True:
                        maxSysBin.append(histojesup.GetNbinsX())
                        maxSysBin.append(histojesdown.GetNbinsX())
                if met == True:
                        maxSysBin.append(histometup.GetNbinsX())
                        maxSysBin.append(histometdown.GetNbinsX())
                if tes == True:
                        maxSysBin.append(histotesup.GetNbinsX())
                        maxSysBin.append(histotesdown.GetNbinsX())
		if fakes == True:
                        maxSysBin.append(histofakesup.GetNbinsX())
                        maxSysBin.append(histofakesdown.GetNbinsX())
		maxFillBin = max(maxSysBin)
	else:
		minSysBin = [histo.FindFirstBinAbove()]
		if jes == True:
			minSysBin.append(histojesup.FindFirstBinAbove())
			minSysBin.append(histojesdown.FindFirstBinAbove())
                if met == True:
                        minSysBin.append(histometup.FindFirstBinAbove())
                        minSysBin.append(histometdown.FindFirstBinAbove())
                if tes == True:
                        minSysBin.append(histotesup.FindFirstBinAbove())
                        minSysBin.append(histotesdown.FindFirstBinAbove())
		if fakes == True:
                        minSysBin.append(histofakesup.FindFirstBinAbove())
                        minSysBin.append(histofakesdown.FindFirstBinAbove())
		minFillBin = min(minSysBin)
                maxSysBin = [histo.FindLastBinAbove()]
                if jes == True:
                        maxSysBin.append(histojesup.FindLastBinAbove())
                        maxSysBin.append(histojesdown.FindLastBinAbove())
                if met == True:
                        maxSysBin.append(histometup.FindLastBinAbove())
                        maxSysBin.append(histometdown.FindLastBinAbove())
                if tes == True:
                        maxSysBin.append(histotesup.FindLastBinAbove())
                        maxSysBin.append(histotesdown.FindLastBinAbove())
		if fakes == True:
                        maxSysBin.append(histofakesup.FindLastBinAbove())
                        maxSysBin.append(histofakesdown.FindLastBinAbove())
                maxFillBin = max(maxSysBin)
	NoZeroBins(histo,histoname,channel,minFillBin,maxFillBin)
        if jes == True:
                NoZeroBins(histojesup,histoname,channel,minFillBin,maxFillBin)
                NoZeroBins(histojesdown,histoname,channel,minFillBin,maxFillBin)
        if met == True:
                NoZeroBins(histometup,histoname,channel,minFillBin,maxFillBin)
                NoZeroBins(histometdown,histoname,channel,minFillBin,maxFillBin)
        if tes ==True:
                NoZeroBins(histotesup,histoname,channel,minFillBin,maxFillBin)
                NoZeroBins(histotesdown,histoname,channel,minFillBin,maxFillBin)
	if fakes == True:
                NoZeroBins(histofakesup,histoname,channel,minFillBin,maxFillBin)
                NoZeroBins(histofakesdown,histoname,channel,minFillBin,maxFillBin)
	
def makeBinShape(histo,histoname,outfile,channel):
        for i in range (histo.FindFirstBinAbove(),histo.FindLastBinAbove()+1):
                if histo.GetBinContent(i) !=0:
                        #print histoname
                        #print i
                        histoBin_up = histo.Clone()
                        histoBin_down = histo.Clone()
                        histoBin_up.SetBinContent(i,(histo.GetBinContent(i)+histo.GetBinError(i)))
                        histoBin_down.SetBinContent(i,(histo.GetBinContent(i)-histo.GetBinError(i)))
			if histoBin_down.GetBinContent(i) < 0:
				histoBin_down.SetBinContent(i,0)
			if channel == "vbf":
				channelLabel = "muhad_2Jets"
			elif channel == "gg1":
				channelLabel = "muhad_1Jet"
			elif channel == "gg0":
				channelLabel = "muhad_0Jet"
                        binName = "Stat_"+channelLabel+"_"+histoname+"_bin"+str(i)
                        histoBin_up.Write(histoname+"_"+binName+"Up")
                        histoBin_down.Write(histoname+"_"+binName+"Down")
                        if channel == "gg1":
                                channelName = "boost"
                        else:
                                channelName = channel
			#print channelName+'mutau/unc.conf'
			f = open(channelName+'mutau/unc.conf','a')
			f.write(binName+" shape\n")
			f.close()
			u= open(channelName+'mutau/unc.vals','a')
			u.write(channelName+'mutau '+histoname+' '+binName+' 1\n')
			u.close()

def writeUpDownNorm(histo,histoUp,histoDown,histoname,channel,sys):
	if histo.Integral() == 0:
		return
	shiftUp = (histoUp.Integral()-histo.Integral())/histo.Integral()+1
	shiftDown = (histoDown.Integral()-histo.Integral())/histo.Integral()+1
        if channel == "gg1":
        	channelName = "boost"
        else:
        	channelName = channel
	u = open(channelName+'mutau/unc.vals','a')
	if sys == "jes":
		normName = 'shape_JES_Norm'
	elif sys == "tes":
		normName = 'shape_TES_Norm'
	elif sys == "ues":
		normName = 'shape_MET_Norm'
	else:
		print "Error: Unknown systematic"
		sys.exit()
	diffUp = histoUp.Integral()/histo.Integral()
	diffUp = abs(1-diffUp) + 1
	#print diffUp
        diffDown = histoDown.Integral()/histo.Integral()
	diffDown = abs(1-diffDown) + 1
	#print diffDown
	diff = max(diffUp,diffDown)
	strDiff = channelName+'mutau '+histoname+' '+normName + ' %f \n'%(diff)
	print channel + " " + sys + " "+ histoname+ " " +str(diff)
	u.write(strDiff)
	

#nonedir = "jesnonesignalFeb26_01JetFix/"
nonedir = "jespfMetOct7/"
#nonedir = "signal_March31_SOverSPlusB/"
#nonedir = "signal_March31_BR1/"
#nonedir = "signal_March31_retest/"
jesupdir = "jesplussignalFeb26_01JetFix/"
jesdowndir = "jesminussignalFeb26_01JetFix/"
uesupdir = "uesplussignalApr26/"
uesdowndir = "uesminussignalApr26/"
tesupdir = "tesup_signal_March9/"
tesdowndir = "tesdown_signal_March9/"
fakesupdir = "fakeShapeShiftUp_May7/"
fakesdowndir = "fakeShapeShiftDown_May7/"
doLoose = False

channel = argv[1]
if channel == "vbf":
	binwidth = 50
else:
	binwidth = 10

startUnc(channel)

#nonefile_str = "LFV_" + channel+"_collMass_type1_fakeRate_zjetsEmbed_newSignal_jesnone_singletfix.root"
nonefile_str = "LFV_" + channel+"_collMass_fakeRate_zjetsEmbed_newSignal.root"
jesupfile_str = "LFV_" + channel+"_collMass_jes_plus_fakeRate_zjetsEmbed_newSignal_jesplus_singletfix.root"
jesdownfile_str = "LFV_" + channel+"_collMass_jes_minus_fakeRate_zjetsEmbed_newSignal_jesminus_singletfix.root"
uesupfile_str = "LFV_" + channel+"_collMass_type1_ues_plus_fakeRate_zjetsEmbed_newSignal_singletfix.root"
uesdownfile_str = "LFV_" + channel+"_collMass_type1_ues_minus_fakeRate_zjetsEmbed_newSignal_singletfix.root"
tesupfile_str = "LFV_" + channel+"_collMass_type1_fakeRate_zjetsEmbed_newSignal_singletfix.root"
tesdownfile_str = "LFV_" + channel+"_collMass_type1_fakeRate_zjetsEmbed_newSignal_singletfix.root"
fakesupfile_str = "LFV_" + channel+"_collMass_type1_fakeRate_zjetsEmbed_newSignal_singletfix.root"
fakesdownfile_str = "LFV_" + channel+"_collMass_type1_fakeRate_zjetsEmbed_newSignal_singletfix.root"

nonefile = ROOT.TFile(nonedir+nonefile_str)
jesupfile = ROOT.TFile(jesupdir+jesupfile_str)
jesdownfile = ROOT.TFile(jesdowndir+jesdownfile_str)
uesupfile = ROOT.TFile(uesupdir+uesupfile_str)
uesdownfile = ROOT.TFile(uesdowndir+uesdownfile_str)
tesupfile = ROOT.TFile(tesupdir+tesupfile_str)
tesdownfile = ROOT.TFile(tesdowndir+tesdownfile_str)
fakesupfile = ROOT.TFile(fakesupdir+fakesupfile_str)
fakesdownfile = ROOT.TFile(fakesdowndir+fakesdownfile_str)
ttbarfullLoose_file = ROOT.TFile("LooseCentral_May25/TTJets_FullLeptMGDecays_8TeV-madgraph-tauola.root")
ttbarsemiLoose_file = ROOT.TFile("LooseCentral_May25/TTJets_SemiLeptMGDecays_8TeV-madgraph-tauola.root")
wwLoose_file = ROOT.TFile("LooseCentral_May25/WWJetsTo2L2Nu_TuneZ2_8TeV.root")
ttLoose_file = ROOT.TFile("LooseCentral_May25/T_t-channel.root")
tbartLoose_file = ROOT.TFile("LooseCentral_May25/Tbar_t-channel.root")
twLoose_file = ROOT.TFile("LooseCentral_May25/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola.root")
tbarwLoose_file = ROOT.TFile("LooseCentral_May25/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola.root")
dy1otherLoose_file = ROOT.TFile('LooseCentral_May25/OtherDY1.root')
dy2otherLoose_file = ROOT.TFile('LooseCentral_May25/OtherDY2.root')
dy3otherLoose_file = ROOT.TFile('LooseCentral_May25/OtherDY3.root')
dy4otherLoose_file = ROOT.TFile('LooseCentral_May25/OtherDY4.root')
zjetsotherMCLoose_file = ROOT.TFile('LooseCentral_May25/OtherM50.root')
ttbarfullLooseJesUp_file = ROOT.TFile("LooseJesUp_May25/TTJets_FullLeptMGDecays_8TeV-madgraph-tauola.root")
ttbarsemiLooseJesUp_file = ROOT.TFile("LooseJesUp_May25/TTJets_SemiLeptMGDecays_8TeV-madgraph-tauola.root")
wwLooseJesUp_file = ROOT.TFile("LooseJesUp_May25/WWJetsTo2L2Nu_TuneZ2_8TeV.root")
ttLooseJesUp_file = ROOT.TFile("LooseJesUp_May25/T_t-channel.root")
tbartLooseJesUp_file = ROOT.TFile("LooseJesUp_May25/Tbar_t-channel.root")
twLooseJesUp_file = ROOT.TFile("LooseJesUp_May25/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola.root")
tbarwLooseJesUp_file = ROOT.TFile("LooseJesUp_May25/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola.root")
dy1otherLooseJesUp_file = ROOT.TFile('LooseJesUp_May25/OtherDY1.root')
dy2otherLooseJesUp_file = ROOT.TFile('LooseJesUp_May25/OtherDY2.root')
dy3otherLooseJesUp_file = ROOT.TFile('LooseJesUp_May25/OtherDY3.root')
dy4otherLooseJesUp_file = ROOT.TFile('LooseJesUp_May25/OtherDY4.root')
zjetsotherMCLooseJesUp_file = ROOT.TFile('LooseJesUp_May25/OtherM50.root')
ttbarfullLooseJesDown_file = ROOT.TFile("LooseJesDown_May25/TTJets_FullLeptMGDecays_8TeV-madgraph-tauola.root")
ttbarsemiLooseJesDown_file = ROOT.TFile("LooseJesDown_May25/TTJets_SemiLeptMGDecays_8TeV-madgraph-tauola.root")
wwLooseJesDown_file = ROOT.TFile("LooseJesDown_May25/WWJetsTo2L2Nu_TuneZ2_8TeV.root")
ttLooseJesDown_file = ROOT.TFile("LooseJesDown_May25/T_t-channel.root")
tbartLooseJesDown_file = ROOT.TFile("LooseJesDown_May25/Tbar_t-channel.root")
twLooseJesDown_file = ROOT.TFile("LooseJesDown_May25/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola.root")
tbarwLooseJesDown_file = ROOT.TFile("LooseJesDown_May25/Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola.root")
dy1otherLooseJesDown_file = ROOT.TFile('LooseJesDown_May25/OtherDY1.root')
dy2otherLooseJesDown_file = ROOT.TFile('LooseJesDown_May25/OtherDY2.root')
dy3otherLooseJesDown_file = ROOT.TFile('LooseJesDown_May25/OtherDY3.root')
dy4otherLooseJesDown_file = ROOT.TFile('LooseJesDown_May25/OtherDY4.root')
zjetsotherMCLooseJesDown_file = ROOT.TFile('LooseJesDown_May25/OtherM50.root')



if channel == "vbf":
	dirname = "vbfmutau"
elif channel == "gg1":
	dirname = "boostmutau"
elif channel == "gg0":
	dirname = "gg0mutau"

lumidir = 'lumicalc_jes/'
data1_lumifile = lumidir + 'data_SingleMu_Run2012A_22Jan2013_v1_2.lumicalc.sum'
data2_lumifile = lumidir + 'data_SingleMu_Run2012B_22Jan2013_v1_2.lumicalc.sum'
data3_lumifile = lumidir + 'data_SingleMu_Run2012C_22Jan2013_v1_2.lumicalc.sum'
data4_lumifile = lumidir + 'data_SingleMu_Run2012D_22Jan2013_v1.lumicalc.sum'
ttbar_full_lumifile = lumidir + 'TTJets_FullLeptMGDecays_8TeV-madgraph-tauola.lumicalc.sum'
ttbar_semi_lumifile = lumidir + 'TTJets_SemiLeptMGDecays_8TeV-madgraph-tauola.lumicalc.sum'
ww_lumifile = lumidir + 'WWJetsTo2L2Nu_TuneZ2_8TeV.lumicalc.sum'
tt_lumifile = lumidir + 'T_t-channel.lumicalc.sum'
tbart_lumifile = lumidir + 'Tbar_t-channel.lumicalc.sum'
tw_lumifile = lumidir + 'T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola.lumicalc.sum'
tbarw_lumifile = lumidir + 'Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola.lumicalc.sum'
dy1jets_lumifile = lumidir + 'DY1Jets_madgraph.lumicalc.sum'
dy2jets_lumifile = lumidir + 'DY2Jets_madgraph.lumicalc.sum'
dy3jets_lumifile = lumidir + 'DY3Jets_madgraph.lumicalc.sum'
dy4jets_lumifile = lumidir + 'DY4Jets_madgraph.lumicalc.sum'
zjets_lumifile = lumidir + 'Zjets_M50.lumicalc.sum'

f = open(data1_lumifile).read().splitlines()
data1_lumi = float(f[0])

f = open(data2_lumifile).read().splitlines()
data2_lumi = float(f[0])

f = open(data3_lumifile).read().splitlines()
data3_lumi = float(f[0])

f = open(data4_lumifile).read().splitlines()
data4_lumi = float(f[0])

f = open(ttbar_semi_lumifile).read().splitlines()
ttbar_semi_efflumi = float(f[0])

f = open(ttbar_full_lumifile).read().splitlines()
ttbar_full_efflumi = float(f[0])

f = open(ww_lumifile).read().splitlines()
ww_efflumi = float(f[0])

f = open(tt_lumifile).read().splitlines()
tt_efflumi = float(f[0])

f = open(tbart_lumifile).read().splitlines()
tbart_efflumi = float(f[0])

f = open(tw_lumifile).read().splitlines()
tw_efflumi = float(f[0])

f = open(tbarw_lumifile).read().splitlines()
tbarw_efflumi = float(f[0])

f = open(dy1jets_lumifile).read().splitlines()
dy1jets_efflumi = float(f[0])

f = open(dy2jets_lumifile).read().splitlines()
dy2jets_efflumi = float(f[0])

f = open(dy3jets_lumifile).read().splitlines()
dy3jets_efflumi = float(f[0])

f = open(dy3jets_lumifile).read().splitlines()
dy4jets_efflumi = float(f[0])

f = open(zjets_lumifile).read().splitlines()
zjets_efflumi = float(f[0])

lumi = data1_lumi+data2_lumi+data3_lumi+data4_lumi
ttbarsemiNorm = lumi/ttbar_semi_efflumi
ttbarfullNorm = lumi/ttbar_full_efflumi
wwNorm = lumi/ww_efflumi
ttNorm = lumi/tt_efflumi
tbartNorm = lumi/tbart_efflumi
twNorm = lumi/tw_efflumi
tbarwNorm = lumi/tbarw_efflumi
dy1jetsNorm = lumi/dy1jets_efflumi
dy2jetsNorm = lumi/dy2jets_efflumi
dy3jetsNorm = lumi/dy3jets_efflumi
dy4jetsNorm = lumi/dy4jets_efflumi
zjetsNorm = lumi/zjets_efflumi

ttbarfullLoose = ttbarfullLoose_file.Get(channel+"NoTauIso/collMass_type1")
ttbarfullLoose.Scale(ttbarfullNorm)
ttbarsemiLoose = ttbarsemiLoose_file.Get(channel+"NoTauIso/collMass_type1")
ttbarsemiLoose.Scale(ttbarsemiNorm)
ttbarLoose = ttbarfullLoose.Clone()
ttbarLoose.Add(ttbarsemiLoose)
ttbarLoose.Rebin(binwidth)
ttLoose = ttLoose_file.Get(channel+"NoTauIso/collMass_type1")
tbartLoose = tbartLoose_file.Get(channel+"NoTauIso/collMass_type1")
twLoose = twLoose_file.Get(channel+"NoTauIso/collMass_type1")
tbarwLoose = tbarwLoose_file.Get(channel+"NoTauIso/collMass_type1")
ttLoose.Scale(ttNorm)
tbartLoose.Scale(tbartNorm)
twLoose.Scale(twNorm)
tbarwLoose.Scale(tbarwNorm)
singletLoose = ttLoose.Clone()
singletLoose.Add(tbartLoose)
singletLoose.Add(twLoose)
singletLoose.Add(tbarwLoose)
singletLoose.Rebin(binwidth)
wwLoose = wwLoose_file.Get(channel+"NoTauIso/collMass_type1")
wwLoose.Scale(wwNorm)
wwLoose.Rebin(binwidth)
dy1otherLoose = dy1otherLoose_file.Get(channel+"NoTauIso/collMass_type1")
dy2otherLoose = dy2otherLoose_file.Get(channel+"NoTauIso/collMass_type1")
dy3otherLoose = dy3otherLoose_file.Get(channel+"NoTauIso/collMass_type1")
dy4otherLoose = dy4otherLoose_file.Get(channel+"NoTauIso/collMass_type1")
zjetsotherMCLoose = zjetsotherMCLoose_file.Get(channel+"NoTauIso/collMass_type1")
dy1otherLoose.Scale(dy1jetsNorm)
dy2otherLoose.Scale(dy2jetsNorm)
dy3otherLoose.Scale(dy3jetsNorm)
dy4otherLoose.Scale(dy4jetsNorm)
zjetsotherMCLoose.Scale(zjetsNorm)
zjetsotherLoose = dy1otherLoose.Clone()
zjetsotherLoose.Add(dy2otherLoose)
zjetsotherLoose.Add(dy3otherLoose)
zjetsotherLoose.Add(dy4otherLoose)
zjetsotherLoose.Add(zjetsotherMCLoose)
zjetsotherLoose.Rebin(binwidth)




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
WWVBF126 = nonefile.Get("vbfmutau/WWVBF126")
WWGG126 = nonefile.Get("vbfmutau/WWGG126")
LFVVBF = nonefile.Get("vbfmutau/LFVVBF")
LFVGG = nonefile.Get("vbfmutau/LFVGG")
SMVBF = nonefile.Get("vbfmutau/SMVBF")
SMGG = nonefile.Get("vbfmutau/SMGG")
WWVBF = nonefile.Get("vbfmutau/WWVBF")
WWGG = nonefile.Get("vbfmutau/WWGG")

ttbarfullLooseJesUp = ttbarfullLooseJesUp_file.Get(channel+"NoTauIso/collMass_jes_plus")
ttbarfullLooseJesUp.Scale(ttbarfullNorm)
ttbarsemiLooseJesUp = ttbarsemiLooseJesUp_file.Get(channel+"NoTauIso/collMass_jes_plus")
ttbarsemiLooseJesUp.Scale(ttbarsemiNorm)
ttbarLooseJesUp = ttbarfullLoose.Clone()
ttbarLooseJesUp.Add(ttbarsemiLooseJesUp)
ttbarLooseJesUp.Rebin(binwidth)
ttLooseJesUp = ttLooseJesUp_file.Get(channel+"NoTauIso/collMass_jes_plus")
tbartLooseJesUp = tbartLoose_file.Get(channel+"NoTauIso/collMass_jes_plus")
twLooseJesUp = twLoose_file.Get(channel+"NoTauIso/collMass_jes_plus")
tbarwLooseJesUp = tbarwLooseJesUp_file.Get(channel+"NoTauIso/collMass_jes_plus")
ttLooseJesUp.Scale(ttNorm)
tbartLooseJesUp.Scale(tbartNorm)
twLooseJesUp.Scale(twNorm)
tbarwLooseJesUp.Scale(tbarwNorm)
singletLooseJesUp = ttLooseJesUp.Clone()
singletLooseJesUp.Add(tbartLooseJesUp)
singletLooseJesUp.Add(twLooseJesUp)
singletLooseJesUp.Add(tbarwLooseJesUp)
singletLooseJesUp.Rebin(binwidth)
wwLooseJesUp = wwLooseJesUp_file.Get(channel+"NoTauIso/collMass_jes_plus")
wwLooseJesUp.Scale(wwNorm)
wwLooseJesUp.Rebin(binwidth)
dy1otherLooseJesUp = dy1otherLooseJesUp_file.Get(channel+"NoTauIso/collMass_jes_plus")
dy2otherLooseJesUp = dy2otherLooseJesUp_file.Get(channel+"NoTauIso/collMass_jes_plus")
dy3otherLooseJesUp = dy3otherLooseJesUp_file.Get(channel+"NoTauIso/collMass_jes_plus")
dy4otherLooseJesUp = dy4otherLooseJesUp_file.Get(channel+"NoTauIso/collMass_jes_plus")
zjetsotherMCLooseJesUp = zjetsotherMCLooseJesUp_file.Get(channel+"NoTauIso/collMass_jes_plus")
dy1otherLooseJesUp.Scale(dy1jetsNorm)
dy2otherLooseJesUp.Scale(dy2jetsNorm)
dy3otherLooseJesUp.Scale(dy3jetsNorm)
dy4otherLooseJesUp.Scale(dy4jetsNorm)
zjetsotherMCLooseJesUp.Scale(zjetsNorm)
zjetsotherLooseJesUp = dy1otherLooseJesUp.Clone()
zjetsotherLooseJesUp.Add(dy2otherLooseJesUp)
zjetsotherLooseJesUp.Add(dy3otherLooseJesUp)
zjetsotherLooseJesUp.Add(dy4otherLooseJesUp)
zjetsotherLooseJesUp.Add(zjetsotherMCLooseJesUp)
zjetsotherLooseJesUp.Rebin(binwidth)

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

dy1otherLooseJesDown = dy1otherLooseJesDown_file.Get(channel+"NoTauIso/collMass_jes_minus")
dy2otherLooseJesDown = dy2otherLooseJesDown_file.Get(channel+"NoTauIso/collMass_jes_minus")
dy3otherLooseJesDown = dy3otherLooseJesDown_file.Get(channel+"NoTauIso/collMass_jes_minus")
dy4otherLooseJesDown = dy4otherLooseJesDown_file.Get(channel+"NoTauIso/collMass_jes_minus")
zjetsotherMCLooseJesDown = zjetsotherMCLooseJesDown_file.Get(channel+"NoTauIso/collMass_jes_minus")
dy1otherLooseJesDown.Scale(dy1jetsNorm)
dy2otherLooseJesDown.Scale(dy2jetsNorm)
dy3otherLooseJesDown.Scale(dy3jetsNorm)
dy4otherLooseJesDown.Scale(dy4jetsNorm)
zjetsotherMCLooseJesDown.Scale(zjetsNorm)
zjetsotherLooseJesDown = dy1otherLooseJesDown.Clone()
zjetsotherLooseJesDown.Add(dy2otherLooseJesDown)
zjetsotherLooseJesDown.Add(dy3otherLooseJesDown)
zjetsotherLooseJesDown.Add(dy4otherLooseJesDown)
zjetsotherLooseJesDown.Add(zjetsotherMCLooseJesDown)
zjetsotherLooseJesDown.Rebin(binwidth)

ttbarfullLooseJesDown = ttbarfullLooseJesDown_file.Get(channel+"NoTauIso/collMass_jes_minus")
ttbarfullLooseJesDown.Scale(ttbarfullNorm)
ttbarsemiLooseJesDown = ttbarsemiLooseJesDown_file.Get(channel+"NoTauIso/collMass_jes_minus")
ttbarsemiLooseJesDown.Scale(ttbarsemiNorm)
ttbarLooseJesDown = ttbarfullLoose.Clone()
ttbarLooseJesDown.Add(ttbarsemiLooseJesDown)
ttbarLooseJesDown.Rebin(binwidth)
ttLooseJesDown = ttLooseJesDown_file.Get(channel+"NoTauIso/collMass_jes_minus")
tbartLooseJesDown = tbartLoose_file.Get(channel+"NoTauIso/collMass_jes_minus")
twLooseJesDown = twLoose_file.Get(channel+"NoTauIso/collMass_jes_minus")
tbarwLooseJesDown = tbarwLooseJesDown_file.Get(channel+"NoTauIso/collMass_jes_minus")
ttLooseJesDown.Scale(ttNorm)
tbartLooseJesDown.Scale(tbartNorm)
twLooseJesDown.Scale(twNorm)
tbarwLooseJesDown.Scale(tbarwNorm)
singletLooseJesDown = ttLooseJesDown.Clone()
singletLooseJesDown.Add(tbartLooseJesDown)
singletLooseJesDown.Add(twLooseJesDown)
singletLooseJesDown.Add(tbarwLooseJesDown)
singletLooseJesDown.Rebin(binwidth)
wwLooseJesDown = wwLooseJesDown_file.Get(channel+"NoTauIso/collMass_jes_minus")
wwLooseJesDown.Scale(wwNorm)
wwLooseJesDown.Rebin(binwidth)

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


zjetsother_shape_MET_Up = uesupfile.Get("vbfmutau/zjetsother")
ttbar_shape_MET_Up = uesupfile.Get("vbfmutau/ttbar")
ww_shape_MET_Up = uesupfile.Get("vbfmutau/ww")
singlet_shape_MET_Up = uesupfile.Get("vbfmutau/singlet")
LFVVBF126_shape_MET_Up = uesupfile.Get("vbfmutau/LFVVBF126")
LFVGG126_shape_MET_Up = uesupfile.Get("vbfmutau/LFVGG126")
SMVBF126_shape_MET_Up = uesupfile.Get("vbfmutau/SMVBF126")
SMGG126_shape_MET_Up = uesupfile.Get("vbfmutau/SMGG126")
LFVVBF_shape_MET_Up = uesupfile.Get("vbfmutau/LFVVBF")
LFVGG_shape_MET_Up = uesupfile.Get("vbfmutau/LFVGG")
SMVBF_shape_MET_Up = uesupfile.Get("vbfmutau/SMVBF")
SMGG_shape_MET_Up = uesupfile.Get("vbfmutau/SMGG")

zjetsother_shape_MET_Down = uesdownfile.Get("vbfmutau/zjetsother")
ttbar_shape_MET_Down = uesdownfile.Get("vbfmutau/ttbar")
ww_shape_MET_Down = uesdownfile.Get("vbfmutau/ww")
singlet_shape_MET_Down = uesdownfile.Get("vbfmutau/singlet")
LFVVBF126_shape_MET_Down = uesdownfile.Get("vbfmutau/LFVVBF126")
LFVGG126_shape_MET_Down = uesdownfile.Get("vbfmutau/LFVGG126")
SMVBF126_shape_MET_Down = uesdownfile.Get("vbfmutau/SMVBF126")
SMGG126_shape_MET_Down = uesdownfile.Get("vbfmutau/SMGG126")
LFVVBF_shape_MET_Down = uesdownfile.Get("vbfmutau/LFVVBF")
LFVGG_shape_MET_Down = uesdownfile.Get("vbfmutau/LFVGG")
SMVBF_shape_MET_Down = uesdownfile.Get("vbfmutau/SMVBF")
SMGG_shape_MET_Down = uesdownfile.Get("vbfmutau/SMGG")

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

fakes_shape_FAKES_Up = fakesupfile.Get("vbfmutau/fakes")
fakes_shape_FAKES_Down = fakesdownfile.Get("vbfmutau/fakes")

##create root file with yields for datacards
outfile = ROOT.TFile(dirname+"/LFV_"+channel+"_jesshape_tesshape_uesshape_fakesshape_binshape.root","RECREATE")
outfile.mkdir(dirname)
outfile.cd(dirname+"/")


fillEmptyBins(fakes,"fakes",channel,
	histofakesup = fakes_shape_FAKES_Up, histofakesdown = fakes_shape_FAKES_Down)
fillEmptyBins(ztautau,"ztautau",channel,histotesup=ztautau_shape_TES_Up,histotesdown=ztautau_shape_TES_Down)
if channel != "vbf":
	fillEmptyBins(zjetsother,"zjetsother",channel,
		histojesup=zjetsother_shape_JES_Up,histojesdown=zjetsother_shape_JES_Down,
                histometup=zjetsother_shape_MET_Up,histometdown=zjetsother_shape_MET_Down,
                histotesup=zjetsother_shape_TES_Up,histotesdown=zjetsother_shape_TES_Down)
	if doLoose == True:
		fillEmptyBins(zjetsotherLoose,"zjetsother",channel,
                	histojesup=zjetsotherLooseJesUp,histojesdown=zjetsotherLooseJesDown,
                	histometup=zjetsother_shape_MET_Up,histometdown=zjetsother_shape_MET_Down,
                	histotesup=zjetsother_shape_TES_Up,histotesdown=zjetsother_shape_TES_Down)
else:
        fillEmptyBins(zjetsother,"zjetsother",channel)
	fillEmptyBins(zjetsotherLoose,"zjetsother",channel)
fillEmptyBins(ttbar,"ttbar",channel,
	histojesup=ttbar_shape_JES_Up,histojesdown=ttbar_shape_JES_Down,
        histometup=ttbar_shape_MET_Up,histometdown=ttbar_shape_MET_Down,
        histotesup=ttbar_shape_TES_Up,histotesdown=ttbar_shape_TES_Down)
fillEmptyBins(ww,"ww",channel,
        histojesup=ww_shape_JES_Up,histojesdown=ww_shape_JES_Down,
        histometup=ww_shape_MET_Up,histometdown=ww_shape_MET_Down,
        histotesup=ww_shape_TES_Up,histotesdown=ww_shape_TES_Down)
fillEmptyBins(singlet,"singlet",channel,
        histojesup=singlet_shape_JES_Up,histojesdown=singlet_shape_JES_Down,
        histometup=singlet_shape_MET_Up,histometdown=singlet_shape_MET_Down,
        histotesup=singlet_shape_TES_Up,histotesdown=singlet_shape_TES_Down)
if doLoose == True:
	fillEmptyBins(ttbarLoose,"ttbar",channel,
        	histojesup=ttbarLooseJesUp,histojesdown=ttbarLooseJesDown,
        	histometup=ttbar_shape_MET_Up,histometdown=ttbar_shape_MET_Down,
        	histotesup=ttbar_shape_TES_Up,histotesdown=ttbar_shape_TES_Down)
	fillEmptyBins(wwLoose,"ww",channel,
        	histojesup=wwLooseJesUp,histojesdown=wwLooseJesDown,
        	histometup=ww_shape_MET_Up,histometdown=ww_shape_MET_Down,
        	histotesup=ww_shape_TES_Up,histotesdown=ww_shape_TES_Down)
	fillEmptyBins(singletLoose,"singlet",channel,
        	histojesup=singletLooseJesUp,histojesdown=singletLooseJesDown,
        	histometup=singlet_shape_MET_Up,histometdown=singlet_shape_MET_Down,
        	histotesup=singlet_shape_TES_Up,histotesdown=singlet_shape_TES_Down)

fillEmptyBins(LFVVBF,"LFVVBF",channel,
        histojesup=LFVVBF_shape_JES_Up,histojesdown=LFVVBF_shape_JES_Down,
        histometup=LFVVBF_shape_MET_Up,histometdown=LFVVBF_shape_MET_Down,
        histotesup=LFVVBF_shape_TES_Up,histotesdown=LFVVBF_shape_TES_Down)
fillEmptyBins(LFVGG,"LFVGG",channel,
        histojesup=LFVGG_shape_JES_Up,histojesdown=LFVGG_shape_JES_Down,
        histometup=LFVGG_shape_MET_Up,histometdown=LFVGG_shape_MET_Down,
        histotesup=LFVGG_shape_TES_Up,histotesdown=LFVGG_shape_TES_Down)
fillEmptyBins(SMVBF126,"SMVBF126",channel,
        histojesup=SMVBF126_shape_JES_Up,histojesdown=SMVBF126_shape_JES_Down,
        histometup=SMVBF126_shape_MET_Up,histometdown=SMVBF126_shape_MET_Down,
        histotesup=SMVBF126_shape_TES_Up,histotesdown=SMVBF126_shape_TES_Down)
fillEmptyBins(SMGG126,"SMGG126",channel,
        histojesup=SMGG126_shape_JES_Up,histojesdown=SMGG126_shape_JES_Down,
        histometup=SMGG126_shape_MET_Up,histometdown=SMGG126_shape_MET_Down,
        histotesup=SMGG126_shape_TES_Up,histotesdown=SMGG126_shape_TES_Down)
fillEmptyBins(WWVBF126,"WWVBF126",channel)
fillEmptyBins(WWGG126,"WWGG126",channel)
	


fakes.Write("fakes")
ztautau.Write("ztautau")
if doLoose == False:
	zjetsother.Write("zjetsother")
	ttbar.Write("ttbar")
	singlet.Write("singlet")
	ww.Write("ww")
else:
	zjetsotherLoose.Scale(zjetsother.Integral()/zjetsotherLoose.Integral())
	zjetsotherLoose.Write("zjetsother")
	ttbarLoose.Scale(ttbar.Integral()/ttbarLoose.Integral())
	ttbarLoose.Write("ttbar")
	singletLoose.Scale(singlet.Integral()/singletLoose.Integral())
	singletLoose.Write("singlet")
	wwLoose.Scale(ww.Integral()/wwLoose.Integral())
	wwLoose.Write("ww")
data_obs.Write("data_obs")
LFVVBF126.Write("LFVVBF126")
LFVGG126.Write("LFVGG126")
SMVBF126.Write("SMVBF126")
SMGG126.Write("SMGG126")
WWVBF126.Write("WWVBF126")
WWGG126.Write("WWGG126")
LFVVBF.Write("LFVVBF")
LFVGG.Write("LFVGG")
SMVBF.Write("SMVBF")
SMGG.Write("SMGG")
WWVBF.Write("WWVBF")
WWGG.Write("WWGG")

makeBinShape(fakes,"fakes",outfile,channel)
makeBinShape(ztautau,"ztautau",outfile,channel)
if channel != "vbf":
	if doLoose == False:
		makeBinShape(zjetsother,"zjetsother",outfile,channel)
	else:
		makeBinShape(zjetsotherLoose,"zjetsother",outfile,channel)
if doLoose == False:
	makeBinShape(ttbar,"ttbar",outfile,channel)
	makeBinShape(ww,"ww",outfile,channel)
	makeBinShape(singlet,"singlet",outfile,channel)
else:
        makeBinShape(ttbarLoose,"ttbar",outfile,channel)
        makeBinShape(wwLoose,"ww",outfile,channel)
        makeBinShape(singletLoose,"singlet",outfile,channel)
makeBinShape(LFVVBF,"LFVVBF",outfile,channel)
makeBinShape(LFVGG,"LFVGG",outfile,channel)
makeBinShape(SMVBF126,"SMVBF126",outfile,channel)
makeBinShape(SMGG126,"SMGG126",outfile,channel)
makeBinShape(WWVBF126,"WWVBF126",outfile,channel)
makeBinShape(WWGG126,"WWGG126",outfile,channel)

if channel != "vbf":
	writeUpDownNorm(zjetsother,zjetsother_shape_JES_Up,zjetsother_shape_JES_Down,"zjetsother",channel,"jes")
writeUpDownNorm(ttbar,ttbar_shape_JES_Up,ttbar_shape_JES_Down,"ttbar",channel,"jes")
writeUpDownNorm(ww,ww_shape_JES_Up,ww_shape_JES_Down,"ww",channel,"jes")
writeUpDownNorm(singlet,singlet_shape_JES_Up,singlet_shape_JES_Down,"singlet",channel,"jes")
writeUpDownNorm(SMVBF126,SMVBF126_shape_JES_Up,SMVBF126_shape_JES_Down,"SMVBF126",channel,"jes")
writeUpDownNorm(SMGG126,SMGG126_shape_JES_Up,SMGG126_shape_JES_Down,"SMGG126",channel,"jes")
writeUpDownNorm(LFVVBF,LFVVBF_shape_JES_Up,LFVVBF_shape_JES_Down,"LFVVBF",channel,"jes")
writeUpDownNorm(LFVGG,LFVGG_shape_JES_Up,LFVGG_shape_JES_Down,"LFVGG",channel,"jes")

if channel != "vbf":
	writeUpDownNorm(zjetsother,zjetsother_shape_MET_Up,zjetsother_shape_MET_Down,"zjetsother",channel,"ues")
writeUpDownNorm(ttbar,ttbar_shape_MET_Up,ttbar_shape_MET_Down,"ttbar",channel,"ues")
writeUpDownNorm(ww,ww_shape_MET_Up,ww_shape_MET_Down,"ww",channel,"ues")
writeUpDownNorm(singlet,singlet_shape_MET_Up,singlet_shape_MET_Down,"singlet",channel,"ues")
writeUpDownNorm(SMVBF126,SMVBF126_shape_MET_Up,SMVBF126_shape_MET_Down,"SMVBF126",channel,"ues")
writeUpDownNorm(SMGG126,SMGG126_shape_MET_Up,SMGG126_shape_MET_Down,"SMGG126",channel,"ues")
writeUpDownNorm(LFVVBF,LFVVBF_shape_MET_Up,LFVVBF_shape_MET_Down,"LFVVBF",channel,"ues")
writeUpDownNorm(LFVGG,LFVGG_shape_MET_Up,LFVGG_shape_MET_Down,"LFVGG",channel,"ues")



writeUpDownNorm(ztautau,ztautau_shape_TES_Up,ztautau_shape_TES_Down,"ztautau",channel,"tes")
if channel != "vbf":
	writeUpDownNorm(zjetsother,zjetsother_shape_TES_Up,zjetsother_shape_TES_Down,"zjetsother",channel,"tes")
writeUpDownNorm(ttbar,ttbar_shape_TES_Up,ttbar_shape_TES_Down,"ttbar",channel,"tes")
writeUpDownNorm(ww,ww_shape_TES_Up,ww_shape_TES_Down,"ww",channel,"tes")
writeUpDownNorm(singlet,singlet_shape_TES_Up,singlet_shape_TES_Down,"singlet",channel,"tes")
writeUpDownNorm(SMVBF126,SMVBF126_shape_TES_Up,SMVBF126_shape_TES_Down,"SMVBF126",channel,"tes")
writeUpDownNorm(SMGG126,SMGG126_shape_TES_Up,SMGG126_shape_TES_Down,"SMGG126",channel,"tes")
writeUpDownNorm(LFVVBF,LFVVBF_shape_TES_Up,LFVVBF_shape_TES_Down,"LFVVBF",channel,"tes")
writeUpDownNorm(LFVGG,LFVGG_shape_TES_Up,LFVGG_shape_TES_Down,"LFVGG",channel,"tes")
#scale up down shapes to original 

'''
ztautau_shape_JES_Up.Scale(ztautau.Integral()/ztautau_shape_JES_Up.Integral())
zjetsother_shape_JES_Up.Scale(zjetsother.Integral()/zjetsother_shape_JES_Up.Integral())
ttbar_shape_JES_Up.Scale(ttbar.Integral()/ttbar_shape_JES_Up.Integral())
ww_shape_JES_Up.Scale(ww.Integral()/ww_shape_JES_Up.Integral())
singlet_shape_JES_Up.Scale(singlet.Integral()/singlet_shape_JES_Up.Integral())
LFVVBF126_shape_JES_Up.Scale(LFVVBF126.Integral()/LFVVBF126_shape_JES_Up.Integral())
LFVGG126_shape_JES_Up.Scale(LFVGG126.Integral()/LFVGG126_shape_JES_Up.Integral())
SMVBF126_shape_JES_Up.Scale(SMVBF126.Integral()/SMVBF126_shape_JES_Up.Integral())
SMGG126_shape_JES_Up.Scale(SMGG126.Integral()/SMGG126_shape_JES_Up.Integral())
LFVVBF_shape_JES_Up.Scale(LFVVBF.Integral()/LFVVBF_shape_JES_Up.Integral())
LFVGG_shape_JES_Up.Scale(LFVGG.Integral()/LFVGG_shape_JES_Up.Integral())
SMVBF_shape_JES_Up.Scale(SMVBF.Integral()/SMVBF_shape_JES_Up.Integral())
SMGG_shape_JES_Up.Scale(SMGG.Integral()/SMGG_shape_JES_Up.Integral())

if zjetsother_shape_JES_Down.Integral() !=0:
        zjetsother_shape_JES_Down.Scale(zjetsother.Integral()/zjetsother_shape_JES_Down.Integral())
ttbar_shape_JES_Down.Scale(ttbar.Integral()/ttbar_shape_JES_Down.Integral())
ww_shape_JES_Down.Scale(ww.Integral()/ww_shape_JES_Down.Integral())
singlet_shape_JES_Down.Scale(singlet.Integral()/singlet_shape_JES_Down.Integral())
LFVVBF126_shape_JES_Down.Scale(LFVVBF126.Integral()/LFVVBF126_shape_JES_Down.Integral())
LFVGG126_shape_JES_Down.Scale(LFVGG126.Integral()/LFVGG126_shape_JES_Down.Integral())
SMVBF126_shape_JES_Down.Scale(SMVBF126.Integral()/SMVBF126_shape_JES_Down.Integral())
SMGG126_shape_JES_Down.Scale(SMGG126.Integral()/SMGG126_shape_JES_Down.Integral())
LFVVBF_shape_JES_Down.Scale(LFVVBF.Integral()/LFVVBF_shape_JES_Down.Integral())
LFVGG_shape_JES_Down.Scale(LFVGG.Integral()/LFVGG_shape_JES_Down.Integral())
SMVBF_shape_JES_Down.Scale(SMVBF.Integral()/SMVBF_shape_JES_Down.Integral())
SMGG_shape_JES_Down.Scale(SMGG.Integral()/SMGG_shape_JES_Down.Integral())

ztautau_shape_MET_Up.Scale(ztautau.Integral()/ztautau_shape_MET_Up.Integral())
zjetsother_shape_MET_Up.Scale(zjetsother.Integral()/zjetsother_shape_MET_Up.Integral())
ttbar_shape_MET_Up.Scale(ttbar.Integral()/ttbar_shape_MET_Up.Integral())
ww_shape_MET_Up.Scale(ww.Integral()/ww_shape_MET_Up.Integral())
singlet_shape_MET_Up.Scale(singlet.Integral()/singlet_shape_MET_Up.Integral())
LFVVBF126_shape_MET_Up.Scale(LFVVBF126.Integral()/LFVVBF126_shape_MET_Up.Integral())
LFVGG126_shape_MET_Up.Scale(LFVGG126.Integral()/LFVGG126_shape_MET_Up.Integral())
SMVBF126_shape_MET_Up.Scale(SMVBF126.Integral()/SMVBF126_shape_MET_Up.Integral())
SMGG126_shape_MET_Up.Scale(SMGG126.Integral()/SMGG126_shape_MET_Up.Integral())
LFVVBF_shape_MET_Up.Scale(LFVVBF.Integral()/LFVVBF_shape_MET_Up.Integral())
LFVGG_shape_MET_Up.Scale(LFVGG.Integral()/LFVGG_shape_MET_Up.Integral())
SMVBF_shape_MET_Up.Scale(SMVBF.Integral()/SMVBF_shape_MET_Up.Integral())
SMGG_shape_MET_Up.Scale(SMGG.Integral()/SMGG_shape_MET_Up.Integral())

ztautau_shape_MET_Down.Scale(ztautau.Integral()/ztautau_shape_MET_Down.Integral())
zjetsother_shape_MET_Down.Scale(zjetsother.Integral()/zjetsother_shape_MET_Down.Integral())
ttbar_shape_MET_Down.Scale(ttbar.Integral()/ttbar_shape_MET_Down.Integral())
ww_shape_MET_Down.Scale(ww.Integral()/ww_shape_MET_Down.Integral())
singlet_shape_MET_Down.Scale(singlet.Integral()/singlet_shape_MET_Down.Integral())
LFVVBF126_shape_MET_Down.Scale(LFVVBF126.Integral()/LFVVBF126_shape_MET_Down.Integral())
LFVGG126_shape_MET_Down.Scale(LFVGG126.Integral()/LFVGG126_shape_MET_Down.Integral())
SMVBF126_shape_MET_Down.Scale(SMVBF126.Integral()/SMVBF126_shape_MET_Down.Integral())
SMGG126_shape_MET_Down.Scale(SMGG126.Integral()/SMGG126_shape_MET_Down.Integral())
LFVVBF_shape_MET_Down.Scale(LFVVBF.Integral()/LFVVBF_shape_MET_Down.Integral())
LFVGG_shape_MET_Down.Scale(LFVGG.Integral()/LFVGG_shape_MET_Down.Integral())
SMVBF_shape_MET_Down.Scale(SMVBF.Integral()/SMVBF_shape_MET_Down.Integral())
SMGG_shape_MET_Down.Scale(SMGG.Integral()/SMGG_shape_MET_Down.Integral())

ztautau_shape_TES_Up.Scale(ztautau.Integral()/ztautau_shape_TES_Up.Integral())
zjetsother_shape_TES_Up.Scale(zjetsother.Integral()/zjetsother_shape_TES_Up.Integral())
ttbar_shape_TES_Up.Scale(ttbar.Integral()/ttbar_shape_TES_Up.Integral())
ww_shape_TES_Up.Scale(ww.Integral()/ww_shape_TES_Up.Integral())
singlet_shape_TES_Up.Scale(singlet.Integral()/singlet_shape_TES_Up.Integral())
LFVVBF126_shape_TES_Up.Scale(LFVVBF126.Integral()/LFVVBF126_shape_TES_Up.Integral())
LFVGG126_shape_TES_Up.Scale(LFVGG126.Integral()/LFVGG126_shape_TES_Up.Integral())
SMVBF126_shape_TES_Up.Scale(SMVBF126.Integral()/SMVBF126_shape_TES_Up.Integral())
SMGG126_shape_TES_Up.Scale(SMGG126.Integral()/SMGG126_shape_TES_Up.Integral())
LFVVBF_shape_TES_Up.Scale(LFVVBF.Integral()/LFVVBF_shape_TES_Up.Integral())
LFVGG_shape_TES_Up.Scale(LFVGG.Integral()/LFVGG_shape_TES_Up.Integral())
SMVBF_shape_TES_Up.Scale(SMVBF.Integral()/SMVBF_shape_TES_Up.Integral())
SMGG_shape_TES_Up.Scale(SMGG.Integral()/SMGG_shape_TES_Up.Integral())


if zjetsother_shape_TES_Down.Integral() !=0:
        zjetsother_shape_TES_Down.Scale(zjetsother.Integral()/zjetsother_shape_TES_Down.Integral())
ttbar_shape_TES_Down.Scale(ttbar.Integral()/ttbar_shape_TES_Down.Integral())
ww_shape_TES_Down.Scale(ww.Integral()/ww_shape_TES_Down.Integral())
singlet_shape_TES_Down.Scale(singlet.Integral()/singlet_shape_TES_Down.Integral())
LFVVBF126_shape_TES_Down.Scale(LFVVBF126.Integral()/LFVVBF126_shape_TES_Down.Integral())
LFVGG126_shape_TES_Down.Scale(LFVGG126.Integral()/LFVGG126_shape_TES_Down.Integral())
SMVBF126_shape_TES_Down.Scale(SMVBF126.Integral()/SMVBF126_shape_TES_Down.Integral())
SMGG126_shape_TES_Down.Scale(SMGG126.Integral()/SMGG126_shape_TES_Down.Integral())
LFVVBF_shape_TES_Down.Scale(LFVVBF.Integral()/LFVVBF_shape_TES_Down.Integral())
LFVGG_shape_TES_Down.Scale(LFVGG.Integral()/LFVGG_shape_TES_Down.Integral())
SMVBF_shape_TES_Down.Scale(SMVBF.Integral()/SMVBF_shape_TES_Down.Integral())
SMGG_shape_TES_Down.Scale(SMGG.Integral()/SMGG_shape_TES_Down.Integral())

fakes_shape_FAKES_Up.Scale(fakes.Integral()/fakes_shape_FAKES_Up.Integral())
fakes_shape_FAKES_Down.Scale(fakes.Integral()/fakes_shape_FAKES_Down.Integral())
'''

if channel != "vbf":
	if doLoose == False:
		zjetsother_shape_JES_Up.Write("zjetsother_shape_MuTau_JESUp")
	else:
		zjetsotherLooseJesUp.Scale(zjetsother_shape_JES_Up.Integral()/zjetsotherLooseJesUp.Integral())
		zjetsotherLooseJesUp.Write("zjetsother_shape_MuTau_JESUp")
if doLoose == False:
	ttbar_shape_JES_Up.Write("ttbar_shape_MuTau_JESUp")
	ww_shape_JES_Up.Write("ww_shape_MuTau_JESUp")
	singlet_shape_JES_Up.Write("singlet_shape_MuTau_JESUp")
else:
        ttbarLooseJesUp.Scale(ttbar_shape_JES_Up.Integral()/ttbarLooseJesUp.Integral())
        ttbarLooseJesUp.Write("ttbar_shape_JESUp")
        singletLooseJesUp.Scale(singlet_shape_JES_Up.Integral()/singletLooseJesUp.Integral())
        singletLooseJesUp.Write("singlet_shape_MuTau_JESUp")
        wwLooseJesUp.Scale(ww_shape_JES_Up.Integral()/wwLooseJesUp.Integral())
        wwLooseJesUp.Write("ww_shape_MuTau_JESUp")
LFVVBF126_shape_JES_Up.Write("LFVVBF126_shape_MuTau_JESUp")
LFVGG126_shape_JES_Up.Write("LFVGG126_shape_MuTau_JESUp")
SMVBF126_shape_JES_Up.Write("SMVBF126_shape_MuTau_JESUp")
SMGG126_shape_JES_Up.Write("SMGG126_shape_MuTau_JESUp")
LFVVBF_shape_JES_Up.Write("LFVVBF_shape_MuTau_JESUp")
LFVGG_shape_JES_Up.Write("LFVGG_shape_MuTau_JESUp")
SMVBF_shape_JES_Up.Write("SMVBF_shape_MuTau_JESUp")
SMGG_shape_JES_Up.Write("SMGG_shape_MuTau_JESUp")

if channel != "vbf":
        if doLoose == False:
                zjetsother_shape_JES_Down.Write("zjetsother_shape_MuTau_JESDown")
        else:   
                zjetsotherLooseJesDown.Scale(zjetsother_shape_JES_Down.Integral()/zjetsotherLooseJesDown.Integral())
                zjetsotherLooseJesDown.Write("zjetsother_shape_MuTau_JESDown")
if doLoose == False:
        ttbar_shape_JES_Down.Write("ttbar_shape_MuTau_JESDown")
        ww_shape_JES_Down.Write("ww_shape_MuTau_JESDown")
        singlet_shape_JES_Down.Write("singlet_shape_MuTau_JESDown")
else:
        ttbarLooseJesDown.Scale(ttbar_shape_JES_Down.Integral()/ttbarLooseJesDown.Integral())
        ttbarLooseJesDown.Write("ttbar_shape_MuTau_JESDown")
        singletLooseJesDown.Scale(singlet_shape_JES_Down.Integral()/singletLooseJesDown.Integral())
        singletLooseJesDown.Write("singlet_shape_MuTau_JESDown")
        wwLooseJesDown.Scale(ww_shape_JES_Down.Integral()/wwLooseJesDown.Integral())
	wwLooseJesDown.Write("ww_shape_MuTau_JESDown")
LFVVBF126_shape_JES_Down.Write("LFVVBF126_shape_MuTau_JESDown")
LFVGG126_shape_JES_Down.Write("LFVGG126_shape_MuTau_JESDown")
SMVBF126_shape_JES_Down.Write("SMVBF126_shape_MuTau_JESDown")
SMGG126_shape_JES_Down.Write("SMGG126_shape_MuTau_JESDown")
LFVVBF_shape_JES_Down.Write("LFVVBF_shape_MuTau_JESDown")
LFVGG_shape_JES_Down.Write("LFVGG_shape_MuTau_JESDown")
SMVBF_shape_JES_Down.Write("SMVBF_shape_MuTau_JESDown")
SMGG_shape_JES_Down.Write("SMGG_shape_MuTau_JESDown")
#ttbarLooseJesDown.Write("ttbarLoose_shape_JESDown")
#singletLooseJesDown.Write("singletLoose_shape_JESDown")
#wwLooseJesDown.Write("wwLoose_shape_JESDown")

if channel != "vbf":
	zjetsother_shape_MET_Up.Write("zjetsother_shape_MuTau_METUp")
ttbar_shape_MET_Up.Write("ttbar_shape_MuTau_METUp")
ww_shape_MET_Up.Write("ww_shape_MuTau_METUp")
singlet_shape_MET_Up.Write("singlet_shape_MuTau_METUp")
LFVVBF126_shape_MET_Up.Write("LFVVBF126_shape_MuTau_METUp")
LFVGG126_shape_MET_Up.Write("LFVGG126_shape_MuTau_METUp")
SMVBF126_shape_MET_Up.Write("SMVBF126_shape_MuTau_METUp")
SMGG126_shape_MET_Up.Write("SMGG126_shape_MuTau_METUp")
LFVVBF_shape_MET_Up.Write("LFVVBF_shape_MuTau_METUp")
LFVGG_shape_MET_Up.Write("LFVGG_shape_MuTau_METUp")
SMVBF_shape_MET_Up.Write("SMVBF_shape_MuTau_METUp")
SMGG_shape_MET_Up.Write("SMGG_shape_MuTau_METUp")

if channel != "vbf":
	zjetsother_shape_MET_Down.Write("zjetsother_shape_MuTau_METDown")
ttbar_shape_MET_Down.Write("ttbar_shape_MuTau_METDown")
ww_shape_MET_Down.Write("ww_shape_MuTau_METDown")
singlet_shape_MET_Down.Write("singlet_shape_MuTau_METDown")
LFVVBF126_shape_MET_Down.Write("LFVVBF126_shape_MuTau_METDown")
LFVGG126_shape_MET_Down.Write("LFVGG126_shape_MuTau_METDown")
SMVBF126_shape_MET_Down.Write("SMVBF126_shape_MuTau_METDown")
SMGG126_shape_MET_Down.Write("SMGG126_shape_MuTau_METDown")
LFVVBF_shape_MET_Down.Write("LFVVBF_shape_MuTau_METDown")
LFVGG_shape_MET_Down.Write("LFVGG_shape_MuTau_METDown")
SMVBF_shape_MET_Down.Write("SMVBF_shape_MuTau_METDown")
SMGG_shape_MET_Down.Write("SMGG_shape_MuTau_METDown")

ztautau_shape_TES_Up.Write("ztautau_shape_MuTau_TESUp")
if channel != "vbf":
	zjetsother_shape_TES_Up.Write("zjetsother_shape_MuTau_TESUp")
ttbar_shape_TES_Up.Write("ttbar_shape_MuTau_TESUp")
ww_shape_TES_Up.Write("ww_shape_MuTau_TESUp")
singlet_shape_TES_Up.Write("singlet_shape_MuTau_TESUp")
LFVVBF126_shape_TES_Up.Write("LFVVBF126_shape_MuTau_TESUp")
LFVGG126_shape_TES_Up.Write("LFVGG126_shape_MuTau_TESUp")
SMVBF126_shape_TES_Up.Write("SMVBF126_shape_MuTau_TESUp")
SMGG126_shape_TES_Up.Write("SMGG126_shape_MuTau_TESUp")
LFVVBF_shape_TES_Up.Write("LFVVBF_shape_MuTau_TESUp")
LFVGG_shape_TES_Up.Write("LFVGG_shape_MuTau_TESUp")
SMVBF_shape_TES_Up.Write("SMVBF_shape_MuTau_TESUp")
SMGG_shape_TES_Up.Write("SMGG_shape_MuTau_TESUp")

ztautau_shape_TES_Down.Write("ztautau_shape_MuTau_TESDown")
if channel != "vbf":
	zjetsother_shape_TES_Down.Write("zjetsother_shape_MuTau_TESDown")
ttbar_shape_TES_Down.Write("ttbar_shape_MuTau_TESDown")
ww_shape_TES_Down.Write("ww_shape_MuTau_TESDown")
singlet_shape_TES_Down.Write("singlet_shape_MuTau_TESDown")
LFVVBF126_shape_TES_Down.Write("LFVVBF126_shape_MuTau_TESDown")
LFVGG126_shape_TES_Down.Write("LFVGG126_shape_MuTau_TESDown")
SMVBF126_shape_TES_Down.Write("SMVBF126_shape_MuTau_TESDown")
SMGG126_shape_TES_Down.Write("SMGG126_shape_MuTau_TESDown")
LFVVBF_shape_TES_Down.Write("LFVVBF_shape_MuTau_TESDown")
LFVGG_shape_TES_Down.Write("LFVGG_shape_MuTau_TESDown")
SMVBF_shape_TES_Down.Write("SMVBF_shape_MuTau_TESDown")
SMGG_shape_TES_Down.Write("SMGG_shape_MuTau_TESDown")

fakes_shape_FAKES_Up.Write("fakes_shape_FAKESUp")
fakes_shape_FAKES_Down.Write("fakes_shape_FAKESDown")

outfile.Write()

