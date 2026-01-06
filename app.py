import streamlit as st
import pandas as pd
import plotly.express as px
# Page configuration
st.set_page_config(
    page_title="Cost Optimization Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .stMetric {
        background-color: white;
        padding: 0.5rem;
        border-radius: 0.3rem;
    }
    </style>
""", unsafe_allow_html=True)

# Load DataFlow data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('dashboard_data/rightsizing_results_dataflow.csv')

        # Convert created_at to datetime if it exists
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading DataFlow data: {str(e)}")
        return None

# Load CloudSQL data
@st.cache_data
def load_cloudsql_data():
    try:
        df = pd.read_csv('dashboard_data/rightsizing_results_cloudsql.csv')

        # Convert created_at to datetime if it exists
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading CloudSQL data: {str(e)}")
        return None

# Load Kubernetes data
@st.cache_data
def load_kubernetes_data():
    try:
        df = pd.read_csv('dashboard_data/rightsizing_results.csv')
        # Convert created_at to datetime if it exists
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
        return df
    except Exception as e:
        st.error(f"Error loading Kubernetes data: {str(e)}")
        return None

# Load Overview data
@st.cache_data
def load_overview_data():
    try:
        df = pd.read_csv('dashboard_data/overview.csv')
        return df
    except Exception as e:
        st.error(f"Error loading Overview data: {str(e)}")
        return None

# Title
st.markdown('<h1 class="main-header">💰 Cost Optimization Dashboard</h1>', unsafe_allow_html=True)
st.markdown("---")

# Load all datasets
df = load_data()
cloudsql_df = load_cloudsql_data()
kubernetes_df = load_kubernetes_data()
overview_df = load_overview_data()

# Use radio button to explicitly control which view is active
# This is more reliable than detecting from st.tabs() which executes both blocks
selected_service = st.radio(
    "Select Service",
    ["📈 Overview Analysis", "🗄️ CloudSQL Cost Optimization", "📊 DataFlow Cost Optimization", "☸️ Kubernetes Cost Optimization"],
    horizontal=True,
    key='service_selector',
    index=0
)

# Determine active tab based on radio selection
if selected_service == '📈 Overview Analysis':
    active_tab = 'Overview'
elif selected_service == '🗄️ CloudSQL Cost Optimization':
    active_tab = 'CloudSQL'
elif selected_service == '📊 DataFlow Cost Optimization':
    active_tab = 'DataFlow'
elif selected_service == '☸️ Kubernetes Cost Optimization':
    active_tab = 'Kubernetes'
else:
    active_tab = 'Overview'

# Create sidebar filter container (will be populated based on active tab)
filter_container = st.sidebar.empty()

# Default filter values (will be set by filter widgets)
selected_region_df = 'All'
selected_project_df = 'All'
selected_current_machine_df = 'All'
selected_target_machine_df = 'All'
selected_region_csql = 'All'
selected_project_csql = 'All'
selected_current_machine_csql = 'All'
selected_target_machine_csql = 'All'
selected_region_k8s = 'All'
selected_project_k8s = 'All'
selected_current_machine_k8s = 'All'
selected_target_machine_k8s = 'All'
selected_service_ov = 'All'
selected_project_ov = 'All'

# Render filters based on detected active tab (BEFORE tab content runs)
if active_tab == 'Overview' and overview_df is not None and not overview_df.empty:
    with filter_container.container():
        st.sidebar.header("🔍 Overview Filters")
        
        ov_services = ['All'] + sorted(overview_df['service'].unique().tolist()) if 'service' in overview_df.columns else ['All']
        ov_projects = ['All'] + sorted(overview_df['project_id'].unique().tolist()) if 'project_id' in overview_df.columns else ['All']
        
        selected_service_ov = st.sidebar.selectbox("Select Service", ov_services, key='overview_service')
        selected_project_ov = st.sidebar.selectbox("Select Project", ov_projects, key='overview_project')
elif active_tab == 'Kubernetes' and kubernetes_df is not None and not kubernetes_df.empty:
    with filter_container.container():
        st.sidebar.header("🔍 Kubernetes Filters")
        
        k8s_regions = ['All'] + sorted(kubernetes_df['region'].unique().tolist()) if 'region' in kubernetes_df.columns else ['All']
        k8s_projects = ['All'] + sorted(kubernetes_df['project_id'].unique().tolist()) if 'project_id' in kubernetes_df.columns else ['All']
        k8s_current_machines = ['All'] + sorted(kubernetes_df['current_machine_type'].unique().tolist()) if 'current_machine_type' in kubernetes_df.columns else ['All']
        k8s_target_machines = ['All'] + sorted(kubernetes_df['target_machine_type'].unique().tolist()) if 'target_machine_type' in kubernetes_df.columns else ['All']
        
        selected_region_k8s = st.sidebar.selectbox("Select Region", k8s_regions, key='kubernetes_region')
        selected_project_k8s = st.sidebar.selectbox("Select Project", k8s_projects, key='kubernetes_project')
        selected_current_machine_k8s = st.sidebar.selectbox("Current Machine Type", k8s_current_machines, key='kubernetes_current_machine')
        selected_target_machine_k8s = st.sidebar.selectbox("Target Machine Type", k8s_target_machines, key='kubernetes_target_machine')
elif active_tab == 'CloudSQL' and cloudsql_df is not None and not cloudsql_df.empty:
    with filter_container.container():
        st.sidebar.header("🔍 CloudSQL Filters")
        
        csql_regions = ['All'] + sorted(cloudsql_df['region'].unique().tolist()) if 'region' in cloudsql_df.columns else ['All']
        csql_projects = ['All'] + sorted(cloudsql_df['project_id'].unique().tolist()) if 'project_id' in cloudsql_df.columns else ['All']
        csql_current_machines = ['All'] + sorted(cloudsql_df['current_machine_type'].unique().tolist()) if 'current_machine_type' in cloudsql_df.columns else ['All']
        csql_target_machines = ['All'] + sorted(cloudsql_df['target_machine_type'].unique().tolist()) if 'target_machine_type' in cloudsql_df.columns else ['All']
        
        selected_region_csql = st.sidebar.selectbox("Select Region", csql_regions, key='cloudsql_region')
        selected_project_csql = st.sidebar.selectbox("Select Project", csql_projects, key='cloudsql_project')
        selected_current_machine_csql = st.sidebar.selectbox("Current Machine Type", csql_current_machines, key='cloudsql_current_machine')
        selected_target_machine_csql = st.sidebar.selectbox("Target Machine Type", csql_target_machines, key='cloudsql_target_machine')
elif active_tab == 'DataFlow' and df is not None and not df.empty:
    with filter_container.container():
        st.sidebar.header("🔍 DataFlow Filters")
        
        df_regions = ['All'] + sorted(df['region'].unique().tolist()) if 'region' in df.columns else ['All']
        df_projects = ['All'] + sorted(df['project_id'].unique().tolist()) if 'project_id' in df.columns else ['All']
        df_current_machines = ['All'] + sorted(df['current_machine_type'].unique().tolist()) if 'current_machine_type' in df.columns else ['All']
        df_target_machines = ['All'] + sorted(df['target_machine_type'].unique().tolist()) if 'target_machine_type' in df.columns else ['All']
        
        selected_region_df = st.sidebar.selectbox("Select Region", df_regions, key='dataflow_region')
        selected_project_df = st.sidebar.selectbox("Select Project", df_projects, key='dataflow_project')
        selected_current_machine_df = st.sidebar.selectbox("Current Machine Type", df_current_machines, key='dataflow_current_machine')
        selected_target_machine_df = st.sidebar.selectbox("Target Machine Type", df_target_machines, key='dataflow_target_machine')

# ==================== DATAFLOW VIEW ====================
if active_tab == 'DataFlow':
    if df is not None and not df.empty:
        # Get filter values from session state
        selected_region_df = st.session_state.get('dataflow_region', 'All')
        selected_project_df = st.session_state.get('dataflow_project', 'All')
        selected_current_machine_df = st.session_state.get('dataflow_current_machine', 'All')
        selected_target_machine_df = st.session_state.get('dataflow_target_machine', 'All')
        
        # Apply filters
        filtered_df = df.copy()
        if selected_region_df != 'All':
            filtered_df = filtered_df[filtered_df['region'] == selected_region_df]
        if selected_project_df != 'All':
            filtered_df = filtered_df[filtered_df['project_id'] == selected_project_df]
        if selected_current_machine_df != 'All':
            filtered_df = filtered_df[filtered_df['current_machine_type'] == selected_current_machine_df]
        if selected_target_machine_df != 'All':
            filtered_df = filtered_df[filtered_df['target_machine_type'] == selected_target_machine_df]
        
        # Calculate metrics
        total_current_cost = filtered_df['current_cost'].sum()
        total_target_cost = filtered_df['target_cost'].sum()
        total_savings = filtered_df['savings'].sum()
        # Formula: Savings Percentage = (Savings / Current Cost) * 100
        savings_percentage = (total_savings / total_current_cost * 100) if total_current_cost > 0 else 0
        # Formula: Cost Reduction Percentage = ((Current Cost - Target Cost) / Current Cost) * 100
        cost_reduction_percentage = ((total_current_cost - total_target_cost) / total_current_cost * 100) if total_current_cost > 0 else 0
        num_projects = filtered_df['project_id'].nunique()
        num_jobs = len(filtered_df)
        avg_savings_per_job = filtered_df['savings'].mean()
        max_savings = filtered_df['savings'].max()
        
        # Key Metrics Row
        st.subheader("📊 Key Performance Indicators")
        
        # Show prominent cost summary with percentages
        # st.markdown("### 💰 Cost Summary")
        # summary_col1, summary_col2, summary_col3 = st.columns(3)
        # 
        # with summary_col1:
        #     st.markdown(f"""
        #     <div style="background-color: #ffebee; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #f44336;">
        #         <h4 style="margin: 0; color: #c62828;">Current Spending (Monthly)</h4>
        #         <h2 style="margin: 0.5rem 0; color: #d32f2f;">${total_current_cost:,.2f}</h2>
        #         <p style="margin: 0; color: #666;">What you're spending now</p>
        #     </div>
        #     """, unsafe_allow_html=True)
        # 
        # with summary_col2:
        #     st.markdown(f"""
        #     <div style="background-color: #e8f5e9; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #4caf50;">
        #         <h4 style="margin: 0; color: #2e7d32;">Target Cost (Monthly)</h4>
        #         <h2 style="margin: 0.5rem 0; color: #388e3c;">${total_target_cost:,.2f}</h2>
        #         <p style="margin: 0; color: #666;">After optimization</p>
        #     </div>
        #     """, unsafe_allow_html=True)
        # 
        # with summary_col3:
        #     st.markdown(f"""
        #     <div style="background-color: #e3f2fd; padding: 1rem; border-radius: 0.5rem; border-left: 4px solid #2196f3;">
        #         <h4 style="margin: 0; color: #1565c0;">Total Savings (Monthly)</h4>
        #         <h2 style="margin: 0.5rem 0; color: #1976d2;">${total_savings:,.2f}</h2>
        #         <p style="margin: 0; color: #666; font-weight: bold;">Savings: {savings_percentage:.2f}%</p>
        #     </div>
        #     """, unsafe_allow_html=True)
        # 
        # st.markdown("<br>", unsafe_allow_html=True)
        # 
        # # Formula explanation
        # with st.expander("📐 View Calculation Formulas"):
        #     st.markdown(f"""
        #     ### Cost Savings Calculation Formulas
        #     
        #     **1. Savings Percentage Formula:**
        #     ```
        #     Savings % = (Total Savings / Total Current Cost) × 100
        #     Savings % = (${total_savings:,.2f} / ${total_current_cost:,.2f}) × 100 = {savings_percentage:.2f}%
        #     ```
        #     
        #     **2. Cost Reduction Percentage Formula:**
        #     ```
        #     Cost Reduction % = ((Current Cost - Target Cost) / Current Cost) × 100
        #     Cost Reduction % = ((${total_current_cost:,.2f} - ${total_target_cost:,.2f}) / ${total_current_cost:,.2f}) × 100 = {cost_reduction_percentage:.2f}%
        #     ```
        #     
        #     **3. Monthly Savings Calculation:**
        #     ```
        #     Monthly Savings = Current Monthly Cost - Target Monthly Cost
        #     Monthly Savings = ${total_current_cost:,.2f} - ${total_target_cost:,.2f} = ${total_savings:,.2f}
        #     ```
        #     
        #     **4. Annual Savings Projection:**
        #     ```
        #     Annual Savings = Monthly Savings × 12
        #     Annual Savings = ${total_savings:,.2f} × 12 = ${total_savings * 12:,.2f}
        #     ```
        #     """)
        
        st.markdown("---")
        
        # Detailed metrics row
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                label="Total Current Cost (Monthly)",
                value=f"${total_current_cost:,.2f}",
                delta=f"100% of spending"
            )
        
        with col2:
            st.metric(
                label="Total Target Cost (Monthly)",
                value=f"${total_target_cost:,.2f}",
                delta=f"-{cost_reduction_percentage:.2f}% reduction"
            )
        
        with col3:
            st.metric(
                label="Total Savings (Monthly)",
                value=f"${total_savings:,.2f}",
                delta=f"{savings_percentage:.2f}% savings"
            )
        
        with col4:
            st.metric(
                label="Number of Projects",
                value=num_projects
            )
        
        with col5:
            st.metric(
                label="Number of Jobs",
                value=num_jobs
            )
        
        st.markdown("---")
        
        # Additional metrics row with percentages
        col6, col7, col8, col9 = st.columns(4)
        
        with col6:
            # Calculate percentage for average savings
            avg_savings_pct = (avg_savings_per_job / filtered_df['current_cost'].mean() * 100) if filtered_df['current_cost'].mean() > 0 else 0
            st.metric(
                label="Average Savings per Job",
                value=f"${avg_savings_per_job:,.2f}",
                delta=f"{avg_savings_pct:.1f}% avg"
            )
        
        with col7:
            # Calculate percentage for max savings
            max_savings_row = filtered_df.loc[filtered_df['savings'].idxmax()]
            max_savings_pct = (max_savings / max_savings_row['current_cost'] * 100) if max_savings_row['current_cost'] > 0 else 0
            st.metric(
                label="Maximum Savings (Single Job)",
                value=f"${max_savings:,.2f}",
                delta=f"{max_savings_pct:.1f}% reduction"
            )
        
        with col8:
            avg_current_rate = filtered_df['current_machine_hourly_rate'].mean()
            st.metric(
                label="Avg Current Hourly Rate",
                value=f"${avg_current_rate:.4f}"
            )
        
        with col9:
            avg_target_rate = filtered_df['target_machine_hourly_rate'].mean()
            # Calculate rate reduction percentage
            rate_reduction_pct = ((avg_current_rate - avg_target_rate) / avg_current_rate * 100) if avg_current_rate > 0 else 0
            st.metric(
                label="Avg Target Hourly Rate",
                value=f"${avg_target_rate:.4f}",
                delta=f"-{rate_reduction_pct:.1f}% lower"
            )
        
        st.markdown("---")
        
        # Charts Section
        st.subheader("📈 Cost Analysis & Visualizations")
        
        # Row 1: Cost Comparison Chart
        st.markdown("### Current vs Target Cost Comparison")
        cost_comparison = pd.DataFrame({
            'Cost Type': ['Current Cost', 'Target Cost', 'Savings'],
            'Amount': [total_current_cost, total_target_cost, total_savings],
            'Percentage': ['100%', f'{100-cost_reduction_percentage:.1f}%', f'{savings_percentage:.1f}%']
        })
        
        # Create custom text with both amount and percentage
        cost_comparison['Display Text'] = cost_comparison.apply(
            lambda row: f"${row['Amount']:,.0f}<br>({row['Percentage']})", axis=1
        )
        
        fig_cost = px.bar(
            cost_comparison,
            x='Cost Type',
            y='Amount',
            color='Cost Type',
            color_discrete_map={
                'Current Cost': '#ff4444',
                'Target Cost': '#44ff44',
                'Savings': '#4444ff'
            },
            text='Display Text',
            labels={'Amount': 'Cost (USD)', 'Cost Type': ''}
        )
        fig_cost.update_layout(
            showlegend=False,
            height=400,
            yaxis_title="Cost (USD)",
            title=f"Total Savings: {savings_percentage:.2f}% (${total_savings:,.2f})"
        )
        fig_cost.update_traces(textposition='outside', textfont_size=10)
        st.plotly_chart(fig_cost, use_container_width=True)
        
        # Row 2: Regional Analysis
        col_chart3, col_chart4 = st.columns(2)
        
        with col_chart3:
            st.markdown("### Savings by Region")
            region_savings = filtered_df.groupby('region').agg({
                'savings': 'sum',
                'current_cost': 'sum',
                'target_cost': 'sum'
            }).reset_index()
            region_savings['Savings %'] = (region_savings['savings'] / region_savings['current_cost'] * 100).round(1)
            region_savings = region_savings.sort_values('savings', ascending=False)
            
            # Create text with both amount and percentage
            region_savings['Display Text'] = region_savings.apply(
                lambda row: f"${row['savings']:,.0f}<br>({row['Savings %']:.1f}%)", axis=1
            )
            
            fig_region = px.bar(
                region_savings,
                x='region',
                y='savings',
                color='savings',
                color_continuous_scale='Viridis',
                text='Display Text',
                labels={'savings': 'Total Savings (USD)', 'region': 'Region'}
            )
            fig_region.update_traces(textposition='outside')
            fig_region.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_region, use_container_width=True)
    
        with col_chart4:
            st.markdown("### Cost Breakdown by Region")
            region_costs = filtered_df.groupby('region').agg({
                'current_cost': 'sum',
                'target_cost': 'sum'
            }).reset_index()
            region_costs_melted = region_costs.melt(
                id_vars='region',
                value_vars=['current_cost', 'target_cost'],
                var_name='Cost Type',
                value_name='Cost'
            )
            region_costs_melted['Cost Type'] = region_costs_melted['Cost Type'].str.replace('_cost', ' Cost').str.title()
            
            fig_region_cost = px.bar(
                region_costs_melted,
                x='region',
                y='Cost',
                color='Cost Type',
                barmode='group',
                color_discrete_map={
                    'Current Cost': '#ff4444',
                    'Target Cost': '#44ff44'
                },
                labels={'Cost': 'Cost (USD)', 'region': 'Region'}
            )
            fig_region_cost.update_layout(height=400)
            st.plotly_chart(fig_region_cost, use_container_width=True)
        
        st.markdown("---")
        
        # Row 3: Machine Type Analysis
        st.markdown("### 🖥️ Machine Type Analysis")
        
        col_chart5, col_chart6 = st.columns(2)
        
        with col_chart5:
            st.markdown("#### Current Machine Types - Cost Distribution")
            current_machine_cost = filtered_df.groupby('current_machine_type').agg({
                'current_cost': 'sum',
                'savings': 'sum'
            }).reset_index().sort_values('current_cost', ascending=False)
            
            fig_current = px.bar(
                current_machine_cost,
                x='current_machine_type',
                y='current_cost',
                color='savings',
                color_continuous_scale='Reds',
                text=[f"${x:,.0f}" for x in current_machine_cost['current_cost']],
                labels={
                    'current_cost': 'Current Cost (USD)',
                    'current_machine_type': 'Current Machine Type',
                    'savings': 'Savings'
                }
            )
            fig_current.update_traces(textposition='outside')
            fig_current.update_layout(height=400, showlegend=True, xaxis_tickangle=-45)
            st.plotly_chart(fig_current, use_container_width=True)
        
        with col_chart6:
            st.markdown("#### Target Machine Types - Cost Distribution")
            target_machine_cost = filtered_df.groupby('target_machine_type').agg({
                'target_cost': 'sum',
                'savings': 'sum'
            }).reset_index().sort_values('target_cost', ascending=False)
            
            fig_target = px.bar(
                target_machine_cost,
                x='target_machine_type',
                y='target_cost',
                color='savings',
                color_continuous_scale='Greens',
                text=[f"${x:,.0f}" for x in target_machine_cost['target_cost']],
                labels={
                    'target_cost': 'Target Cost (USD)',
                    'target_machine_type': 'Target Machine Type',
                    'savings': 'Savings'
                }
            )
            fig_target.update_traces(textposition='outside')
            fig_target.update_layout(height=400, showlegend=True, xaxis_tickangle=-45)
            st.plotly_chart(fig_target, use_container_width=True)
        
        # Machine Type Migration Analysis
        st.markdown("#### Machine Type Migration Patterns")
        migration_pattern = filtered_df.groupby(['current_machine_type', 'target_machine_type']).agg({
            'savings': ['sum', 'count'],
            'current_cost': 'sum',
            'target_cost': 'sum'
        }).reset_index()
        migration_pattern.columns = ['Current Machine', 'Target Machine', 'Total Savings', 'Count', 'Current Cost', 'Target Cost']
        migration_pattern = migration_pattern.sort_values('Total Savings', ascending=False)
        
        fig_migration = px.scatter(
            migration_pattern,
            x='Current Cost',
            y='Total Savings',
            size='Count',
            color='Current Machine',
            hover_data=['Target Machine', 'Count'],
            labels={
                'Current Cost': 'Current Cost (USD)',
                'Total Savings': 'Total Savings (USD)',
                'Count': 'Number of Migrations'
            },
            title="Migration Impact: Current Cost vs Savings"
        )
        fig_migration.update_layout(height=500)
        st.plotly_chart(fig_migration, use_container_width=True)
        
        st.markdown("---")
        
        # Row 4: Project and Job Analysis
        st.markdown("### 📋 Project & Job Level Analysis")
        
        col_chart7, col_chart8 = st.columns(2)
        
        with col_chart7:
            st.markdown("#### Top Projects by Savings")
            project_savings = filtered_df.groupby('project_id').agg({
                'savings': 'sum',
                'current_cost': 'sum',
                'job_name': 'count'
            }).reset_index()
            project_savings.columns = ['Project ID', 'Total Savings', 'Current Cost', 'Job Count']
            project_savings = project_savings.sort_values('Total Savings', ascending=False).head(15)
            
            fig_projects = px.bar(
                project_savings,
                x='Total Savings',
                y='Project ID',
                orientation='h',
                color='Total Savings',
                color_continuous_scale='Blues',
                text=[f"${x:,.0f}" for x in project_savings['Total Savings']],
                labels={'Total Savings': 'Total Savings (USD)', 'Project ID': 'Project ID'}
            )
            fig_projects.update_traces(textposition='outside')
            fig_projects.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig_projects, use_container_width=True)
        
        with col_chart8:
            st.markdown("#### Top Jobs by Savings")
            job_savings = filtered_df.nlargest(20, 'savings')[['job_name', 'savings', 'current_cost', 'target_cost', 'project_id']]
            
            fig_jobs = px.bar(
                job_savings,
                x='savings',
                y='job_name',
                orientation='h',
                color='savings',
                color_continuous_scale='Oranges',
                text=[f"${x:,.0f}" for x in job_savings['savings']],
                labels={'savings': 'Savings (USD)', 'job_name': 'Job Name'},
                hover_data=['project_id', 'current_cost', 'target_cost']
            )
            fig_jobs.update_traces(textposition='outside')
            fig_jobs.update_layout(height=500, showlegend=False)
            st.plotly_chart(fig_jobs, use_container_width=True)
        
        st.markdown("---")
        
        # Row 5: Hourly Rates Analysis
        st.markdown("### 📊 Hourly Rates Analysis")
        
        st.markdown("#### Current vs Target Hourly Rates")
        rate_comparison = filtered_df[['current_machine_hourly_rate', 'target_machine_hourly_rate']].melt(
            var_name='Rate Type',
            value_name='Hourly Rate'
        )
        rate_comparison['Rate Type'] = rate_comparison['Rate Type'].str.replace('_machine_hourly_rate', '').str.replace('_', ' ').str.title()
        
        fig_rates = px.box(
            rate_comparison,
            x='Rate Type',
            y='Hourly Rate',
            color='Rate Type',
            color_discrete_map={
                'Current Machine Hourly Rate': '#ff4444',
                'Target Machine Hourly Rate': '#44ff44'
            },
            labels={'Hourly Rate': 'Hourly Rate (USD)'}
        )
        fig_rates.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig_rates, use_container_width=True)
        
        st.markdown("---")
        
        # Summary Table
        st.subheader("📋 Detailed Summary Table")
        
        # Create summary by various dimensions
        tab1, tab2, tab3, tab4 = st.tabs(["By Region", "By Current Machine", "By Target Machine", "By Project"])
        
        with tab1:
            region_summary = filtered_df.groupby('region').agg({
                'project_id': 'nunique',
                'job_name': 'count',
                'current_cost': 'sum',
                'target_cost': 'sum',
                'savings': 'sum',
                'current_machine_hourly_rate': 'mean',
                'target_machine_hourly_rate': 'mean'
            }).reset_index()
            region_summary.columns = ['Region', 'Projects', 'Jobs', 'Current Cost', 'Target Cost', 'Savings', 
                                    'Avg Current Rate/hr', 'Avg Target Rate/hr']
            region_summary['Savings %'] = (region_summary['Savings'] / region_summary['Current Cost'] * 100).round(2)
            region_summary = region_summary.sort_values('Savings', ascending=False)
            st.dataframe(region_summary.style.format({
                'Current Cost': '${:,.2f}',
                'Target Cost': '${:,.2f}',
                'Savings': '${:,.2f}',
                'Avg Current Rate/hr': '${:.4f}',
                'Avg Target Rate/hr': '${:.4f}',
                'Savings %': '{:.1f}%'
            }), use_container_width=True)
        
        with tab2:
            current_machine_summary = filtered_df.groupby('current_machine_type').agg({
                'project_id': 'nunique',
                'job_name': 'count',
                'current_cost': 'sum',
                'target_cost': 'sum',
                'savings': 'sum'
            }).reset_index()
            current_machine_summary.columns = ['Current Machine Type', 'Projects', 'Jobs', 'Current Cost', 'Target Cost', 'Savings']
            current_machine_summary['Savings %'] = (current_machine_summary['Savings'] / current_machine_summary['Current Cost'] * 100).round(2)
            current_machine_summary = current_machine_summary.sort_values('Savings', ascending=False)
            st.dataframe(current_machine_summary.style.format({
                'Current Cost': '${:,.2f}',
                'Target Cost': '${:,.2f}',
                'Savings': '${:,.2f}',
                'Savings %': '{:.1f}%'
            }), use_container_width=True)
        
        with tab3:
            target_machine_summary = filtered_df.groupby('target_machine_type').agg({
                'project_id': 'nunique',
                'job_name': 'count',
                'current_cost': 'sum',
                'target_cost': 'sum',
                'savings': 'sum'
            }).reset_index()
            target_machine_summary.columns = ['Target Machine Type', 'Projects', 'Jobs', 'Current Cost', 'Target Cost', 'Savings']
            target_machine_summary['Savings %'] = (target_machine_summary['Savings'] / target_machine_summary['Current Cost'] * 100).round(2)
            target_machine_summary = target_machine_summary.sort_values('Savings', ascending=False)
            st.dataframe(target_machine_summary.style.format({
                'Current Cost': '${:,.2f}',
                'Target Cost': '${:,.2f}',
                'Savings': '${:,.2f}',
                'Savings %': '{:.1f}%'
            }), use_container_width=True)
        
        with tab4:
            project_summary = filtered_df.groupby('project_id').agg({
                'job_name': 'count',
                'current_cost': 'sum',
                'target_cost': 'sum',
                'savings': 'sum',
                'region': 'first'
            }).reset_index()
            project_summary.columns = ['Project ID', 'Jobs', 'Current Cost', 'Target Cost', 'Savings', 'Region']
            project_summary['Savings %'] = (project_summary['Savings'] / project_summary['Current Cost'] * 100).round(2)
            project_summary = project_summary.sort_values('Savings', ascending=False)
            st.dataframe(project_summary.style.format({
                'Current Cost': '${:,.2f}',
                'Target Cost': '${:,.2f}',
                'Savings': '${:,.2f}',
                'Savings %': '{:.1f}%'
            }), use_container_width=True)
        
        st.markdown("---")
        
        # Full Data Table with Filters
        st.subheader("🔍 Complete Data View")
        
        # Search and filter options
        search_term = st.text_input("Search in data (Job Name, Project ID, etc.)", "")
        
        if search_term:
            mask = (
                filtered_df['job_name'].str.contains(search_term, case=False, na=False) |
                filtered_df['project_id'].str.contains(search_term, case=False, na=False) |
                filtered_df['current_machine_type'].str.contains(search_term, case=False, na=False) |
                filtered_df['target_machine_type'].str.contains(search_term, case=False, na=False)
            )
            display_df = filtered_df[mask]
        else:
            display_df = filtered_df.copy()
        
        # Select columns to display
        default_cols = ['project_id', 'job_name', 'current_machine_type', 'target_machine_type', 
                    'region', 'current_cost', 'target_cost', 'savings']
        available_cols = filtered_df.columns.tolist()
        selected_cols = st.multiselect("Select columns to display", available_cols, default=default_cols)
        
        if selected_cols:
            display_df = display_df[selected_cols]
        
        # Add savings percentage column if cost columns are present
        if 'current_cost' in display_df.columns and 'savings' in display_df.columns:
            display_df = display_df.copy()
            display_df['Savings %'] = (display_df['savings'] / display_df['current_cost'] * 100).round(2)
            # Reorder columns to put Savings % after savings
            if 'Savings %' in display_df.columns:
                cols = [col for col in display_df.columns if col != 'Savings %']
                savings_idx = cols.index('savings') if 'savings' in cols else len(cols)
                cols.insert(savings_idx + 1, 'Savings %')
                display_df = display_df[cols]
        
        # Display data with pagination
        format_dict = {
            'current_cost': '${:,.2f}',
            'target_cost': '${:,.2f}',
            'savings': '${:,.2f}',
            'current_machine_hourly_rate': '${:.4f}',
            'target_machine_hourly_rate': '${:.4f}'
        }
        if 'Savings %' in display_df.columns:
            format_dict['Savings %'] = '{:.2f}%'
        
        st.dataframe(
            display_df.style.format(format_dict, subset=[col for col in format_dict.keys() if col in display_df.columns]),
            use_container_width=True,
            height=400
        )
        
        # Export option
        csv = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name='cost_optimization_filtered_data.csv',
            mime='text/csv'
        )
        
        st.markdown("---")
        
        # Footer
        st.markdown("### 💡 Key Insights")
        insights_col1, insights_col2 = st.columns(2)
        
        with insights_col1:
            annual_savings = total_savings * 12
            st.info(f"""
            **💵 Cost Impact:**
                - **Current Spending:** ${total_current_cost:,.2f}/month (100%)
                - **Target Cost:** ${total_target_cost:,.2f}/month ({100-cost_reduction_percentage:.1f}% of current)
                - **Monthly Savings:** ${total_savings:,.2f} ({savings_percentage:.2f}% reduction)
                - **Annual Savings Projection:** ${annual_savings:,.2f}
            - Average savings per job: **${avg_savings_per_job:,.2f}**
            
            **📊 Scale:**
            - Total projects analyzed: **{num_projects}**
            - Total jobs optimized: **{num_jobs}**
            """)
        
        with insights_col2:
            top_region = filtered_df.groupby('region')['savings'].sum().idxmax()
            top_region_savings = filtered_df.groupby('region')['savings'].sum().max()
            top_region_pct = (top_region_savings / filtered_df[filtered_df['region'] == top_region]['current_cost'].sum() * 100)
            top_current_machine = filtered_df.groupby('current_machine_type')['current_cost'].sum().idxmax()
            
            st.info(f"""
            **🎯 Top Opportunities:**
                - Highest savings region: **{top_region}** (${top_region_savings:,.2f}, {top_region_pct:.1f}% savings)
            - Most expensive machine type: **{top_current_machine}**
                - Maximum single job savings: **${max_savings:,.2f}** ({max_savings_pct:.1f}% reduction)
                - **Cost Reduction:** You can reduce costs by **{cost_reduction_percentage:.2f}%** while maintaining performance
            """)
    
    else:
        st.error("Unable to load DataFlow data. Please check if rightsizing_results_dataflow exists and is properly formatted.")

# ==================== CLOUDSQL VIEW ====================
if active_tab == 'CloudSQL':
    if cloudsql_df is not None and not cloudsql_df.empty:
        # Get filter values from session state
        selected_region_csql = st.session_state.get('cloudsql_region', 'All')
        selected_project_csql = st.session_state.get('cloudsql_project', 'All')
        selected_current_machine_csql = st.session_state.get('cloudsql_current_machine', 'All')
        selected_target_machine_csql = st.session_state.get('cloudsql_target_machine', 'All')
        
        # Apply filters to CloudSQL data
        filtered_cloudsql_df = cloudsql_df.copy()
        
        if selected_region_csql != 'All':
            filtered_cloudsql_df = filtered_cloudsql_df[filtered_cloudsql_df['region'] == selected_region_csql]
        if selected_project_csql != 'All':
            filtered_cloudsql_df = filtered_cloudsql_df[filtered_cloudsql_df['project_id'] == selected_project_csql]
        if selected_current_machine_csql != 'All':
            filtered_cloudsql_df = filtered_cloudsql_df[filtered_cloudsql_df['current_machine_type'] == selected_current_machine_csql]
        if selected_target_machine_csql != 'All':
            filtered_cloudsql_df = filtered_cloudsql_df[filtered_cloudsql_df['target_machine_type'] == selected_target_machine_csql]
        
        # Calculate CloudSQL metrics (based on query 1: CloudSQL Savings Summary)
        cloudsql_total_target = filtered_cloudsql_df['target_cost'].sum()
        cloudsql_total_current = filtered_cloudsql_df['current_cost'].sum()
        cloudsql_total_savings = filtered_cloudsql_df['savings'].sum()
        cloudsql_savings_pct = (cloudsql_total_savings / cloudsql_total_current * 100) if cloudsql_total_current > 0 else 0
        cloudsql_cost_reduction_pct = ((cloudsql_total_current - cloudsql_total_target) / cloudsql_total_current * 100) if cloudsql_total_current > 0 else 0
        cloudsql_num_clusters = filtered_cloudsql_df['resource_name'].nunique()
        cloudsql_num_projects = filtered_cloudsql_df['project_id'].nunique()
        
        # 1. CloudSQL Savings Summary
        st.subheader("📊 CloudSQL Savings Summary")
        
        col_cs1, col_cs2, col_cs3, col_cs4, col_cs5 = st.columns(5)
        
        with col_cs1:
            st.metric(
                label="Current Cost (Monthly)",
                value=f"${cloudsql_total_current:,.2f}",
                delta="100% of spending"
            )
        
        with col_cs2:
            st.metric(
                label="Target Cost (Monthly)",
                value=f"${cloudsql_total_target:,.2f}",
                delta=f"-{cloudsql_cost_reduction_pct:.2f}% reduction"
            )
        
        with col_cs3:
            st.metric(
                label="Total Savings (Monthly)",
                value=f"${cloudsql_total_savings:,.2f}",
                delta=f"{cloudsql_savings_pct:.2f}% savings"
            )
        
        with col_cs4:
            st.metric(
                label="Number of Clusters",
                value=cloudsql_num_clusters
            )
        
        with col_cs5:
            st.metric(
                label="Number of Projects",
                value=cloudsql_num_projects
            )
        
        st.markdown("---")
        
        # 2. CloudSQL Top 10 Savings by Cluster (based on query 2)
        st.subheader("🏆 CloudSQL Top 10 Savings by Cluster")
        
        # Query equivalent: GROUP BY resource_name, ORDER BY savings DESC, LIMIT 10
        cluster_savings = filtered_cloudsql_df.groupby('resource_name').agg({
            'target_cost': 'sum',
            'current_cost': 'sum',
            'savings': 'sum'
        }).reset_index()
        cluster_savings.columns = ['Cluster', 'Estimated', 'Actual', 'Savings']
        cluster_savings = cluster_savings.sort_values('Savings', ascending=False).head(10)
        cluster_savings['Savings %'] = (cluster_savings['Savings'] / cluster_savings['Actual'] * 100).round(2)
        
        col_chart_cs1, col_chart_cs2 = st.columns(2)
        
        with col_chart_cs1:
            # Bar chart for Top 10 Clusters
            cluster_savings['Display Text'] = cluster_savings.apply(
                lambda row: f"${row['Savings']:,.0f}<br>({row['Savings %']:.1f}%)", axis=1
            )
            
            fig_clusters = px.bar(
                cluster_savings,
                x='Savings',
                y='Cluster',
                orientation='h',
                color='Savings',
                color_continuous_scale='Blues',
                text='Display Text',
                labels={'Savings': 'Savings (USD)', 'Cluster': 'Cluster Name'},
                title="Top 10 Clusters by Savings"
            )
            fig_clusters.update_traces(textposition='outside')
            fig_clusters.update_layout(height=500, showlegend=False, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_clusters, use_container_width=True)
        
        with col_chart_cs2:
            # Table view
            st.markdown("#### Detailed Cluster Savings")
            st.dataframe(
                cluster_savings[['Cluster', 'Actual', 'Estimated', 'Savings', 'Savings %']].style.format({
                    'Actual': '${:,.2f}',
                    'Estimated': '${:,.2f}',
                    'Savings': '${:,.2f}',
                    'Savings %': '{:.2f}%'
                }),
                use_container_width=True,
                height=500
            )
        
        st.markdown("---")
        
        # 3. CloudSQL Top 3 Savings by Project (based on query 3)
        st.subheader("🎯 CloudSQL Top 3 Savings by Project")
        
        # Query equivalent: GROUP BY project_id, ORDER BY savings DESC, LIMIT 3
        project_savings = filtered_cloudsql_df.groupby('project_id').agg({
            'target_cost': 'sum',
            'current_cost': 'sum',
            'savings': 'sum',
            'resource_name': 'count'
        }).reset_index()
        project_savings.columns = ['Project ID', 'Estimated', 'Actual', 'Savings', 'Clusters']
        project_savings = project_savings.sort_values('Savings', ascending=False).head(3)
        project_savings['Savings %'] = (project_savings['Savings'] / project_savings['Actual'] * 100).round(2)
        
        col_chart_cs3, col_chart_cs4 = st.columns(2)
        
        with col_chart_cs3:
            # Bar chart for Top 3 Projects
            project_savings['Display Text'] = project_savings.apply(
                lambda row: f"${row['Savings']:,.0f}<br>({row['Savings %']:.1f}%)", axis=1
            )
            
            fig_projects = px.bar(
                project_savings,
                x='Savings',
                y='Project ID',
                orientation='h',
                color='Savings',
                color_continuous_scale='Greens',
                text='Display Text',
                labels={'Savings': 'Savings (USD)', 'Project ID': 'Project ID'},
                title="Top 3 Projects by Savings",
                hover_data=['Clusters', 'Actual', 'Estimated']
            )
            fig_projects.update_traces(textposition='outside')
            fig_projects.update_layout(height=400, showlegend=False, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_projects, use_container_width=True)
        
        with col_chart_cs4:
            # Table view
            st.markdown("#### Detailed Project Savings")
            st.dataframe(
                project_savings[['Project ID', 'Clusters', 'Actual', 'Estimated', 'Savings', 'Savings %']].style.format({
                    'Actual': '${:,.2f}',
                    'Estimated': '${:,.2f}',
                    'Savings': '${:,.2f}',
                    'Savings %': '{:.2f}%'
                }),
                use_container_width=True,
                height=400
            )
        
        st.markdown("---")
        
        # Additional CloudSQL Analysis
        st.subheader("📈 Additional CloudSQL Analysis")
        
        # Cost Comparison Chart
        col_chart_cs5, col_chart_cs6 = st.columns(2)
        
        with col_chart_cs5:
            st.markdown("### CloudSQL Cost Comparison")
            cloudsql_cost_comp = pd.DataFrame({
                'Cost Type': ['Current Cost', 'Target Cost', 'Savings'],
                'Amount': [cloudsql_total_current, cloudsql_total_target, cloudsql_total_savings],
                'Percentage': ['100%', f'{100-cloudsql_cost_reduction_pct:.1f}%', f'{cloudsql_savings_pct:.1f}%']
            })
            cloudsql_cost_comp['Display Text'] = cloudsql_cost_comp.apply(
                lambda row: f"${row['Amount']:,.0f}<br>({row['Percentage']})", axis=1
            )
            
            fig_cloudsql_cost = px.bar(
                cloudsql_cost_comp,
                x='Cost Type',
                y='Amount',
                color='Cost Type',
                color_discrete_map={
                    'Current Cost': '#ff4444',
                    'Target Cost': '#44ff44',
                    'Savings': '#4444ff'
                },
                text='Display Text',
                labels={'Amount': 'Cost (USD)', 'Cost Type': ''}
            )
            fig_cloudsql_cost.update_layout(
                showlegend=False,
                height=400,
                yaxis_title="Cost (USD)",
                title=f"Total Savings: {cloudsql_savings_pct:.2f}% (${cloudsql_total_savings:,.2f})"
            )
            fig_cloudsql_cost.update_traces(textposition='outside', textfont_size=10)
            st.plotly_chart(fig_cloudsql_cost, use_container_width=True)
        
        with col_chart_cs6:
            st.markdown("### CloudSQL Savings by Region")
            cloudsql_region_savings = filtered_cloudsql_df.groupby('region').agg({
                'savings': 'sum',
                'current_cost': 'sum',
                'target_cost': 'sum',
                'resource_name': 'nunique'
            }).reset_index()
            cloudsql_region_savings.columns = ['Region', 'Savings', 'Current Cost', 'Target Cost', 'Clusters']
            cloudsql_region_savings['Savings %'] = (cloudsql_region_savings['Savings'] / cloudsql_region_savings['Current Cost'] * 100).round(1)
            cloudsql_region_savings = cloudsql_region_savings.sort_values('Savings', ascending=False)
            
            cloudsql_region_savings['Display Text'] = cloudsql_region_savings.apply(
                lambda row: f"${row['Savings']:,.0f}<br>({row['Savings %']:.1f}%)", axis=1
            )
            
            fig_cloudsql_region = px.bar(
                cloudsql_region_savings,
                x='Region',
                y='Savings',
                color='Savings',
                color_continuous_scale='Viridis',
                text='Display Text',
                labels={'Savings': 'Total Savings (USD)', 'Region': 'Region'},
                title="Savings by Region"
            )
            fig_cloudsql_region.update_traces(textposition='outside')
            fig_cloudsql_region.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_cloudsql_region, use_container_width=True)
        
        st.markdown("---")
        
        # Machine Type Analysis
        col_chart_cs7, col_chart_cs8 = st.columns(2)
        
        with col_chart_cs7:
            st.markdown("### Current Machine Types - Cost Distribution")
            cloudsql_current_machine = filtered_cloudsql_df.groupby('current_machine_type').agg({
                'current_cost': 'sum',
                'savings': 'sum'
            }).reset_index().sort_values('current_cost', ascending=False).head(10)
            
            cloudsql_current_machine['Savings %'] = (cloudsql_current_machine['savings'] / cloudsql_current_machine['current_cost'] * 100).round(1)
            
            fig_cloudsql_current = px.bar(
                cloudsql_current_machine,
                x='current_machine_type',
                y='current_cost',
                color='savings',
                color_continuous_scale='Reds',
                text=[f"${x:,.0f}" for x in cloudsql_current_machine['current_cost']],
                labels={
                    'current_cost': 'Current Cost (USD)',
                    'current_machine_type': 'Current Machine Type',
                    'savings': 'Savings'
                },
                title="Top 10 Current Machine Types"
            )
            fig_cloudsql_current.update_traces(textposition='outside')
            fig_cloudsql_current.update_layout(height=400, showlegend=True, xaxis_tickangle=-45)
            st.plotly_chart(fig_cloudsql_current, use_container_width=True)
        
        with col_chart_cs8:
            st.markdown("### Target Machine Types - Cost Distribution")
            cloudsql_target_machine = filtered_cloudsql_df.groupby('target_machine_type').agg({
                'target_cost': 'sum',
                'savings': 'sum'
            }).reset_index().sort_values('target_cost', ascending=False).head(10)
            
            cloudsql_target_machine['Savings %'] = (cloudsql_target_machine['savings'] / (cloudsql_target_machine['target_cost'] + cloudsql_target_machine['savings']) * 100).round(1)
            
            fig_cloudsql_target = px.bar(
                cloudsql_target_machine,
                x='target_machine_type',
                y='target_cost',
                color='savings',
                color_continuous_scale='Greens',
                text=[f"${x:,.0f}" for x in cloudsql_target_machine['target_cost']],
                labels={
                    'target_cost': 'Target Cost (USD)',
                    'target_machine_type': 'Target Machine Type',
                    'savings': 'Savings'
                },
                title="Top 10 Target Machine Types"
            )
            fig_cloudsql_target.update_traces(textposition='outside')
            fig_cloudsql_target.update_layout(height=400, showlegend=True, xaxis_tickangle=-45)
            st.plotly_chart(fig_cloudsql_target, use_container_width=True)
        
        st.markdown("---")
        
        # Detailed Summary Tables
        st.subheader("📋 CloudSQL Detailed Summary Tables")
        
        cloudsql_tab1, cloudsql_tab2, cloudsql_tab3 = st.tabs(["By Region", "By Machine Type", "By Cluster"])
        
        with cloudsql_tab1:
            cloudsql_region_summary = filtered_cloudsql_df.groupby('region').agg({
                'project_id': 'nunique',
                'resource_name': 'nunique',
                'current_cost': 'sum',
                'target_cost': 'sum',
                'savings': 'sum'
            }).reset_index()
            cloudsql_region_summary.columns = ['Region', 'Projects', 'Clusters', 'Current Cost', 'Target Cost', 'Savings']
            cloudsql_region_summary['Savings %'] = (cloudsql_region_summary['Savings'] / cloudsql_region_summary['Current Cost'] * 100).round(2)
            cloudsql_region_summary = cloudsql_region_summary.sort_values('Savings', ascending=False)
            st.dataframe(cloudsql_region_summary.style.format({
                'Current Cost': '${:,.2f}',
                'Target Cost': '${:,.2f}',
                'Savings': '${:,.2f}',
                'Savings %': '{:.1f}%'
            }), use_container_width=True)
        
        with cloudsql_tab2:
            cloudsql_machine_summary = filtered_cloudsql_df.groupby(['current_machine_type', 'target_machine_type']).agg({
                'resource_name': 'count',
                'current_cost': 'sum',
                'target_cost': 'sum',
                'savings': 'sum'
            }).reset_index()
            cloudsql_machine_summary.columns = ['Current Machine', 'Target Machine', 'Clusters', 'Current Cost', 'Target Cost', 'Savings']
            cloudsql_machine_summary['Savings %'] = (cloudsql_machine_summary['Savings'] / cloudsql_machine_summary['Current Cost'] * 100).round(2)
            cloudsql_machine_summary = cloudsql_machine_summary.sort_values('Savings', ascending=False)
            st.dataframe(cloudsql_machine_summary.style.format({
                'Current Cost': '${:,.2f}',
                'Target Cost': '${:,.2f}',
                'Savings': '${:,.2f}',
                'Savings %': '{:.1f}%'
            }), use_container_width=True)
        
        with cloudsql_tab3:
            cloudsql_cluster_summary = filtered_cloudsql_df.groupby(['resource_name', 'project_id']).agg({
                'current_cost': 'sum',
                'target_cost': 'sum',
                'savings': 'sum',
                'current_machine_type': 'first',
                'target_machine_type': 'first'
            }).reset_index()
            cloudsql_cluster_summary.columns = ['Cluster', 'Project ID', 'Current Cost', 'Target Cost', 'Savings', 'Current Machine', 'Target Machine']
            cloudsql_cluster_summary['Savings %'] = (cloudsql_cluster_summary['Savings'] / cloudsql_cluster_summary['Current Cost'] * 100).round(2)
            cloudsql_cluster_summary = cloudsql_cluster_summary.sort_values('Savings', ascending=False)
            st.dataframe(cloudsql_cluster_summary.style.format({
                'Current Cost': '${:,.2f}',
                'Target Cost': '${:,.2f}',
                'Savings': '${:,.2f}',
                'Savings %': '{:.1f}%'
            }), use_container_width=True)
        
        st.markdown("---")
        
        # Key Insights
        st.markdown("### 💡 CloudSQL Key Insights")
        insights_cs_col1, insights_cs_col2 = st.columns(2)
        
        with insights_cs_col1:
            cloudsql_annual_savings = cloudsql_total_savings * 12
            st.info(f"""
            **💵 CloudSQL Cost Impact:**
            - **Current Spending:** ${cloudsql_total_current:,.2f}/month (100%)
            - **Target Cost:** ${cloudsql_total_target:,.2f}/month ({100-cloudsql_cost_reduction_pct:.1f}% of current)
            - **Monthly Savings:** ${cloudsql_total_savings:,.2f} ({cloudsql_savings_pct:.2f}% reduction)
            - **Annual Savings Projection:** ${cloudsql_annual_savings:,.2f}
            
            **📊 Scale:**
            - Total clusters analyzed: **{cloudsql_num_clusters}**
            - Total projects: **{cloudsql_num_projects}**
            """)
        
        with insights_cs_col2:
            if len(cluster_savings) > 0:
                top_cluster = cluster_savings.iloc[0]
                top_project = project_savings.iloc[0] if len(project_savings) > 0 else None
                
                top_cluster_text = f"- Top saving cluster: **{top_cluster['Cluster']}** (${top_cluster['Savings']:,.2f}, {top_cluster['Savings %']:.1f}%)\n"
                top_project_text = f"- Top saving project: **{top_project['Project ID']}** (${top_project['Savings']:,.2f}, {top_project['Savings %']:.1f}%)\n" if top_project is not None else ""
                
                st.info(f"""
                **🎯 Top Opportunities:**
                {top_cluster_text}{top_project_text}
                - **Cost Reduction:** Reduce CloudSQL costs by **{cloudsql_cost_reduction_pct:.2f}%** while maintaining performance
                - Average savings per cluster: **${cloudsql_total_savings/cloudsql_num_clusters:,.2f}**
                """)
    
    else:
        st.error("Unable to load CloudSQL data. Please check if Cloud SQL exists and is properly formatted.")

# ==================== KUBERNETES VIEW ====================
if active_tab == 'Kubernetes':
    if kubernetes_df is not None and not kubernetes_df.empty:
        # Get filter values from session state
        selected_region_k8s = st.session_state.get('kubernetes_region', 'All')
        selected_project_k8s = st.session_state.get('kubernetes_project', 'All')
        selected_current_machine_k8s = st.session_state.get('kubernetes_current_machine', 'All')
        selected_target_machine_k8s = st.session_state.get('kubernetes_target_machine', 'All')
        
        # Apply filters to Kubernetes data
        filtered_k8s_df = kubernetes_df.copy()
        
        if selected_region_k8s != 'All':
            filtered_k8s_df = filtered_k8s_df[filtered_k8s_df['region'] == selected_region_k8s]
        if selected_project_k8s != 'All':
            filtered_k8s_df = filtered_k8s_df[filtered_k8s_df['project_id'] == selected_project_k8s]
        if selected_current_machine_k8s != 'All':
            filtered_k8s_df = filtered_k8s_df[filtered_k8s_df['current_machine_type'] == selected_current_machine_k8s]
        if selected_target_machine_k8s != 'All':
            filtered_k8s_df = filtered_k8s_df[filtered_k8s_df['target_machine_type'] == selected_target_machine_k8s]
        
        # Calculate Kubernetes metrics (based on query 1: Kubernetes Savings Summary)
        k8s_total_target = filtered_k8s_df['target_cost'].sum()
        k8s_total_current = filtered_k8s_df['current_cost'].sum()
        k8s_total_savings = filtered_k8s_df['savings'].sum()
        k8s_savings_pct = (k8s_total_savings / k8s_total_current * 100) if k8s_total_current > 0 else 0
        k8s_cost_reduction_pct = ((k8s_total_current - k8s_total_target) / k8s_total_current * 100) if k8s_total_current > 0 else 0
        k8s_num_clusters = filtered_k8s_df['cluster_name'].nunique()
        k8s_num_projects = filtered_k8s_df['project_id'].nunique()
        k8s_total_nodes = filtered_k8s_df['node_count'].sum() if 'node_count' in filtered_k8s_df.columns else 0
        
        # 1. Kubernetes Savings Summary
        st.subheader("📊 Kubernetes Savings Summary")
        
        col_k8s1, col_k8s2, col_k8s3, col_k8s4, col_k8s5, col_k8s6 = st.columns(6)
        
        with col_k8s1:
            st.metric(
                label="Current Cost (Monthly)",
                value=f"${k8s_total_current:,.2f}",
                delta="100% of spending"
            )
        
        with col_k8s2:
            st.metric(
                label="Target Cost (Monthly)",
                value=f"${k8s_total_target:,.2f}",
                delta=f"-{k8s_cost_reduction_pct:.2f}% reduction"
            )
        
        with col_k8s3:
            st.metric(
                label="Total Savings (Monthly)",
                value=f"${k8s_total_savings:,.2f}",
                delta=f"{k8s_savings_pct:.2f}% savings"
            )
        
        with col_k8s4:
            st.metric(
                label="Number of Clusters",
                value=k8s_num_clusters
            )
        
        with col_k8s5:
            st.metric(
                label="Number of Projects",
                value=k8s_num_projects
            )
        
        with col_k8s6:
            st.metric(
                label="Total Nodes",
                value=int(k8s_total_nodes) if k8s_total_nodes > 0 else 0
            )
        
        st.markdown("---")
        
        # 2. Kubernetes Top 10 Savings by Cluster (based on query 2)
        st.subheader("🏆 Kubernetes Top 10 Savings by Cluster")
        
        # Query equivalent: GROUP BY cluster_name, ORDER BY savings DESC, LIMIT 10
        k8s_cluster_savings = filtered_k8s_df.groupby('cluster_name').agg({
            'target_cost': 'sum',
            'current_cost': 'sum',
            'savings': 'sum',
            'node_count': 'sum'
        }).reset_index()
        k8s_cluster_savings.columns = ['Cluster', 'Estimated', 'Actual', 'Savings', 'Nodes']
        k8s_cluster_savings = k8s_cluster_savings.sort_values('Savings', ascending=False).head(10)
        k8s_cluster_savings['Savings %'] = (k8s_cluster_savings['Savings'] / k8s_cluster_savings['Actual'] * 100).round(2)
        
        col_chart_k8s1, col_chart_k8s2 = st.columns(2)
        
        with col_chart_k8s1:
            # Bar chart for Top 10 Clusters
            k8s_cluster_savings['Display Text'] = k8s_cluster_savings.apply(
                lambda row: f"${row['Savings']:,.0f}<br>({row['Savings %']:.1f}%)", axis=1
            )
            
            fig_k8s_clusters = px.bar(
                k8s_cluster_savings,
                x='Savings',
                y='Cluster',
                orientation='h',
                color='Savings',
                color_continuous_scale='Blues',
                text='Display Text',
                labels={'Savings': 'Savings (USD)', 'Cluster': 'Cluster Name'},
                title="Top 10 Clusters by Savings",
                hover_data=['Nodes', 'Actual', 'Estimated']
            )
            fig_k8s_clusters.update_traces(textposition='outside')
            fig_k8s_clusters.update_layout(height=500, showlegend=False, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_k8s_clusters, use_container_width=True)
        
        with col_chart_k8s2:
            # Table view
            st.markdown("#### Detailed Cluster Savings")
            st.dataframe(
                k8s_cluster_savings[['Cluster', 'Nodes', 'Actual', 'Estimated', 'Savings', 'Savings %']].style.format({
                    'Actual': '${:,.2f}',
                    'Estimated': '${:,.2f}',
                    'Savings': '${:,.2f}',
                    'Savings %': '{:.2f}%',
                    'Nodes': '{:.0f}'
                }),
                use_container_width=True,
                height=500
            )
        
        st.markdown("---")
        
        # 3. Kubernetes Top 3 Savings by Project (based on query 3)
        st.subheader("🎯 Kubernetes Top 3 Savings by Project")
        
        # Query equivalent: GROUP BY project_id, ORDER BY savings DESC, LIMIT 3
        k8s_project_savings = filtered_k8s_df.groupby('project_id').agg({
            'target_cost': 'sum',
            'current_cost': 'sum',
            'savings': 'sum',
            'cluster_name': 'count',
            'node_count': 'sum'
        }).reset_index()
        k8s_project_savings.columns = ['Project ID', 'Estimated', 'Actual', 'Savings', 'Clusters', 'Nodes']
        k8s_project_savings = k8s_project_savings.sort_values('Savings', ascending=False).head(3)
        k8s_project_savings['Savings %'] = (k8s_project_savings['Savings'] / k8s_project_savings['Actual'] * 100).round(2)
        
        col_chart_k8s3, col_chart_k8s4 = st.columns(2)
        
        with col_chart_k8s3:
            # Bar chart for Top 3 Projects
            k8s_project_savings['Display Text'] = k8s_project_savings.apply(
                lambda row: f"${row['Savings']:,.0f}<br>({row['Savings %']:.1f}%)", axis=1
            )
            
            fig_k8s_projects = px.bar(
                k8s_project_savings,
                x='Savings',
                y='Project ID',
                orientation='h',
                color='Savings',
                color_continuous_scale='Greens',
                text='Display Text',
                labels={'Savings': 'Savings (USD)', 'Project ID': 'Project ID'},
                title="Top 3 Projects by Savings",
                hover_data=['Clusters', 'Nodes', 'Actual', 'Estimated']
            )
            fig_k8s_projects.update_traces(textposition='outside')
            fig_k8s_projects.update_layout(height=400, showlegend=False, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_k8s_projects, use_container_width=True)
        
        with col_chart_k8s4:
            # Table view
            st.markdown("#### Detailed Project Savings")
            st.dataframe(
                k8s_project_savings[['Project ID', 'Clusters', 'Nodes', 'Actual', 'Estimated', 'Savings', 'Savings %']].style.format({
                    'Actual': '${:,.2f}',
                    'Estimated': '${:,.2f}',
                    'Savings': '${:,.2f}',
                    'Savings %': '{:.2f}%',
                    'Nodes': '{:.0f}'
                }),
                use_container_width=True,
                height=400
            )
        
        st.markdown("---")
        
        # Additional Kubernetes Analysis
        st.subheader("📈 Additional Kubernetes Analysis")
        
        # Cost Comparison Chart
        col_chart_k8s5, col_chart_k8s6 = st.columns(2)
        
        with col_chart_k8s5:
            st.markdown("### Kubernetes Cost Comparison")
            k8s_cost_comp = pd.DataFrame({
                'Cost Type': ['Current Cost', 'Target Cost', 'Savings'],
                'Amount': [k8s_total_current, k8s_total_target, k8s_total_savings],
                'Percentage': ['100%', f'{100-k8s_cost_reduction_pct:.1f}%', f'{k8s_savings_pct:.1f}%']
            })
            k8s_cost_comp['Display Text'] = k8s_cost_comp.apply(
                lambda row: f"${row['Amount']:,.0f}<br>({row['Percentage']})", axis=1
            )
            
            fig_k8s_cost = px.bar(
                k8s_cost_comp,
                x='Cost Type',
                y='Amount',
                color='Cost Type',
                color_discrete_map={
                    'Current Cost': '#ff4444',
                    'Target Cost': '#44ff44',
                    'Savings': '#4444ff'
                },
                text='Display Text',
                labels={'Amount': 'Cost (USD)', 'Cost Type': ''}
            )
            fig_k8s_cost.update_layout(
                showlegend=False,
                height=400,
                yaxis_title="Cost (USD)",
                title=f"Total Savings: {k8s_savings_pct:.2f}% (${k8s_total_savings:,.2f})"
            )
            fig_k8s_cost.update_traces(textposition='outside', textfont_size=10)
            st.plotly_chart(fig_k8s_cost, use_container_width=True)
        
        with col_chart_k8s6:
            st.markdown("### Kubernetes Savings by Region")
            k8s_region_savings = filtered_k8s_df.groupby('region').agg({
                'savings': 'sum',
                'current_cost': 'sum',
                'target_cost': 'sum',
                'cluster_name': 'nunique',
                'node_count': 'sum'
            }).reset_index()
            k8s_region_savings.columns = ['Region', 'Savings', 'Current Cost', 'Target Cost', 'Clusters', 'Nodes']
            k8s_region_savings['Savings %'] = (k8s_region_savings['Savings'] / k8s_region_savings['Current Cost'] * 100).round(1)
            k8s_region_savings = k8s_region_savings.sort_values('Savings', ascending=False)
            
            k8s_region_savings['Display Text'] = k8s_region_savings.apply(
                lambda row: f"${row['Savings']:,.0f}<br>({row['Savings %']:.1f}%)", axis=1
            )
            
            fig_k8s_region = px.bar(
                k8s_region_savings,
                x='Region',
                y='Savings',
                color='Savings',
                color_continuous_scale='Viridis',
                text='Display Text',
                labels={'Savings': 'Total Savings (USD)', 'Region': 'Region'},
                title="Savings by Region"
            )
            fig_k8s_region.update_traces(textposition='outside')
            fig_k8s_region.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_k8s_region, use_container_width=True)
        
        st.markdown("---")
        
        # Machine Type Analysis
        col_chart_k8s7, col_chart_k8s8 = st.columns(2)
        
        with col_chart_k8s7:
            st.markdown("### Current Machine Types - Cost Distribution")
            k8s_current_machine = filtered_k8s_df.groupby('current_machine_type').agg({
                'current_cost': 'sum',
                'savings': 'sum',
                'node_count': 'sum'
            }).reset_index().sort_values('current_cost', ascending=False).head(10)
            
            k8s_current_machine['Savings %'] = (k8s_current_machine['savings'] / k8s_current_machine['current_cost'] * 100).round(1)
            
            fig_k8s_current = px.bar(
                k8s_current_machine,
                x='current_machine_type',
                y='current_cost',
                color='savings',
                color_continuous_scale='Reds',
                text=[f"${x:,.0f}" for x in k8s_current_machine['current_cost']],
                labels={
                    'current_cost': 'Current Cost (USD)',
                    'current_machine_type': 'Current Machine Type',
                    'savings': 'Savings'
                },
                title="Top 10 Current Machine Types",
                hover_data=['node_count']
            )
            fig_k8s_current.update_traces(textposition='outside')
            fig_k8s_current.update_layout(height=400, showlegend=True, xaxis_tickangle=-45)
            st.plotly_chart(fig_k8s_current, use_container_width=True)
        
        with col_chart_k8s8:
            st.markdown("### Target Machine Types - Cost Distribution")
            k8s_target_machine = filtered_k8s_df.groupby('target_machine_type').agg({
                'target_cost': 'sum',
                'savings': 'sum',
                'node_count': 'sum'
            }).reset_index().sort_values('target_cost', ascending=False).head(10)
            
            k8s_target_machine['Savings %'] = (k8s_target_machine['savings'] / (k8s_target_machine['target_cost'] + k8s_target_machine['savings']) * 100).round(1)
            
            fig_k8s_target = px.bar(
                k8s_target_machine,
                x='target_machine_type',
                y='target_cost',
                color='savings',
                color_continuous_scale='Greens',
                text=[f"${x:,.0f}" for x in k8s_target_machine['target_cost']],
                labels={
                    'target_cost': 'Target Cost (USD)',
                    'target_machine_type': 'Target Machine Type',
                    'savings': 'Savings'
                },
                title="Top 10 Target Machine Types",
                hover_data=['node_count']
            )
            fig_k8s_target.update_traces(textposition='outside')
            fig_k8s_target.update_layout(height=400, showlegend=True, xaxis_tickangle=-45)
            st.plotly_chart(fig_k8s_target, use_container_width=True)
        
        st.markdown("---")
        
        # Node Count Analysis (Unique to Kubernetes)
        st.markdown("### 📊 Node Count Analysis")
        col_chart_k8s9, col_chart_k8s10 = st.columns(2)
        
        with col_chart_k8s9:
            st.markdown("#### Clusters by Node Count")
            k8s_node_dist = filtered_k8s_df.groupby('cluster_name').agg({
                'node_count': 'first',
                'savings': 'sum'
            }).reset_index()
            k8s_node_dist = k8s_node_dist.sort_values('node_count', ascending=False)
            
            fig_k8s_nodes = px.bar(
                k8s_node_dist.head(15),
                x='node_count',
                y='cluster_name',
                orientation='h',
                color='savings',
                color_continuous_scale='Purples',
                labels={
                    'node_count': 'Number of Nodes',
                    'cluster_name': 'Cluster Name',
                    'savings': 'Savings (USD)'
                },
                title="Top 15 Clusters by Node Count"
            )
            fig_k8s_nodes.update_layout(height=500, showlegend=True, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_k8s_nodes, use_container_width=True)
        
        with col_chart_k8s10:
            st.markdown("#### Average Nodes per Cluster by Project")
            k8s_project_nodes = filtered_k8s_df.groupby('project_id').agg({
                'node_count': 'mean',
                'cluster_name': 'count',
                'savings': 'sum'
            }).reset_index()
            k8s_project_nodes.columns = ['Project ID', 'Avg Nodes', 'Clusters', 'Savings']
            k8s_project_nodes = k8s_project_nodes.sort_values('Avg Nodes', ascending=False)
            
            fig_k8s_avg_nodes = px.bar(
                k8s_project_nodes,
                x='Avg Nodes',
                y='Project ID',
                orientation='h',
                color='Savings',
                color_continuous_scale='Oranges',
                labels={
                    'Avg Nodes': 'Average Nodes per Cluster',
                    'Project ID': 'Project ID',
                    'Savings': 'Total Savings (USD)'
                },
                title="Average Nodes per Cluster by Project",
                hover_data=['Clusters']
            )
            fig_k8s_avg_nodes.update_layout(height=500, showlegend=True, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_k8s_avg_nodes, use_container_width=True)
        
        st.markdown("---")
        
        # Detailed Summary Tables
        st.subheader("📋 Kubernetes Detailed Summary Tables")
        
        k8s_tab1, k8s_tab2, k8s_tab3 = st.tabs(["By Region", "By Machine Type", "By Cluster"])
        
        with k8s_tab1:
            k8s_region_summary = filtered_k8s_df.groupby('region').agg({
                'project_id': 'nunique',
                'cluster_name': 'nunique',
                'current_cost': 'sum',
                'target_cost': 'sum',
                'savings': 'sum',
                'node_count': 'sum'
            }).reset_index()
            k8s_region_summary.columns = ['Region', 'Projects', 'Clusters', 'Current Cost', 'Target Cost', 'Savings', 'Total Nodes']
            k8s_region_summary['Savings %'] = (k8s_region_summary['Savings'] / k8s_region_summary['Current Cost'] * 100).round(2)
            k8s_region_summary = k8s_region_summary.sort_values('Savings', ascending=False)
            st.dataframe(k8s_region_summary.style.format({
                'Current Cost': '${:,.2f}',
                'Target Cost': '${:,.2f}',
                'Savings': '${:,.2f}',
                'Savings %': '{:.1f}%',
                'Total Nodes': '{:.0f}'
            }), use_container_width=True)
        
        with k8s_tab2:
            k8s_machine_summary = filtered_k8s_df.groupby(['current_machine_type', 'target_machine_type']).agg({
                'cluster_name': 'count',
                'current_cost': 'sum',
                'target_cost': 'sum',
                'savings': 'sum',
                'node_count': 'sum'
            }).reset_index()
            k8s_machine_summary.columns = ['Current Machine', 'Target Machine', 'Clusters', 'Current Cost', 'Target Cost', 'Savings', 'Total Nodes']
            k8s_machine_summary['Savings %'] = (k8s_machine_summary['Savings'] / k8s_machine_summary['Current Cost'] * 100).round(2)
            k8s_machine_summary = k8s_machine_summary.sort_values('Savings', ascending=False)
            st.dataframe(k8s_machine_summary.style.format({
                'Current Cost': '${:,.2f}',
                'Target Cost': '${:,.2f}',
                'Savings': '${:,.2f}',
                'Savings %': '{:.1f}%',
                'Total Nodes': '{:.0f}'
            }), use_container_width=True)
        
        with k8s_tab3:
            k8s_cluster_summary = filtered_k8s_df.groupby(['cluster_name', 'project_id']).agg({
                'current_cost': 'sum',
                'target_cost': 'sum',
                'savings': 'sum',
                'current_machine_type': 'first',
                'target_machine_type': 'first',
                'node_count': 'first'
            }).reset_index()
            k8s_cluster_summary.columns = ['Cluster', 'Project ID', 'Current Cost', 'Target Cost', 'Savings', 'Current Machine', 'Target Machine', 'Nodes']
            k8s_cluster_summary['Savings %'] = (k8s_cluster_summary['Savings'] / k8s_cluster_summary['Current Cost'] * 100).round(2)
            k8s_cluster_summary = k8s_cluster_summary.sort_values('Savings', ascending=False)
            st.dataframe(k8s_cluster_summary.style.format({
                'Current Cost': '${:,.2f}',
                'Target Cost': '${:,.2f}',
                'Savings': '${:,.2f}',
                'Savings %': '{:.1f}%',
                'Nodes': '{:.0f}'
            }), use_container_width=True)
        
        st.markdown("---")
        
        # Key Insights
        st.markdown("### 💡 Kubernetes Key Insights")
        insights_k8s_col1, insights_k8s_col2 = st.columns(2)
        
        with insights_k8s_col1:
            k8s_annual_savings = k8s_total_savings * 12
            avg_nodes_per_cluster = k8s_total_nodes / k8s_num_clusters if k8s_num_clusters > 0 else 0
            st.info(f"""
            **💵 Kubernetes Cost Impact:**
            - **Current Spending:** ${k8s_total_current:,.2f}/month (100%)
            - **Target Cost:** ${k8s_total_target:,.2f}/month ({100-k8s_cost_reduction_pct:.1f}% of current)
            - **Monthly Savings:** ${k8s_total_savings:,.2f} ({k8s_savings_pct:.2f}% reduction)
            - **Annual Savings Projection:** ${k8s_annual_savings:,.2f}
            
            **📊 Scale:**
            - Total clusters analyzed: **{k8s_num_clusters}**
            - Total projects: **{k8s_num_projects}**
            - Total nodes: **{int(k8s_total_nodes)}**
            - Average nodes per cluster: **{avg_nodes_per_cluster:.1f}**
            """)
        
        with insights_k8s_col2:
            if len(k8s_cluster_savings) > 0:
                top_cluster_k8s = k8s_cluster_savings.iloc[0]
                top_project_k8s = k8s_project_savings.iloc[0] if len(k8s_project_savings) > 0 else None
                
                top_cluster_k8s_text = f"- Top saving cluster: **{top_cluster_k8s['Cluster']}** (${top_cluster_k8s['Savings']:,.2f}, {top_cluster_k8s['Savings %']:.1f}%)\n"
                top_project_k8s_text = f"- Top saving project: **{top_project_k8s['Project ID']}** (${top_project_k8s['Savings']:,.2f}, {top_project_k8s['Savings %']:.1f}%)\n" if top_project_k8s is not None else ""
                
                avg_savings_per_node = k8s_total_savings / k8s_total_nodes if k8s_total_nodes > 0 else 0
                node_text = f"- Average savings per node: **${avg_savings_per_node:,.2f}**\n" if k8s_total_nodes > 0 else ""
                
                st.info(f"""
                **🎯 Top Opportunities:**
                {top_cluster_k8s_text}{top_project_k8s_text}
                - **Cost Reduction:** Reduce Kubernetes costs by **{k8s_cost_reduction_pct:.2f}%** while maintaining performance
                - Average savings per cluster: **${k8s_total_savings/k8s_num_clusters:,.2f}**
                {node_text}
                """)
    
    else:
        st.error("Unable to load Kubernetes data. Please check if Kubernetes data exists and is properly formatted.")

# ==================== OVERVIEW VIEW ====================
if active_tab == 'Overview':
    if overview_df is not None and not overview_df.empty:
        # Get filter values from session state
        selected_service_ov = st.session_state.get('overview_service', 'All')
        selected_project_ov = st.session_state.get('overview_project', 'All')
        
        # Apply filters
        filtered_ov_df = overview_df.copy()
        
        if selected_service_ov != 'All':
            filtered_ov_df = filtered_ov_df[filtered_ov_df['service'] == selected_service_ov]
        if selected_project_ov != 'All':
            filtered_ov_df = filtered_ov_df[filtered_ov_df['project_id'] == selected_project_ov]
        
        # Overall Summary Metrics
        total_estimated = filtered_ov_df['Estimated'].sum()
        total_actual = filtered_ov_df['Actual'].sum()
        total_savings = filtered_ov_df['Savings'].sum()
        savings_pct = (total_savings / total_actual * 100) if total_actual > 0 else 0
        cost_reduction_pct = ((total_actual - total_estimated) / total_actual * 100) if total_actual > 0 else 0
        num_services = filtered_ov_df['service'].nunique()
        num_projects = filtered_ov_df['project_id'].nunique()
        num_entries = len(filtered_ov_df)
        
        # 1. Overall Summary
        st.subheader("📊 Overall Summary")
        
        col_ov1, col_ov2, col_ov3, col_ov4, col_ov5, col_ov6 = st.columns(6)
        
        with col_ov1:
            st.metric(
                label="Total Actual Cost",
                value=f"${total_actual:,.2f}",
                delta="100% of spending"
            )
        
        with col_ov2:
            st.metric(
                label="Total Estimated Cost",
                value=f"${total_estimated:,.2f}",
                delta=f"-{cost_reduction_pct:.2f}% reduction"
            )
        
        with col_ov3:
            st.metric(
                label="Total Savings",
                value=f"${total_savings:,.2f}",
                delta=f"{savings_pct:.2f}% savings"
            )
        
        with col_ov4:
            st.metric(
                label="Number of Services",
                value=num_services
            )
        
        with col_ov5:
            st.metric(
                label="Number of Projects",
                value=num_projects
            )
        
        with col_ov6:
            st.metric(
                label="Total Entries",
                value=num_entries
            )
        
        st.markdown("---")
        
        # 2. Service vs Cost Analysis
        st.subheader("📈 Service vs Cost Analysis")
        
        # Aggregate by service
        service_analysis = filtered_ov_df.groupby('service').agg({
            'Estimated': 'sum',
            'Actual': 'sum',
            'Savings': 'sum',
            'project_id': 'nunique'
        }).reset_index()
        service_analysis.columns = ['Service', 'Estimated', 'Actual', 'Savings', 'Projects']
        service_analysis['Savings %'] = (service_analysis['Savings'] / service_analysis['Actual'] * 100).round(2)
        service_analysis = service_analysis.sort_values('Actual', ascending=False)
        
        col_chart_ov1, col_chart_ov2 = st.columns(2)
        
        with col_chart_ov1:
            st.markdown("### Service Cost Comparison")
            service_analysis['Display Text'] = service_analysis.apply(
                lambda row: f"${row['Actual']:,.0f}<br>Savings: ${row['Savings']:,.0f}", axis=1
            )
            
            fig_service_cost = px.bar(
                service_analysis,
                x='Service',
                y='Actual',
                color='Savings',
                color_continuous_scale='Blues',
                text='Display Text',
                labels={'Actual': 'Actual Cost (USD)', 'Service': 'Service'},
                title="Actual Cost by Service",
                hover_data=['Estimated', 'Savings', 'Projects']
            )
            fig_service_cost.update_traces(textposition='outside')
            fig_service_cost.update_layout(height=500, showlegend=True)
            st.plotly_chart(fig_service_cost, use_container_width=True)
        
        with col_chart_ov2:
            st.markdown("### Service Savings Analysis")
            service_analysis['Savings Display'] = service_analysis.apply(
                lambda row: f"${row['Savings']:,.0f}<br>({row['Savings %']:.1f}%)", axis=1
            )
            
            fig_service_savings = px.bar(
                service_analysis,
                x='Service',
                y='Savings',
                color='Savings %',
                color_continuous_scale='Greens',
                text='Savings Display',
                labels={'Savings': 'Savings (USD)', 'Service': 'Service'},
                title="Total Savings by Service",
                hover_data=['Actual', 'Estimated', 'Projects']
            )
            fig_service_savings.update_traces(textposition='outside')
            fig_service_savings.update_layout(height=500, showlegend=True)
            st.plotly_chart(fig_service_savings, use_container_width=True)
        
        st.markdown("---")
        
        # 3. Project vs Cost Analysis
        st.subheader("🏢 Project vs Cost Analysis")
        
        # Aggregate by project
        project_analysis = filtered_ov_df.groupby('project_id').agg({
            'Estimated': 'sum',
            'Actual': 'sum',
            'Savings': 'sum',
            'service': lambda x: ', '.join(sorted(x.unique()))
        }).reset_index()
        project_analysis.columns = ['Project ID', 'Estimated', 'Actual', 'Savings', 'Services']
        project_analysis['Savings %'] = (project_analysis['Savings'] / project_analysis['Actual'] * 100).round(2)
        project_analysis = project_analysis.sort_values('Actual', ascending=False)
        
        col_chart_ov3, col_chart_ov4 = st.columns(2)
        
        with col_chart_ov3:
            st.markdown("### Top Projects by Actual Cost")
            top_projects_cost = project_analysis.head(15).copy()
            top_projects_cost['Display Text'] = top_projects_cost.apply(
                lambda row: f"${row['Actual']:,.0f}<br>Savings: ${row['Savings']:,.0f}", axis=1
            )
            
            fig_project_cost = px.bar(
                top_projects_cost,
                x='Actual',
                y='Project ID',
                orientation='h',
                color='Savings',
                color_continuous_scale='Reds',
                text='Display Text',
                labels={'Actual': 'Actual Cost (USD)', 'Project ID': 'Project ID'},
                title="Top 15 Projects by Actual Cost",
                hover_data=['Estimated', 'Savings', 'Services']
            )
            fig_project_cost.update_traces(textposition='outside')
            fig_project_cost.update_layout(height=600, showlegend=True, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_project_cost, use_container_width=True)
        
        with col_chart_ov4:
            st.markdown("### Top Projects by Savings")
            top_projects_savings = project_analysis.sort_values('Savings', ascending=False).head(15).copy()
            top_projects_savings['Savings Display'] = top_projects_savings.apply(
                lambda row: f"${row['Savings']:,.0f}<br>({row['Savings %']:.1f}%)", axis=1
            )
            
            fig_project_savings = px.bar(
                top_projects_savings,
                x='Savings',
                y='Project ID',
                orientation='h',
                color='Savings %',
                color_continuous_scale='Purples',
                text='Savings Display',
                labels={'Savings': 'Savings (USD)', 'Project ID': 'Project ID'},
                title="Top 15 Projects by Savings",
                hover_data=['Actual', 'Estimated', 'Services']
            )
            fig_project_savings.update_traces(textposition='outside')
            fig_project_savings.update_layout(height=600, showlegend=True, yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_project_savings, use_container_width=True)
        
        st.markdown("---")
        
        # 4. Service (X-axis) vs Cost & Project (X-axis) vs Cost
        st.subheader("📊 Service vs Cost & Project vs Cost")
        
        col_chart_ov7, col_chart_ov8 = st.columns(2)
        
        with col_chart_ov7:
            st.markdown("### Service (X-axis) - Cost")
            service_x_cost = service_analysis.sort_values('Actual', ascending=True).copy()
            service_x_cost['Display Text'] = service_x_cost.apply(
                lambda row: f"${row['Actual']:,.0f}", axis=1
            )
            
            fig_service_x = px.bar(
                service_x_cost,
                x='Service',
                y='Actual',
                color='Actual',
                color_continuous_scale='Blues',
                text='Display Text',
                labels={'Actual': 'Cost (USD)', 'Service': 'Service'},
                title="Cost by Service (Service on X-axis)",
                hover_data=['Estimated', 'Savings', 'Savings %']
            )
            fig_service_x.update_traces(textposition='outside')
            fig_service_x.update_layout(height=500, showlegend=False, xaxis_tickangle=-45 if len(service_x_cost) > 3 else 0)
            st.plotly_chart(fig_service_x, use_container_width=True)
        
        with col_chart_ov8:
            st.markdown("### Project (X-axis) - Cost")
            # Show top projects for readability (can adjust number)
            project_x_cost = project_analysis.sort_values('Actual', ascending=False).head(20).sort_values('Actual', ascending=True).copy()
            project_x_cost['Display Text'] = project_x_cost.apply(
                lambda row: f"${row['Actual']:,.0f}", axis=1
            )
            
            fig_project_x = px.bar(
                project_x_cost,
                x='Project ID',
                y='Actual',
                color='Actual',
                color_continuous_scale='Reds',
                text='Display Text',
                labels={'Actual': 'Cost (USD)', 'Project ID': 'Project ID'},
                title="Cost by Project (Top 20 Projects, Project on X-axis)",
                hover_data=['Estimated', 'Savings', 'Services']
            )
            fig_project_x.update_traces(textposition='outside')
            fig_project_x.update_layout(height=500, showlegend=False, xaxis_tickangle=-90)
            st.plotly_chart(fig_project_x, use_container_width=True)
        
        st.markdown("---")
        
        # 5. Service Breakdown by Project
        st.subheader("🔍 Service Breakdown by Project")
        
        # Cost comparison chart - Actual vs Estimated by Service
        col_chart_ov5, col_chart_ov6 = st.columns(2)
        
        with col_chart_ov5:
            st.markdown("### Actual vs Estimated Cost by Service")
            service_cost_melted = service_analysis.melt(
                id_vars='Service',
                value_vars=['Actual', 'Estimated'],
                var_name='Cost Type',
                value_name='Cost'
            )
            
            fig_service_compare = px.bar(
                service_cost_melted,
                x='Service',
                y='Cost',
                color='Cost Type',
                barmode='group',
                color_discrete_map={
                    'Actual': '#ff4444',
                    'Estimated': '#44ff44'
                },
                labels={'Cost': 'Cost (USD)', 'Service': 'Service'},
                title="Actual vs Estimated Cost by Service"
            )
            fig_service_compare.update_layout(height=500, showlegend=True)
            st.plotly_chart(fig_service_compare, use_container_width=True)
        
        with col_chart_ov6:
            st.markdown("### Savings Distribution by Service")
            fig_savings_dist = px.pie(
                service_analysis,
                values='Savings',
                names='Service',
                title="Savings Distribution by Service",
                hover_data=['Actual', 'Estimated']
            )
            fig_savings_dist.update_traces(textposition='inside', textinfo='percent+label')
            fig_savings_dist.update_layout(height=500)
            st.plotly_chart(fig_savings_dist, use_container_width=True)
        
        st.markdown("---")
        
        # 6. Detailed Summary Tables
        st.subheader("📋 Detailed Summary Tables")
        
        ov_tab1, ov_tab2, ov_tab3 = st.tabs(["By Service", "By Project", "Full Data"])
        
        with ov_tab1:
            st.markdown("#### Service Level Summary")
            service_summary_display = service_analysis[['Service', 'Projects', 'Actual', 'Estimated', 'Savings', 'Savings %']].copy()
            service_summary_display = service_summary_display.sort_values('Actual', ascending=False)
            st.dataframe(
                service_summary_display.style.format({
                    'Actual': '${:,.2f}',
                    'Estimated': '${:,.2f}',
                    'Savings': '${:,.2f}',
                    'Savings %': '{:.2f}%'
                }),
                use_container_width=True,
                height=400
            )
        
        with ov_tab2:
            st.markdown("#### Project Level Summary")
            project_summary_display = project_analysis[['Project ID', 'Services', 'Actual', 'Estimated', 'Savings', 'Savings %']].copy()
            project_summary_display = project_summary_display.sort_values('Actual', ascending=False)
            st.dataframe(
                project_summary_display.style.format({
                    'Actual': '${:,.2f}',
                    'Estimated': '${:,.2f}',
                    'Savings': '${:,.2f}',
                    'Savings %': '{:.2f}%'
                }),
                use_container_width=True,
                height=400
            )
        
        with ov_tab3:
            st.markdown("#### Full Data View")
            filtered_display = filtered_ov_df[['service', 'project_id', 'Actual', 'Estimated', 'Savings']].copy()
            filtered_display.columns = ['Service', 'Project ID', 'Actual', 'Estimated', 'Savings']
            filtered_display['Savings %'] = (filtered_display['Savings'] / filtered_display['Actual'] * 100).round(2)
            filtered_display = filtered_display.sort_values('Actual', ascending=False)
            st.dataframe(
                filtered_display.style.format({
                    'Actual': '${:,.2f}',
                    'Estimated': '${:,.2f}',
                    'Savings': '${:,.2f}',
                    'Savings %': '{:.2f}%'
                }),
                use_container_width=True,
                height=400
            )
        
        st.markdown("---")
        
        # 7. Key Insights
        st.subheader("💡 Key Insights")
        insights_ov_col1, insights_ov_col2 = st.columns(2)
        
        with insights_ov_col1:
            annual_savings = total_savings * 12
            top_service = service_analysis.iloc[0] if len(service_analysis) > 0 else None
            top_service_text = f"- Highest cost service: **{top_service['Service']}** (${top_service['Actual']:,.2f}, {top_service['Savings %']:.2f}% savings)\n" if top_service is not None else ""
            
            st.info(f"""
            **💵 Overall Cost Impact:**
            - **Total Current Spending:** ${total_actual:,.2f}/month (100%)
            - **Total Estimated Cost:** ${total_estimated:,.2f}/month ({100-cost_reduction_pct:.1f}% of current)
            - **Total Monthly Savings:** ${total_savings:,.2f} ({savings_pct:.2f}% reduction)
            - **Annual Savings Projection:** ${annual_savings:,.2f}
            
            **📊 Coverage:**
            - Services analyzed: **{num_services}** ({', '.join(sorted(filtered_ov_df['service'].unique()))})
            - Projects analyzed: **{num_projects}**
            - Total entries: **{num_entries}**
            """)
        
        with insights_ov_col2:
            top_project = project_analysis.iloc[0] if len(project_analysis) > 0 else None
            top_project_text = f"- Highest cost project: **{top_project['Project ID']}** (${top_project['Actual']:,.2f}, {top_project['Savings']:,.2f} savings)\n" if top_project is not None else ""
            
            top_savings_service = service_analysis.sort_values('Savings', ascending=False).iloc[0] if len(service_analysis) > 0 else None
            top_savings_service_text = f"- Top saving service: **{top_savings_service['Service']}** (${top_savings_service['Savings']:,.2f})\n" if top_savings_service is not None else ""
            
            avg_savings_per_service = total_savings / num_services if num_services > 0 else 0
            avg_savings_per_project = total_savings / num_projects if num_projects > 0 else 0
            
            st.info(f"""
            **🎯 Key Highlights:**
            {top_service_text}{top_project_text}{top_savings_service_text}
            - **Cost Reduction Potential:** Reduce costs by **{cost_reduction_pct:.2f}%** across all services
            - Average savings per service: **${avg_savings_per_service:,.2f}**
            - Average savings per project: **${avg_savings_per_project:,.2f}**
            """)
        
        st.markdown("---")
        
        # 8. Additional Analysis: Service-Project Matrix
        st.subheader("🔬 Service-Project Cost Matrix")
        
        # Create a pivot table for service vs project
        service_project_matrix = filtered_ov_df.pivot_table(
            index='service',
            columns='project_id',
            values='Actual',
            aggfunc='sum',
            fill_value=0
        )
        
        # Create heatmap
        fig_heatmap = px.imshow(
            service_project_matrix,
            labels=dict(x="Project ID", y="Service", color="Cost (USD)"),
            title="Cost Heatmap: Service vs Project",
            color_continuous_scale='YlOrRd',
            aspect="auto"
        )
        fig_heatmap.update_layout(height=600)
        st.plotly_chart(fig_heatmap, use_container_width=True)
        
        # Display matrix table
        st.markdown("#### Service-Project Cost Matrix Table")
        st.dataframe(
            service_project_matrix.style.format('${:,.2f}'),
            use_container_width=True,
            height=400
        )
    
    else:
        st.error("Unable to load Overview data. Please check if Overview data exists and is properly formatted.")
