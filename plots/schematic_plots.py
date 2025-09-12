import numpy as np
import matplotlib.pyplot as plt

# ───────────────────────── GLOBAL FONT + FIGURE SETTINGS ─────────────────────
plt.rcParams["font.family"]        = "Segoe UI Emoji"
plt.rcParams["axes.unicode_minus"] = False

FIG_WIDTH     = 12.5   # overall width in inches
FIG_HEIGHT    = 10     # overall height in inches

# ───────────────────────── FONT SIZES ──────────────────────────────────────
TITLE_FONT       = 18   # font size for panel titles
YLABEL_FONT      = 14   # font size for y-axis label
TICKLABEL_FONT   = 14   # font size for tick labels
LEGEND_FONT      = 16   # font size for legend text

# ─────────────────────────── SPACING CONSTANTS ─────────────────────────────
SEG_WIDTH             = 1.5   # width of each “pre|stress|post” segment
INNER_MARGIN          = 0.25   # margin on left/right of non-German-stress segments
GER_STRESS_MARGIN_L   = 0.10   # left margin for German stress segment (closer to left border)
GER_STRESS_MARGIN_R   = 0.20  # right margin for German stress segment (keep from right border)
LABEL_OFFSET_X        = 0.02   # horizontal gap from line to first emoji
EMOJI_HSPACE          = 0.085  # gap between emojis in the same row
ROW_VSPACE            = 0.25   # vertical gap between stacked rows of emojis
EMOJI_SIZE            = 14     # emoji fontsize
TICK_LEN              = 0.04   # half-length of the little tick marks
LINE_WIDTH            = 0.9    # width of main vertical lines
TICK_LINE_WIDTH       = 0.9    # width of half-ticks
SEPARATOR_WIDTH       = 1.2    # width of dashed separators between segments
SEPARATOR_COLOR       = 'grey'

# ───────────────────────── UPDATED HEIGHT RATIOS ────────────────────────────
# Catalan : German : Legend
HEIGHT_RATIOS = [3, 4, 0.2]
HSPACE        = 0.3   # space between Catalan & German panels

# ─────────────────────────── DATA DICTIONARIES ───────────────────────────────
CATALAN_GROUPS = {
    "pre":    [(1,2,[['⏱️']]), (2,3,[['⏱️']]), (1,3,[['⏱️']])],
    "stress": [(1,2,[['⏱️','⏱️']]), (2,3,[['🎯'],['⏱️','⏱️']]), (1,3,[['🎯'],['⏱️','⏱️']])],
    "post":   [(1,2,[['〽️']]), (2,3,[['〽️']]), (1,3,[['〽️']])],
}
GERMAN_GROUPS = {
    "stress": [
        (0,1,[['⏱️']]),
        (1,2,[['〽️','🎵'],['⏱️']]),
        (2,3,[['〽️','🎵'],['⏱️']]),
        (0,2,[['〽️'],['⏱️']]),
        (1,3,[['〽️','🎵'],['⏱️']]),
        (0,3,[['⏱️']]),
    ],
    "post": [(1,2,[['🎵']]), (1,3,[['🎵']])],
}
LEGEND_ITEMS = [
    ('⏱️:','duration'),
    ('〽️:',r'$f_0$ slope'),
    ('🎵:',r'$f_0$ median'),
    ('🎯:','spectral centroid (CoG)'),
]

# ─────────────────────────── DRAW HELPERS ───────────────────────────────────
def draw_group(ax, seg_key, lines, panel_title):
    """
    Draw vertical lines, half-ticks, and emojis for one segment.
    Uses separate left/right margins for German stress.
    """
    x0, x1, x2, x3 = 0, SEG_WIDTH, 2*SEG_WIDTH, 3*SEG_WIDTH
    seg_map = {'pre':(x0,x1), 'stress':(x1,x2), 'post':(x2,x3)}
    left, right = seg_map[seg_key]
    if panel_title=='German' and seg_key=='stress':
        left += GER_STRESS_MARGIN_L
        right -= GER_STRESS_MARGIN_R
    else:
        left += INNER_MARGIN
        right -= INNER_MARGIN

    # x-positions for each line
    xs = np.linspace(left, right, len(lines)) if len(lines)>1 else [(left+right)/2]
    for (y0,y1,rows), x in zip(lines, xs):
        # main vertical line
        ax.plot([x,x],[y0,y1], color='black', linewidth=LINE_WIDTH, zorder=2)
        # half-ticks
        ax.plot([x-TICK_LEN,x],[y0,y0], color='black', linewidth=TICK_LINE_WIDTH, zorder=2)
        ax.plot([x-TICK_LEN,x],[y1,y1], color='black', linewidth=TICK_LINE_WIDTH, zorder=2)
        # stack emojis
        y_mid = (y0+y1)/2
        off0  = (len(rows)-1)*ROW_VSPACE/2
        for i,row in enumerate(rows):
            y = y_mid + off0 - i*ROW_VSPACE
            for j,emo in enumerate(row):
                ax.text(
                    x + LABEL_OFFSET_X + j*EMOJI_HSPACE,
                    y,
                    emo,
                    fontsize=EMOJI_SIZE,
                    ha='left', va='center', zorder=3
                )


def draw_panel(ax, title, yticks, groups):
    """
    Configure panel axes, draw segments, and dashed separators.
    """
    W = SEG_WIDTH
    ax.set_xlim(0,3*W)
    ax.set_xticks([(i+0.5)*W for i in range(3)])
    ax.set_xticklabels(['pre-stressed','stressed','post-stressed'], fontsize=TICKLABEL_FONT)
    ax.set_ylim(min(yticks)-0.2, max(yticks)+0.2)
    ax.set_yticks(yticks)
    ax.set_ylabel('prominence level', fontsize=YLABEL_FONT, rotation=90)
    ax.set_title(title, fontsize=TITLE_FONT, fontweight='bold', pad=6)
    # dashed separators thicker
    for boundary in (1,2):
        ax.axvline(boundary*W, color=SEPARATOR_COLOR, linestyle='--', linewidth=SEPARATOR_WIDTH, zorder=1)
    ax.yaxis.grid(color='0.90', linestyle=':', linewidth=1)
    for key in ('pre','stress','post'):
        draw_group(ax, key, groups.get(key,[]), title)


# ─────────────────────────────── BUILD FIGURE ───────────────────────────────
fig = plt.figure(figsize=(FIG_WIDTH, FIG_HEIGHT))
gs  = fig.add_gridspec(3, 1, height_ratios=HEIGHT_RATIOS, hspace=HSPACE)

# Catalan panel (row 1)
ax_cat = fig.add_subplot(gs[0])
draw_panel(ax_cat, 'Catalan', [1,2,3], CATALAN_GROUPS)

# German panel (row 2)
ax_ger = fig.add_subplot(gs[1], sharex=ax_cat)
draw_panel(ax_ger, 'German', [0,1,2,3], GERMAN_GROUPS)

# Legend panel (row 3)
ax_leg = fig.add_subplot(gs[2])
ax_leg.axis('off')
legend_str = '    '.join(f'{sym} {lbl}' for sym,lbl in LEGEND_ITEMS)
# legend lower in its own row
ax_leg.text(0.5, 0.3, legend_str, ha='center', va='center', fontsize=LEGEND_FONT)

plt.tight_layout()
plt.show()

# Optional: save to files
fig.savefig('schematic_plots.png', dpi=300, bbox_inches='tight')
fig.savefig('schematic_plots.svg',               bbox_inches='tight')
