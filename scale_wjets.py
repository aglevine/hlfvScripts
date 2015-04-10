from sys import argv, stdout, stderr
import ROOT
import sys

savedir = 'vbf_fullmt/'

wjets_file = ROOT.TFile(savedir+'WplusJets_madgraph_Extension.root')
wjets1_file = ROOT.TFile(savedir+'Wplus1Jets_madgraph.root')
wjets2_file = ROOT.TFile(savedir+'Wplus2Jets_madgraph.root')
wjets3_file = ROOT.TFile(savedir+'Wplus3Jets_madgraph.root')
wjets4_file = ROOT.TFile(savedir+'Wplus4Jets_madgraph.root')

wjets_file.cd()
dirList = ROOT.gDirectory.GetListOfKeys()
for k1 in dirList:
	print k1
	h1 = k1.GetTitle()
	print h1
	wjets_file.cd(h1)
	varList = ROOT.gDirectory.GetListOfKeys()
	for v1 in varList:
		print v1
		
	


