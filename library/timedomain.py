import matplotlib
import matplotlib.pyplot as plt
import numpy as np 


def transform(F,S,verbose=0,overs=0,window=False):
	"""
	Transforms f,s into time domain and returns distance to first and second peak in metres

	USAGE: transform(F,S,verbose,overs,window)
	where,
	F is frequency vector in Hz
	S is S21 s-parameter vector as a dimentionless voltage ratio in complex form
	verbose is verbosity: Increasing levels of detail outputted. Ranges from 1 which just provides output to 3 which plots graphs with zoom to peak 
	overs is multiplies the length of the S vector by padding with zeros [default = 0]
	window applies a Hanning window [default = False]
	"""
    	# transforms f,s into time domain, returns time of peak
    	# overs times frequency extension for oversampling
    	# window True will apply a hanning window to the frequency data
    	# verbose:  0=no printing, just return range   1=print summary  2=close-up graphs  3=full graph + close-up
    	# Improved on 13 Oct 2016 - when oversampling, rounds off to the nearest power of two
    	# Assume F is in Hz
    
    	pts = np.shape(F)[0]
    	c = 299792458
    	fmax=F[-1]+(F[2]-F[1]) # fmax is one more than the last frequency in the file
    
    	# add the DC value
    	if F[0]>0:
        	pts = pts + 1;
        	S = np.insert(S,0,0)
        if verbose>2: print 'Transform: adding a DC value to the file'
    
    	# apply a window
    	if window:
        	w=np.hanning(pts*2); w=w[pts:];  w=w/mean(w);
        	S = S * w;
        	if verbose>2: print 'Transform: applying Hanning window'

    	# IFFT without oversampling
    	T = np.fft.ifft(S);
    	X = np.linspace(0,c/F[0],pts,endpoint=False);
        
    	# Oversample by extending frequency axis and IFFT again
    	if overs>0:
        	newtotallength=int(2**np.floor(np.log(overs*pts)/np.log(2)))
        	#print 'Oversampling. You requested %i, you get %i x (rounding to power of two)' % (overs,int(newtotallength/pts))
        	FO=np.linspace(fmax/pts,fmax*overs,newtotallength,endpoint=True);  # changed endpoint from True
        	SO = np.pad(S,(0,newtotallength-pts),'constant')
        	TO = np.fft.ifft(SO)*(newtotallength*1.0/pts);
        	XO = np.linspace(0,c/F[0],newtotallength,endpoint=False);
    	else:
        	TO = T;
        	XO = X;

        
    	# find the first peak
    	peakindex = np.abs(TO).argmax()
    	Xpeak=XO[peakindex]
    	Tpeak=np.abs(TO[peakindex])
    	peakrange = slice(peakindex-5*overs,peakindex+5*overs)   # speed up the graph
	    
	# find the second peak
	reduced_TO = np.copy(TO)
	reduced_TO[peakindex-5*(1+overs):peakindex+5*(1+overs)] = 0.0000000001
	peakindex2 = (20*np.log10(np.abs(reduced_TO))).argmax()
	Xpeak2 = XO[peakindex2]
	Tpeak2 = np.abs(TO[peakindex2])
	peakrange2 = slice(peakindex2-5*overs,peakindex2+5*overs)

    	# plot if requested
    	if verbose>2:
        	# plot - wide
        	plt.figure(figsize=(14,6))
        	plt.plot(X,20*np.log10(np.abs(T)),'b-',marker='o',ms=4,lw=1)
        	plt.ylim([-120,1]);  plt.grid(True);   # plt.xlim([0,100]); 
        	plt.ylabel('response, dB');  plt.xlabel('distance, m');  plt.title('Full unambiguous range, first copy')#

    	if verbose>1:
        	# plot - narrow
        	matplotlib.rcParams.update({'font.size': 18})
        	plt.figure(figsize=(15,8))
        	plt.plot(X,20*np.log10(np.abs(T)),'k--',marker='.',ms=16,lw=2,label='normal sampling')
        	if overs>0:
            		plt.plot(XO[peakrange],20*np.log10(np.abs(TO[peakrange])),'k-',lw=2,label='%i x oversampling' % overs)
            		plt.plot(Xpeak,20*np.log10(Tpeak),marker='+',ms=20,color='k',label='detected peak position')
        	plt.xlim([Xpeak-1,Xpeak+1]);
        	plt.ylim([np.around(20*np.log10(Tpeak)-35,decimals=-1),np.around(20*np.log10(Tpeak)+5,decimals=0)]);
        	plt.grid(True); plt.legend(loc=0);
        	plt.ylabel('response, dB');  plt.xlabel('distance, m');
        	#title('Peak at %8.5f m' % Xpeak)

    	if verbose>0: print 'Fmax=%4.1f GHz. %i points, %ix oversampled. Window=%i. Peak found at %8.5f m and %8.5f m' % ((fmax)/1e9, pts, overs, window, Xpeak,Xpeak2)

    	return Xpeak,Xpeak2

def simulatefile(snr=60,fmax=8e9,pts=10001,signals = [[1,10.0]]):
    	# simulatefile(snr=60, fmax=8e9, pts=10001,overs=10,signals = [[1,10.0]])
    	# snr  in dB signal to noise, per-bin. Use >99 for no noise
    	# fmax in Hz
    	# pts = VNA frequency points
    	# signals - list of lists, [[Voltage,Xpos],[...]]
    	# returns vectors of F (freq Hz) and S (response)

    	# First make frequency vector
	F=np.linspace(0,fmax,pts,endpoint=True);
    
    	# initialise the complex response vector and fill with (complex) noise
    	R=np.zeros(np.shape(F)[0]);
    	if snr<99:
        	R = R + np.random.randn(np.shape(F)[0])*np.exp(1.0j*np.random.random(np.shape(F)[0])*2*np.pi)*10**(-snr/20)*np.sqrt(pts);
    
    	# add each of the signals
    	c = 299792458
    	for a in signals:
        	R = R + a[0]*exp(-1.0j*2*np.pi*a[1]*F/c);

    	# to do - phase noise on the signals
    	# to do - frequency quantisation - if applicable. The VNA must have a minimum frequency step?
    	# to do - non-flat passband modelling
    	# to do - fibre optic time-domain effects if any
    
    	return F,R

def plotresponse(F,S):
    	# plots the magnitude and phase of the response
    	plt.figure(figsize=(14,2))
    	plt.plot(F,20*np.log10(np.abs(S)))
    	plt.grid(True); plt.xlabel('Frequency, GHz'); plt.ylabel('Response, dB'); plt.title('Response magnitude plot')
    	plt.figure(figsize=(14,2))
    	plt.plot(F,180*np.unwrap(np.angle(S))/np.pi)
    	plt.grid(True); plt.xlabel('Frequency, GHz'); plt.ylabel('Unwrapped phase, Kdegrees'); plt.title('Response phase plot')
