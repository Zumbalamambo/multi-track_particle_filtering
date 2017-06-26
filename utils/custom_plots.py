import matplotlib.pyplot as plt
import numpy as np
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
# https://matplotlib.org/examples/color/named_colors.html
colors = {1:'deepskyblue', 2:'lightskyblue', 3:'limegreen', 4:'orangered',
          5:'red', 6:'gold', 7:'snow'}

fc='black'
cm='gray'
theme_col = colors[3]
fig, ax = plt.subplots(1, 1)#, figsize=(7,7))
fig.patch.set_facecolor(fc)


def show_img_return_input(img, name, cm='gray', ask=True):
    plt.ion()
    plt.imshow(img, cmap=cm)
    plt.show()
    ax.spines['bottom'].set_color(theme_col)
    ax.spines['top'].set_color(theme_col)
    ax.spines['right'].set_color(theme_col)
    ax.spines['left'].set_color(theme_col)
    ax.tick_params(axis='x', colors=theme_col)
    ax.tick_params(axis='y', colors=theme_col)
    ax.yaxis.label.set_color(theme_col)
    ax.xaxis.label.set_color(theme_col)
    if type(name)==int:
        ax.set_title('frame '+str(name))
    else:
        ax.set_title(name)
    ax.title.set_color(theme_col)
    plt.tight_layout()
    plt.draw()
    if ask:
        accept = input('OK? ')
    else:
        accept = 'y'
        plt.pause(0.0001)
    plt.cla()
    return(accept)


def write_img(img, name, out_dir, cm='gray'):
    plt.ion()
    #plt.imshow(img, cmap=cm, vmin=vmin, vmax=vmax)
    plt.imshow(img, cmap=cm)
    ax.spines['bottom'].set_color(theme_col)
    ax.spines['top'].set_color(theme_col)
    ax.spines['right'].set_color(theme_col)
    ax.spines['left'].set_color(theme_col)
    ax.tick_params(axis='x', colors=theme_col)
    ax.tick_params(axis='y', colors=theme_col)
    ax.yaxis.label.set_color(theme_col)
    ax.xaxis.label.set_color(theme_col)
    plt.xticks([])
    plt.yticks([])
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    if type(name)==int:
        ax.set_title('frame '+str(name))
    else:
        ax.set_title(name)
    ax.title.set_color(theme_col)
    plt.savefig(out_dir+'/'+name, bbox_inches='tight')
    plt.cla()