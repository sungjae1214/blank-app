import streamlit as st
import xarray as xr
import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import numpy as np
plt.rc('font', family='Malgun Gothic')   # 윈도우
# plt.rc('font', family='AppleGothic')   # 맥
plt.rcParams['axes.unicode_minus'] = False
st.set_page_config(page_title="해수온 상승 대시보드", layout="wide")

st.title("🌊 해수온 상승과 바다의 미래: 변화와 대응 전략")
st.markdown("NOAA OISST (Optimum Interpolation Sea Surface Temperature) 데이터를 활용한 시각화")

# ---------------------------
# 데이터 불러오기
# ---------------------------
@st.cache_data
def load_data():
    url = "https://psl.noaa.gov/thredds/dodsC/Datasets/noaa.oisst.v2/sst.mnmean.nc"
    ds = xr.open_dataset(url)
    return ds

ds = load_data()
sst = ds['sst']

# ---------------------------
# 전 세계 평균 해수온 시계열
# ---------------------------
st.subheader("📈 전 세계 평균 해수온 추이")

global_mean = sst.mean(dim=["lat","lon"])
global_df = global_mean.to_dataframe().reset_index()

fig, ax = plt.subplots(figsize=(8,4))
ax.plot(global_df['time'], global_df['sst'], color="red")
ax.set_title("전 세계 평균 해수온 (°C)")
ax.set_ylabel("온도 (°C)")
ax.set_xlabel("연도")
st.pyplot(fig)

# ---------------------------
# 한반도 주변 해수온 시계열
# ---------------------------
st.subheader("📊 한반도 주변 해수온 추이")

lat_range = st.slider("위도 범위 선택", 30, 50, (33, 40))
lon_range = st.slider("경도 범위 선택", 120, 145, (125, 135))

region = sst.sel(lat=slice(lat_range[0], lat_range[1]),
                 lon=slice(lon_range[0], lon_range[1]))
region_mean = region.mean(dim=["lat","lon"])
region_df = region_mean.to_dataframe().reset_index()

fig, ax = plt.subplots(figsize=(8,4))
ax.plot(region_df['time'], region_df['sst'], color="blue")
ax.set_title("한반도 주변 평균 해수온 (°C)")
ax.set_ylabel("온도 (°C)")
ax.set_xlabel("연도")
st.pyplot(fig)

# ---------------------------
# 지도 시각화 (산호 백화/이상)
# ---------------------------
st.subheader("🗺️ 해수온 지도 시각화")

year = st.slider("연도 선택", 1982, 2023, 2020)
month = st.slider("월 선택", 1, 12, 8)

# 시간 차원 제거
selected = sst.sel(time=f"{year}-{month:02d}").squeeze()

fig = plt.figure(figsize=(10,5))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.set_global()

pcm = ax.pcolormesh(selected['lon'], selected['lat'], selected,
                    cmap="coolwarm", transform=ccrs.PlateCarree(), shading="auto")

ax.add_feature(cfeature.COASTLINE)
ax.set_title(f"{year}-{month:02d} 해수온 (°C)")
plt.colorbar(pcm, ax=ax, orientation="horizontal", pad=0.05, label="°C")

st.pyplot(fig)

