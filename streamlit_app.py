
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import json

# Configure page settings
st.set_page_config(
    page_title="AI Analytics Engine",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f2937 0%, #374151 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #3b82f6;
    }
    .kpi-container {
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        margin: 1rem 0;
    }
    .sidebar .sidebar-content {
        background: #f8fafc;
    }
    .stAlert > div {
        padding: 1rem;
        border-radius: 10px;
    }
    .success-metric {
        border-left-color: #10b981;
    }
    .warning-metric {
        border-left-color: #f59e0b;
    }
    .error-metric {
        border-left-color: #ef4444;
    }
</style>
""", unsafe_allow_html=True)

# Sample data (matching the original application)
@st.cache_data
def load_app_data():
    return {
        "executive_kpis": {
            "total_revenue": 12500000,
            "monthly_growth": 8.5,
            "customer_acquisition_cost": 125,
            "customer_lifetime_value": 2800,
            "churn_rate": 2.1,
            "employee_satisfaction": 87,
            "operational_efficiency": 94.2,
            "cost_savings": 2100000
        },
        "anomaly_detection": [
            {"timestamp": "2024-01-12", "metric_value": 145.17, "is_anomaly": True, "severity": "High"},
            {"timestamp": "2024-01-29", "metric_value": 67.45, "is_anomaly": True, "severity": "Medium"},
            {"timestamp": "2024-08-04", "metric_value": 134.74, "is_anomaly": True, "severity": "Medium"},
            {"timestamp": "2024-10-06", "metric_value": 56.21, "is_anomaly": True, "severity": "High"},
            {"timestamp": "2024-12-30", "metric_value": 168.37, "is_anomaly": True, "severity": "High"}
        ],
        "etl_pipelines": [
            {"name": "Customer Data Pipeline", "status": "Success", "records": 461782, "duration": 107},
            {"name": "Sales Analytics Pipeline", "status": "Failed", "records": 0, "duration": 179},
            {"name": "Marketing Pipeline", "status": "Success", "records": 79369, "duration": 161},
            {"name": "Financial Reporting Pipeline", "status": "Success", "records": 321699, "duration": 25},
            {"name": "Product Analytics Pipeline", "status": "Success", "records": 171616, "duration": 108}
        ]
    }

# Initialize session state for conversations
if 'conversations' not in st.session_state:
    st.session_state.conversations = []
if 'current_query' not in st.session_state:
    st.session_state.current_query = ""

# Load data
app_data = load_app_data()

# Main header
st.markdown("""
<div class="main-header">
    <h1 style="color: white; margin: 0;">🤖 AI Analytics Engine</h1>
    <p style="color: #d1d5db; margin: 0;">Real-time executive insights and conversational reporting</p>
</div>
""", unsafe_allow_html=True)

# Sidebar navigation
st.sidebar.title("Navigation")
selected_section = st.sidebar.selectbox(
    "Select Dashboard Section",
    ["📊 Executive Dashboard", "💬 Conversational Reports", "🔍 Anomaly Detection", "⚙️ ETL Pipelines"]
)

# Executive Dashboard Section
if selected_section == "📊 Executive Dashboard":
    st.header("Executive Dashboard")
    st.subheader("Key Performance Indicators")

    kpis = app_data["executive_kpis"]

    # Create KPI columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Revenue",
            value=f"${kpis['total_revenue']:,}",
            delta=f"+{kpis['monthly_growth']}%"
        )
        st.metric(
            label="Cost Savings",
            value=f"${kpis['cost_savings']:,}",
            delta="2,000+ hours saved"
        )

    with col2:
        st.metric(
            label="Customer LTV",
            value=f"${kpis['customer_lifetime_value']:,}",
            delta=f"CAC: ${kpis['customer_acquisition_cost']}"
        )
        st.metric(
            label="Employee Satisfaction",
            value=f"{kpis['employee_satisfaction']}%",
            delta="+3% from last quarter"
        )

    with col3:
        st.metric(
            label="Operational Efficiency",
            value=f"{kpis['operational_efficiency']}%",
            delta="+5.2% from automation"
        )
        st.metric(
            label="Churn Rate",
            value=f"{kpis['churn_rate']}%",
            delta="-0.8% improvement"
        )

    with col4:
        st.metric(
            label="AI Model Accuracy",
            value="92%",
            delta="Anomaly Detection"
        )
        st.metric(
            label="Pipeline Uptime",
            value="99.7%",
            delta="AWS Infrastructure"
        )

    # Revenue trend chart
    st.subheader("Revenue Trends")

    # Generate sample revenue data
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
    revenue_trend = [kpis['total_revenue'] * (1 + np.random.normal(0, 0.05)) for _ in dates]

    fig_revenue = go.Figure()
    fig_revenue.add_trace(go.Scatter(
        x=dates, 
        y=revenue_trend,
        mode='lines+markers',
        name='Monthly Revenue',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=8)
    ))
    fig_revenue.update_layout(
        title="Monthly Revenue Performance",
        xaxis_title="Month",
        yaxis_title="Revenue ($)",
        height=400,
        showlegend=False
    )
    st.plotly_chart(fig_revenue, use_container_width=True)

# Conversational Reports Section
elif selected_section == "💬 Conversational Reports":
    st.header("Conversational Reports")
    st.subheader("Ask questions about your data in natural language")

    # Chat interface
    col1, col2 = st.columns([3, 1])

    with col1:
        query_input = st.text_input(
            "Enter your question:",
            placeholder="e.g., What's our churn rate? Show revenue trends...",
            key="query_input"
        )

    with col2:
        if st.button("Ask AI", type="primary"):
            if query_input:
                # Simulate AI response
                response_time = np.random.uniform(0.5, 2.0)

                # Add to conversation history
                conversation = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "query": query_input,
                    "response_time": response_time,
                    "satisfaction": np.random.choice([4, 5])
                }
                st.session_state.conversations.append(conversation)

                # Show response
                with st.spinner(f"Analyzing... ({response_time:.1f}s)"):
                    time.sleep(min(response_time, 2))

                if "churn" in query_input.lower():
                    st.success(f"📊 Current churn rate is {app_data['executive_kpis']['churn_rate']}%, which is 0.8% better than last quarter. The main contributing factors are improved customer support and product updates.")
                elif "revenue" in query_input.lower():
                    st.success(f"💰 Total revenue is ${app_data['executive_kpis']['total_revenue']:,} with {app_data['executive_kpis']['monthly_growth']}% monthly growth. Revenue has shown consistent upward trends across all quarters.")
                elif "cost" in query_input.lower():
                    st.success(f"💡 Our AI-driven automation has saved ${app_data['executive_kpis']['cost_savings']:,} annually by eliminating 2,000+ manual hours through ETL pipeline automation.")
                else:
                    st.success("🤖 I've analyzed your query. Based on the current data, all key metrics are performing within expected ranges. Would you like me to dive deeper into any specific area?")

    # Conversation history
    if st.session_state.conversations:
        st.subheader("Recent Conversations")

        for i, conv in enumerate(reversed(st.session_state.conversations[-10:])):  # Show last 10
            with st.expander(f"Query: {conv['query'][:50]}... - {conv['timestamp']}"):
                st.write(f"**Query:** {conv['query']}")
                st.write(f"**Response Time:** {conv['response_time']:.1f}s")
                st.write(f"**Satisfaction:** {'⭐' * conv['satisfaction']}")

    # Analytics summary
    st.subheader("Conversation Analytics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Queries", len(st.session_state.conversations))
    with col2:
        avg_response = np.mean([c['response_time'] for c in st.session_state.conversations]) if st.session_state.conversations else 0
        st.metric("Avg Response Time", f"{avg_response:.1f}s")
    with col3:
        avg_satisfaction = np.mean([c['satisfaction'] for c in st.session_state.conversations]) if st.session_state.conversations else 0
        st.metric("Avg Satisfaction", f"{avg_satisfaction:.1f}/5")

# Anomaly Detection Section
elif selected_section == "🔍 Anomaly Detection":
    st.header("Real-Time Anomaly Detection")

    # Key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Model Accuracy", "92%", "SageMaker ML Model")
    with col2:
        anomalies_detected = len(app_data["anomaly_detection"])
        st.metric("Anomalies Detected", anomalies_detected, "Last 30 days")
    with col3:
        st.metric("Detection Latency", "< 100ms", "Real-time processing")

    # Anomaly alerts
    st.subheader("Recent Anomaly Alerts")

    for anomaly in app_data["anomaly_detection"][-3:]:  # Show last 3
        severity_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}
        alert_type = "error" if anomaly["severity"] == "High" else "warning"

        st.alert(
            f"{severity_color[anomaly['severity']]} **{anomaly['severity']} Severity Anomaly** - Database Response Time: {anomaly['metric_value']:.1f}ms on {anomaly['timestamp']}",
            icon="⚠️" if alert_type == "warning" else "🚨"
        )

    # Anomaly visualization
    st.subheader("Anomaly Detection Over Time")

    # Generate sample time series data with anomalies
    dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='D')
    normal_data = 100 + 20 * np.sin(2 * np.pi * np.arange(len(dates)) / 365.25) + np.random.normal(0, 5, len(dates))

    # Create anomaly points
    anomaly_dates = [datetime.strptime(a["timestamp"], "%Y-%m-%d") for a in app_data["anomaly_detection"]]
    anomaly_values = [a["metric_value"] for a in app_data["anomaly_detection"]]

    fig_anomaly = go.Figure()

    # Normal data line
    fig_anomaly.add_trace(go.Scatter(
        x=dates,
        y=normal_data,
        mode='lines',
        name='Normal Range',
        line=dict(color='#10b981', width=2),
        opacity=0.7
    ))

    # Anomaly points
    fig_anomaly.add_trace(go.Scatter(
        x=anomaly_dates,
        y=anomaly_values,
        mode='markers',
        name='Anomalies',
        marker=dict(
            color='red',
            size=12,
            symbol='x',
            line=dict(width=2, color='darkred')
        )
    ))

    fig_anomaly.update_layout(
        title="Database Response Time - Anomaly Detection",
        xaxis_title="Date",
        yaxis_title="Response Time (ms)",
        height=500,
        hovermode='x unified'
    )

    st.plotly_chart(fig_anomaly, use_container_width=True)

# ETL Pipelines Section
elif selected_section == "⚙️ ETL Pipelines":
    st.header("ETL Pipeline Management")
    st.subheader("AWS-powered Data Processing Automation")

    # Pipeline overview metrics
    pipelines = app_data["etl_pipelines"]
    successful_pipelines = len([p for p in pipelines if p["status"] == "Success"])
    total_records = sum([p["records"] for p in pipelines if p["status"] == "Success"])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Pipeline Success Rate", f"{(successful_pipelines/len(pipelines)*100):.0f}%")
    with col2:
        st.metric("Records Processed", f"{total_records:,}")
    with col3:
        st.metric("AWS Services", "3", "Glue, Step Functions, SageMaker")
    with col4:
        st.metric("Cost Optimization", "2,000+", "Hours saved annually")

    # Pipeline status table
    st.subheader("Current Pipeline Status")

    pipeline_df = pd.DataFrame(pipelines)

    # Add status indicators
    def status_indicator(status):
        if status == "Success":
            return "✅ Success"
        elif status == "Failed":
            return "❌ Failed"
        else:
            return "⏳ Running"

    pipeline_df["Status"] = pipeline_df["status"].apply(status_indicator)
    pipeline_df["Records Processed"] = pipeline_df["records"].apply(lambda x: f"{x:,}")
    pipeline_df["Duration (min)"] = pipeline_df["duration"]

    st.dataframe(
        pipeline_df[["name", "Status", "Records Processed", "Duration (min)"]].rename(columns={"name": "Pipeline Name"}),
        use_container_width=True,
        hide_index=True
    )

    # Pipeline performance visualization
    st.subheader("Pipeline Performance Analytics")

    fig_pipeline = go.Figure()

    # Records processed bar chart
    fig_pipeline.add_trace(go.Bar(
        x=[p["name"] for p in pipelines],
        y=[p["records"] for p in pipelines],
        name="Records Processed",
        marker_color=['#10b981' if p["status"] == "Success" else '#ef4444' for p in pipelines]
    ))

    fig_pipeline.update_layout(
        title="ETL Pipeline Performance - Records Processed",
        xaxis_title="Pipeline",
        yaxis_title="Records Processed",
        height=400,
        showlegend=False
    )
    fig_pipeline.update_xaxes(tickangle=45)

    st.plotly_chart(fig_pipeline, use_container_width=True)

    # AWS Architecture info
    st.subheader("AWS Architecture Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.info("""
        **🔧 AWS Glue ETL Jobs**
        - Multi-stage data processing
        - Automated schema detection
        - Serverless scaling
        - Cost-optimized execution
        """)

    with col2:
        st.info("""
        **📊 AWS Step Functions**
        - Workflow orchestration  
        - Error handling & retry logic
        - Pipeline monitoring
        - State machine automation
        """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 1rem;">
    <p>🤖 AI Analytics Engine - Powered by AWS SageMaker, Glue & Step Functions</p>
    <p>Built with Streamlit • Real-time Insights • Conversational AI • 92% Anomaly Detection Accuracy</p>
</div>
""", unsafe_allow_html=True)
