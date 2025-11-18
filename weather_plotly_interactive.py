

import pandas as pd
import plotly.graph_objects as go
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# 读取数据
csv_path = r'123.csv'
df = pd.read_csv(csv_path)

# 反转数据顺序，让时间从早到晚（8月到9月）
df = df.iloc[::-1].reset_index(drop=True)


# 彩虹渐变色
rainbow_cmap = LinearSegmentedColormap.from_list('rainbow', ['#2b6cb0','#38b2ac','#68d391','#f6e05e','#f6ad55','#e53e3e','#b83280'])
norm_temp = (df['T'] - df['T'].min()) / (df['T'].max() - df['T'].min())
colors = [f'rgba{tuple(int(255*x) for x in rainbow_cmap(val)[:3]) + (0.85,)}' for val in norm_temp]
# 点大小随温度变化
sizes = 16 + 18 * norm_temp







# 极简自由画布艺术点阵动画
import numpy as np
total_frames = 36  # 更快的动画
canvas_w, canvas_h = 1.0, 1.0
# 时间映射为横坐标，温度归一化后映射为纵坐标，叠加艺术扰动
time_norm = np.linspace(0.08, 0.92, len(df))
temp_norm = (df['T'] - df['T'].min()) / (df['T'].max() - df['T'].min())
temp_y = 0.15 + 0.7 * temp_norm
frames = []
for f in range(1, total_frames+1):
    frac = f / total_frames
    n_points = int(1 + frac * (len(df)-1))
    # 使用原始温度相关的点大小
    frame_sizes = sizes[:n_points]
    # 每一帧点的颜色为真实温度色彩
    frame_colors = colors[:n_points]
    # 艺术扰动：轻微波浪
    wave = 0.06 * np.sin(np.arange(n_points) * 2 * np.pi / max(6, len(df)//3) + frac*2*np.pi)
    frames.append(go.Frame(
        data=[
            go.Scatter(
                x=time_norm[:n_points],
                y=temp_y[:n_points] + wave,
                mode='markers',
                marker=dict(
                    size=frame_sizes,
                    color=frame_colors,
                    opacity=0.92,
                    symbol='circle',
                ),
                hovertemplate='<b>%{customdata[0]}</b><br>温度: %{customdata[1]:.1f}°C',
                customdata=list(zip(df['当地时间 香港(机场)'][:n_points], df['T'][:n_points])),
                showlegend=False
            )
        ],
        name=str(f)
    ))

# 初始帧
init_wave = 0.06 * np.sin(np.arange(1) * 2 * np.pi / max(6, len(df)//3))
fig = go.Figure(
    data=[
        go.Scatter(
            x=[time_norm[0]],
            y=[temp_y[0] + init_wave[0]],
            mode='markers',
            marker=dict(
                size=sizes[0],
                color=colors[0],
                opacity=0.92,
                symbol='circle',
            ),
            hovertemplate='<b>%{customdata[0]}</b><br>温度: %{customdata[1]:.1f}°C',
            customdata=[(df['当地时间 香港(机场)'][0], df['T'][0])],
            showlegend=False
        ),
        # 其余点（不可见），用于初始帧显示全部温度色彩分布
        go.Scatter(
            x=time_norm[1:],
            y=temp_y[1:] + init_wave[0],
            mode='markers',
            marker=dict(
                size=sizes[1:],
                color=colors[1:],
                opacity=0.0,
                symbol='circle',
            ),
            hoverinfo='skip',
            showlegend=False
        )
    ],
    layout=go.Layout(
        font=dict(family='Microsoft YaHei, Arial', size=20, color='#3d2c29'),
        plot_bgcolor='#ffffff',
        paper_bgcolor='#ffffff',
        hoverlabel=dict(bgcolor='#f7b267', font_size=18, font_family='Microsoft YaHei'),
        margin=dict(l=60, r=40, t=60, b=60),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(120,120,120,0.08)',
            gridwidth=1,
            showline=True,
            linecolor='rgba(120,120,120,0.13)',
            linewidth=1,
            zeroline=False,
            showticklabels=True,
            tickfont=dict(size=13, color='rgba(80,80,80,0.45)'),
            tickvals=[time_norm[0], time_norm[len(df)//3], time_norm[2*len(df)//3], time_norm[-1]],
            ticktext=[str(df['当地时间 香港(机场)'].iloc[0]), str(df['当地时间 香港(机场)'].iloc[len(df)//3]), str(df['当地时间 香港(机场)'].iloc[2*len(df)//3]), str(df['当地时间 香港(机场)'].iloc[-1])],
            range=[0, 1],
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(120,120,120,0.08)',
            gridwidth=1,
            showline=True,
            linecolor='rgba(120,120,120,0.13)',
            linewidth=1,
            zeroline=False,
            showticklabels=True,
            tickfont=dict(size=13, color='rgba(80,80,80,0.45)'),
            tickvals=[0.15, 0.4, 0.6, 0.85],
            ticktext=[str(round(df['T'].min(),1)), str(round(df['T'].quantile(0.33),1)), str(round(df['T'].quantile(0.66),1)), str(round(df['T'].max(),1))],
            range=[0, 1],
        ),
        updatemenus=[],
        showlegend=False
    ),
    frames=frames
)

fig.write_html("weather_plot.html", auto_open=True, include_plotlyjs='cdn')
