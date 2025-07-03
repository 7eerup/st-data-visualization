import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime

# 앱 제목
st.title("📊 고객 행동 데이터 시각화 대시보드")

# 파일 업로드
uploaded_file = st.file_uploader("CSV 파일 업로드", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=["timestamp"])

    # 기본 전처리
    df['hour'] = df['timestamp'].dt.hour
    df['weekday'] = df['timestamp'].dt.day_name()

    # 필터
    region = st.sidebar.multiselect("지역 선택", options=df["region"].unique(), default=df["region"].unique())
    device = st.sidebar.multiselect("디바이스 선택", options=df["device"].unique(), default=df["device"].unique())

    filtered_df = df[(df["region"].isin(region)) & (df["device"].isin(device))]

    # 유입 채널 분석
    st.subheader("1. 유입 채널 분포")
    channel_counts = filtered_df["channel"].value_counts()
    fig1 = px.pie(names=channel_counts.index, values=channel_counts.values, title="유입 채널 비율")
    st.plotly_chart(fig1)

    # 시간대 분석
    st.subheader("2. 시간대별 방문자 수")
    hour_counts = filtered_df.groupby("hour")["user_id"].count()
    fig2 = plt.figure()
    sns.lineplot(x=hour_counts.index, y=hour_counts.values)
    plt.xlabel("시간대")
    plt.ylabel("방문자 수")
    plt.grid(True)
    st.pyplot(fig2)

    # 제품 클릭 분석
    st.subheader("3. 제품 클릭 Top 10")
    top_products = filtered_df["product_clicked"].value_counts().nlargest(10)
    fig3 = px.bar(x=top_products.index, y=top_products.values, labels={'x':'제품명', 'y':'클릭수'})
    st.plotly_chart(fig3)

    # 전환율 (conversion rate)
    st.subheader("4. 전환율 분석")
    conversion_rate = filtered_df["converted"].value_counts(normalize=True).get("Yes", 0) * 100
    st.metric(label="전환율", value=f"{conversion_rate:.2f} %")

    # 요일별 방문 heatmap
    st.subheader("5. 요일 & 시간별 방문자 수 (Heatmap)")
    heatmap_df = filtered_df.groupby(["weekday", "hour"])["user_id"].count().unstack(fill_value=0)
    fig4 = plt.figure(figsize=(10, 5))
    sns.heatmap(heatmap_df, cmap="YlGnBu")
    plt.title("요일 & 시간별 방문자 수")
    st.pyplot(fig4)

    # 리포트 다운로드
    st.subheader("📥 데이터 다운로드")
    csv = filtered_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button("📤 필터링된 데이터 다운로드", data=csv, file_name="filtered_data.csv", mime="text/csv")
