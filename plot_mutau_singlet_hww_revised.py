from sys import argv, stdout, stderr
import getopt
import ROOT
import sys
import math
import array
import numpy
import makeOldQCD


##get qcd normalization (choose selections for qcd)

def yieldHisto(histo,xmin,xmax):
	binmin = int(histo.FindBin(xmin))
	binwidth = histo.GetBinWidth(binmin)
	binmax = int(xmax/binwidth)
	signal = histo.Integral(binmin,binmax)
	print "binmin" + str(binmin)
	print "binmax" + str(binmax)
	return signal

def make_histo(savedir,file_str, channel,var,lumidir,lumi,lumi_str=""):
	histoFile = ROOT.TFile(savedir+file_str+".root")
	ROOT.gROOT.cd()
	histo = histoFile.Get(channel+"/"+var).Clone()
	if shape_norm == True:
		histo.Scale(1/histo.Integral())
	else:
		if (lumi_str == ""):
			lumi_str = file_str
 		lumifile = lumidir + lumi_str +".lumicalc.sum"
		f = open(lumifile).read().splitlines()
		efflumi = float(f[0])
		if "DY4Jets" in file_str:
			print "checking dy4jets:"
			print efflumi
			print histo.Integral()
		histo.Scale(lumi/efflumi)
	return histo
	
try:
        opts, args = getopt.getopt(sys.argv[1:],"ts:p:c:v:",["savedir=","predir=","channel=","var="])
except getopt.GetoptError:
        print 'plot_mutau_singlet.py -s <savedir> -p <predir> -c <channel> -v <var>'
        sys.exit(2)
for opt,arg in opts:
        if opt == "-t":
                print 'plot_mutau_singlet.py -s <savedir> -p <predir> -c <channel> -v <var>'
                sys.exit()
        elif opt in ("-s","--savedir"):
                savedir = arg
        elif opt in ("-p","--predir"):
                predir = arg
        elif opt in ("-c","--channel"):
                channel = arg
        elif opt in ("-v","--var"):
                var = arg

shape_norm = False
if shape_norm == False:
	ynormlabel = " "
else:
	ynormlabel = "Normalized to 1 "
if "jes" in savedir:
	jes = True #jes up or down (or unshifted)
else:
	jes = False
if "ues" in savedir: #ues up or down
	ues = True
else:
	ues = False 
print savedir
if "NewTauId" in savedir:
	newtauid = True
	print "NewTauID in savedir"
else:
	newtauid = False
print "JJJJJJJEEEEEEEEESSSSSSSSSSS" + str(jes)
presel =  True #use preselection cuts or not
blind = True
systematics = True
if shape_norm == True:
	systematics = False
fakeRate = True #apply fake rate method
zjetsEmbed = True #use embedded data samples for zjets
DYShape = False #use DY MC shape for ztautau
seperateSemiFull = False #seperate semi and fully leptonic ttbar
plotData=True 
plotSave=True #save plot as a pdf for AN
logScale=False

##savedir contains the root files for plotting
if presel:
        savedir = predir
##import parameters for input variable	
import mutau_vars
print savedir
print predir
print channel
print var

##Set up style
ROOT.gROOT.LoadMacro("tdrstyle.C")
ROOT.setTDRStyle()

ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

#check for mismatches in systematics directories

if "jes" in predir and not ("jes" in savedir):
	print "Error: jes mismatch"
	sys.exit()
if "jes" in savedir and not ("jes" in predir):
        print "Error: jes mismatch"
        sys.exit()
if "jes_minus" in var and not ("jesminus" in savedir) or "jes_plus" in var and not ("jesplus" in savedir):
	print "Error: jes doesn't match"
	sys.exit()
if var == "collMass_type1" and (("jesminus" in savedir) or ("jesplus" in savedir)):
	print "Error: jes doesn't match"
	sys.exit()
if "ues" in predir and not ("ues" in savedir):
        print "Error: ues mismatch"
        sys.exit()
if "ues" in savedir and not ("ues" in predir) and fakeRate == False:  #make sure that predir doesn't have to be used if ues mismatch
	print "Error: ues mismatch"
	sys.exit()
if "ues_minus" in var and not ("uesminus" in savedir) or "ues_plus" in var and not ("uesplus" in savedir):
        print "Error: ues doesn't match"
        sys.exit()
if var == "collMass_type1" and (("uesminus" in savedir) or ("uesplus" in savedir)):
        print "Error: ues doesn't match"
        sys.exit()
if var == "collMass_jes_minus" or var == "collMass_jes_plus" or var == "collMass_type1_ues_minus" or var == "collMass_type1_ues_plus":
	datavar = "collMass_type1"
elif var == "tMtToPfMet_ues":
	datavar = "tMtToPfMet_Ty1"
getVarParams = "mutau_vars."+var
varParams = eval(getVarParams)
xlabel = varParams[0]
if presel:
	binwidth = varParams[7]
else:
	binwidth = varParams[1]
print var
print channel
if (("collMass" in var or "higgs" in var or "pfMetEt" in var) and (channel == "gg0" or channel == "ssgg0")):
	binwidth = 10
	print "binwidth 10"
elif (("collMass" in var or "higgs" in var or "pfMetEt" in var) and (channel == "gg1" or channel == "ssgg1")):
	binwidth = 10
	print "binwidth 10"
elif "ztautau" in channel and "collMass" in var:
	binwidth = 20
elif "intermediate" in savedir:
	binwidth = 20
if presel == False:
	legend = eval(varParams[2])
else:
	legend = eval(varParams[8])
blindlow = varParams[3]
blindhigh = varParams[4]
if var == "m_t_Mass" and channel =="gg":
	blindhigh  = 120
if presel == True:
	if var == "fullMT_type1" and channel == "vbf":
		blindlow = 100
		blindhigh = 150
	elif var == "m_t_Mass" and (channel == "vbf" or channel == "gg1"):
		blindlow = 70
		blindhigh = 120
	elif var =="m_t_Mass" and channel == "ztautaucontrolvbf":
		blindlow = 80
		blindhigh = 110
	elif var == "m_t_Mass" and channel == "gg0":
		blindlow=80
		blindhigh=130
	elif var == "collMass_type1" and (channel == "gg1" or channel =="vbf"or channel == "gg0"):
		blindlow = 100
		blindhigh = 150
	elif var == "tMtToPfMet_Ty1" and channel == "gg1":
		blindlow = 0
		blindhigh = 10
if blindlow==blindhigh:
        blind = False
isGeV = varParams[5]
xRange = varParams[6]
canvas = ROOT.TCanvas("canvas","canvas",800,800)
if plotData==True: #make pads for main plot and ratio plot
	p_lfv = ROOT.TPad('p_lfv','p_lfv',0,0,1,1)
	p_lfv.SetLeftMargin(0.2147651)
	p_lfv.SetRightMargin(0.06543624)
	p_lfv.SetTopMargin(0.04895105)
	p_lfv.SetBottomMargin(0.305)
	if logScale == True:
		p_lfv.SetLogy()
	p_lfv.Draw()
	p_ratio = ROOT.TPad('p_ratio','p_ratio',0,0,1,0.295)
        p_ratio.SetLeftMargin(0.2147651)
        p_ratio.SetRightMargin(0.06543624)
        p_ratio.SetTopMargin(0.04895105)
	p_ratio.SetBottomMargin(0.295)
	p_ratio.SetGridy()
	p_ratio.Draw()
	p_lfv.cd()
else: #only make pad for main plot
	p_lfv = ROOT.TPad('p_lfv','p_lfv',0,0,1,1)
        p_lfv.SetLeftMargin(0.2147651)
        p_lfv.SetRightMargin(0.06543624)
        p_lfv.SetTopMargin(0.04895105)
        p_lfv.SetBottomMargin(0.1311189)
        if logScale == True:
                p_lfv.SetLogy()
        p_lfv.Draw()
	p_lfv.cd()

if jes==True:
        lumidir = 'lumicalc_jes/'
elif ues == True:
        lumidir = 'lumicalc_ues/'
elif newtauid == True:
	lumidir = 'lumicalc_NewTauID/'
	print "new tau id"
else:
        lumidir = 'lumicalc_Jan17/'
vartype1 = var
varnotype1 = var
nojesvar = var
if var == "collMass_type1":
        #var = "collMass_type1"
	var = "collMass"
        datavar = "collMass_type1"
	vartype1 = "collMass_type1"
	varnotype1 = "collMass"
	nojesvar = "collMass"
if var == "type1_pfMetEt":
	var = "pfMetEt"
	vartype1 = "type1_pfMetEt"
	varnotype1 = "pfMetEt"
	nojesvar = "pfMetEt"
elif "jes" in var and "collMass" in var:
	nojesvar = "collMass"
	datavar = "collMass"
	vartype1 = "collMass_type1"
elif "jes" in var and "pfMetEt" in var:
	nojesvar = "pfMetEt"
	datavar = "pfMetEt"
	vartype1 = "type1_pfMetEt"
	var = "pfMetEt"
#compute data luminosity
data1_lumifile = lumidir + 'data_SingleMu_Run2012A_22Jan2013_v1_2.lumicalc.sum'
data2_lumifile = lumidir + 'data_SingleMu_Run2012B_22Jan2013_v1_2.lumicalc.sum'
data3_lumifile = lumidir + 'data_SingleMu_Run2012C_22Jan2013_v1_2.lumicalc.sum'
data4_lumifile = lumidir + 'data_SingleMu_Run2012D_22Jan2013_v1.lumicalc.sum'
f = open(data1_lumifile).read().splitlines()
data1_lumi = float(f[0])

f = open(data2_lumifile).read().splitlines()
data2_lumi = float(f[0])

f = open(data3_lumifile).read().splitlines()
data3_lumi = float(f[0])

f = open(data4_lumifile).read().splitlines()
data4_lumi = float(f[0])
lumi = data1_lumi+data2_lumi+data3_lumi+data4_lumi

LFVStack = ROOT.THStack("stack","")

print var
hgglfv = make_histo(savedir,"LFV_GluGlu_Dec9",channel,var,lumidir,lumi)
hvbflfv = make_histo(savedir,"LFV_VBF_Dec9",channel,var,lumidir,lumi)
hggsm = make_histo(savedir,"GGH_H2Tau_M-125",channel,var,lumidir,lumi)
zjetsMC = make_histo(savedir,"Zjets_M50",channel,varnotype1,lumidir,lumi)
if zjetsEmbed:
	dy1jets = make_histo(savedir,"DY1Jets_madgraph",channel,varnotype1,lumidir,lumi)
        dy2jets = make_histo(savedir,"DY2Jets_madgraph",channel,varnotype1,lumidir,lumi)
        dy3jets = make_histo(savedir,"DY3Jets_madgraph",channel,varnotype1,lumidir,lumi)
        dy4jets = make_histo(savedir,"DY4Jets_madgraph",channel,varnotype1,lumidir,lumi)
	dy1other = make_histo(savedir, "OtherDY1",channel,varnotype1,lumidir,lumi,"DY1Jets_madgraph")
        dy2other = make_histo(savedir, "OtherDY2",channel,varnotype1,lumidir,lumi,"DY2Jets_madgraph")
        dy3other = make_histo(savedir, "OtherDY3",channel,varnotype1,lumidir,lumi,"DY3Jets_madgraph")
        dy4other = make_histo(savedir, "OtherDY4",channel,varnotype1,lumidir,lumi,"DY4Jets_madgraph")
	zjetsotherMC = make_histo(savedir,"OtherM50",channel,varnotype1,lumidir,lumi,"Zjets_M50")
wjets4 = make_histo(savedir,"Wplus4Jets_madgraph",channel,var,lumidir,lumi) #changed to datavar to save time when running jes
wjetsFiltered = make_histo(savedir,"WplusJets_madgraph_filtered",channel,var,lumidir,lumi)
ttbar_semi = make_histo(savedir,"TTJets_SemiLeptMGDecays_8TeV-madgraph-tauola",channel,var,lumidir,lumi)
ttbar_full = make_histo(savedir,"TTJets_FullLeptMGDecays_8TeV-madgraph-tauola",channel,var,lumidir,lumi)
ww = make_histo(savedir,"WWJetsTo2L2Nu_TuneZ2_8TeV",channel,varnotype1,lumidir,lumi)
tt = make_histo(savedir,"T_t-channel",channel,var,lumidir,lumi)
tbart = make_histo(savedir,"Tbar_t-channel",channel,var,lumidir,lumi)
tw = make_histo(savedir,"T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola",channel,var,lumidir,lumi)
tbarw = make_histo(savedir,"Tbar_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola",channel,var,lumidir,lumi)
hvbfsm = make_histo(savedir,"VBF_H2Tau_M-125",channel,var,lumidir,lumi)
hvbfww = make_histo(savedir,"HiggsToWWVBF125",channel,nojesvar,lumidir,lumi)
hggww = make_histo(savedir,"HiggsToWWGG125",channel,nojesvar,lumidir,lumi)
wwfull = make_histo(savedir,"WWpythia",channel,vartype1,lumidir,lumi)
wz = make_histo(savedir,"WZ",channel,vartype1,lumidir,lumi)
zz = make_histo(savedir,"ZZ",channel,vartype1,lumidir,lumi)
vhsm = make_histo(savedir,"VH_H2Tau_M-125",channel,nojesvar,lumidir,lumi)
vhlfv = make_histo(savedir, "LFV_VH_H2MuTau_LONG-MuTauMC",channel,nojesvar,lumidir,lumi)
hwwvhtth = make_histo(savedir,"HWWVHTTH125",channel,nojesvar,lumidir,lumi)
if zjetsEmbed:
	dataEmb_ntuple_file_str = 'dataEmbedded_2012.root'
wjets1_ntuple_file_str = 'Wplus1Jets.root'
wjets2_ntuple_file_str = 'Wplus2Jets.root'
wjets3_ntuple_file_str = 'Wplus3Jets.root'
data_ntuple_file_str = 'data_2012.root'
if zjetsEmbed:
	dataEmb_ntuple_file = ROOT.TFile(savedir+dataEmb_ntuple_file_str)
wjets1_ntuple_file = ROOT.TFile(savedir+wjets1_ntuple_file_str)
wjets2_ntuple_file = ROOT.TFile(savedir+wjets2_ntuple_file_str)
wjets3_ntuple_file = ROOT.TFile(savedir+wjets3_ntuple_file_str)
data_ntuple_file = ROOT.TFile(savedir+data_ntuple_file_str)

if fakeRate == False: # go to predir for QCD
	hgglfv_pre_ntuple_file = ROOT.TFile(predir+hgglfv_ntuple_file_str)
	hvbflfv_pre_ntuple_file = ROOT.TFile(predir+hvbflfv_ntuple_file_str)
	zjets_pre_ntuple_file = ROOT.TFile(predir+zjets_ntuple_file_str)
	wjets1_pre_ntuple_file = ROOT.TFile(predir+wjets1_ntuple_file_str)
	wjets2_pre_ntuple_file = ROOT.TFile(predir+wjets2_ntuple_file_str)
	wjets3_pre_ntuple_file = ROOT.TFile(predir+wjets3_ntuple_file_str)
	wjets4_pre_ntuple_file = ROOT.TFile(predir+wjets4_ntuple_file_str)
	wjetsFiltered_pre_ntuple_file = ROOT.TFile(predir+wjetsFiltered_ntuple_file_str)
	ttbar_semi_pre_ntuple_file = ROOT.TFile(predir+ttbar_semi_ntuple_file_str)
	ttbar_full_pre_ntuple_file = ROOT.TFile(predir+ttbar_full_ntuple_file_str)
	ww_pre_ntuple_file = ROOT.TFile(predir+ww_ntuple_file_str)
	tt_pre_ntuple_file = ROOT.TFile(predir+tt_ntuple_file_str)
	tbart_pre_ntuple_file = ROOT.TFile(predir+tbart_ntuple_file_str)
	tw_pre_ntuple_file = ROOT.TFile(predir+tw_ntuple_file_str)
	tbarw_pre_ntuple_file = ROOT.TFile(predir+tbarw_ntuple_file_str)
	data_pre_ntuple_file = ROOT.TFile(predir+data_ntuple_file_str)

#get histograms
ntuple_spot = channel
if zjetsEmbed:
	zjets = dataEmb_ntuple_file.Get(ntuple_spot+"/"+varnotype1).Clone()
	print "ztautua1:"+str(zjets.Integral())
#changed w+jets to datavar to save time when running jes (w+jets MC not used in data driven fake rate estimation)
wjets1 = wjets1_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
wjets2 = wjets2_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
wjets3 = wjets3_ntuple_file.Get(ntuple_spot+"/"+var).Clone()
data = data_ntuple_file.Get(ntuple_spot+"/"+varnotype1).Clone()

dataEmb1_lumifile = lumidir + 'data_EmbeddedDoubleMu_Run2012A_v1.lumicalc.sum'
dataEmb2_lumifile = lumidir + 'data_EmbeddedDoubleMu_Run2012B_v1.lumicalc.sum'
dataEmb3_lumifile = lumidir + 'data_EmbeddedDoubleMu_Run2012C_v1.lumicalc.sum'
dataEmb4_lumifile = lumidir + 'data_EmbeddedDoubleMu_Run2012D_v1.lumicalc.sum'
wjets_extension_lumifile = lumidir + 'WplusJets_madgraph_Extension.lumicalc.sum'
wjets1_lumifile = lumidir + 'Wplus1Jets_madgraph.lumicalc.sum'
wjets1_ext_lumifile = lumidir + 'Wplus1Jets_madgraph_extension.lumicalc.sum'
wjets2_lumifile = lumidir + 'Wplus2Jets_madgraph.lumicalc.sum'
wjets2_ext_lumifile = lumidir + 'Wplus2Jets_madgraph_extension.lumicalc.sum'
wjets3_lumifile = lumidir + 'Wplus3Jets_madgraph.lumicalc.sum'
wjets3_ext_lumifile = lumidir + 'Wplus3Jets_madgraph_extension.lumicalc.sum'

f = open(wjets_extension_lumifile).read().splitlines()
wjets_extension_efflumi = float(f[0])

f = open(wjets1_lumifile).read().splitlines()
wjets1_efflumi = float(f[0])

f = open(wjets1_ext_lumifile).read().splitlines()
wjets1_ext_efflumi = float(f[0])

f = open(wjets2_lumifile).read().splitlines()
wjets2_efflumi = float(f[0])

f = open(wjets2_ext_lumifile).read().splitlines()
wjets2_ext_efflumi = float(f[0])

f = open(wjets3_lumifile).read().splitlines()
wjets3_efflumi = float(f[0])

f = open(wjets3_ext_lumifile).read().splitlines()
wjets3_ext_efflumi = float(f[0])

f = open(dataEmb1_lumifile).read().splitlines()
dataEmb1_lumi = float(f[0])

f = open(dataEmb2_lumifile).read().splitlines()
dataEmb2_lumi = float(f[0])

f = open(dataEmb3_lumifile).read().splitlines()
dataEmb3_lumi = float(f[0])

f = open(dataEmb4_lumifile).read().splitlines()
dataEmb4_lumi = float(f[0])

print "lumi: " + str(lumi)
lumiEmb = dataEmb1_lumi+dataEmb2_lumi+dataEmb3_lumi+dataEmb4_lumi
wjets1_total_efflumi = wjets1_efflumi+wjets1_ext_efflumi
wjets2_total_efflumi = wjets2_efflumi+wjets2_ext_efflumi
wjets3_total_efflumi = wjets3_efflumi+wjets3_ext_efflumi

#define normalzing factors to normalize MC to data
wjets1_datanorm = lumi/wjets1_total_efflumi
wjets2_datanorm = lumi/wjets2_total_efflumi
wjets3_datanorm = lumi/wjets3_total_efflumi

if fakeRate == False:
#get qcd normalization (non fake rate method)
	qcd_norm = makeOldQCD.make_qcd_norm(presel, var, predir, savedir, channel ,wjets1_pre_ntuple_file, wjets2_pre_ntuple_file, wjets3_pre_ntuple_file, wjets4_pre_ntuple_file, wjetsFiltered_pre_ntuple_file, zjets_pre_ntuple_file, ttbar_semi_pre_ntuple_file, ttbar_full_pre_ntuple_file, ww_pre_ntuple_file, data_pre_ntuple_file,data_ntuple_file, wjets1_datanorm, wjets2_datanorm, wjets3_datanorm, wjets4_datanorm, wjetsFiltered_datanorm, zjets_datanorm, ttbar_semi_datanorm, ttbar_full_datanorm, ww_datanorm)
	if channel == "highMtssvbf":
		antiiso_ntuple_spot = "highMtssantiisomuonvbf"
	elif channel == "highMtvbf":
		antiiso_ntuple_spot = "highMtantiisomuonvbf"
	elif channel == "highMtssgg":
		antiiso_ntuple_spot = "highMtssantiisomuongg"
	elif channel == "ssvbf":
		antiiso_ntuple_spot = "ssantiisomuonvbf"
	elif channel == "ssgg":
		antiiso_ntuple_spot = "ssantiisomuongg"
	else:
		antiiso_ntuple_spot = "antiisomuon"+channel #channel = vbf or gg
	qcd = data_ntuple_file.Get(antiiso_ntuple_spot+"/"+var).Clone() #get antiisolated qcd shape
	if qcd_norm < 0:  #if approximately no qcd
		qcd.Scale(0)
	else:
		qcd.Scale(qcd_norm/qcd.Integral()) #normalized qcd shape

if shape_norm == False: #normalize histos to data
	wjets1_norm = wjets1_datanorm
	wjets2_norm = wjets2_datanorm
	wjets3_norm = wjets3_datanorm
	ztautau_norm = lumi/lumiEmb
	zjets.Scale(ztautau_norm)
	wjets1.Scale(wjets1_norm)
	wjets2.Scale(wjets2_norm)
        wjets3.Scale(wjets3_norm)

#add up histograms for combined processes
wjets = wjets1.Clone()
wjets.Add(wjets2)
wjets.Add(wjets3)
wjets.Add(wjets4)
wjets.Add(wjetsFiltered)
singlet = tt.Clone()
singlet.Add(tbart)
singlet.Add(tw)
singlet.Add(tbarw)
print "testing singlet"
print tt.Integral()
print tbart.Integral()
print tw.Integral()
print tbarw.Integral()

hsm = hvbfsm.Clone()
hsm.Add(hggsm)
hsm.Add(hvbfww)
hsm.Add(hggww)
if presel == True and "gg0" in channel:
        wjets.Scale(0.8585376)
ttbar = ttbar_full.Clone()
ttbar.Add(ttbar_semi)
if zjetsEmbed == False: #check whether or not to use embedded method
        zjets = zjetsMC.Clone()
else:
        dyjets = dy1jets.Clone()
        dyjets.Add(dy2jets)
        dyjets.Add(dy3jets)
        dyjets.Add(dy4jets)
        dyjets.Add(zjetsMC)
	print "dyjets:"
	print dy1jets.Integral()
	print dy2jets.Integral()
	print dy3jets.Integral()
	print dy4jets.Integral()
	print zjetsMC.Integral()
        if DYShape == True:
                zjets = dyjets.Clone()
        else:
                if zjets.Integral() != 0:
                        zjets.Scale(dyjets.Integral()/zjets.Integral())
			print "ztautau2:"+str(zjets.Integral())
        zjetsother = dy1other.Clone()
        zjetsother.Add(dy2other)
        zjetsother.Add(dy3other)
        zjetsother.Add(dy4other)
        zjetsother.Add(zjetsotherMC)
if shape_norm == True: 	#normailze histos to 1 (ttbar, wjets, zjetsother normalized later)
	if fakeRate == False:
		qcd_norm = 1/(qcd.Integral())
		qcd.Scale(1/qcd.Integral())
	singlet.Scale(1/singlet.Integral())
	if zjetsEmbed == False:
		zjets = zjetsMC.Clone()
	zjets.Scale(1/zjets.Integral())
	data.Scale(1/data.Integral())	

xbinLength = data.GetBinWidth(1)
isGeV = varParams[5]
widthOfBin = binwidth*xbinLength
if isGeV:
	ylabel = ynormlabel + " Events / " + str(int(widthOfBin)) + " GeV"
else:
	ylabel = ynormlabel  + " Events / " + str(widthOfBin)

if fakeRate == False:
	qcd.Rebin(binwidth)
if channel == "highMtssvbf":
	fakechannel = "highMtssantiisotauvbf"
elif channel == "highMtssgg0":
	fakechannel = "highMtssantiisotaugg0"
elif channel == "highMtssgg":
	fakechannel = "highMtssantiisotaugg"
elif channel == "ttbarcontrolvbf":
	fakechannel = "antiisotauvbf"
else:
	fakechannel = "antiisotau"+channel
if fakeRate == True:
	wjets = data_ntuple_file.Get(fakechannel+"/"+varnotype1).Clone()
	if shape_norm == True:
		wjets.Scale(1/wjets.Integral())
	if zjetsEmbed == False:
		zjetsFakes = zjets_ntuple_file.Get(fakechannel+"/"+var).Clone()
		zjetsFakes.Scale(-1*zjets_datanorm)
		zjets.Add(zjetsFakes)
	else:
		zjetsFakes = dataEmb_ntuple_file.Get(fakechannel+"/"+varnotype1).Clone()
		
		zjetsMCFakes = make_histo(savedir,"Zjets_M50",fakechannel,varnotype1,lumidir,lumi)
		dy1jetsFakes = make_histo(savedir,"DY1Jets_madgraph",fakechannel,varnotype1,lumidir,lumi)
        	dy2jetsFakes = make_histo(savedir,"DY2Jets_madgraph",fakechannel,varnotype1,lumidir,lumi)
        	dy3jetsFakes = make_histo(savedir,"DY3Jets_madgraph",fakechannel,varnotype1,lumidir,lumi)
        	dy4jetsFakes = make_histo(savedir,"DY4Jets_madgraph",fakechannel,varnotype1,lumidir,lumi)
		dy1otherFakes = make_histo(savedir, "OtherDY1",fakechannel,varnotype1,lumidir,lumi,"DY1Jets_madgraph")
        	dy2otherFakes = make_histo(savedir, "OtherDY2",fakechannel,varnotype1,lumidir,lumi,"DY2Jets_madgraph")
        	dy3otherFakes = make_histo(savedir, "OtherDY3",fakechannel,varnotype1,lumidir,lumi,"DY3Jets_madgraph")
        	dy4otherFakes = make_histo(savedir, "OtherDY4",fakechannel,varnotype1,lumidir,lumi,"DY4Jets_madgraph")
		zjetsotherMCFakes = make_histo(savedir,"OtherM50",fakechannel,varnotype1,lumidir,lumi,"Zjets_M50")
		dyjetsFakes = dy1jetsFakes.Clone()
		dyjetsFakes.Add(dy2jetsFakes)
		dyjetsFakes.Add(dy3jetsFakes)
		dyjetsFakes.Add(dy4jetsFakes)
		dyjetsFakes.Add(zjetsMCFakes)
		if DYShape == True:
			zjetsFakes = dyjetsFakes.Clone()
		else:
			if zjetsFakes.Integral() != 0:
				print "ZJETSFAKES!!!!!!" + str(zjetsFakes.Integral())
				zjetsFakes.Scale(-1*dyjetsFakes.Integral()/zjetsFakes.Integral())
		wjets.Add(zjetsFakes)
		zjetsotherFakes = dy1otherFakes.Clone()
		zjetsotherFakes.Add(dy2otherFakes)
		zjetsotherFakes.Add(dy3otherFakes)
		zjetsotherFakes.Add(dy4otherFakes)
		zjetsotherFakes.Add(zjetsotherMCFakes)
		zjetsotherFakes.Scale(-1)
		zjetsother.Add(zjetsotherFakes)
		
	ttbar_semi_fakes = make_histo(savedir,"TTJets_SemiLeptMGDecays_8TeV-madgraph-tauola",fakechannel,var,lumidir,lumi)
	ttbar_full_fakes = make_histo(savedir,"TTJets_FullLeptMGDecays_8TeV-madgraph-tauola",fakechannel,var,lumidir,lumi)
	ttbar_full_fakes.Scale(-1)
	ttbar_semi_fakes.Scale(-1)
	ttbar.Add(ttbar_full_fakes)
	ttbar.Add(ttbar_semi_fakes)
if shape_norm == True:
	wjets.Scale(1/wjets.Integral())
	ttbar.Scale(1/ttbar.Integral())
	zjetsother.Scale(1/zjetsother.Integral())
wjets.Rebin(binwidth)
zjets.Rebin(binwidth)
zjetsother.Rebin(binwidth)
ttbar.Rebin(binwidth)
ttbar_full.Rebin(binwidth)
ttbar_semi.Rebin(binwidth)
ww.Rebin(binwidth)
wwfull.Rebin(binwidth)
wz.Rebin(binwidth)
zz.Rebin(binwidth)
vhsm.Rebin(binwidth)
vhlfv.Rebin(binwidth)
hwwvhtth.Rebin(binwidth)
singlet.Rebin(binwidth)
hgglfv.Rebin(binwidth)
hvbflfv.Rebin(binwidth)
hvbfsm.Rebin(binwidth)
hggsm.Rebin(binwidth)
hvbfww.Rebin(binwidth)
hggww.Rebin(binwidth)
hsm.Rebin(binwidth)
data.Rebin(binwidth)
if zjetsEmbed == False: #don't use zjetsother if zjets embed method is not used
	zjetsother = zjets.Clone()
	zjetsother.Scale(0)

if systematics == True:
	if fakeRate == True:
		fakesLow = data_ntuple_file.Get(fakechannel+"/"+varnotype1).Clone()
		fakesLow.Add(zjetsFakes)
		fakesLow.Scale(0.7)
		fakesHigh = data_ntuple_file.Get(fakechannel+"/"+varnotype1).Clone()
		fakesHigh.Add(zjetsFakes)
		fakesHigh.Scale(1.3)
        	fakesLow.Rebin(binwidth)
        	fakesHigh.Rebin(binwidth)
	size = wjets.GetNbinsX()
	#build tgraph of systematic bands
	xUncert = array.array('f',[])
	yUncert = array.array('f',[])
	yFakesNoStack = array.array('f',[])
	exlUncert = array.array('f',[])
	exhUncert = array.array('f',[])
	eylUncert = array.array('f',[])
	eyhUncert = array.array('f',[])
	binLength = wjets.GetBinCenter(2)-wjets.GetBinCenter(1)
	for i in range(1,size+1):
		if wjets.GetBinContent(i) != 0 or wjets.GetBinContent(i) == 0:
			if fakeRate == True:
				stackBinContent = wjets.GetBinContent(i)+zjets.GetBinContent(i)+zjetsother.GetBinContent(i)+ttbar.GetBinContent(i)+ww.GetBinContent(i)+singlet.GetBinContent(i)
			else:
				stackBinContent = wjets.GetBinContent(i)+zjets.GetBinContent(i)+zjetsother.GetBinContent(i)+ttbar.GetBinContent(i)+ww.GetBinContent(i)+singlet.GetBinContent(i)+qcd.GetBinContent(i)
			wjetsBinContent = wjets.GetBinContent(i)
			xUncert.append(wjets.GetBinCenter(i))
			yUncert.append(stackBinContent)
			yFakesNoStack.append(wjetsBinContent)
			exlUncert.append(binLength/2)
			exhUncert.append(binLength/2)
			if fakeRate == True:
                        	eylUncert.append(wjetsBinContent-fakesLow.GetBinContent(i)+zjets.GetBinError(i)+zjetsother.GetBinError(i)+ttbar.GetBinError(i)+ww.GetBinError(i)+singlet.GetBinError(i)+hsm.GetBinError(i))
                        	eyhUncert.append(fakesHigh.GetBinContent(i) +zjets.GetBinError(i)+zjetsother.GetBinError(i)+ttbar.GetBinError(i)+ww.GetBinError(i) + singlet.GetBinError(i) +hsm.GetBinError(i) - wjetsBinContent)
			else:
                                eylUncert.append(wjets.GetBinError(i)+zjets.GetBinError(i)+zjetsother.GetBinError(i)+ttbar.GetBinError(i)+ww.GetBinError(i)+ singlet.GetBinError(i) +qcd.GetBinError(i)+hsm.GetBinError(i))
                                eyhUncert.append(wjets.GetBinError(i)+zjets.GetBinError(i)+zjetsother.GetBinError(i)+ttbar.GetBinError(i)+ww.GetBinError(i)+singlet.GetBinError(i)+ qcd.GetBinError(i)+hsm.GetBinError(i))
	xUncertVec = ROOT.TVectorF(len(xUncert),xUncert)
	yUncertVec = ROOT.TVectorF(len(yUncert),yUncert)
	yFakesNoStackVec = ROOT.TVectorF(len(yFakesNoStack),yFakesNoStack)
	exlUncertVec = ROOT.TVectorF(len(exlUncert),exlUncert)
	exhUncertVec = ROOT.TVectorF(len(exhUncert),exhUncert)
	eylUncertVec = ROOT.TVectorF(len(eylUncert),eylUncert)
	eyhUncertVec = ROOT.TVectorF(len(eyhUncert),eyhUncert)	
	systErrors = ROOT.TGraphAsymmErrors(xUncertVec,yUncertVec,exlUncertVec,exhUncertVec,eylUncertVec,eyhUncertVec)
	fakeErrorsNoStack =  ROOT.TGraphAsymmErrors(xUncertVec,yFakesNoStackVec,exlUncertVec,exhUncertVec,eylUncertVec,eyhUncertVec)

# create root file with yields for datacards
outfile_name = savedir+"LFV"+"_"+channel+"_"+var
if fakeRate == True:
	outfile_name = outfile_name + "_fakeRate"
if zjetsEmbed == True:
	outfile_name = outfile_name +"_zjetsEmbed"
if DYShape == True:
	outfile_name = outfile_name +"_dyshape"
outfile_name = outfile_name +"_newSignal" #relic from when "old signal" (pre december 2013 signal without proper tau decays) was used
if logScale == True:
	outfile_name = outfile_name +"_log"
if "jesnone" in savedir:
	outfile_name = outfile_name + "_jesnone"
elif "jesminus" in savedir:
	outfile_name = outfile_name + "_jesminus"
elif "jesplus" in savedir:
	outfile_name = outfile_name + "_jesplus"

outfile = ROOT.TFile(outfile_name+".root","RECREATE")
outfile.mkdir("vbfmutau")
outfile.cd("vbfmutau/")
if fakeRate == False:
	qcd.Write("qcd")
	wjets.Write("wjets")
else:
	wjets.Write("fakes")
	if systematics == True:
		fakeErrorsNoStack.Write("fake rate error graph")
if zjetsEmbed == False:
	zjets.Write("zjets")
else:
	zjets.Write("ztautau")
	zjetsother.Write("zjetsother")
ttbar.Write("ttbar")
ttbar_semi.Write("ttbarsemi")
ttbar_full.Write("ttbarfull")
ww.Write("ww")
singlet.Write("singlet")
data.Write("data_obs")
hvbflfvScaled = hvbflfv.Clone()
hvbflfvScaled.Scale(0.1)
hgglfvScaled = hgglfv.Clone()
hgglfvScaled.Scale(0.1)
hvbflfvScaled.Write("LFVVBF126")
hgglfvScaled.Write("LFVGG126")
hvbfsm.Write("SMVBF126")
hggsm.Write("SMGG126")
hvbfww.Write("WWVBF126")
hggww.Write("WWGG126")
hvbflfvScaled.Write("LFVVBF")
hgglfvScaled.Write("LFVGG")
hvbfsm.Write("SMVBF")
hggsm.Write("SMGG")
hvbfww.Write("WWVBF")
hggww.Write("WWGG")
wz.Write("WZ")
zz.Write("ZZ")
vhsm.Write("VHSM")
vhlfv.Write("VHLFV")
hwwvhtth.Write("HWWVHTTH")
outfile.Write()

if (presel == True or plotData ==False) and ( channel == "vbf" and plotSave == True and shape_norm == False):
        hgglfv.Scale(10)
        hvbflfv.Scale(10)
hgglfv.SetLineColor(ROOT.EColor.kBlue)
hvbflfv.SetLineColor(ROOT.EColor.kRed)
hvbfsm.SetLineColor(ROOT.EColor.kMagenta)
hggsm.SetLineColor(ROOT.EColor.kMagenta)
hvbfww.SetLineColor(ROOT.EColor.kOrange+3)
hggww.SetLineColor(ROOT.EColor.kOrange+3)
wjets.SetFillColor(ROOT.EColor.kMagenta-10)
wjets.SetLineColor(ROOT.EColor.kMagenta+4)
wjets.SetLineWidth(1)
zjets.SetFillColor(ROOT.EColor.kOrange-4)
zjets.SetLineColor(ROOT.EColor.kOrange+4)
zjets.SetLineWidth(1)
zjetsother.SetFillColor(ROOT.EColor.kAzure+3)
zjetsother.SetLineColor(ROOT.EColor.kAzure+4)
zjetsother.SetLineWidth(1)
ttbar.SetFillColor(40)
ttbar.SetLineColor(ROOT.EColor.kBlack)
ttbar.SetLineWidth(1)
ttbar_full.SetFillColor(ROOT.EColor.kGreen+3)
ttbar_semi.SetFillColor(ROOT.EColor.kCyan-6)
ww.SetFillColor(ROOT.EColor.kRed+2)
ww.SetLineColor(ROOT.EColor.kRed+4)
ww.SetLineWidth(1)
singlet.SetFillColor(ROOT.EColor.kGreen-2)
singlet.SetLineColor(ROOT.EColor.kGreen+4)
singlet.SetLineWidth(1)
if fakeRate == False:
	qcd.SetFillColor(ROOT.EColor.kCyan)
	qcd.SetLineColor(ROOT.EColor.kBlue+4)
	qcd.SetLineWidth(1)
	qcd.SetMarkerSize(0)
wjets.SetMarkerSize(0)
zjets.SetMarkerSize(0)
zjetsother.SetMarkerSize(0)
ttbar.SetMarkerSize(0)
ttbar_full.SetMarkerSize(0)
ttbar_semi.SetMarkerSize(0)
ww.SetMarkerSize(0)
singlet.SetMarkerSize(0)
hgglfv.SetMarkerSize(0)
hvbflfv.SetMarkerSize(0)
hvbfsm.SetMarkerSize(0)
hggsm.SetMarkerSize(0)
hvbfww.SetMarkerSize(0)
hggww.SetMarkerSize(0)
hgglfv.SetLineWidth(3)
hvbflfv.SetLineWidth(3)
hvbflfv.SetLineStyle(ROOT.kDashed)
hvbfsm.SetLineWidth(3)
hvbfsm.SetLineStyle(ROOT.kDashed)
hggsm.SetLineWidth(3)
hvbfww.SetLineWidth(3)
hvbfww.SetLineStyle(ROOT.kDashed)
hggww.SetLineWidth(3)
hsm.SetFillColor(ROOT.EColor.kMagenta)
hsm.SetLineColor(ROOT.EColor.kMagenta)
hsm.SetLineWidth(1)
data.SetMarkerSize(1)
LFVStack.Add(wjets)
LFVStack.Add(ww)
if seperateSemiFull == False:
	LFVStack.Add(ttbar)
else:
	LFVStack.Add(ttbar_full)
	LFVStack.Add(ttbar_semi)

LFVStack.Add(singlet)
if zjetsEmbed == False:
	LFVStack.Add(zjets)
else:
	LFVStack.Add(zjetsother)
	LFVStack.Add(zjets)
if fakeRate == False:
	legend.AddEntry(qcd,'QCD',"f")
legend.SetFillColor(0)
legend.SetBorderSize(0)
legend.SetFillStyle(0)
if fakeRate == False:
	LFVStack.Add(qcd)
LFVStack.Add(hsm)
maxLFVStack = LFVStack.GetMaximum()
maxhgglfv=hgglfv.GetMaximum()
maxhvbflfv=hvbflfv.GetMaximum()
maxhvbfsm = hvbfsm.GetMaximum()
maxhggsm = hggsm.GetMaximum()
maxhvbfww = hvbfww.GetMaximum()
maxhggww = hggww.GetMaximum()
maxdata = data.GetMaximum()
maxHist = max(maxLFVStack,maxhgglfv,maxhvbflfv,maxhvbfsm,maxhggsm,maxhvbfww,maxhggww,maxdata)
if var == "vbfj1eta" or var == "vbfj2eta":
	maxHist = maxHist*1.40/1.20
LFVStack.SetMaximum(maxHist*1.20)
LFVStack.Draw('hist')
if shape_norm == False and plotData == True:
	data.Draw("sames,E1")
if xRange != 0:
        LFVStack.GetXaxis().SetRangeUser(0,xRange)
hgglfv.Scale(0.1)
hvbflfv.Scale(0.1)
hgglfv.Draw('sameshist')
hvbflfv.Draw('sameshist')
if shape_norm == False and plotData == True:
	legend.AddEntry(data,'Observed',"p")
if systematics == True:
	systErrors.SetFillStyle(3001)
        systErrors.SetFillColor(ROOT.EColor.kGray+3)
        systErrors.SetMarkerSize(0)
        systErrors.Draw('sames,E2')
	legend.AddEntry(systErrors,'Bkg. Uncertainty')
legend.AddEntry(hsm,'SM Higgs')
if fakeRate == False:
        legend.AddEntry(wjets,'W+Jets','f')
else:
        legend.AddEntry(wjets, 'Fake(jet#rightarrow#tau)','f')
if zjetsEmbed == False:
        legend.AddEntry(zjets,'Z+Jets')
else:
        legend.AddEntry(zjets, 'Z#rightarrow#tau#tau (embedded)','f')
        legend.AddEntry(zjetsother, 'Z#rightarrowl^{+}l^{-}','f')
legend.AddEntry(singlet,'Single Top',"f")
if seperateSemiFull == False:
        legend.AddEntry(ttbar,'t#bar{t}')
else:
        legend.AddEntry(ttbar_full, 'TT Fully Leptonic')
        legend.AddEntry(ttbar_semi, 'TT Semi Leptonic')
legend.AddEntry(ww,'EWK Di-Boson',"f")
if (channel == "vbf" or channel == "ztautaucontrolvbf") and plotSave == True and shape_norm == False and ( presel == True or plotData == False):
        legend.AddEntry(hgglfv,'GG LFV Higgs BR=1.0')
        legend.AddEntry(hvbflfv, 'VBF LFV Higgs BR=1.0')
else:
        legend.AddEntry(hgglfv,'LFV GG Higgs')
        legend.AddEntry(hvbflfv, 'LFV VBF Higgs')
#create shaded region if blinded
if blind == True and shape_norm == False and plotData == True:
	binblindlow = data.FindBin(blindlow)
	binblindhigh = data.FindBin(blindhigh)
	for x in range(binblindlow, binblindhigh+1):
		data.SetBinContent(x, -1000)
	pave = ROOT.TPave(blindlow,0,blindhigh,maxHist*1.25,4,"br")
	pave.SetFillColor(ROOT.kGray+1)
	pave.SetFillStyle(3003)
	pave.SetBorderSize(0)
if plotData == True:
	legend.SetTextSize(0.025)
else:
	legend.SetTextSize(0.024)
legend.Draw('sames')
LFVStack.GetXaxis().SetTitle(xlabel)
LFVStack.GetXaxis().SetNdivisions(510)
LFVStack.GetXaxis().SetTitleOffset(3.0)
LFVStack.GetXaxis().SetLabelOffset(3.0)
LFVStack.GetXaxis().SetLabelSize(0.035)
LFVStack.GetYaxis().SetTitle(ylabel)
LFVStack.GetYaxis().SetTitleOffset(1.40)
LFVStack.GetYaxis().SetLabelSize(0.035)

if var =="collMass_type1":
	LFVStack.GetYaxis().SetRangeUser(0,4.2)
latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextSize(0.04)
latex.SetTextAlign(31)
latexStr = "%.1f fb^{-1}, #sqrt{s} = 8 TeV"%(lumi/1000)
latex.DrawLatex(0.9,0.96,latexStr)
latex.SetTextAlign(11)
latex.DrawLatex(0.25,0.96,"CMS preliminary")
#signal to background ratio
lowbound = 100
highbound = 150
binminSignal = int(hgglfv.FindBin(lowbound))
binwidthSignal =  hgglfv.GetBinWidth(binminSignal)
binmaxSignal = int(highbound/binwidthSignal)
if fakeRate == True and zjetsEmbed == True:
	stackYield = 0
	for i in range(binminSignal,binmaxSignal+1):
		stackYield = stackYield+wjets.GetBinContent(i)+zjets.GetBinContent(i)+zjetsother.GetBinContent(i)+ttbar.GetBinContent(i)+ww.GetBinContent(i)+singlet.GetBinContent(i)+hsm.GetBinContent(i)
	print wjets.Integral()
	print zjets.Integral()
	print zjetsother.Integral()
	print ttbar.Integral()
	print ww.Integral()
	print singlet.Integral()
	print hsm.Integral()
	sbratio = (hvbflfv.Integral(binminSignal,binmaxSignal)+hgglfv.Integral(binminSignal,binmaxSignal))/stackYield
	print "S: " + str((hvbflfv.Integral(binminSignal,binmaxSignal)+hgglfv.Integral(binminSignal,binmaxSignal)))
	print "B: " + str(stackYield)
	print "S/sqrt(S+B) : " + str((hvbflfv.Integral(binminSignal,binmaxSignal)+hgglfv.Integral(binminSignal,binmaxSignal))/math.sqrt(stackYield+(hvbflfv.Integral(binminSignal,binmaxSignal)+hgglfv.Integral(binminSignal,binmaxSignal))))
	print "Bin Range of S/sqrt(S+B): " + str(binminSignal) + "->" + str(binmaxSignal)
if plotData==True:
	p_ratio.cd()
	ROOT.gROOT.LoadMacro("tdrstyle.C")
	ROOT.setTDRStyle()
	ratio = data.Clone()
	mc = wjets.Clone()
	mc.Add(zjets)
	if zjetsEmbed == True:
		mc.Add(zjetsother)
	mc.Add(ttbar)
	mc.Add(ww)
	mc.Add(singlet)
	mc.Add(hsm)
	if fakeRate == False:
		mc.Add(qcd)
	mc.Scale(-1)
	ratio.Add(mc)
	mc.Scale(-1)
	ratio.Divide(mc)
	ratio.Draw("E1")
	if xRange != 0:
		ratio.GetXaxis().SetRangeUser(0,xRange)
		lineOne = ROOT.TLine(0.0, 1.0, xRange +widthOfBin,1.0)
	else:
        	lineOne = ROOT.TLine(ratio.GetXaxis().GetXmin(), 1.0, ratio.GetXaxis().GetXmax(),1.0)
	
        #lineOne.Draw('sames')
	if blind == True:
        	paveRatio = ROOT.TPave(blindlow,-1.0,blindhigh,1.0,4,"br")
        	paveRatio.SetFillColor(1)
        	paveRatio.SetFillStyle(3002)
        	paveRatio.SetBorderSize(0)
 	       	paveRatio.Draw('sameshist')

	size = wjets.GetNbinsX()
	xRatio = array.array('f',[])
	yRatio = array.array('f',[])
	exlRatio = array.array('f',[])
	exhRatio = array.array('f',[])
	eylRatio = array.array('f',[])
	eyhRatio = array.array('f',[])
	binLength = wjets.GetBinCenter(2)-wjets.GetBinCenter(1)
	print binwidth
 	if zjetsEmbed == False:
		print "systematics not configured for no zjetsEmbed!!"
		sys.exit()
	for i in range(1,size+1):
		if wjets.GetBinContent(i) != 0:
			stackBinContent = wjets.GetBinContent(i)+zjets.GetBinContent(i)+zjetsother.GetBinContent(i)+ttbar.GetBinContent(i)+ww.GetBinContent(i)+singlet.GetBinContent(i)+hsm.GetBinContent(i)
			if data.GetBinContent(i) != 0 and stackBinContent == 0:
				print "data but no MC!!"
				sys.exit(2)
			wjetsBinContent = wjets.GetBinContent(i)
			ratioBinContent = ratio.GetBinContent(i)
			xRatio.append(wjets.GetBinCenter(i))
			yRatio.append(0.0)
			exlRatio.append(binLength/2)
			exhRatio.append(binLength/2)
			if fakeRate == True and systematics == True:
				eylRatio.append(-(fakesLow.GetBinContent(i)-wjetsBinContent -zjets.GetBinError(i)-zjetsother.GetBinError(i)-ttbar.GetBinError(i)-ww.GetBinError(i)-singlet.GetBinError(i)-hsm.GetBinError(i))*(data.GetBinContent(i))/(stackBinContent*stackBinContent))
                        	eyhRatio.append((fakesHigh.GetBinContent(i)-wjetsBinContent+zjets.GetBinError(i)+zjetsother.GetBinError(i)+ttbar.GetBinError(i)+ww.GetBinError(i)+singlet.GetBinError(i)+hsm.GetBinError(i))*(data.GetBinContent(i))/(stackBinContent*stackBinContent))
			else:
                                eylRatio.append(-(-wjets.GetBinError(i) -zjets.GetBinError(i)-zjetsother.GetBinError(i)-ttbar.GetBinError(i)-ww.GetBinError(i)-singlet.GetBinError(i)-hsm.GetBinError(i))*(data.GetBinContent(i))/(stackBinContent*stackBinContent))
                        	eyhRatio.append((wjets.GetBinError(i)+zjets.GetBinError(i)+zjetsother.GetBinError(i)+ttbar.GetBinError(i)+ww.GetBinError(i)+singlet.GetBinError(i)+hsm.GetBinError(i))*(data.GetBinContent(i))/(stackBinContent*stackBinContent))
	if systematics == True:
		xRatioVec = ROOT.TVectorF(len(xRatio),xRatio)
		yRatioVec = ROOT.TVectorF(len(yRatio),yRatio)
		exlRatioVec = ROOT.TVectorF(len(exlRatio),exlRatio)
		exhRatioVec = ROOT.TVectorF(len(exhRatio),exhRatio)
		eylRatioVec = ROOT.TVectorF(len(eylRatio),eylRatio)
		eyhRatioVec = ROOT.TVectorF(len(eyhRatio),eyhRatio)	
		ratioErrors = ROOT.TGraphAsymmErrors(xRatioVec,yRatioVec,exlRatioVec,exhRatioVec,eylRatioVec,eyhRatioVec)
		ratioErrors.SetFillStyle(3002)
        	ratioErrors.Draw('sames,E2')
		ratioErrors.SetFillColor(ROOT.EColor.kGray+3)
	ratio.GetXaxis().SetTitle(xlabel)
	ratio.GetXaxis().SetTitleSize(0.12)
	ratio.GetXaxis().SetNdivisions(510)
	ratio.GetXaxis().SetTitleOffset(1.1)
	ratio.GetXaxis().SetLabelSize(0.12)
	ratio.GetXaxis().SetLabelFont(42)
	ratio.GetYaxis().SetNdivisions(505)
	ratio.GetYaxis().SetLabelFont(42)
	ratio.GetYaxis().SetLabelSize(0.1)
	ratio.GetYaxis().SetRangeUser(-1,1)
	ratio.GetYaxis().SetTitle("#frac{Data-Predicted}{Predicted}")
	ratio.GetYaxis().CenterTitle(1)
	ratio.GetYaxis().SetTitleOffset(0.4)
	ratio.GetYaxis().SetTitleSize(0.12)
	ratio.SetTitle("")
if seperateSemiFull:
	outfile_name = outfile_name+"_semifull"
if shape_norm == False:
	canvas.SaveAs(outfile_name+".png")
else:
	canvas.SaveAs(outfile_name+"_shape.png")
if shape_norm == False and fakeRate == False and zjetsEmbed == True and systematics == True and plotData == False and channel =="vbf" and presel == True and DYShape == False and plotSave == True:
	if var == "mPt":
		canvas.SaveAs(savedir+"muhad_VBF_muPt_After_Presel.pdf")
	elif var == "tPt":
		canvas.SaveAs(savedir+"muhad_VBF_tauPt_After_Presel.pdf")
	elif var == "tMtToPfMet_Ty1":
		canvas.SaveAs(savedir+"muhad_VBF_MT_After_Presel.pdf")
	elif var == "tPhiMETPhiType1":
		canvas.SaveAs(savedir+"muhad_VBF_dPhi_tau_met_After_Presel.pdf")
	elif var == "mPhiMETPhiType1":
		canvas.SaveAs(savedir+"muhad_VBF_dPhi_mu_met_After_Presel.pdf")
	elif var == "collMass_type1":
		canvas.SaveAs(savedir+"muhad_VBF_m_colinear_After_Presel.pdf")
        elif var == "vbfDeta":
                canvas.SaveAs(savedir+"muhad_VBF_dEta_jj_After_Presel.pdf")
        elif var == "vbfMass":
                canvas.SaveAs(savedir+"muhad_VBF_Mjj_After_Presel.pdf")
        elif var == "vbfj1eta":
                canvas.SaveAs(savedir+"muhad_VBF_jet1eta_After_Presel.pdf")
        elif var == "vbfj2eta":
                canvas.SaveAs(savedir+"muhad_VBF_jet2eta_After_Presel.pdf")
        elif var == "vbfj1pt":
                canvas.SaveAs(savedir+"muhad_VBF_jet1pt_After_Presel.pdf")
        elif var == "vbfj2pt":
                canvas.SaveAs(savedir+"muhad_VBF_jet2pt_After_Presel.pdf")
if shape_norm == False and fakeRate == True and zjetsEmbed == True and systematics == True and plotData == True and channel =="vbf" and presel == True and DYShape == False and plotSave == True:
	if var == "collMass_type1" and blind == True:
		canvas.SaveAs(savedir+"muhad_VBF_m_colinear_After_Presel_WITHDATA.pdf")
        elif var == "mPt":
                canvas.SaveAs(savedir+"muhad_VBF_muPt_After_Presel_WITHDATA.pdf")
        elif var == "tPt":
                canvas.SaveAs(savedir+"muhad_VBF_tauPt_After_Presel_WITHDATA.pdf")
        elif var == "tMtToPfMet_Ty1":
                canvas.SaveAs(savedir+"muhad_VBF_MT_After_Presel_WITHDATA.pdf")
        elif var == "tPhiMETPhiType1":
                canvas.SaveAs(savedir+"muhad_VBF_dPhi_tau_met_After_Presel_WITHDATA.pdf")
        elif var == "mPhiMETPhiType1":
                canvas.SaveAs(savedir+"muhad_VBF_dPhi_mu_met_After_Presel_WITHDATA.pdf")
        elif var == "vbfDeta":
                canvas.SaveAs(savedir+"muhad_VBF_dEta_jj_After_Presel_WITHDATA.pdf")
        elif var == "vbfMass":
                canvas.SaveAs(savedir+"muhad_VBF_Mjj_After_Presel_WITHDATA.pdf")
        elif var == "vbfj1eta":
                canvas.SaveAs(savedir+"muhad_VBF_jet1eta_After_Presel_WITHDATA.pdf")
        elif var == "vbfj2eta":
                canvas.SaveAs(savedir+"muhad_VBF_jet2eta_After_Presel_WITHDATA.pdf")
        elif var == "vbfj1pt":
                canvas.SaveAs(savedir+"muhad_VBF_jet1pt_After_Presel_WITHDATA.pdf")
        elif var == "vbfj2pt":
                canvas.SaveAs(savedir+"muhad_VBF_jet2pt_After_Presel_WITHDATA.pdf")
if shape_norm == False and fakeRate == True and zjetsEmbed == True and systematics == True and plotData == True and channel =="gg1" and presel == True and DYShape == False and plotSave == True:
        if var == "collMass_type1" and blind == True:
                canvas.SaveAs(savedir+"muhad_Boost_m_colinear_After_Presel_WITHDATA.pdf")
if shape_norm == False and fakeRate == True and zjetsEmbed == True and systematics == True and plotData == True and channel =="gg0" and presel == True and DYShape == False and plotSave == True:
        if var == "collMass_type1" and blind == True:
                canvas.SaveAs(savedir+"muhad_GG_m_colinear_After_Presel_WITHDATA.pdf")
if shape_norm == False and fakeRate == True and zjetsEmbed == True and systematics == True and plotData == True and channel =="ztautaucontrolvbf" and presel == True and DYShape == False and plotSave == True:
	if var == "collMass_type1":
		canvas.SaveAs(savedir+"muhad_VBF_ztautau_control.pdf")
	elif var == "vbfDeta":
                canvas.SaveAs(savedir+"muhad_VBF_ztautau_control_dEta_jj.pdf")
        elif var == "vbfMass":
                canvas.SaveAs(savedir+"muhad_VBF_ztautau_control_Mjj.pdf")
        elif var == "vbfj1eta":
                canvas.SaveAs(savedir+"muhad_VBF_ztautau_control_jet1eta.pdf")
        elif var == "vbfj2eta":
                canvas.SaveAs(savedir+"muhad_VBF_ztautau_control_jet2eta.pdf")
        elif var == "vbfj1pt":
                canvas.SaveAs(savedir+"muhad_VBF_ztautau_control_jet1pt.pdf")
        elif var == "vbfj2pt":
                canvas.SaveAs(savedir+"muhad_VBF_ztautau_control_jet2pt.pdf")
if shape_norm == False and fakeRate == True and zjetsEmbed == True and systematics == True and plotData == False and channel =="vbf" and presel == False and DYShape == False and plotSave == True and blind == False:
	if var == "collMass_type1":
		canvas.SaveAs(savedir + "muhad_VBF_m_colinear_After_Allsel.pdf")
if shape_norm == False and fakeRate == True and zjetsEmbed == True and systematics == True and plotData == True and channel =="vbf" and presel == False and DYShape == False and plotSave == True and blind == True:
        if var == "collMass_type1":
                canvas.SaveAs(savedir + "muhad_VBF_m_colinear_After_allsel_WITHDATA.pdf")
if shape_norm == False and fakeRate == True and zjetsEmbed == True and systematics == True and plotData == True and channel =="gg1" and presel == False and DYShape == False and plotSave == True and blind == True:
        if var == "collMass_type1":
                canvas.SaveAs(savedir + "muhad_Boost_m_colinear_After_Allsel_WITHDATA.pdf")
if shape_norm == False and fakeRate == True and zjetsEmbed == True and systematics == True and plotData == True and channel =="gg0" and presel == False and DYShape == False and plotSave == True and blind == True:
        if var == "collMass_type1":
                canvas.SaveAs(savedir + "muhad_GG_m_colinear_After_Allsel_WITHDATA.pdf")

if shape_norm == True and fakeRate == True and zjetsEmbed == True and systematics == False and plotData == False and channel =="vbf" and presel == True and DYShape == False and plotSave == True:
	if var == "collMass_type1":
		canvas.SaveAs(savedir+"m_colinear_muhad_VBF_After_Presel_Shape.pdf")
print "data scale factor = " + str(data.Integral()/data.GetEffectiveEntries())
if fakeRate == True:
	print "fakes scale factor = " + str(wjets.Integral()/data.GetEffectiveEntries())
if zjetsEmbed == True:
	print "z tau tau scale factor = " + str (zjets.Integral()/zjets.GetEffectiveEntries())
	print "z jets other scale factor = " + str(zjetsother.Integral()/zjetsother.GetEffectiveEntries())
print "ttbar scale factor = " + str (ttbar.Integral()/ttbar.GetEffectiveEntries())
print "ww scale factor = " + str (ww.Integral()/ww.GetEffectiveEntries())
print "singlet scale factor = " + str(singlet.Integral()/singlet.GetEffectiveEntries())
print "LFV VBF scale factor = " + str(hvbflfv.Integral()*0.1/hvbflfv.GetEffectiveEntries())
print "LFV GG scale factor = " + str(hgglfv.Integral()*0.1/hgglfv.GetEffectiveEntries())
print "SM GG scale factor = " + str (hggsm.Integral()*0.1/hggsm.GetEffectiveEntries())
print "SM VBF scale factor = " + str(hvbfsm.Integral()*0.1/hvbfsm.GetEffectiveEntries())
if hggww.GetEffectiveEntries() == 0:
	print "WW HGG scale factor = 0.272249527694" 
else:
	print "WW HGG scale factor = " + str (hggww.Integral()/hggww.GetEffectiveEntries())
print "WW HVBF scale factor = " + str(hvbfww.Integral()/hvbfww.GetEffectiveEntries())
print "WZ scale factor = " + str(wz.Integral()/wz.GetEffectiveEntries())
print "ZZ scale factor = " + str(zz.Integral()/zz.GetEffectiveEntries())
print "VH SM scale factor = " + str(vhsm.Integral()/vhsm.GetEffectiveEntries())
print "VH LFV scale factor = " + str(vhlfv.Integral()/vhlfv.GetEffectiveEntries())
if hwwvhtth.GetEffectiveEntries() == 0:
	print "HWWVHTTH scale factor = 0.0307283633846"
else:
	print "HWWVHTTH scale factor = " + str(hwwvhtth.Integral()/hwwvhtth.GetEffectiveEntries())
if fakeRate == False:
	print "QCD Yield: " + str(yieldHisto(qcd,lowbound,highbound))
	print "W+jets Yield: " + str(yieldHisto(wjets,lowbound,highbound))
	print "Wplus1Jets Yield: " + str(yieldHisto(wjets1,lowbound,highbound))
	print "Wplus2Jets Yield: " + str(yieldHisto(wjets2,lowbound,highbound))
	print "Wplus3Jets Yield: " + str(yieldHisto(wjets3,lowbound,highbound))
	print "Wplus4Jets Yield: " + str(yieldHisto(wjets4,lowbound,highbound))
	print "WplusJetsFiltered Yield: " + str(yieldHisto(wjetsFiltered,lowbound,highbound))

else:
	print "Fakes Yield: " + str(yieldHisto(wjets,lowbound,highbound))
print "Data Yield: " + str(yieldHisto(data,lowbound,highbound))
if zjetsEmbed == True:
	print "ZTauTau Yield: " + str(yieldHisto(zjets,lowbound,highbound))
	print "Zjetsother Yield: " + str(yieldHisto(zjetsother,lowbound,highbound))
print "TTBar Yield: " + str(yieldHisto(ttbar,lowbound,highbound))
print "WW Yield: " + str(yieldHisto(ww,lowbound,highbound))
print "Singlet Yield: " + str(yieldHisto(singlet,lowbound,highbound))
print "LFV VBF Yield: " + str(yieldHisto(hvbflfv,lowbound,highbound))
print "LFV GG Yield: " + str(yieldHisto(hgglfv,lowbound,highbound))
print "SM GG Yield: " + str(yieldHisto(hggsm,lowbound,highbound))
print "WW HGG Yield: " +str(yieldHisto(hggww,lowbound,highbound))
print "WW HVBF Yield: " + str(yieldHisto(hvbfww,lowbound,highbound))
print "WW Full Yield: " + str(yieldHisto(wwfull,lowbound,highbound))
print "WZ Yield: " + str(yieldHisto(wz,lowbound,highbound))
print "ZZ Yield: " + str(yieldHisto(zz,lowbound,highbound))
print "VHSM Yield: " + str(yieldHisto(vhsm,lowbound,highbound))
print "VHLFV Yield: " + str(yieldHisto(vhlfv,lowbound,highbound))
print "HWWVHTTH Yield: " + str(yieldHisto(hwwvhtth,lowbound,highbound))
