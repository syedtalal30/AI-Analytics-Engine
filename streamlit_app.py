import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import json
import requests
import yfinance as yf

# Configure page settings
st.set_page_config(
    page_title="AI Analytics Engine - Dynamic Company Data",
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
    .company-selector {
        background: linear-gradient(90deg, #3b82f6 0%, #1d4ed8 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #3b82f6;
    }
    .success-metric { border-left-color: #10b981; }
    .warning-metric { border-left-color: #f59e0b; }
    .error-metric { border-left-color: #ef4444; }
    .company-info {
        background: #f8fafc;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Popular companies for quick selection
POPULAR_COMPANIES = {
    "Apple Inc.": "AAPL",
    "Microsoft Corporation": "MSFT", 
    "Amazon.com Inc.": "AMZN",
    "Alphabet Inc. (Google)": "GOOGL",
    "Tesla Inc.": "TSLA",
    "NVIDIA Corporation": "NVDA",
    "Meta Platforms Inc.": "META",
    "Netflix Inc.": "NFLX",
    "Adobe Inc.": "ADBE",
    "Salesforce Inc.": "CRM",
    "Intel Corporation": "INTC",
    "Cisco Systems Inc.": "CSCO",
    "Oracle Corporation": "ORCL",
    "IBM": "IBM",
    "Disney": "DIS"
}

@st.cache_data(ttl=300)  # Cache for 5 minutes
def get_company_data(symbol):
    """Fetch real company data using Yahoo Finance"""
    try:
        # Get company info
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        # Get historical data for charts
        hist = ticker.history(period="1y")
        
        # Calculate key metrics
        current_price = info.get('currentPrice', 0)
        market_cap = info.get('marketCap', 0)
        revenue = info.get('totalRevenue', 0)
        
        # Calculate growth metrics
        if len(hist) > 30:
            monthly_change = ((hist['Close'][-1] - hist['Close'][-30]) / hist['Close'][-30]) * 100
        else:
            monthly_change = 0
            
        # Simulate additional metrics for professional demo
        operational_efficiency = min(95, max(75, 85 + np.random.normal(0, 5)))
        employee_satisfaction = min(95, max(70, 80 + np.random.normal(0, 8)))
        
        return {
            "company_info": {
                "name": info.get('longName', 'Unknown Company'),
                "symbol": symbol,
                "sector": info.get('sector', 'Unknown'),
                "industry": info.get('industry', 'Unknown'),
                "description": info.get('longBusinessSummary', 'No description available')[:300] + "...",
                "employees": info.get('fullTimeEmployees', 0),
                "website": info.get('website', ''),
                "country": info.get('country', 'Unknown')
            },
            "financial_metrics": {
                "current_price": current_price,
                "market_cap": market_cap,
                "total_revenue": revenue,
                "monthly_growth": monthly_change,
                "operational_efficiency": operational_efficiency,
                "employee_satisfaction": employee_satisfaction,
                "pe_ratio": info.get('trailingPE', 0),
                "profit_margin": info.get('profitMargins', 0) * 100 if info.get('profitMargins') else 0,
                "revenue_growth": info.get('revenueGrowth', 0) * 100 if info.get('revenueGrowth') else 0
            },
            "stock_data": hist,
            "raw_info": info
        }
    except Exception as e:
        st.error(f"Error fetching data for {symbol}: {str(e)}")
        return None

def generate_company_insights(company_data):
    """Generate AI-like insights about the company"""
    if not company_data:
        return []
        
    insights = []
    metrics = company_data["financial_metrics"]
    info = company_data["company_info"]
    
    # Market cap insights
    if metrics["market_cap"] > 1e12:
        insights.append(f"💎 {info['name']} is a mega-cap company with market capitalization over $1 trillion")
    elif metrics["market_cap"] > 1e11:
        insights.append(f"🏢 {info['name']} is a large-cap company with strong market presence")
    
    # Growth insights
    if metrics["monthly_growth"] > 10:
        insights.append(f"📈 Strong monthly performance with {metrics['monthly_growth']:.1f}% growth")
    elif metrics["monthly_growth"] < -10:
        insights.append(f"📉 Recent challenges with {abs(metrics['monthly_growth']):.1f}% decline this month")
    
    # Valuation insights
    if metrics["pe_ratio"] > 0:
        if metrics["pe_ratio"] > 25:
            insights.append(f"⚡ High growth expectations with P/E ratio of {metrics['pe_ratio']:.1f}")
        elif metrics["pe_ratio"] < 15:
            insights.append(f"💰 Potentially undervalued with P/E ratio of {metrics['pe_ratio']:.1f}")
    
    # Sector insights
    sector_performance = {
        "Technology": "🚀 Operating in the high-growth technology sector",
        "Healthcare": "🏥 Part of the defensive healthcare sector",
        "Financial Services": "🏦 Operating in the cyclical financial services sector",
        "Consumer Cyclical": "🛍️ Exposed to consumer spending trends",
        "Energy": "⚡ Part of the volatile energy sector"
    }
    
    if info["sector"] in sector_performance:
        insights.append(sector_performance[info["sector"]])
    
    return insights[:4]  # Return top 4 insights

# Initialize session state
if 'selected_company' not in st.session_state:
    st.session_state.selected_company = "AAPL"
if 'company_data' not in st.session_state:
    st.session_state.company_data = None
if 'conversations' not in st.session_state:
    st.session_state.conversations = []

# Main header
st.markdown("""
<div class="main-header">
    <h1 style="color: white; margin: 0;">🤖 AI Analytics Engine</h1>
    <p style="color: #d1d5db; margin: 0;">Dynamic Company Analytics with Real-Time Data</p>
</div>
""", unsafe_allow_html=True)

# Company Selection Interface
st.markdown("""
<div class="company-selector">
    <h3 style="color: white; margin: 0;">🏢 Select Company for Analysis</h3>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 2, 1])

with col1:
    # Dropdown for popular companies
    selected_company_name = st.selectbox(
        "Choose from popular companies:",
        options=list(POPULAR_COMPANIES.keys()),
        index=0
    )
    selected_symbol = POPULAR_COMPANIES[selected_company_name]

with col2:
    # Custom ticker input
    custom_symbol = st.text_input(
        "Or enter custom ticker symbol:",
        placeholder="e.g., TSLA, NVDA, MSFT",
        help="Enter any valid stock ticker symbol"
    )

with col3:
    # Load data button
    if st.button("🔄 Load Company Data", type="primary"):
        symbol = custom_symbol.upper() if custom_symbol else selected_symbol
        st.session_state.selected_company = symbol
        
        with st.spinner(f"Loading data for {symbol}..."):
            st.session_state.company_data = get_company_data(symbol)
        
        if st.session_state.company_data:
            st.success(f"✅ Successfully loaded data for {symbol}")
        else:
            st.error(f"❌ Failed to load data for {symbol}")

# Load initial data if not already loaded
if st.session_state.company_data is None:
    with st.spinner("Loading initial data..."):
        st.session_state.company_data = get_company_data(st.session_state.selected_company)

# Sidebar navigation
st.sidebar.title("📊 Dashboard Navigation")
selected_section = st.sidebar.selectbox(
    "Select Analysis Section",
    ["🏢 Company Overview", "📈 Financial Dashboard", "💬 AI Insights Chat", "📊 Technical Analysis"]
)

# Display company data if available
if st.session_state.company_data:
    company_data = st.session_state.company_data
    
    # Company Overview Section
    if selected_section == "🏢 Company Overview":
        st.header("🏢 Company Overview")
        
        # Company basic info
        info = company_data["company_info"]
        metrics = company_data["financial_metrics"]
        
        st.markdown(f"""
        <div class="company-info">
            <h2>{info['name']} ({info['symbol']})</h2>
            <p><strong>Sector:</strong> {info['sector']} | <strong>Industry:</strong> {info['industry']}</p>
            <p><strong>Country:</strong> {info['country']} | <strong>Employees:</strong> {info['employees']:,}</p>
            <p><strong>Description:</strong> {info['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Key metrics overview
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Stock Price",
                f"${metrics['current_price']:.2f}",
                delta=f"{metrics['monthly_growth']:.1f}% (30d)"
            )
            
        with col2:
            market_cap_b = metrics['market_cap'] / 1e9
            st.metric(
                "Market Cap",
                f"${market_cap_b:.1f}B",
                delta=f"P/E: {metrics['pe_ratio']:.1f}" if metrics['pe_ratio'] > 0 else "N/A"
            )
            
        with col3:
            revenue_b = metrics['total_revenue'] / 1e9 if metrics['total_revenue'] > 0 else 0
            st.metric(
                "Annual Revenue",
                f"${revenue_b:.1f}B" if revenue_b > 0 else "N/A",
                delta=f"{metrics['revenue_growth']:.1f}% growth" if metrics['revenue_growth'] != 0 else "N/A"
            )
            
        with col4:
            st.metric(
                "Profit Margin",
                f"{metrics['profit_margin']:.1f}%" if metrics['profit_margin'] > 0 else "N/A",
                delta=f"Efficiency: {metrics['operational_efficiency']:.1f}%"
            )
        
        # AI-generated insights
        st.subheader("🤖 AI-Generated Insights")
        insights = generate_company_insights(company_data)
        
        for insight in insights:
            st.info(insight)
    
    # Financial Dashboard Section
    elif selected_section == "📈 Financial Dashboard":
        st.header("📈 Financial Dashboard")
        
        metrics = company_data["financial_metrics"]
        stock_data = company_data["stock_data"]
        
        # Financial KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Current Price", f"${metrics['current_price']:.2f}")
            st.metric("P/E Ratio", f"{metrics['pe_ratio']:.1f}" if metrics['pe_ratio'] > 0 else "N/A")
            
        with col2:
            st.metric("Market Cap", f"${metrics['market_cap']/1e9:.1f}B")
            st.metric("Profit Margin", f"{metrics['profit_margin']:.1f}%")
            
        with col3:
            st.metric("Revenue Growth", f"{metrics['revenue_growth']:.1f}%")
            st.metric("Monthly Change", f"{metrics['monthly_growth']:.1f}%")
            
        with col4:
            st.metric("Operational Efficiency", f"{metrics['operational_efficiency']:.1f}%")
            st.metric("Employee Satisfaction", f"{metrics['employee_satisfaction']:.0f}%")
        
        # Stock price chart
        st.subheader("📊 Stock Price Performance (1 Year)")
        
        if not stock_data.empty:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=stock_data.index,
                y=stock_data['Close'],
                mode='lines',
                name='Stock Price',
                line=dict(color='#3b82f6', width=2)
            ))
            
            fig.update_layout(
                title=f"{company_data['company_info']['name']} Stock Price - Last 12 Months",
                xaxis_title="Date",
                yaxis_title="Price ($)",
                height=500,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Volume chart
            st.subheader("📈 Trading Volume")
            fig_volume = go.Figure()
            
            fig_volume.add_trace(go.Bar(
                x=stock_data.index,
                y=stock_data['Volume'],
                name='Volume',
                marker_color='#10b981'
            ))
            
            fig_volume.update_layout(
                title="Daily Trading Volume",
                xaxis_title="Date",
                yaxis_title="Volume",
                height=300
            )
            
            st.plotly_chart(fig_volume, use_container_width=True)
    
    # AI Insights Chat Section
    elif selected_section == "💬 AI Insights Chat":
        st.header("💬 AI-Powered Company Insights")
        st.subheader(f"Ask questions about {company_data['company_info']['name']}")
        
        # Chat interface
        col1, col2 = st.columns([3, 1])
        
        with col1:
            query_input = st.text_input(
                "Ask about the company:",
                placeholder=f"e.g., What's {company_data['company_info']['name']}'s competitive advantage?",
                key="company_query"
            )
        
        with col2:
            if st.button("🤖 Ask AI", type="primary"):
                if query_input:
                    # Simulate AI response based on company data
                    response_time = np.random.uniform(1.0, 2.5)
                    
                    with st.spinner(f"Analyzing {company_data['company_info']['name']}..."):
                        time.sleep(min(response_time, 2))
                    
                    company_name = company_data['company_info']['name']
                    metrics = company_data['financial_metrics']
                    info = company_data['company_info']
                    
                    # Generate contextual responses
                    if any(word in query_input.lower() for word in ['price', 'stock', 'valuation']):
                        response = f"📊 {company_name} is currently trading at ${metrics['current_price']:.2f} with a market cap of ${metrics['market_cap']/1e9:.1f}B. The stock has shown {metrics['monthly_growth']:.1f}% movement over the last 30 days."
                    elif any(word in query_input.lower() for word in ['growth', 'revenue', 'financial']):
                        response = f"💰 {company_name} reported revenue growth of {metrics['revenue_growth']:.1f}% with a profit margin of {metrics['profit_margin']:.1f}%. The company operates in the {info['sector']} sector."
                    elif any(word in query_input.lower() for word in ['sector', 'industry', 'competition']):
                        response = f"🏢 {company_name} operates in the {info['industry']} industry within the {info['sector']} sector. The company employs {info['employees']:,} people and is based in {info['country']}."
                    elif any(word in query_input.lower() for word in ['future', 'outlook', 'prediction']):
                        pe_insight = f"With a P/E ratio of {metrics['pe_ratio']:.1f}, " if metrics['pe_ratio'] > 0 else ""
                        response = f"🔮 {pe_insight}{company_name} shows {'strong' if metrics['monthly_growth'] > 0 else 'challenging'} recent performance. The company's operational efficiency of {metrics['operational_efficiency']:.1f}% suggests {'strong' if metrics['operational_efficiency'] > 85 else 'moderate'} management execution."
                    else:
                        response = f"🤖 {company_name} is a {info['sector']} company with strong fundamentals. Current market cap is ${metrics['market_cap']/1e9:.1f}B with {metrics['operational_efficiency']:.1f}% operational efficiency. What specific aspect would you like to explore?"
                    
                    st.success(response)
                    
                    # Add to conversation history
                    conversation = {
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "company": company_name,
                        "query": query_input,
                        "response": response,
                        "response_time": response_time
                    }
                    st.session_state.conversations.append(conversation)
        
        # Display recent conversations
        if st.session_state.conversations:
            st.subheader("🕐 Recent AI Conversations")
            
            for conv in reversed(st.session_state.conversations[-5:]):
                with st.expander(f"{conv['company']}: {conv['query'][:50]}... - {conv['timestamp']}"):
                    st.write(f"**Company:** {conv['company']}")
                    st.write(f"**Question:** {conv['query']}")
                    st.write(f"**AI Response:** {conv['response']}")
                    st.write(f"**Response Time:** {conv['response_time']:.1f}s")
    
    # Technical Analysis Section
    elif selected_section == "📊 Technical Analysis":
        st.header("📊 Technical Analysis")
        
        stock_data = company_data["stock_data"]
        
        if not stock_data.empty:
            # Calculate technical indicators
            stock_data['SMA_20'] = stock_data['Close'].rolling(window=20).mean()
            stock_data['SMA_50'] = stock_data['Close'].rolling(window=50).mean()
            
            # RSI calculation (simplified)
            delta = stock_data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            stock_data['RSI'] = 100 - (100 / (1 + rs))
            
            # Main price chart with moving averages
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=stock_data.index,
                y=stock_data['Close'],
                mode='lines',
                name='Close Price',
                line=dict(color='#3b82f6', width=2)
            ))
            
            fig.add_trace(go.Scatter(
                x=stock_data.index,
                y=stock_data['SMA_20'],
                mode='lines',
                name='SMA 20',
                line=dict(color='#f59e0b', width=1)
            ))
            
            fig.add_trace(go.Scatter(
                x=stock_data.index,
                y=stock_data['SMA_50'],
                mode='lines',
                name='SMA 50',
                line=dict(color='#10b981', width=1)
            ))
            
            fig.update_layout(
                title=f"{company_data['company_info']['name']} - Technical Analysis",
                xaxis_title="Date",
                yaxis_title="Price ($)",
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # RSI Chart
            st.subheader("📈 Relative Strength Index (RSI)")
            
            fig_rsi = go.Figure()
            
            fig_rsi.add_trace(go.Scatter(
                x=stock_data.index,
                y=stock_data['RSI'],
                mode='lines',
                name='RSI',
                line=dict(color='#8b5cf6', width=2)
            ))
            
            # Add overbought/oversold lines
            fig_rsi.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="Overbought (70)")
            fig_rsi.add_hline(y=30, line_dash="dash", line_color="green", annotation_text="Oversold (30)")
            
            fig_rsi.update_layout(
                title="RSI Indicator",
                xaxis_title="Date",
                yaxis_title="RSI",
                height=300,
                yaxis=dict(range=[0, 100])
            )
            
            st.plotly_chart(fig_rsi, use_container_width=True)
            
            # Technical summary
            current_rsi = stock_data['RSI'].iloc[-1]
            st.subheader("📋 Technical Summary")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                trend = "Bullish" if stock_data['Close'].iloc[-1] > stock_data['SMA_20'].iloc[-1] else "Bearish"
                st.metric("Short-term Trend", trend)
                
            with col2:
                long_trend = "Bullish" if stock_data['Close'].iloc[-1] > stock_data['SMA_50'].iloc[-1] else "Bearish"
                st.metric("Long-term Trend", long_trend)
                
            with col3:
                rsi_signal = "Overbought" if current_rsi > 70 else "Oversold" if current_rsi < 30 else "Neutral"
                st.metric("RSI Signal", rsi_signal, delta=f"RSI: {current_rsi:.1f}")

else:
    st.warning("⚠️ No company data loaded. Please select a company and click 'Load Company Data'")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; padding: 1rem;">
    <p>🤖 AI Analytics Engine - Real-Time Company Analytics with Live Market Data</p>
    <p>Built with Streamlit • Yahoo Finance API • Dynamic Data • Professional Analysis</p>
</div>
""", unsafe_allow_html=True)
