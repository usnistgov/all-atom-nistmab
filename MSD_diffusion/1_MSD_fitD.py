import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import os

# =================================================================
# CONFIGURATION & INDIVIDUAL STYLING
# =================================================================
PREFIX = "ci30"
REPS = [1, 2, 3, 4]
DATA_DIR = "/lab/mml/kipp/645div/nistmab/analysis/diffusion/data_output_txt_files/"
FIT_RANGE = (20, 50)
TIMESTEP = 0.5  # ns

# Reference Value
EXP_REF_D = 4e-7  # cm2/s

# Extracted Base Colors (from Rg Plot)
RG_COLORS   = ['#406cb7', '#308e3a', '#f4d922', '#a32727']
# Darker counterparts (Added "black" component)
DARK_COLORS = ['#284473', '#1d5723', '#a89517', '#661818']

STYLING = {
    'com':      {'alpha': [1.0, 1.0, 1.0, 1.0], 'zorder': [10, 10, 11, 9]},
    'atom':     {'alpha': [0.8, 0.7, 0.9, 0.7], 'zorder': [5, 5, 5, 5]},
    'fit_com':  {'alpha': [1.0, 1.0, 1.0, 1.0], 'zorder': [15, 15, 15, 15]},
    'fit_atom': {'alpha': [0.8, 0.8, 0.9, 0.7], 'zorder': [13, 13, 13, 12]}
}

FONT_SIZE = 14
plt.rcParams.update({'font.size': FONT_SIZE})
# =================================================================

def load_rep_data(rep_num, prefix):
    suffix = f"{prefix}_r0{rep_num}.txt"
    return {
        'com': np.loadtxt(os.path.join(DATA_DIR, f"mda_msd_mass_{suffix}")) * 0.01,
        'atom': np.loadtxt(os.path.join(DATA_DIR, f"mda_centeratom_msd_{suffix}")) * 0.01
    }

def calculate_d(lagtimes, msd_values, fit_range):
    mask = (fit_range[0] <= lagtimes) & (lagtimes <= fit_range[1])
    x, y = lagtimes[mask], msd_values[mask]
    if len(x) <= 2: 
        return None, None, None, None, None, None, None
    
    # Run fit and request the covariance matrix to calculate errors
    p, cov = np.polyfit(x, y, 1, cov=True)
    slope, intercept = p[0], p[1]
    
    # Extract standard errors from the diagonal of the covariance matrix
    slope_err = np.sqrt(cov[0, 0])
    intercept_err = np.sqrt(cov[1, 1])
    
    d_coeff = (1.0/6.0) * slope
    d_err = (1.0/6.0) * slope_err
    
    return d_coeff, d_err, slope, slope_err, intercept, intercept_err, (x, slope * x + intercept)

def run_analysis():
    plot_data = []
    results_summary = []
    
    for i, r in enumerate(REPS):
        data = load_rep_data(r, PREFIX)
        lagtimes = np.arange(len(data['atom'])) * TIMESTEP
        rep_curves = []

        for key in ['com', 'atom']:
            # Data Curve: COM is solid ('-'), ATOM is dotted (':')
            rep_curves.append({
                'type': 'data', 'x': lagtimes, 'y': data[key],
                'color': RG_COLORS[i], 'label': f'r0{r} {key.upper()}',
                'alpha': STYLING[key]['alpha'][i],
                'zorder': STYLING[key]['zorder'][i],
                'linestyle': ':' if key == 'atom' else '-'
            })
            
            # Fit Curve: Always dashed ('--')
            d, d_err, slope, slope_err, intercept, intercept_err, fit_res = calculate_d(lagtimes, data[key], FIT_RANGE)
            if d is not None:
                d_cm2s = d * 1e-5  # Convert nm^2/ns to cm^2/s
                d_cm2s_err = d_err * 1e-5
                
                # Store data including standard errors
                results_summary.append({
                    'type': key.upper(),
                    'rep': r,
                    'd_nm2ns': d,
                    'd_nm2ns_err': d_err,
                    'd_cm2s': d_cm2s,
                    'd_cm2s_err': d_cm2s_err,
                    'slope': slope,
                    'slope_err': slope_err,
                    'intercept': intercept,
                    'intercept_err': intercept_err
                })

                f_key = f'fit_{key}'
                rep_curves.append({
                    'type': 'fit', 'x': fit_res[0], 'y': fit_res[1],
                    'color': DARK_COLORS[i], 
                    'label': f"r0{r} {key.upper()} Fit",
                    'alpha': STYLING[f_key]['alpha'][i],
                    'zorder': STYLING[f_key]['zorder'][i],
                    'linestyle': '--'
                })
        plot_data.append(rep_curves)

    # Save fit equations, coefficients, and uncertainties to a text file
    txt_filename = f"nistmab_diffusion_results_{PREFIX}.txt"
    with open(txt_filename, 'w') as f:
        f.write(f"NISTmAb Diffusion Analysis Results (with Standard Errors) for {PREFIX}\n")
        f.write(f"Fit Range: {FIT_RANGE[0]} to {FIT_RANGE[1]} ns\n")
        f.write("=" * 140 + "\n")
        f.write(f"{'Type':<8}{'Replicate':<12}{'D [cm2/s] (val +/- err)':<32}{'D [nm2/ns] (val +/- err)':<28}{'Equation (MSD = (slope +/- err)*tau + (intercept +/- err))':<60}\n")
        f.write("-" * 140 + "\n")
        for res in results_summary:
            d_cm2s_str = f"{res['d_cm2s']:.4e} +/- {res['d_cm2s_err']:.2e}"
            d_nm2ns_str = f"{res['d_nm2ns']:.4f} +/- {res['d_nm2ns_err']:.4f}"
            eq_str = f"MSD = ({res['slope']:.4f} +/- {res['slope_err']:.4f}) * tau + ({res['intercept']:.4f} +/- {res['intercept_err']:.4f})"
            f.write(f"{res['type']:<8}r0{res['rep']:<9}{d_cm2s_str:<32}{d_nm2ns_str:<28}{eq_str}\n")
        f.write("=" * 140 + "\n")
    print(f"Saved results summary to: {txt_filename}")

    def generate_plot(filename, figsize=(8, 6), show_fits=True, x_lim=None, y_lim=None, box_bounds=None):
        fig, ax = plt.subplots(figsize=figsize)
        
        for curves in plot_data:
            for c in curves:
                if c['type'] == 'fit' and not show_fits: continue
                ax.plot(c['x'], c['y'], linestyle=c['linestyle'], 
                        color=c['color'], label=c['label'], 
                        alpha=c['alpha'], zorder=c['zorder'], lw=2.0)

        # Draw Inset Box indicator if requested
        if box_bounds:
            bx, by = box_bounds # Extract (x_range, y_range)
            rect = Rectangle((bx[0], by[0]), bx[1]-bx[0], by[1]-by[0],
                             linewidth=1.5, edgecolor='gray', facecolor='gray', 
                             alpha=0.2, zorder=2)
            ax.add_patch(rect)

        # Reference Line (1 cm^2/s = 10^5 nm^2/ns)
        max_x = x_lim[1] if x_lim else 1000
        ref_x = np.array([0, max_x])
        ref_y = ref_x * (6 * (EXP_REF_D * 1e5))
        ax.plot(ref_x, ref_y, '-.', color='black', lw=2, 
                label=f'Ref D={EXP_REF_D:.1e}', zorder=1)

        if x_lim: ax.set_xlim(x_lim)
        if y_lim: ax.set_ylim(y_lim)
        ax.set_xlabel(r'$\tau$ [ns]')
        ax.set_ylabel(r'MSD [$nm^2$]')
        ax.legend(loc='center left', bbox_to_anchor=(1.02, 0.5), ncol=2, fontsize=10)
        
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()

    # Define the bounds for the inset plot to reuse for the box
    inset_x, inset_y = (17, 55), (0.4, 2.25)

    # Generate Big Plot with the gray box
    generate_plot(f"nofits_{PREFIX}.png", figsize=(7, 6), show_fits=False, 
                  x_lim=(0,1000), y_lim=(0,32), box_bounds=(inset_x, inset_y))
    
    # Generate Small Plot (Inset)
    generate_plot(f"fits_{PREFIX}.png", figsize=(4, 4), show_fits=True, 
                  x_lim=inset_x, y_lim=inset_y)

if __name__ == "__main__":
    run_analysis()
