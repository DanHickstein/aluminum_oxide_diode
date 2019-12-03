import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate
from io import StringIO
import warnings


def main():
    fig, axs = plt.subplots(2, 1, figsize=(10,8), dpi=100, tight_layout=True)

    wl, responsivity, uncertainty, uncertainty_percent = get_nist_data()
    new_wls = np.linspace(np.min(wl), np.max(wl), 1000)
    new_respon = interpolated_responsivity(new_wls)

    for ax in axs:
        ax.errorbar(wl, responsivity, uncertainty, marker='o', ms=4, label='NIST measured data')
        ax.plot(new_wls, new_respon, label='Spline fit')

        ax.grid(alpha=0.2)
        ax.grid(alpha=0.1, which='minor')
        ax.set_xlabel('Wavelength (nm)')
        ax.set_ylabel('Responsivity (A/W)')

    axs[0].legend()
    axs[0].set_title('Calibration for NIST aluminum oxide diode SN 448, calibrated July 17, 2019')
    axs[1].set_yscale('log')

    fund = 1035.0
    for h in [5,6,7,8,9,10]:
        hwl = fund/h
        resp = interpolated_responsivity(hwl)
        axs[1].plot(hwl, resp, 'o', color='r')
        axs[1].annotate('H%i, %.1f nm: %.2e A/W'%(h, hwl, resp), xy=(hwl, resp), xytext=(5,5), textcoords='offset points', ha='left', fontsize=8, color='r')


    plt.savefig('Diode responsivity.png', dpi=200)
    plt.show()


data_from_nist = u"""\
Wavelength (nm)	Responsivity (mA/W)	Uncertainty (mA/W) k=2	Uncertainty (%) k=2
51.9	7.85150	1.71718	21.87
53.7	8.94460	0.87438	9.78
55.6	9.87450	0.74643	7.56
58.4	10.34000	0.66455	6.43
59.9	11.79000	0.99163	8.41
62.2	13.02500	0.88038	6.76
63.9	13.42700	0.87347	6.51
65.7	13.21800	0.80872	6.12
66.9	14.45400	0.95339	6.60
68.3	14.61300	0.93873	6.42
69.9	15.60700	1.42770	9.15
71.2	15.56000	1.16939	7.52
73.5	13.69200	1.04588	7.64
75.2	14.57400	0.94395	6.48
77.1	14.85700	0.90851	6.12
80.0	14.24900	1.00143	7.03
81.8	14.89700	0.93127	6.25
84.4	14.85400	0.95054	6.40
86.5	13.25400	0.81435	6.14
88.6	12.91000	0.75156	5.82
92.0	12.48100	0.71261	5.71
116.4	2.19550	0.20918	9.53
118.0	1.73280	0.16525	9.54
121.6	1.08140	0.10316	9.54
125.4	0.71479	0.06900	9.65
135.4	0.24339	0.00779	3.20
140.3	0.13161	0.00445	3.38
144.1	0.07749	0.01492	19.25
148.7	0.02897	0.00114	3.93
154.5	0.01784	0.00154	8.65
160.8	0.01080	0.00050	4.62
164.8	0.00942	0.00097	10.27
170.1	0.00843	0.00038	4.53
175.0	0.00749	0.00067	8.92
182.3	0.00666	0.00118	17.71
187.9	0.00605	0.00100	16.54
193.7	0.00382	0.00085	22.28
200.0	0.00293	0.00052	17.88
206.7	0.00176	0.00022	12.30
215.0	0.00176	0.00097	55.19
220.0	0.00129	0.00104	80.36
225.0	0.00103	0.00056	54.48
230.0	0.00081	0.00154	188.89
235.0	0.00029	0.00152	525.23
240.1	0.00076	0.00055	72.49
245.1	0.00047	0.00027	57.96
249.9	0.00025	0.00201	797.10
255.1	0.00192	0.00036	18.59"""


def get_nist_data():

    # Wavelength is in nm, responsivity and uncertainty are in mA/W.
    wl, responsivity, uncertainty, uncertainty_percent = np.loadtxt(StringIO(data_from_nist), unpack=True, skiprows=1)
    return wl, responsivity*1e-3, uncertainty*1e-3, uncertainty_percent

wl, responsivity, uncertainty, uncertainty_percent = get_nist_data()
interp = scipy.interpolate.UnivariateSpline(wl, responsivity, s=len(wl)*5e-12)


def interpolated_responsivity(wavelength):
    if np.any(wavelength>np.max(wl)) or np.any(wavelength<np.min(wl)):
        warnings.warn("Warning: you are requesting values outside of the data range. Exterpolation will be attempted, but the results might not be good.")

    respon = interp(wavelength)
    return respon




if __name__ == '__main__':
    main()
