﻿# -*- coding: utf-8 -*-
"""
    biosppy.plotting
    ----------------
    
    This module provides utilities to plot data.
    
    :copyright: (c) 2015 by Instituto de Telecomunicacoes
    :license: BSD 3-clause, see LICENSE for more details.
"""

# Imports
# built-in
import os

# 3rd party
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

# local
from . import utils
from biosppy.signals import tools as st

# Globals
MAJOR_LW = 2.5
MINOR_LW = 1.5

# matplotlib definitions
### TO DO
### fig.tight_layout()


def _plot_filter(b, a, sampling_rate=1000., nfreqs=512, ax=None):
    """Compute and plot the frequency response of a digital filter.
    
    Args:
        b (array): Numerator coefficients.
        
        a (array): Denominator coefficients.
        
        sampling_rate (int, float): Sampling frequency (Hz).
        
        nfreqs (int): Number of frequency points to compute.
        
        ax (axis): Plot Axis to use (optional).
    
    Returns:
        fig (Figure): Figure object.
    
    """
    
    # compute frequency response
    freqs, resp = st._filter_resp(b, a, sampling_rate=sampling_rate, nfreqs=nfreqs)
    
    # plot
    if ax is None:
        fig = plt.figure()
        ax = fig.add_subplot(111)
    else:
        fig = ax.figure
    
    # amplitude
    ax.semilogy(freqs, np.abs(resp), 'b', linewidth=MAJOR_LW)
    ax.set_ylabel('Amplitude (dB)', color='b')
    ax.set_xlabel('Frequency (Hz)')
    
    # phase
    angles = np.unwrap(np.angle(resp))
    ax2 = ax.twinx()
    ax2.plot(freqs, angles, 'g', linewidth=MAJOR_LW)
    ax2.set_ylabel('Angle (radians)', color='g')
    
    ax.grid()
    
    return fig


def plot_filter(ftype='FIR', band='lowpass', order=None, frequency=None,
                sampling_rate=1000., path=None, show=True, **kwargs):
    """Plot the frequency response of the filter specified with the given parameters.
    
    Args:
        ftype (str): Filter type:
            * Finite Impulse Response filter ('FIR');
            * Butterworth filter ('butter');
            * Chebyshev filters ('cheby1', 'cheby2');
            * Elliptic filter ('ellip');
            * Bessel filter ('bessel').
        
        band (str): Band type:
            * Low-pass filter ('lowpass');
            * High-pass filter ('highpass');
            * Band-pass filter ('bandpass');
            * Band-stop filter ('bandstop').
        
        order (int): Order of the filter.
        
        frequency (int, float, list, array): Cutoff frequencies; format depends on type of band:
            * 'lowpass' or 'bandpass': single frequency;
            * 'bandpass' or 'bandstop': pair of frequencies.
        
        sampling_rate (int, float): Sampling frequency (Hz).
        
        path (str): If provided, the plot will be saved to the specified file (optional).
        
        show (bool): If True, show the plot immediately.
        
        **kwargs (dict): Additional keyword arguments are passed to the underlying scipy.signal function.
    
    """
    
    # get filter
    b, a = st.get_filter(ftype=ftype, band=band, order=order, frequency=frequency,
                         sampling_rate=sampling_rate, **kwargs)
    
    # plot
    fig = _plot_filter(b, a, sampling_rate)
    
    # save to file
    if path is not None:
        path = utils.normpath(path)
        root, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext not in ['png', 'jpg']:
            path = root + '.png'
        
        fig.savefig(path, dpi=200, bbox_inches='tight')
    
    # show
    if show:
        plt.show()
    
    # close
    plt.close(fig)


def plot_spectrum(signal=None, sampling_rate=1000., path=None, show=True):
    """Plot the power spectrum of a signal (one-sided).
    
    Args:
        signal (array): Input signal.
        
        sampling_rate (int, float): Sampling frequency (Hz).
        
        path (str): If provided, the plot will be saved to the specified file (optional).
        
        show (bool): If True, show the plot immediately.
    
    """
    
    freqs, power = st.power_spectrum(signal, sampling_rate, pad=0, pow2=False, decibel=True)
    
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ax.plot(freqs, power, linewidth=MAJOR_LW)
    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Power (dB)')
    ax.grid()
    
    # save to file
    if path is not None:
        path = utils.normpath(path)
        root, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext not in ['png', 'jpg']:
            path = root + '.png'
        
        fig.savefig(path, dpi=200, bbox_inches='tight')
    
    # show
    if show:
        plt.show()
    
    # close
    plt.close(fig)


def plot_bvp(ts=None, raw=None, filtered=None, onsets=None, heart_rate_ts=None,
             heart_rate=None, path=None, show=False):
    """Create a summary plot from the output of signals.bvp.bvp.
    
    Args:
        ts (array): Signal time axis reference (seconds).
        
        raw (array): Raw BVP signal.
        
        filtered (array): Filtered BVP signal.
        
        onsets (array): Indices of BVP pulse onsets.
        
        heart_rate_ts (array): Heart rate time axis reference (seconds).
        
        heart_rate (array): Instantaneous heart rate (bpm).
        
        path (str): If provided, the plot will be saved to the specified file (optional).
        
        show (bool): If True, show the plot immediately.
    
    """
    
    fig = plt.figure()
    fig.suptitle('BVP Summary')
    
    # raw signal
    ax1 = fig.add_subplot(311)
    
    ax1.plot(ts, raw, linewidth=MAJOR_LW, label='Raw')
    
    ax1.set_ylabel('Amplitude')
    ax1.legend()
    ax1.grid()
    
    # filtered signal with onsets
    ax2 = fig.add_subplot(312, sharex=ax1)
    
    ymin = np.min(filtered)
    ymax = np.max(filtered)
    alpha = 0.1 * (ymax - ymin)
    ymax += alpha
    ymin -= alpha
    
    ax2.plot(ts, filtered, linewidth=MAJOR_LW, label='Filtered')
    ax2.vlines(ts[onsets], ymin, ymax, color='m', linewidth=MINOR_LW, label='Onsets')
    
    ax2.set_ylabel('Amplitude')
    ax2.legend()
    ax2.grid()
    
    # heart rate
    ax3 = fig.add_subplot(313, sharex=ax1)
    
    ax3.plot(heart_rate_ts, heart_rate, linewidth=MAJOR_LW, label='Heart Rate')
    
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Heart Rate (bmp)')
    ax3.legend()
    ax3.grid()
    
    # save to file
    if path is not None:
        path = utils.normpath(path)
        root, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext not in ['png', 'jpg']:
            path = root + '.png'
        
        fig.savefig(path, dpi=200, bbox_inches='tight')
    
    # show
    if show:
        plt.show()
    
    # close
    plt.close(fig)


def plot_eda(ts=None, raw=None, filtered=None, onsets=None, peaks=None,
             amplitudes=None, path=None, show=False):
    """Create a summary plot from the output of signals.eda.eda.
    
    Args:
        ts (array): Signal time axis reference (seconds).
        
        raw (array): Raw EDA signal.
        
        filtered (array): Filtered EDA signal.
        
        onsets (array): Indices of SCR pulse onsets.
        
        peaks (array): Indices of the SCR peaks.
        
        amplitudes (array): SCR pulse amplitudes.
        
        path (str): If provided, the plot will be saved to the specified file (optional).
        
        show (bool): If True, show the plot immediately.
    
    """
    
    fig = plt.figure()
    fig.suptitle('EDA Summary')
    
    # raw signal
    ax1 = fig.add_subplot(311)
    
    ax1.plot(ts, raw, linewidth=MAJOR_LW, label='raw')
    
    ax1.set_ylabel('Amplitude')
    ax1.legend()
    ax1.grid()
    
    # filtered signal with onsets, peaks
    ax2 = fig.add_subplot(312, sharex=ax1)
    
    ymin = np.min(filtered)
    ymax = np.max(filtered)
    alpha = 0.1 * (ymax - ymin)
    ymax += alpha
    ymin -= alpha
    
    ax2.plot(ts, filtered, linewidth=MAJOR_LW, label='Filtered')
    ax2.vlines(ts[onsets], ymin, ymax, color='m', linewidth=MINOR_LW, label='Onsets')
    ax2.vlines(ts[peaks], ymin, ymax, color='g', linewidth=MINOR_LW, label='Peaks')
    
    ax2.set_ylabel('Amplitude')
    ax2.legend()
    ax2.grid()
    
    # amplitudes
    ax3 = fig.add_subplot(313, sharex=ax1)
    
    ax3.plot(ts[onsets], amplitudes, linewidth=MAJOR_LW, label='Amplitudes')
    
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Amplitude')
    ax3.legend()
    ax3.grid()
    
    # save to file
    if path is not None:
        path = utils.normpath(path)
        root, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext not in ['png', 'jpg']:
            path = root + '.png'
        
        fig.savefig(path, dpi=200, bbox_inches='tight')
    
    # show
    if show:
        plt.show()
    
    # close
    plt.close(fig)


def plot_emg(ts=None, raw=None, filtered=None, onsets=None, path=None, show=False):
    """Create a summary plot from the output of signals.emg.emg.
    
    Args:
        ts (array): Signal time axis reference (seconds).
        
        raw (array): Raw EMG signal.
        
        filtered (array): Filtered EMG signal.
        
        onsets (array): Indices of EMG pulse onsets.
        
        path (str): If provided, the plot will be saved to the specified file (optional).
        
        show (bool): If True, show the plot immediately.
    
    """
    
    fig = plt.figure()
    fig.suptitle('EMG Summary')
    
    # raw signal
    ax1 = fig.add_subplot(211)
    
    ax1.plot(ts, raw, linewidth=MAJOR_LW, label='Raw')
    
    ax1.set_ylabel('Amplitude')
    ax1.legend()
    ax1.grid()
    
    # filtered signal with onsets
    ax2 = fig.add_subplot(212, sharex=ax1)
    
    ymin = np.min(filtered)
    ymax = np.max(filtered)
    alpha = 0.1 * (ymax - ymin)
    ymax += alpha
    ymin -= alpha
    
    ax2.plot(ts, filtered, linewidth=MAJOR_LW, label='Filtered')
    ax2.vlines(ts[onsets], ymin, ymax, color='m', linewidth=MINOR_LW, label='Onsets')
    
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Amplitude')
    ax2.legend()
    ax2.grid()
    
    # save to file
    if path is not None:
        path = utils.normpath(path)
        root, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext not in ['png', 'jpg']:
            path = root + '.png'
        
        fig.savefig(path, dpi=200, bbox_inches='tight')
    
    # show
    if show:
        plt.show()
    
    # close
    plt.close(fig)


def plot_resp(ts=None, raw=None, filtered=None, zeros=None, resp_rate_ts=None,
              resp_rate=None, path=None, show=False):
    """Create a summary plot from the output of signals.bvp.bvp.
    
    Args:
        ts (array): Signal time axis reference (seconds).
        
        raw (array): Raw BVP signal.
        
        filtered (array): Filtered BVP signal.
        
        zeros (array): Indices of Respiration zero crossings.
        
        resp_rate_ts (array): Respiration rate time axis reference (seconds).
        
        resp_rate (array): Instantaneous respiration rate (Hz).
        
        path (str): If provided, the plot will be saved to the specified file (optional).
        
        show (bool): If True, show the plot immediately.
    
    """
    
    fig = plt.figure()
    fig.suptitle('Respiration Summary')
    
    # raw signal
    ax1 = fig.add_subplot(311)
    
    ax1.plot(ts, raw, linewidth=MAJOR_LW, label='Raw')
    
    ax1.set_ylabel('Amplitude')
    ax1.legend()
    ax1.grid()
    
    # filtered signal with zeros
    ax2 = fig.add_subplot(312, sharex=ax1)
    
    ymin = np.min(filtered)
    ymax = np.max(filtered)
    alpha = 0.1 * (ymax - ymin)
    ymax += alpha
    ymin -= alpha
    
    ax2.plot(ts, filtered, linewidth=MAJOR_LW, label='Filtered')
    ax2.vlines(ts[zeros], ymin, ymax, color='m', linewidth=MINOR_LW, label='Zero crossings')
    
    ax2.set_ylabel('Amplitude')
    ax2.legend()
    ax2.grid()
    
    # heart rate
    ax3 = fig.add_subplot(313, sharex=ax1)
    
    ax3.plot(resp_rate_ts, resp_rate, linewidth=MAJOR_LW, label='Respiration Rate')
    
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Respiration Rate (Hz)')
    ax3.legend()
    ax3.grid()
    
    # save to file
    if path is not None:
        path = utils.normpath(path)
        root, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext not in ['png', 'jpg']:
            path = root + '.png'
        
        fig.savefig(path, dpi=200, bbox_inches='tight')
    
    # show
    if show:
        plt.show()
    
    # close
    plt.close(fig)


def plot_eeg(ts=None, raw=None, filtered=None, labels=None, features_ts=None,
             theta=None, alpha_low=None, alpha_high=None, beta=None,
             gamma=None, plf_pairs=None, plf=None, path=None, show=False):
    """Create a summary plot from the output of signals.eeg.eeg.
    
    Args:
        ts (array): Signal time axis reference (seconds).
        
        raw (array): Raw EEG signal.
        
        filtered (array): Filtered EEG signal.
        
        labels (list): Channel labels.
        
        features_ts (array): Features time axis reference (seconds).
        
        theta (array): Average power in the 4 to 8 Hz frequency band; each column is one EEG channel.
        
        alpha_low (array): Average power in the 8 to 10 Hz frequency band; each column is one EEG channel.
        
        alpha_high (array): Average power in the 10 to 13 Hz frequency band; each column is one EEG channel.
        
        beta (array): Average power in the 13 to 25 Hz frequency band; each column is one EEG channel.
        
        gamma (array): Average power in the 25 to 40 Hz frequency band; each column is one EEG channel.
        
        plf_pairs (list): PLF pair indices.
        
        plf (array): PLF matrix; each column is a channel pair.
        
        path (str): If provided, the plot will be saved to the specified file (optional).
        
        show (bool): If True, show the plot immediately.
    
    """
    
    nrows = 10
    alpha = 2.
    
    figs = []
    
    # raw
    fig = _plot_multichannel(ts=ts, signal=raw, labels=labels,
                             nrows=nrows, alpha=alpha,
                             title='EEG Summary - Raw',
                             xlabel='Time (s)',
                             ylabel='Amplitude')
    figs.append(('_Raw', fig))
    
    # filtered
    fig = _plot_multichannel(ts=ts, signal=filtered, labels=labels,
                             nrows=nrows, alpha=alpha,
                             title='EEG Summary - Filtered',
                             xlabel='Time (s)',
                             ylabel='Amplitude')
    figs.append(('_Filtered', fig))
    
    # band-power
    names = ('Theta Band', 'Lower Alpha Band', 'Higher Alpha Band', 'Beta Band', 'Gamma Band')
    args = (theta, alpha_low, alpha_high, beta, gamma)
    for n, a in zip(names, args):
        fig = _plot_multichannel(ts=features_ts, signal=a, labels=labels,
                                 nrows=nrows, alpha=alpha,
                                 title='EEG Summary - %s' % n,
                                 xlabel='Time (s)',
                                 ylabel='Power')
        figs.append(('_' + n.replace(' ', '_'), fig))
    
    # PLF
    plf_labels = ['%s vs %s' % (labels[p[0]], labels[p[1]]) for p in plf_pairs]
    fig = _plot_multichannel(ts=features_ts, signal=plf, labels=plf_labels,
                             nrows=nrows, alpha=alpha,
                             title='EEG Summary - Phase-Locking Factor',
                             xlabel='Time (s)',
                             ylabel='PLF')
    figs.append(('_PLF', fig))
    
    # save to file
    if path is not None:
        path = utils.normpath(path)
        root, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext not in ['png', 'jpg']:
            ext = '.png'
        
        for n, fig in figs:
            path = root + n + ext
            fig.savefig(path, dpi=200, bbox_inches='tight')
    
    # show
    if show:
        plt.show()
    
    # close
    for _, fig in figs:
        plt.close(fig)


def _yscaling(signal=None, alpha=1.5):
    """Get y axis limits for a signal with scaling.
    
    Args:
        signal (array): Input signal
        
        alpha (float): Scaling factor.
    
    Returns:
        ymin (float): Minimum y value.
        
        ymax (float): Maximum y value.
    
    """
    
    mi = np.min(signal)
    m = np.mean(signal)
    mx = np.max(signal)
    
    if mi == mx:
        ymin = m - 1
        ymax = m + 1
    else:
        ymin = m - alpha * (m - mi)
        ymax = m + alpha * (mx - m)
    
    return ymin, ymax


def _plot_multichannel(ts=None, signal=None, labels=None, nrows=10, alpha=2., title=None, xlabel=None, ylabel=None):
    """Plot a multi-channel signal.
    
    Args:
        ts (array): Signal time axis reference (seconds).
        
        signal (array): Multi-channel signal; each column is one channel.
        
        labels (list): Channel labels (optional).
        
        nrows (int): Maximum number of rows to use (optional).
        
        alpha (float): Scaling factor for y axis.
        
        title (str): Plot title (optional).
        
        xlabel (str): Label for x axis (optional).
        
        ylabel (str): Label for y axis (optional).
    
    Returns:
        fig (Figure): Figure object.
    
    """
    
    # ensure numpy
    signal = np.array(signal)
    nch = signal.shape[1]
    
    # check labels
    if labels is None:
        labels = ['Ch. %d' % i for i in xrange(nch)]
    
    nrows = 10
    if nch < nrows:
        nrows = nch
    
    ncols = int(np.ceil(nch / float(nrows)))
    
    fig = plt.figure()
    
    # title
    if title is not None:
        fig.suptitle(title)
    
    gs = gridspec.GridSpec(nrows, ncols, hspace=0, wspace=0.2)
    
    # reference axes
    ax0 = fig.add_subplot(gs[0, 0])
    ax0.plot(ts, signal[:, 0], linewidth=MAJOR_LW, label=labels[0])
    ymin, ymax = _yscaling(signal[:, 0], alpha=alpha)
    ax0.set_ylim(ymin, ymax)
    ax0.legend()
    ax0.grid()
    axs = {(0, 0): ax0}
    
    for i in xrange(1, nch-1):
        a = i % nrows
        b = int(np.floor(i / float(nrows)))
        ax = fig.add_subplot(gs[a, b], sharex=ax0)
        axs[(a, b)] = ax
        
        ax.plot(ts, signal[:, i], linewidth=MAJOR_LW, label=labels[i])
        ymin, ymax = _yscaling(signal[:, i], alpha=alpha)
        ax.set_ylim(ymin, ymax)
        ax.legend()
        ax.grid()
    
    # last plot
    i = nch - 1
    a = i % nrows
    b = int(np.floor(i / float(nrows)))
    ax = fig.add_subplot(gs[a, b], sharex=ax0)
    axs[(a, b)] = ax
    
    ax.plot(ts, signal[:, -1], linewidth=MAJOR_LW, label=labels[-1])
    ymin, ymax = _yscaling(signal[:, -1], alpha=alpha)
    ax.set_ylim(ymin, ymax)
    ax.legend()
    ax.grid()
    
    if xlabel is not None:
        ax.set_xlabel(xlabel)
        
        for b in xrange(0, ncols - 1):
            a = nrows - 1
            ax = axs[(a, b)]
            ax.set_xlabel(xlabel)
    
    if ylabel is not None:
        # middle left
        a = nrows / 2
        ax = axs[(a, 0)]
        ax.set_ylabel(ylabel)
    
    return fig


def plot_ecg(ts=None, raw=None, filtered=None, rpeaks=None, templates_ts=None,
             templates=None, heart_rate_ts=None, heart_rate=None, path=None, show=False):
    """Create a summary plot from the output of signals.ecg.ecg.
    
    Args:
        ts (array): Signal time axis reference (seconds).
        
        raw (array): Raw BVP signal.
        
        filtered (array): Filtered BVP signal.
        
        rpeaks (array): R-peak location indices.
        
        templates_ts (array): Templates time axis reference (seconds).
        
        templates (array): Extracted heartbeat templates.
        
        heart_rate_ts (array): Heart rate time axis reference (seconds).
        
        heart_rate (array): Instantaneous heart rate (bpm).
        
        path (str): If provided, the plot will be saved to the specified file (optional).
        
        show (bool): If True, show the plot immediately.
    
    """
    
    fig = plt.figure()
    fig.suptitle('ECG Summary')
    gs = gridspec.GridSpec(6, 2)
    
    # raw signal
    ax1 = fig.add_subplot(gs[:2, 0])
    
    ax1.plot(ts, raw, linewidth=MAJOR_LW, label='Raw')
    
    ax1.set_ylabel('Amplitude')
    ax1.legend()
    ax1.grid()
    
    # filtered signal with rpeaks
    ax2 = fig.add_subplot(gs[2:4, 0], sharex=ax1)
    
    ymin = np.min(filtered)
    ymax = np.max(filtered)
    alpha = 0.1 * (ymax - ymin)
    ymax += alpha
    ymin -= alpha
    
    ax2.plot(ts, filtered, linewidth=MAJOR_LW, label='Filtered')
    ax2.vlines(ts[rpeaks], ymin, ymax, color='m', linewidth=MINOR_LW, label='R-peaks')
    
    ax2.set_ylabel('Amplitude')
    ax2.legend()
    ax2.grid()
    
    # heart rate
    ax3 = fig.add_subplot(gs[4:, 0], sharex=ax1)
    
    ax3.plot(heart_rate_ts, heart_rate, linewidth=MAJOR_LW, label='Heart Rate')
    
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Heart Rate (bmp)')
    ax3.legend()
    ax3.grid()
    
    # templates
    ax4 = fig.add_subplot(gs[1:5, 1])
    
    ax4.plot(templates_ts, templates.T, 'm', linewidth=MINOR_LW, alpha=0.7)
    
    ax4.set_xlabel('Time (s)')
    ax4.set_ylabel('Amplitude')
    ax4.set_title('Templates')
    ax4.grid()
    
    # save to file
    if path is not None:
        path = utils.normpath(path)
        root, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext not in ['png', 'jpg']:
            path = root + '.png'
        
        fig.savefig(path, dpi=200, bbox_inches='tight')
    
    # show
    if show:
        plt.show()
    
    # close
    plt.close(fig)

