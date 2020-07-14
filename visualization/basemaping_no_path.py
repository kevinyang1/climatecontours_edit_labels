import matplotlib as mpl
import glob
#mpl.use('Agg')
import os
#os.environ['PROJ_LIB'] = "/global/homes/a/amahesh/.conda/envs/plotting_env/share/proj"
import matplotlib.pyplot as plt

import mpl_toolkits as tk
import numpy as np
import netCDF4 as nc
import h5py as h5
from matplotlib.colors import ListedColormap
import pandas as pd
from mpl_toolkits.basemap import Basemap
import metpy.calc
from metpy.units import units
import stat

dpi = 96

""" This is Sean's plotting function """
def plot_mask_double(namedir, img_array, img_array2, storm_mask, plt_title, 
    my_cmap=None,my_cmap2=None, my_cmap3=None, u_wind=None, v_wind=None, 
    v_max=None, v_min=None,v_max2=None, v_min2=None, line=None, land=True):
    """
    img_array: This is the contour that is being plotted (i.e. TMQ)
    storm_mask: This creates a mask on top of the img_array contour showing the storm labels.  If you do not wish
            to see a predefined mask, you can input np.zeros(img_array.shape) for this field
    plt_title: The title of the plot
    my_cmap: input a custom colormap for the img_array contour.  The default colormap is good though
    u_wind: wind values in the u direction
    v_wind: wind values in the v direction
    """
    # Set alpha
    if my_cmap is None:
        # Choose colormap
        cmap = mpl.cm.viridis
        # Get the colormap colors
        my_cmap = cmap(np.arange(cmap.N))
        alpha = np.linspace(0, 1, cmap.N)
        my_cmap[:,0] = (1-alpha) + alpha * my_cmap[:,0]
        my_cmap[:,1] = (1-alpha) + alpha * my_cmap[:,1]
        my_cmap[:,2] = (1-alpha) + alpha * my_cmap[:,2]

        # Create new colormap
        my_cmap = ListedColormap(my_cmap)

    # l = p['label'] / 100
    p = storm_mask #p['prediction']
    p = np.roll(p,[0,1152//2])
    p1 = (p == 100)
    p2 = (p == 2)

    d = img_array #h['climate']['data'][0,...]
    d = np.roll(d,[0,1152//2])
    
    d2 = img_array2
    d2 = np.roll(d2,[0,1152//2])

    lats = np.linspace(-90,90,768)
    longs = np.linspace(-180,180,1152)

    def do_fig(figsize):
        fig = plt.figure(figsize=figsize, dpi=dpi)
        ax=fig.add_axes([0,0,1,1])
        ax.axis('off')

        my_map = Basemap(projection='cyl', llcrnrlat=min(lats), lon_0=np.median(longs),
                  llcrnrlon=min(longs), urcrnrlat=max(lats), urcrnrlon=max(longs), resolution = 'c',fix_aspect=False)
        xx, yy = np.meshgrid(longs, lats)
        x_map,y_map = my_map(xx,yy)
        my_map.drawcoastlines(color=[0.5,0.5,0.5])

        my_map.contour(x_map,y_map,d,line,cmap=my_cmap, vmax=v_max, vmin=v_min)
        my_map.contourf(x_map,y_map,d2,64,cmap=my_cmap2, vmax=v_max2, vmin=v_min2)
        if u_wind is not None and v_wind is not None:
            wind_speed = np.sqrt(u_wind**2 + v_wind**2)
            my_map.quiver(x_map[::20,::20],y_map[::20,::20], u_wind[::20,::20], v_wind[::20,::20], wind_speed[::20,::20], alpha=0.5, cmap=my_cmap3)

        if (not land):
            my_map.fillcontinents(alpha=0.5)
        mask_ex = plt.gcf()
        path = namedir + "/" + plt_title
        mask_ex.savefig(path, dpi=dpi, quality=100,pad_inches = 0)
        os.chmod(path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH)
        plt.clf()
        plt.close(fig)

    do_fig((1152/dpi,768/dpi))


""" This is Sean's plotting function """
def plot_mask_flat(namedir ,img_array, storm_mask, plt_title, my_cmap=None, 
    my_cmap2 = None, u_wind=None, v_wind=None, 
    v_max=None, v_min=None, land=True):
    """
    img_array: This is the contour that is being plotted (i.e. TMQ)
    storm_mask: This creates a mask on top of the img_array contour showing the storm labels.  If you do not wish
            to see a predefined mask, you can input np.zeros(img_array.shape) for this field
    plt_title: The title of the plot
    my_cmap: input a custom colormap for the img_array contour.  The default colormap is good though
    u_wind: wind values in the u direction
    v_wind: wind values in the v direction
    """
    # Set alpha
    if my_cmap is None:
        # Choose colormap
        cmap = mpl.cm.viridis
        # Get the colormap colors
        my_cmap = cmap(np.arange(cmap.N))
        alpha = np.linspace(0, 1, cmap.N)
        my_cmap[:,0] = (1-alpha) + alpha * my_cmap[:,0]
        my_cmap[:,1] = (1-alpha) + alpha * my_cmap[:,1]
        my_cmap[:,2] = (1-alpha) + alpha * my_cmap[:,2]

        # Create new colormap
        my_cmap = ListedColormap(my_cmap)

    # l = p['label'] / 100
    p = storm_mask #p['prediction']
    p = np.roll(p,[0,1152//2])
    p1 = (p == 100)
    p2 = (p == 2)

    d = img_array #h['climate']['data'][0,...]
    d = np.roll(d,[0,1152//2])

    lats = np.linspace(-90,90,768)
    longs = np.linspace(-180,180,1152)

    def do_fig(figsize):
        fig = plt.figure(figsize=figsize,dpi=dpi)
        ax=fig.add_axes([0,0,1,1])
        ax.axis('off')

        my_map = Basemap(projection='cyl', llcrnrlat=min(lats), lon_0=np.median(longs),
                  llcrnrlon=min(longs), urcrnrlat=max(lats), urcrnrlon=max(longs), resolution = 'c',fix_aspect=False)
        xx, yy = np.meshgrid(longs, lats)
        x_map,y_map = my_map(xx,yy)
        my_map.drawcoastlines(color=[0.5,0.5,0.5])

        my_map.contourf(x_map,y_map,d,64,cmap=my_cmap, vmax=v_max, vmin=v_min)

        if u_wind is not None and v_wind is not None:
            wind_speed = np.sqrt(u_wind**2 + v_wind**2)
            my_map.quiver(x_map[::20,::20],y_map[::20,::20], u_wind[::20,::20], v_wind[::20,::20], wind_speed[::20,::20], alpha=0.5, cmap=my_cmap2)
        
        if (not land):
            my_map.fillcontinents(alpha=0.5)
        mask_ex = plt.gcf()
        path = namedir + "/" + plt_title
        mask_ex.savefig(path ,dpi=dpi,quality=100,pad_inches = 0)
        os.chmod(path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH)
        plt.clf()
        plt.close(fig)

    do_fig((1152/dpi,768/dpi))


def plot_mask_triple(namedir, img_array, img_array2, img_array3, storm_mask, plt_title, 
                     my_cmap=None,my_cmap2=None, my_cmap3=None, my_cmap4=None,
                     u_wind=None, v_wind=None, v_max=None, v_min=None,thresh=False,
                     v_max2=None, v_min2=None, v_max3=None, v_min3=None, line=None, line2=None,
                    land = True):
    """
    img_array: This is the contour that is being plotted (i.e. TMQ)
    storm_mask: This creates a mask on top of the img_array contour showing the storm labels.  If you do not wish
            to see a predefined mask, you can input np.zeros(img_array.shape) for this field
    plt_title: The title of the plot
    my_cmap: input a custom colormap for the img_array contour.  The default colormap is good though
    u_wind: wind values in the u direction
    v_wind: wind values in the v direction
    """
    # Set alpha
    if my_cmap2 is None:
        # Choose colormap
        cmap2 = mpl.cm.viridis
        # Get the colormap colors
        my_cmap2 = cmap2(np.arange(cmap2.N))
        alpha2 = np.linspace(0, 1, cmap2.N)
        my_cmap2[:,0] = (1-alpha2) + alpha2 * my_cmap2[:,0]
        my_cmap2[:,1] = (1-alpha2) + alpha2 * my_cmap2[:,1]
        my_cmap2[:,2] = (1-alpha2) + alpha2 * my_cmap2[:,2]

        # Create new colormap
        my_cmap2 = ListedColormap(my_cmap2)

    if my_cmap is None:
        # Choose colormap
        cmap = mpl.cm.viridis
        # Get the colormap colors
        my_cmap = cmap(np.arange(cmap.N))
        alpha = np.linspace(0, 1, cmap.N)
        my_cmap[:,0] = (1-alpha) + alpha * my_cmap[:,0]
        my_cmap[:,1] = (1-alpha) + alpha * my_cmap[:,1]
        my_cmap[:,2] = (1-alpha) + alpha * my_cmap[:,2]

        # Create new colormap
        my_cmap = ListedColormap(my_cmap)

    # l = p['label'] / 100
    p = storm_mask #p['prediction']
    p = np.roll(p,[0,1152//2])
    p1 = (p == 100)
    p2 = (p == 2)

    d = img_array #h['climate']['data'][0,...]
    d = np.roll(d,[0,1152//2])
    
    d2 = img_array2
    d2 = np.roll(d2,[0,1152//2])
    
    d3 = img_array3
    d3 = np.roll(d3,[0,1152//2])

    lats = np.linspace(-90,90,768)
    longs = np.linspace(-180,180,1152)

    def do_fig(figsize):
        fig = plt.figure(figsize=figsize,dpi=dpi)
        ax=fig.add_axes([0,0,1,1])
        ax.axis('off')

        my_map = Basemap(projection='cyl', llcrnrlat=min(lats), lon_0=np.median(longs),
                  llcrnrlon=min(longs), urcrnrlat=max(lats), urcrnrlon=max(longs), resolution = 'c',fix_aspect=False)
        xx, yy = np.meshgrid(longs, lats)
        x_map,y_map = my_map(xx,yy)
        my_map.drawcoastlines(color=[0.5,0.5,0.5])

        my_map.contour(x_map,y_map,d,line,cmap=my_cmap, vmax=v_max, vmin=v_min)
        my_map.contour(x_map,y_map,d3,line2,cmap=my_cmap4, vmax=v_max3, vmin=v_min3)
        my_map.contourf(x_map,y_map,d2,64,cmap=my_cmap2, vmax=v_max2, vmin=v_min2)
        if u_wind is not None and v_wind is not None:
            wind_speed = np.sqrt(u_wind**2 + v_wind**2)
            my_map.quiver(x_map[::20,::20],y_map[::20,::20], u_wind[::20,::20], v_wind[::20,::20], wind_speed[::20,::20], alpha=0.5, cmap=my_cmap3)

        if (not land):
            my_map.fillcontinents(alpha=0.5)
        mask_ex = plt.gcf()
        path = namedir + "/" + plt_title
        mask_ex.savefig(path ,dpi=dpi,quality=100,pad_inches = 0)
        os.chmod(path, stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH)
        plt.clf()
        plt.close(fig)

    do_fig((1152/dpi,768/dpi))

""" Select files from folder to convert """
#sourceDir_path = '/global/cfs/projectdirs/ClimateNet/qa_pipeline/colby_scripts/netcdf_to_xml/pull_from_werner/2000'
#source_files = []

#testImg_names = []

#testImg_path = '/global/project/projectdirs/ClimateNet/Images_test/ivt/*.jpg'
#testImg_files = glob.glob(testImg_path)
# "/global/project/projectdirs/ClimateNet/Images_test/labels_0/data-2002-12-31-01-1.jpg"
#for file in testImg_files:
#    temp = file[-24:-3] + 'h5'
#    source_files += [sourceDir_path + temp]
    # "/global/cscratch1/sd/amahesh/gb_data/All-Hist/data-2002-12-31-01-1.h5"
    #testImg_names += [file[-24:]]
    # "data-2002-12-31-01-1.jpg"

#other50_path = sourceDir_path + '*-01-1.h5'
#source_files_iter = glob.iglob(other50_path)

#source_files = set(source_files)

def start_composit_img(source_file_dir, print_dir):
    #count = 0
    psl_path = "/global/project/projectdirs/dasrepo/gmd/input/ALLHIST/run1/CAM5-1-0.25degree_All-Hist_est1_v3_run1.cam.h2."
    
    for filename in os.listdir(source_file_dir):
        
        #if count >= 150: return
        psl_date = filename[-19:]
        
        #month = int(sfile[-13:-11])
        #if sfile in source_files or month < 6 or month > 10: continue
        #count += 1
        #print(count)
        #filepath = sfile[:]
        #print(filepath)
        data_in = nc.Dataset(source_file_dir+"/"+filename)
        #print(data_in)
        psl_data = nc.Dataset(psl_path+psl_date)
        #print(psl_data)
        
        for hour in np.arange(8):
            name = "data-" + filename[-19:-8] + "0" + str(hour+1)+'-1.jpg'
            
            
            #TMQ = data_in['climate']['data'][:,:,0]
            TMQ = psl_data.variables['TMQ'][hour]
            # PS = data_in['climate']['data'][:,:,6]
            PS = psl_data.variables['PS'][hour]
            #PSL = data_in['climate']['data'][:,:,7]
            PSL = psl_data.variables['PSL'][hour]
            #U850 = data_in['climate']['data'][:,:,1]
            U850 = psl_data.variables['U850'][hour]
            #V850 = data_in['climate']['data'][:,:,2]
            V850 = psl_data.variables['V850'][hour]
            #UBOT = data_in['climate']['data'][:,:,3]
            UBOT = psl_data.variables['UBOT'][hour]
            #VBOT = data_in['climate']['data'][:,:,4]
            VBOT = psl_data.variables['VBOT'][hour]
            #QREFHT = data_in['climate']['data'][:,:,5]
            QREFHT = psl_data.variables['QREFHT'][hour]
            #print(TMQ.shape)

            """ Plot TMQ from the data file"""

            
            #if name not in os.listdir(print_dir+"/tmq"):
            plot_mask_flat(print_dir+"/tmq", TMQ, np.zeros(TMQ.shape), name, 
                               'viridis', land=False)
            


            # Plot TMQ, U850, and V850 from the data file
           # plot_mask_flat(print_dir+"/tmq_wind_850", TMQ, np.zeros(TMQ.shape), 
                           #name, 'viridis',my_cmap2='Blues', u_wind=U850, v_wind=V850, land=False)


            # Plot TMQ, UBOT, and VBOT from the data file
           # plot_mask_flat(print_dir+"/tmq_wind_bot", TMQ, np.zeros(TMQ.shape), 
                           #name, 'viridis',my_cmap2='Blues', u_wind=UBOT, v_wind=VBOT, land=False)
            
            """PSL"""
            #if name not in os.listdir(print_dir+"/psl"):
            plot_mask_flat(print_dir+"/psl", PSL, np.zeros(PSL.shape), name, 
                       'viridis', v_max=102000,v_min=99500, land=False)
            


            #  Calculate and plot the IVT approximation
            # USE IVT FOR WERNER
            #IVT_u = U850 * QREFHT
            #IVT_v = V850 * QREFHT
            #IVT = np.sqrt(IVT_u**2 + IVT_v**2)
            #plot_mask_flat(print_dir+"ivt", IVT, np.zeros(TMQ.shape), name, 'viridis',v_max=0.42,v_min=0)
            """ PLOT IVT FROM WERNER"""
            IVT = data_in.variables["IVT"][hour]
            #print(np.percentile(IVT, [1, 99]))
            #if name not in os.listdir(print_dir+"/ivt"):
            plot_mask_flat(print_dir+"/ivt", IVT, np.zeros(TMQ.shape), name, 'viridis',v_max=1200)
             #v_max=0.42


            """ Plot Vorticity calculated by U850, and V850 from the data file"""
            # vorticity = abs(np.gradient(V850, axis=1) - np.gradient(U850, axis=0))
            
            #if name not in os.listdir(print_dir+"/vorticity"):
            new_vor = metpy.calc.vorticity(U850 * units.meter / units.second,
                                           V850 * units.meter / units.second,
                                           np.full((768, 1151), 1) * units.meter,
                                           np.full((767, 1152), 1) * units.meter)
            new_vor_arr = np.array(abs(new_vor))
            
            plot_mask_flat(print_dir+"/vorticity", new_vor_arr, np.zeros(new_vor_arr.shape), 
                          name, 'viridis',v_max=7,v_min=1.3, land=False)
            


            """ Plot PSL, Vorticity from the data file"""
            #if name not in os.listdir(print_dir+"/vor_psl"):
            
            plot_mask_double(print_dir+"/vor_psl", new_vor_arr, PSL, np.zeros(new_vor_arr.shape), name, my_cmap='Reds',my_cmap2='viridis',v_max2=102000,v_min2=99500,line=8,v_max=7,v_min=1.3, land=False)
            

        #break
            
            #plot_mask_triple(print_dir+"/vor_psl_ivt", new_vor_arr, IVT, PSL, np.zeros(PSL.shape), name, my_cmap='Reds',my_cmap2='viridis',my_cmap4='cool',line=10,line2=10,
                        #v_max=7,v_min=1.3,
                        #v_max2=0.42,v_min2=0.00,
                        #v_max3=101500,v_min3=99000)
            
        #test for 8 hours in first day


        # plot_mask_double("./global/project/projectdirs/ClimateNet/Images_test/vor_ps_wind", PS, vorticity, np.zeros(vorticity.shape), name, 
        #                my_cmap='Wistia',v_max=129000,v_min=55000,my_cmap2='viridis',my_cmap3 = 'PiYG',line=3,v_max2=7,v_min2=1.3, u_wind=U850, v_wind=V850)

print_dir = '/global/cfs/projectdirs/ClimateNet/qa_pipeline/colby_scripts/netcdf_to_xml/jpg_out/container_d'

source_file_dir = '/global/cfs/projectdirs/ClimateNet/qa_pipeline/colby_scripts/netcdf_to_xml/pull_from_werner/2003'


start_composit_img(source_file_dir, print_dir)
