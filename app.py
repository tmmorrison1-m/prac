



#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:





# In[1]:


import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# In[2]:


from datetime import datetime


# In[3]:


df1 = pd.read_csv('practice_data1.csv')


# In[4]:


df2 = pd.read_json('practice_data2.json')


# In[5]:


format_string = '%Y-%m-%d'




# In[6]:


df1['date2'] = df1.date.map(lambda x:datetime.strptime(x,format_string))


# In[7]:


df1.date = df1.date2


# In[ ]:





# In[8]:


df_merge = pd.merge(df2.groupby('date')['spend'].sum().reset_index(),df1.groupby('date')['revenue'].sum().reset_index(),how='left',on='date').fillna(0,inplace=False)


# In[9]:


df_merge['profit'] = df_merge.revenue - df_merge.spend


# In[10]:


df_merge['ROAS'] = df_merge.revenue/df_merge.spend


# In[14]:


df_final = df_merge


# In[12]:

def main():
    # 1. PAGE TITLE
    st.title("Executive Marketing Dashboard")


    # In[15]:


    # 2. KPI ROW
    # Calculate totals
    total_rev = df_final['revenue'].sum()
    total_spend = df_final['spend'].sum()
    avg_roas = total_rev / total_spend if total_spend > 0 else 0

    # Create columns for the cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Revenue", f"${total_rev:,.0f}")
    col2.metric("Total Spend", f"${total_spend:,.0f}")
    col3.metric("Aggregate ROAS", f"{avg_roas:.2f}x")


    # In[16]:


    # 3. THE "TREND" CHART (Dual Axis)
    st.subheader("Revenue vs. Spend Trends")

    # We use Plotly Graph Objects for custom dual-axis charts
    fig = go.Figure()

    # Bar for Revenue
    fig.add_trace(go.Bar(
        x=df_final['date'], 
        y=df_final['revenue'], 
        name='Revenue',
        marker_color='lightgreen'
    ))

    # Bar for Spend
    fig.add_trace(go.Bar(
        x=df_final['date'], 
        y=df_final['spend'], 
        name='Spend',
        marker_color='indianred'
    ))

    # Line for ROAS (on secondary Y-axis)
    fig.add_trace(go.Scatter(
        x=df_final['date'], 
        y=df_final['ROAS'], 
        name='ROAS',
        yaxis='y2',
        line=dict(color='blue', width=3)
    ))

    # Layout for dual axis
    fig.update_layout(
        yaxis=dict(title="Dollars ($)"),
        yaxis2=dict(title="ROAS Multiplier", overlaying='y', side='right'),
        legend=dict(x=0, y=1.2, orientation='h') # Legend on top
    )

    st.plotly_chart(fig, use_container_width=True)


    # In[17]:


    # 4. RAW DATA (Trust but verify)
    with st.expander("View Raw Data Source"):
        st.dataframe(df_final)


    # In[ ]:










if __name__ == '__main__':
    main()
