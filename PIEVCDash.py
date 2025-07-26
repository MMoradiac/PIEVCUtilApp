import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash_cytoscape as cyto
import dash_auth
import copy
import random

#-----------------------------------------------------------------------------------------------------------------------
# Import Data
## Infrastructure Classification
InfraClassification_df = pd.read_csv('data/InfraClassification_df.csv')
## Project Team
ProjectTeam_df = pd.read_csv('data/ProjectTeam_df.csv',encoding='latin1')
## Studies Overview
StudiesOverview_df = pd.read_csv('data/StudiesOverview_df.csv',encoding='latin1')
## Risk Profile
RiskProfile_df = pd.read_csv('data/RiskProfile_df.csv')
## ClimateDataInfras
ClimateDataInfras_df = pd.read_csv('data/ClimateDataInfras_df.csv')

ClimateData_df = pd.read_csv('data/ClimateData_df.csv',encoding='latin1')
## Recommendation
Recommendation_df = pd.read_csv('data/Recommendation_df.csv')


# Infrastructure classification sunburst plot
InfraClassification_df_sb = copy.copy(InfraClassification_df)
InfraClassification_df_sb.replace(to_replace="NAN", value=np.nan, inplace=True)
sb = px.sunburst(InfraClassification_df_sb, path=['Infrastructure Layer 1', 'Infrastructure Layer 2', 'Components'],custom_data=['Infrastructure Layer 1', 'Infrastructure Layer 2'])
sb.update_layout(margin={'l': 0, 'r': 0, 'b': 0, 't': 0},paper_bgcolor='rgba(0,0,0,0)')
sb.update_traces(hovertemplate='<b>Infrastructure Type: %{customdata[0]} <br> Label: %{label}',branchvalues='total', selector=dict(type='sunburst'))
sb.update_traces(insidetextorientation='radial', selector=dict(type='sunburst'))

FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"

#-----------------------------------------------------------------------------------------------------------------------
# Start App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP,FONT_AWESOME])
server = app.server
app.title = 'PIEVCAnalysis'
#-----------------------------------------------------------------------------------------------------------------------
# App Style
# styling the sidebar
SIDEBAR_STYLE = {
    "overflow": "auto",
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "24rem",
    "padding": "2rem 1rem",
    "background-color": "#DEFFD2",
}

# padding for the page content
CONTENT_STYLE = {
    "margin-left": "20rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    'display': 'flex'
}

tab_style_sidebar = {
    'borderBottom': '1px solid #287F06',
    'borderTop': '1px solid #287F06',
    'borderLeft': '1px solid #287F06',
    'borderRight': '1px solid #287F06',
    'padding': '6px',
    'backgroundColor': '#DEFFD2',
    'font-size': '12px'
}

tab_selected_style_sidebar = {
    'borderTop': '1px solid #287F06',
    'borderBottom': '1px solid #287F06',
    'backgroundColor': '#4B9072',
    'color': 'white',
    'padding': '6px',
    'font-size': '12px'
}

sidebar = html.Div(
    [
        html.H1("PIEVC Report Analysis Utility", className="display-4"),
        html.P('BETA',style={"margin-left": "280px",'color': 'red',"font-family":"Trebuchet MS"}),
        html.Hr(),
        html.Label(["This utility allows users to explore findings for all PIEVC assessment reports submitted to the PIEVC Program from January 2016 to August 2021. The Utility was designed to increase accessibility of findings in PIEVC Protocol assessment reports available at ",dcc.Link('www.pievc.ca',href='https://pievc.ca')]),
        html.Img(src=app.get_asset_url('Logo.png'),style={'margin-left':'50px'}),
        html.P(['If you have any questions or comments about this utility, please contact ',html.A('pievc@iclr.org', href='mailto:pievc@iclr.org'), ' and include ', html.Q('PIEVC Utility'),' as the subject.'], style={'font-size': '12px', 'color': 'red', "font-family": "Trebuchet MS"}),
        html.Div([
                dcc.Tabs(children=[
                        dcc.Tab(label='Author',
                                children=[
                                    html.Label('The Utility was created by Mohsen Moradi, under the guidance of Prof. Andrew Binns, of the University of Guelph’s School of Engineering, and was funded by the Institute for Catastrophic Loss Reduction.',style={'font-size': '12px'}),
                                ],style=tab_style_sidebar,selected_style=tab_selected_style_sidebar
                                ),
                        dcc.Tab(label='Contact Us',
                                children=[
                                    html.Label(['If you have any questions or comments about this utility, please contact ', html.A('pievc@iclr.org',href='mailto:pievc@iclr.org'), ' and include ', html.Q('PIEVC Utility'), ' as the subject.'],style={'font-size': '12px'}),
                                ],style=tab_style_sidebar,selected_style=tab_selected_style_sidebar
                                ),
                        dcc.Tab(label='How to Cite',
                                children=[
                                    html.Label('How to cite: Moradi, M., Binns, A., Sandink, D., Lapp, D., 2021. PIEVC Report Analysis Utility v1. Toronto/Ottawa: PIEVC Program',style={'font-size': '12px'}),
                                ],style=tab_style_sidebar,selected_style=tab_selected_style_sidebar
                                )
                ],style={'height': '30px'}
                )
            ])
    ],
    style=SIDEBAR_STYLE,
)

drop_opt = [{'label':study_id,'value':study_id} for study_id in ProjectTeam_df['Study'].unique().tolist()]
drop_Study = dcc.Dropdown(id='drop_Study',clearable=False,searchable=False,options=drop_opt,value=drop_opt[0]['value'],style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_province = dcc.Dropdown(id='opt_province',clearable=False,searchable=False,multi=True,style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_study_multi = dcc.Dropdown(id='opt_infra_province_study',clearable=False,searchable=False,multi=True,style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_study_threshold = dcc.Dropdown(id='opt_study_threshold',clearable=False,searchable=False,style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_study_sunburstRisk1 = dcc.Dropdown(id='opt_study_sunburstRisk1',clearable=False,searchable=False,style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_study_sunburstRisk2 = dcc.Dropdown(id='opt_study_sunburstRisk2',clearable=False,searchable=False,style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_location_sunburstRisk1 = dcc.Dropdown(id='opt_location_sunburstRisk1',clearable=False,searchable=False,style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_location_sunburstRisk2 = dcc.Dropdown(id='opt_location_sunburstRisk2',clearable=False,searchable=False,style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_risklevel_sunburstRisk1 = dcc.Dropdown(id='opt_risklevel_sunburstRisk1',clearable=False,searchable=False,options=[{'label':'High','value':'High'},{'label':'Medium','value':'Medium'}], value='High', style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_risklevel_sunburstRisk2 = dcc.Dropdown(id='opt_risklevel_sunburstRisk2',clearable=False,searchable=False,options=[{'label':'High','value':'High'},{'label':'Medium','value':'Medium'}], value='High',style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_opt_timehorizon_sunburstRisk1 = [{'label':'Current','value':'Current'},{'label':'Short Term','value':'Short Term'},{'label':'Medium Term','value':'Medium Term'},{'label':'Long Term','value':'Long Term'}]
drop_timehorizon_sunburstRisk1 = dcc.Dropdown(id='opt_timehorizon_sunburstRisk1',clearable=False,searchable=False,options=drop_opt_timehorizon_sunburstRisk1, value=drop_opt_timehorizon_sunburstRisk1[0]['value'], style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_timehorizon_sunburstRisk2 = dcc.Dropdown(id='opt_timehorizon_sunburstRisk2',clearable=False,searchable=False,options=drop_opt_timehorizon_sunburstRisk1, value=drop_opt_timehorizon_sunburstRisk1[0]['value'], style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})

drop_opt_infra = [{'label':i,'value':i} for i in InfraClassification_df['Infrastructure Layer 1'].unique().tolist()]
drop_InfraClass_multi = dcc.Dropdown(id='drop_InfraClass_multi',clearable=False,searchable=False,options=drop_opt_infra,value='Buildings',multi=True,style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a'})
drop_InfraClass_single = dcc.Dropdown(id='drop_InfraClass_single',clearable=False,searchable=False,options=drop_opt_infra,value='Coastal Infrastructure',style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a','margin-right':'-80px'})
drop_InfraClass_comp_init = InfraClassification_df[InfraClassification_df['Infrastructure Layer 1']=='Coastal Infrastructure']['Infrastructure Layer 2'].unique().tolist()[0]
drop_InfraClass_comp = dcc.Dropdown(id='opt_InfraClass_comp',clearable=False,searchable=False,value=drop_InfraClass_comp_init,style={'margin': '4px', 'box-shadow': '0px 0px #ebb36a', 'border-color': '#ebb36a','margin-right':'-80px'})

tab_style = {
    'borderBottom': '1px solid #d3a15f',
    'borderTop': '1px solid #d3a15f',
    'borderLeft': '1px solid #d3a15f',
    'borderRight': '1px solid #d3a15f',
    'padding': '6px',
    'fontWeight': 'bold',
    'backgroundColor': '#F2F2F2'
}

tab_selected_style = {
    'borderTop': '1px solid #d3a15f',
    'borderBottom': '1px solid #d3a15f',
    'backgroundColor': '#ebb36a',
    'color': 'white',
    'padding': '6px'
}

#-----------------------------------------------------------------------------------------------------------------------
# App Layout
app.layout = html.Div([
    sidebar,
    html.Div([
        html.Div([
        # <Box 1>: Infrastructure classification sunburst & Description
        html.Div([
            html.Div([
                html.Div([
                    html.H3([
                        'Infrastructure Classification ',
                        html.I(className="fas fa-info-circle fa-lg", id="target-sb",style={'font-size':'20px'})],style={'padding-left': '15px'}),
                    dbc.Tooltip("Click on it to know more!", target="target-sb"),
                    html.Hr(style={'margin-right': '6rem','margin-left': '0.8rem'}),
                    dcc.Graph(figure=sb,config={'responsive': True},style={'height': '500px','maxHeight': '500px','overflow': 'hidden'}),
                ],style={'width':'55%'}),
                html.Div([
                    html.Div([
                        html.H3('Description of Infrastructure'),
                        html.Hr(style={'margin-right': '2rem'}),
                        html.P('Infrastructure:'),
                    ],style={'width':'100%','margin-bottom':'-15px'}),
                    html.Div([
                        drop_InfraClass_single
                    ],style={'width':'80%','margin-left': '-0.7rem','margin-bottom':'10px'}),
                    html.Div([
                        html.P('Component:')
                    ],style={'margin-bottom':'-15px'}),
                    html.Div([
                        drop_InfraClass_comp
                    ],style={'width':'80%','margin-left': '-0.7rem','margin-bottom':'15px'}),
                    html.Div([
                        dcc.Tabs(children=[
                                dcc.Tab(label='Description',
                                        children=[
                                            dcc.Loading(id='DescripTab',color='#4B9072',type="circle")
                                        ],style=tab_style,selected_style=tab_selected_style
                                        ),
                                dcc.Tab(label='Studies',
                                        children=[
                                            html.P(['This section provides list of studies that assessed infrastructure selected above. ',html.I(className="fas fa-info-circle fa-lg", id="target-infradescrip",style={'font-size':'15px'})]),
                                            dbc.Tooltip("Please scroll down to see all studies!", target="target-infradescrip"),
                                            html.Hr(style={'margin-right': '2rem'}),
                                            dcc.Loading(id='StudiesTab',color='#4B9072',type="circle"),
                                            html.Hr(style={'margin-right': '2rem'}),
                                            html.P('Studies are coded based on the consulting company, year, province, and location as below:',style={'font-size':'12px'}),
                                            dcc.Markdown('_**Company (Year) (Province) (Location)**_',style={'font-size':'12px'})
                                        ],style=tab_style,selected_style=tab_selected_style
                                        )
                        ],style={'margin-right': '30px','height': '44px'}
                        )
                    ])
                ],style={'width':'45%'})
            ],className='row')
        ],className='box',style={'margin-right': '-0.8rem','margin-left': '-1rem','margin-bottom': '1rem','margin-top': '1rem','padding-left':'15px', 'padding-top':'15px', 'padding-bottom':'15px','backgroundColor':'#111111','border-radius': '15px','background-color': '#F2F2F2'}),
        # <Box 2>: Overview table
        html.Div([
            html.Div([
                html.H3('Overview Table'),
                html.Hr(),
                html.P(['An overview of PIEVC studies included in this utility is provided here. ',
                        html.I(className="fas fa-info-circle fa-lg", id="target-overviewTable",style={'font-size':'15px'})]),
                dbc.Tooltip("Scroll down in the table to know more!", target="target-overviewTable")
            ]),
            html.Div([
                dcc.Graph(id='table_Overview')
            ]),
            html.Div([
                dcc.Markdown("***** **AI**:(Airport Infrastructure), **Br**:(Bridges), **Bu**:(Buildings), **CI**:(Coastal Infrastructures), **E**:(Electrical), **M**: (Mechanical), **F**: (Fuel), "
                             "**PW**:(Portable Water), **RLNBI**:(Recreational Lands and Nature-Based Infrastructure), **RAI**:(Roads & Associated Infrastructure), **SW**:(Stormwater), **WW**:(Wastewater)",style={'font-size':'14px','margin-top':'10px'}),
                dcc.Markdown('****** This column indicates whether a site visit of the infrastructure(s) or building(s) was conducted as part of the PIEVC Protocol vulnerability assessment',style={'font-size':'14px','margin-top':'-10px'})

            ])
        ],className='box',style={'margin-right': '-0.8rem','margin-left': '-1rem','margin-bottom': '1rem','margin-top': '1rem','padding-right':'15px','padding-left':'15px', 'padding-top':'15px', 'padding-bottom':'15px','backgroundColor':'#111111','border-radius': '15px','background-color': '#F2F2F2'}),
        # <Box 3>: Project Team
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H3(['Project Team ',
                                 html.I(className="fas fa-info-circle fa-lg", id="target-prjTeam",style={'font-size':'20px'})],style={'padding-left': '15px'}),
                        dbc.Tooltip("Use the dropdown menu to select a study included in the Utility. The project team for the study will then be displayed in the table below", target="target-prjTeam"),
                        html.Hr()
                    ]),
                    html.Div([
                        html.P('Choose Study:')
                    ]),
                    html.Div([
                        drop_Study
                    ],style={'width':'75%','margin-left': '-0.6rem','margin-bottom': '0.5rem','margin-top': '-0.3rem'}),
                    dcc.Loading(dcc.Graph(id='table_ProjectTeam'),color='#4B9072',type="circle")
                ],style={'width':'63%','margin-right': '1rem','margin-left': '0rem','margin-bottom': '1rem','margin-top': '1rem','padding-right':'15px','padding-left':'15px', 'padding-top':'15px', 'padding-bottom':'15px','backgroundColor':'#111111','border-radius': '15px','background-color': '#F2F2F2'}),
                html.Div([
                    html.Img(src=app.get_asset_url('PIEVCImg.png'),style={'width': '100%', 'position': 'relative', 'opacity': '80%','margin-top': '1rem'})
                ],style={'width':'31%'}),
            ],className='row'),
        ],className='box'),
        # <Box >: Climate Data Map
        html.Div([
            html.Div([
                html.H3("Geo-Spatial Distribution of PIEVC reports"),
                html.Hr(style={'margin-right': '30rem'}),
                html.P('The map shows spatial distribution of PIEVC studies based on the chosen infrastructure from the sidebar.')
            ]),
            html.Div([
                html.Iframe(srcDoc=open('map/ClimateMap.html').read(),width='100%',height='400')
            ])
        ],className='box',style={'margin-right': '0rem','margin-left': '-0.5rem','margin-bottom': '1rem','margin-top': '1rem','padding-right':'15px','padding-left':'15px', 'padding-top':'15px', 'padding-bottom':'15px','backgroundColor':'#111111','border-radius': '15px','background-color': '#F2F2F2'}),
        # <Box >: Select Infrastructure & Select Location & Select Study
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Infrastructure, Location, and Study:",id="BoxInfrastructureLocationStudy"),
                    html.Hr(),
                    html.P(['The results from PIEVC reports can be compared and explored in the', html.Q(html.A("Threshold",href="#BoxThreshold")), ', ',html.Q(html.A("Climate Parameters",href="#BoxClimateParameters"))
                            , "and, ",html.Q(html.A("Risk Analysis",href="#BoxRiskAnalysis")),' sections. For these investigations, please choose infrastructure, location, and study.'])
                ]),
                html.Div([
                    html.Div([
                        html.P(['Infrastructure: ', html.I(className="fas fa-info-circle fa-lg", id="target-infrasAnalysis",style={'font-size':'15px'})]),
                        dbc.Tooltip("You can select multiple infrastructures", target="target-infrasAnalysis"),
                    ],style={'margin-bottom':'-1rem'}),
                    html.Div([
                        dcc.Loading(drop_InfraClass_multi,color='#4B9072',type="circle")
                    ])
                ]),
                html.Div([
                    html.Div([
                        html.P(['Location: ',html.I(className="fas fa-info-circle fa-lg", id="target-locationAnalysis",style={'font-size':'15px'})]),
                        dbc.Tooltip("You can select multiple locations", target="target-locationAnalysis"),
                    ],style={'margin-bottom':'-1rem'}),
                    html.Div([
                        dcc.Loading(drop_province,color='#4B9072',type="circle")
                    ])
                ]),
                html.Div([
                    html.Div([
                        html.P(['Study: ',html.I(className="fas fa-info-circle fa-lg", id="target-studyAnalysis",style={'font-size':'15px'})]),
                        dbc.Tooltip("You can select multiple studies", target="target-studyAnalysis"),
                    ],style={'margin-bottom':'-1rem'}),
                    html.Div([
                        dcc.Loading(drop_study_multi,color='#4B9072',type="circle")
                    ])
                ])
            ],className='box',style={'width':'40%','margin-right': '0rem','margin-left': '0.3rem','margin-bottom': '1rem','margin-top': '1rem','padding-right':'15px','padding-left':'15px', 'padding-top':'15px', 'padding-bottom':'15px','backgroundColor':'#111111','border-radius': '15px','background-color': '#F2F2F2'}),
            # <Box >: Threshold
            html.Div([
                html.Div([
                    html.H3('Threshold',id="BoxThreshold"),
                    html.Hr(),
                    html.P('Thresholds allow study authors to determine whether or not infrastructure is expected to affected by change in specific climate parameters. This section will allow you to identify how thresholds were determined for the selected studies.'),
                    html.P(['Choose study to see the sources used to calculate climate threshold. ',html.I(className="fas fa-info-circle fa-lg", id="target-threshold",style={'font-size':'15px'})]),
                    dbc.Tooltip("you are offered thresholds for studies that were selected based on the criteria selected in the 'Infrastructure, Location, and Study' box ", target="target-threshold"),
                ]),
                html.Div([
                    dcc.Loading(drop_study_threshold,color='#4B9072',type="circle")
                ],style={'width':'75%'}),
                html.Div(id='Threshold_statement')
            ],className='box',style={'width':'57%','margin-right': '0rem','margin-left': '1rem','margin-bottom': '1rem','margin-top': '1rem','padding-right':'15px','padding-left':'15px', 'padding-top':'15px', 'padding-bottom':'15px','backgroundColor':'#111111','border-radius': '15px','background-color': '#F2F2F2'}),
        ],className='row'),
        # <Box >: Network Plot
        html.Div([
            html.Div([
                html.H3('Climate Parameters',id="BoxClimateParameters"),
                html.Hr(style={'width':'30'}),
                html.P(['This chart allows you to identify parameters that were included in studies selected in the ',html.Q(html.A("Infrastructure, Location and Study",href="#BoxInfrastructureLocationStudy")),
                        ' section. Select multiple studies to view shared parameters. ',
                        html.I(className="fas fa-info-circle fa-lg", id="target-ClimateParam",style={'font-size':'15px'})]),
                dbc.Tooltip("Drag the circles to get a better view of studies and their parameters ", target="target-ClimateParam"),
            ]),
            html.Div(
                dcc.Loading(cyto.Cytoscape(id='NetworkPlot',layout={'name': 'circle'},style={'width': '100%', 'height': '400px'},elements=[],stylesheet=[],minZoom=0.2,maxZoom=1),color='#4B9072',type="circle"),

            ),
        ],className='box',style={'margin-right': '0rem','margin-left': '-0.9rem','margin-bottom': '1rem','margin-top': '1rem','padding-right':'15px','padding-left':'15px', 'padding-top':'15px', 'padding-bottom':'15px','backgroundColor':'#111111','border-radius': '15px','background-color': '#F2F2F2'}),
        # <Box> Scatter Risk plot
        html.Div([
            html.Div([
                html.H3('Risk Analysis Overview'),
                html.Hr(style={'width':'30'}),
                html.P(['This section provides summaries of risks identified by the studies that consider the selected infrastructure in the ',
                        html.Q(html.A('Infrastructure, Location, and Study',href='#BoxInfrastructureLocationStudy'))," section. ",
                        html.I(className="fas fa-info-circle fa-lg", id="target-RiskAnalysisOverview",style={'font-size':'15px'})]),
                dbc.Tooltip("Hover over the circles to know more", target="target-RiskAnalysisOverview"),
            ]),
            html.Div(
                dcc.Loading(dcc.Graph(id='ScatterRiskPlot'),color='#4B9072',type="circle")
            ),
            html.Div([
                dcc.Markdown('***** **Other**: Fire, Lightning, Pest and Diseases, UV Exposure, Air pollution, Solar radiation',style={'font-size':'14px','margin-top':'15px'}),
                dcc.Markdown('****** **Composite**: Permafrost, Flooding, Drought, Ice accumulation, Fog, Storms, Freshet',style={'font-size': '14px', 'margin-top': '-10px'})

            ])
        ],className='box',style={'margin-right': '0rem','margin-left': '-0.9rem','margin-bottom': '1rem','margin-top': '1rem','padding-right':'15px','padding-left':'15px', 'padding-top':'15px', 'padding-bottom':'15px','backgroundColor':'#111111','border-radius': '15px','background-color': '#F2F2F2'}),
        # <Box > Risk Profile
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Risk Analysis 1',id="BoxRiskAnalysis"),
                    html.Hr(),
                    html.P('This section allows you to view specific interactions between infrastructure and climate parameters that were assessed in studies selected above.'),
                    html.P('Choose study, location, risk level and time horizon to see the risk profile.')
                ]),
                html.Div([
                    html.Div([
                       html.P('Study:')
                    ],style={'margin-bottom':'-1rem'}),
                    html.Div([
                        drop_study_sunburstRisk1
                    ])
                ]),
                html.Div([
                    html.Div([
                        html.P('Location:')
                    ],style={'margin-bottom':'-1rem'}),
                    html.Div([
                        drop_location_sunburstRisk1
                        ])
                ]),
                html.Div([
                    html.Div([
                        html.P(['Assessment Level: ',html.I(className="fas fa-info-circle fa-lg", id="target-RiskLevel1",style={'font-size':'15px'})]),
                        dbc.Tooltip("High level assessment provides risk analysis of climate-infrastructure interaction at a general level. Medium level assessment goes into detail about infrastructure components.", target="target-RiskLevel1"),
                    ],style={'margin-bottom':'-1rem'}),
                    html.Div([
                        drop_risklevel_sunburstRisk1
                        ])
                ]),
                html.Div([
                    html.Div([
                        html.P(['Time Horizon: ',html.I(className="fas fa-info-circle fa-lg", id="target-TimeHorizon1",style={'font-size':'15px'})]),
                        dbc.Tooltip("Current (Baseline): 1980-2020 \n Short Term: 2010-2040 \n Medium Term: 2040-2070 \n Long Term: 2070-2100 ",target="target-TimeHorizon1"),
                    ], style={'margin-bottom': '-1rem'}),
                    html.Div([
                        drop_timehorizon_sunburstRisk1
                        ])
                ]),
                html.Div([
                    dcc.Loading(dcc.Graph(id='Risk_sunburst1'),color='#4B9072',type="circle")
                ])
            ],className='box',style={'width':'49%','margin-right': '0rem','margin-left': '0rem','margin-bottom': '1rem','margin-top': '1rem','padding-right':'15px','padding-left':'15px', 'padding-top':'15px', 'padding-bottom':'15px','backgroundColor':'#111111','border-radius': '15px','background-color': '#F2F2F2'}),
            html.Div([
                html.Div([
                    html.H3('Risk Analysis 2'),
                    html.Hr(),
                    html.P('This section allows you to view specific interactions between infrastructure and climate parameters that were assessed in studies selected above.'),
                    html.P('Choose study, location, risk level and time horizon to see the risk profile.')
                ]),
                html.Div([
                    html.Div([
                        html.P('Study:')
                    ], style={'margin-bottom': '-1rem'}),
                    html.Div([
                        drop_study_sunburstRisk2
                    ])
                ]),
                html.Div([
                    html.Div([
                        html.P('Location:')
                    ], style={'margin-bottom': '-1rem'}),
                    html.Div([
                        drop_location_sunburstRisk2
                    ])
                ]),
                html.Div([
                    html.Div([
                        html.P(['Assessment Level: ',html.I(className="fas fa-info-circle fa-lg", id="target-RiskLevel2",style={'font-size':'15px'})]),
                        dbc.Tooltip("High level assessment provides risk analysis of climate-infrastructure interaction at a general level. Medium level assessment goes into detail about infrastructure components.",target="target-RiskLevel2"),
                    ], style={'margin-bottom': '-1rem'}),
                    html.Div([
                        drop_risklevel_sunburstRisk2
                    ])
                ]),
                html.Div([
                    html.Div([
                        html.P(['Time Horizon: ',html.I(className="fas fa-info-circle fa-lg", id="target-TimeHorizon2",style={'font-size':'15px'})]),
                        dbc.Tooltip("Current (Baseline): 1980-2020 \n Short Term: 2010-2040 \n Medium Term: 2040-2070 \n Long Term: 2070-2100 ",target="target-TimeHorizon2"),
                    ], style={'margin-bottom': '-1rem'}),
                    html.Div([
                        drop_timehorizon_sunburstRisk2
                    ])
                ]),
                html.Div([
                    dcc.Loading(dcc.Graph(id='Risk_sunburst2'),color='#4B9072',type="circle")
                ])
            ],className='box',style={'width':'49%','margin-right': '0rem','margin-left': '1rem','margin-bottom': '1rem','margin-top': '1rem','padding-right':'15px','padding-left':'15px', 'padding-top':'15px', 'padding-bottom':'15px','backgroundColor':'#111111','border-radius': '15px','background-color': '#F2F2F2'})
        ],className='row'),
        html.Div([
            html.Div([
                html.H3('Recommendations'),
                html.Hr(),
                html.P(['This section provides summaries of recommendations provided in studies selected in the ', html.Q(html.A('Infrastructure, Location, and Study',href='#BoxInfrastructureLocationStudy'))," section."])
            ]),
            html.Div(id='Recom_statement')
        ],className='box',style={'margin-right': '-0.5rem','margin-left': '-0.8rem','margin-bottom': '1rem','margin-top': '1rem','padding-right':'15px','padding-left':'15px', 'padding-top':'15px', 'padding-bottom':'15px','backgroundColor':'#111111','border-radius': '15px','background-color': '#F2F2F2'})

    ],className='main',style={"margin-left": "26rem","margin-right": "2rem"}),
    ])
])

#-----------------------------------------------------------------------------------------------------------------------
@app.callback(Output('opt_InfraClass_comp','options'),
              [Input('drop_InfraClass_single','value')]
)
def InfraClassification_Component(opt_infra):

    _InfraClassification_df = pd.read_csv('data/InfraClassification_df.csv')
    opt_components = _InfraClassification_df[_InfraClassification_df['Infrastructure Layer 1']==opt_infra]['Infrastructure Layer 2'].unique().tolist()
    opt_components = [dict(label=val, value=val) for val in opt_components]

    return opt_components

@app.callback([Output('DescripTab','children'),
               Output('StudiesTab','children')],
              [Input('drop_InfraClass_single','value'),
               Input('opt_InfraClass_comp','value')]

)
def InfraClassification_DescriptionStudy(opt_infra,opt_infra_comp):

    _RiskProfile_df = RiskProfile_df
    _InfraClassification_df = pd.read_csv('data/InfraClassification_df.csv')
    _InfraClassification_df.replace(to_replace="NAN", value='N/A', inplace=True)
    comp_df = _InfraClassification_df[(_InfraClassification_df['Infrastructure Layer 1']==opt_infra) & (_InfraClassification_df['Infrastructure Layer 2']==opt_infra_comp)]

    Statement_descrip = ''
    for i_comp,i_descrip in zip(comp_df['Components'],comp_df['Description']):
        if not i_comp == "N/A":
            Statement_descrip += '''\n**{}:** '''.format(i_comp)
            Statement_descrip += '''{}\n'''.format(i_descrip)
        else:
            Statement_descrip += '''\n**{}:** '''.format(opt_infra_comp)
            Statement_descrip += '''{}\n'''.format(i_descrip)

    Studies_infra = _RiskProfile_df[_RiskProfile_df['Infrastructure']==opt_infra]['Study'].unique().tolist()
    Statement_study = ''
    for i in Studies_infra:
        Statement_study += '''\n{}\n'''.format(i)

    return html.Div([dcc.Markdown(Statement_descrip)],style={'margin-right':'25px'}), html.Div([dcc.Markdown(Statement_study)],style={'margin-right':'25px',"overflow": "auto","height": "200px"})

@app.callback([Output('table_Overview','figure'),
               Output('table_ProjectTeam','figure')],
              [Input('drop_Study','value')]
)
def Overview_Team_Table(opt_study):

    # Overview Table
    _StudiesOverview_df = StudiesOverview_df.copy()
    _StudiesOverview_df = _StudiesOverview_df.drop(columns=['_id'])
    _StudiesOverview_df = _StudiesOverview_df.rename(columns={'Infrastructure':'Infrastructure*'})
    _StudiesOverview_df = _StudiesOverview_df.rename(columns={'Site Visit':'Site Visit**'})

    table_Overview = go.Figure(data=[go.Table(
        columnwidth=[400, 200, 250, 200, 120, 250, 120],
        header=dict(values=list(_StudiesOverview_df.columns),
                    fill_color='grey',
                    line_color='darkslategray',
                    align=['center', 'center', 'center', 'center', 'center', 'center', 'center'],
                    font=dict(color='white', size=12)),
        cells=dict(values=[_StudiesOverview_df.Title, _StudiesOverview_df['Consulting Company'], _StudiesOverview_df['Client'],
                           _StudiesOverview_df.Location, _StudiesOverview_df.Year,
                           _StudiesOverview_df['Infrastructure*'], _StudiesOverview_df['Site Visit**']],
                   fill_color='white',
                   align=['left', 'center', 'center', 'center', 'center', 'center', 'center'],
                   line_color='darkslategray'))
    ])
    table_Overview.update_layout(margin={'l': 0, 'r': 0, 'b': 0, 't': 0})

    # Project Team
    _ProjectTeam_df = ProjectTeam_df.copy()
    _ProjectTeam_df.replace(to_replace="NAN", value='N/A', inplace=True)
    ProjectTeam_opt = _ProjectTeam_df.loc[_ProjectTeam_df.Study == opt_study]
    ProjectTeam_opt = ProjectTeam_opt.drop(columns=['Study'])
    ProjectTeam_opt = ProjectTeam_opt.drop(columns=['_id'])
    table_ProjectTeam = go.Figure(data=[go.Table(
        columnwidth=[250, 300, 250],
        header=dict(values=list(ProjectTeam_opt.columns),
                    fill_color='grey',
                    line_color='darkslategray',
                    align=['center', 'center', 'center'],
                    font=dict(color='white', size=12)),
        cells=dict(values=[ProjectTeam_opt['Team Member'], ProjectTeam_opt['Role'], ProjectTeam_opt['Organization']],
                   fill_color='white',
                   align=['center', 'center', 'center'],
                   line_color='darkslategray'))
    ])
    table_ProjectTeam.update_layout(margin={'l': 0, 'r': 0, 'b': 0, 't': 0})
    table_ProjectTeam.update_layout(height=250)

    return table_Overview,table_ProjectTeam

@app.callback(Output('opt_province','options'),
              [Input('drop_InfraClass_multi','value')]
)
def Select_Infrastructure_Province(opt_infra_multi):

    _RiskProfile_df = RiskProfile_df.copy()

    # Extract provinces with the given infrastructures
    if isinstance(opt_infra_multi, list):
        opt_infra_multi_list = opt_infra_multi
    else:
        opt_infra_multi_list = [opt_infra_multi]

    opt_provinces = _RiskProfile_df[_RiskProfile_df['Infrastructure'].isin(opt_infra_multi_list)]['Province'].unique().tolist()
    opt_provinces = [dict(label=val, value=val) for val in opt_provinces]

    return opt_provinces

@app.callback(Output('opt_province','value'),
              [Input('opt_province','options')]
)
def Select_Infrastructure_Province_initial(opt_infra_province):
    return opt_infra_province[0]['value']

@app.callback(Output('opt_infra_province_study','options'),
              [Input('drop_InfraClass_multi','value'),
               Input('opt_province','value')]
)
def Select_Study(opt_infra_multi,opt_province_multi):

    _RiskProfile_df = RiskProfile_df.copy()

    # Extract study with the given infrastructures and provinces
    if isinstance(opt_infra_multi, list):
        opt_infra_multi_list = opt_infra_multi
    else:
        opt_infra_multi_list = [opt_infra_multi]

    provinces_df = _RiskProfile_df[_RiskProfile_df['Infrastructure'].isin(opt_infra_multi_list)]

    if isinstance(opt_province_multi, list):
        opt_province_multi_list = opt_province_multi
    else:
        opt_province_multi_list = [opt_province_multi]

    opt_infra_province_study_list = provinces_df[provinces_df['Province'].isin(opt_province_multi_list)]['Study'].unique().tolist()
    opt_infra_province_study = [dict(label=val, value=val) for val in opt_infra_province_study_list]

    return opt_infra_province_study

@app.callback(Output('opt_infra_province_study','value'),
              [Input('opt_infra_province_study','options')]
)
def Select_Study_init(opt_infra_province_study):
    return opt_infra_province_study[0]['value']

@app.callback(Output('opt_study_threshold','options'),
              [Input('drop_InfraClass_multi','value'),
               Input('opt_province','value')]
)
def Select_Study_Threshold(opt_infra_multi,opt_province_multi):

    _RiskProfile_df = RiskProfile_df

    # Extract study with the given infrastructures and provinces
    if isinstance(opt_infra_multi, list):
        opt_infra_multi_list = opt_infra_multi
    else:
        opt_infra_multi_list = [opt_infra_multi]

    provinces_df = _RiskProfile_df[_RiskProfile_df['Infrastructure'].isin(opt_infra_multi_list)]

    if isinstance(opt_province_multi, list):
        opt_province_multi_list = opt_province_multi
    else:
        opt_province_multi_list = [opt_province_multi]

    opt_infra_province_study_list = provinces_df[provinces_df['Province'].isin(opt_province_multi_list)]['Study'].unique().tolist()
    opt_infra_province_study = [dict(label=val, value=val) for val in opt_infra_province_study_list]

    return opt_infra_province_study

@app.callback(Output('opt_study_threshold','value'),
              [Input('opt_study_threshold','options')]
)
def Select_Study_Threshold_init(opt_study_threshold):
    return opt_study_threshold[0]['value']

@app.callback(Output('Threshold_statement','children'),
              [Input('opt_study_threshold','value')]
)
def Threshold_Description(opt_study_thres):
    Threshold_statement_list = ClimateData_df[ClimateData_df['Study']==opt_study_thres]['Threshold'].values.tolist()[0].split('&&')
    Statement_out = ''
    for Thr_st in Threshold_statement_list:
        title_st, statement_st = Thr_st.split(':')
        Statement_out += '''** {} :** \n {} \n'''.format(title_st,statement_st)

    return html.Div([dcc.Markdown(Statement_out)])


@app.callback([Output('NetworkPlot','elements'),
               Output('NetworkPlot','stylesheet')],
              [Input('opt_infra_province_study','value'),
               Input('drop_InfraClass_multi','value')]
)
def NetworkPlot(opt_infra_province_study,drop_InfraClass_multi):
    _RiskProfile_df = RiskProfile_df.copy()

    if isinstance(opt_infra_province_study, list):
        opt_infra_province_study_list = opt_infra_province_study
    else:
        opt_infra_province_study_list = [opt_infra_province_study]

    if isinstance(drop_InfraClass_multi, list):
        drop_InfraClass_multi_list = drop_InfraClass_multi
    else:
        drop_InfraClass_multi_list = [drop_InfraClass_multi]

    color_list = ["#" + ''.join([random.choice('0123456789ABCDEF') for j in range(6)])for i in range(100)]
    ClimateParam_list = []
    for i_study in opt_infra_province_study_list:
        list_infras = _RiskProfile_df['Infrastructure'][_RiskProfile_df['Study'] == i_study].unique().tolist()
        list_infras_study = list(set(list_infras).intersection(set(drop_InfraClass_multi_list)))
        for i_infra in list_infras_study:
            list_infras_study_clim = ClimateDataInfras_df['ClimateParam'][(ClimateDataInfras_df[i_infra] == 'Yes') & (ClimateDataInfras_df['Study'] == i_study)].unique().tolist()

            ClimateParam_list += list_infras_study_clim
    ClimateParam_list = list(set(ClimateParam_list))

    ClimateParam_nodes = []
    for i_elm in ClimateParam_list:
        id_ = i_elm+'id'
        ClimateParam_nodes.append({'data':{'id':id_,'ClimStud':i_elm}})

    Infras_nodes = []
    i_count = 0
    color_Infras = [{'selector': 'node','style': {'label': 'data(ClimStud)'}}]
    for i_study in opt_infra_province_study_list:
        list_infras = _RiskProfile_df['Infrastructure'][_RiskProfile_df['Study'] == i_study].unique().tolist()
        list_infras_study = list(set(list_infras).intersection(set(drop_InfraClass_multi_list)))
        for i_infras_study in list_infras_study:
            id_ = i_study+i_infras_study+'id'
            ClimStud_ = i_study+':'+i_infras_study
            Infras_nodes.append({'data':{'id':id_, 'ClimStud':ClimStud_}})
            color_code = color_list[i_count]
            color_Infras.append({'selector':'[ClimStud *= '+'"'+ClimStud_+'"'+']','style':{'background-color': color_code,'shape': 'rectangle'}})
            i_count += 1


    edges = []
    for i_study in opt_infra_province_study_list:
        list_infras = _RiskProfile_df['Infrastructure'][_RiskProfile_df['Study'] == i_study].unique().tolist()
        list_infras_study = list(set(list_infras).intersection(set(drop_InfraClass_multi_list)))
        for i_infra in list_infras_study:
            list_infras_study_clim = ClimateDataInfras_df['ClimateParam'][(ClimateDataInfras_df[i_infra] == 'Yes') & (ClimateDataInfras_df['Study'] == i_study)].unique().tolist()
            for mm in list_infras_study_clim:
                source_ = i_study+i_infra+'id'
                target_ = mm+'id'
                edges.append({'data':{'source':source_,'target':target_}})

    my_elements = Infras_nodes + ClimateParam_nodes + edges

    return my_elements,color_Infras

@app.callback(Output('ScatterRiskPlot','figure'),
              [Input('drop_InfraClass_multi','value')]
)
def ScatterPlot(drop_InfraClass_multi):

    def RiskScoreValueCalculator(var):
        if var == 'High':
            score = 12
        elif var == 'Med' or var == 'Mod-Low' or var == 'Mod-High':
            score = 7
        elif var == 'Low':
            score = 2
        else:
            score = 0
        return score

    def DotCoord(n_dots,up,left):
        n_row = n_dots//5
        reminder = n_dots%5
        x_coord = []
        y_coord = []
        x_spc = 0.3
        y_spc = 0.05
        for i in range(n_row):
            yloc = up - y_spc*i
            x_coord += [left,left+x_spc,left+x_spc+x_spc,left+x_spc+x_spc+x_spc,left+x_spc+x_spc+x_spc+x_spc]
            y_coord += [yloc,yloc,yloc,yloc,yloc]

        if reminder == 1:
            x_coord += [left]
            y_coord += [up - y_spc*n_row]
        if reminder == 2:
            x_coord += [left,left+x_spc]
            y_coord += [up - y_spc*n_row,up - y_spc*n_row]
        if reminder == 3:
            x_coord += [left, left+x_spc, left+x_spc+x_spc]
            y_coord += [up - y_spc * n_row, up - y_spc * n_row, up - y_spc * n_row]
        if reminder == 4:
            x_coord += [left, left+x_spc, left+x_spc+x_spc,left+x_spc+x_spc+x_spc]
            y_coord += [up - y_spc * n_row, up - y_spc * n_row, up - y_spc * n_row,up - y_spc * n_row]

        return x_coord,y_coord


    _RiskProfile_df = RiskProfile_df.copy()

    if isinstance(drop_InfraClass_multi, list):
        drop_InfraClass_multi_list = drop_InfraClass_multi
    else:
        drop_InfraClass_multi_list = [drop_InfraClass_multi]

    LowRisk_point_x = []
    LowRisk_point_y = []
    LowRisk_color = []
    LowRisk_hovertext = []
    MedRisk_point_x = []
    MedRisk_point_y = []
    MedRisk_color = []
    MedRisk_hovertext = []
    HighRisk_point_x = []
    HighRisk_point_y = []
    HighRisk_color = []
    HighRisk_hovertext = []
    ClimateParamGeneral = ['Temperature','Precipitation','Wind','Sea','Composite','Other']
    y_lb = [i*1 for i in range(len(drop_InfraClass_multi_list)+1)]
    y_margin = 0.05
    x_margin = 0.4
    y_margin_in = 1/6
    count = 0
    for i_infras in drop_InfraClass_multi_list:
        _RiskProfile_df['Score_current'] = _RiskProfile_df['Risk (Current)'].apply(RiskScoreValueCalculator)
        _RiskProfile_df['Score_short'] = _RiskProfile_df['Risk (Short Term)'].apply(RiskScoreValueCalculator)
        _RiskProfile_df['Score_medium'] = _RiskProfile_df['Risk (Medium Term)'].apply(RiskScoreValueCalculator)
        _RiskProfile_df['Score_long'] = _RiskProfile_df['Risk (Long Term)'].apply(RiskScoreValueCalculator)

        RiskProfile_infra_df = _RiskProfile_df[_RiskProfile_df['Infrastructure'] == i_infras]

        count_in = 0
        for i_climparam in ClimateParamGeneral:

            RiskProfile_infra_df_ClimParam = RiskProfile_infra_df[RiskProfile_infra_df['Climate Parameter General'] == i_climparam]

            RiskProfile_infra_df_gb_current_ClimParam = RiskProfile_infra_df_ClimParam.groupby('Study')[['Score_current']].max().reset_index()
            RiskProfile_infra_df_gb_short_ClimParam = RiskProfile_infra_df_ClimParam.groupby('Study')[['Score_short']].max().reset_index()
            RiskProfile_infra_df_gb_medium_ClimParam = RiskProfile_infra_df_ClimParam.groupby('Study')[['Score_medium']].max().reset_index()
            RiskProfile_infra_df_gb_long_ClimParam = RiskProfile_infra_df_ClimParam.groupby('Study')[['Score_long']].max().reset_index()

            RiskCount_current_df = RiskProfile_infra_df_gb_current_ClimParam['Score_current'].value_counts().reset_index().rename(columns={'count': 'RiskScore', 'Score_current': 'Counts'})
            RiskCount_short_df = RiskProfile_infra_df_gb_short_ClimParam['Score_short'].value_counts().reset_index().rename(columns={'count': 'RiskScore', 'Score_short': 'Counts'})
            RiskCount_medium_df = RiskProfile_infra_df_gb_medium_ClimParam['Score_medium'].value_counts().reset_index().rename(columns={'count': 'RiskScore', 'Score_medium': 'Counts'})
            RiskCount_long_df = RiskProfile_infra_df_gb_long_ClimParam['Score_long'].value_counts().reset_index().rename(columns={'count': 'RiskScore', 'Score_long': 'Counts'})

            if 2 in RiskCount_current_df.RiskScore.to_list():
                n_Low = RiskCount_current_df['Counts'][RiskCount_current_df['RiskScore'] == 2].to_list()[0]
                LowRisk_point_x += DotCoord(n_Low, y_lb[count + 1] - count_in*y_margin_in - y_margin, x_margin)[0]
                LowRisk_point_y += DotCoord(n_Low, y_lb[count + 1] - count_in*y_margin_in - y_margin, x_margin)[1]
                LowRisk_color += ['green' for i in range(n_Low)]
                LowRisk_hovertext += RiskProfile_infra_df_gb_current_ClimParam['Study'][RiskProfile_infra_df_gb_current_ClimParam['Score_current'] == 2].to_list()
            if 7 in RiskCount_current_df.RiskScore.to_list():
                n_Med = RiskCount_current_df['Counts'][RiskCount_current_df['RiskScore'] == 7].to_list()[0]
                MedRisk_point_x += DotCoord(n_Med, y_lb[count + 1] - count_in*y_margin_in - y_margin, 2 + x_margin)[0]
                MedRisk_point_y += DotCoord(n_Med, y_lb[count + 1] - count_in*y_margin_in - y_margin, 2 + x_margin)[1]
                MedRisk_color += ['yellow' for i in range(n_Med)]
                MedRisk_hovertext += RiskProfile_infra_df_gb_current_ClimParam['Study'][RiskProfile_infra_df_gb_current_ClimParam['Score_current'] == 7].to_list()
            if 12 in RiskCount_current_df.RiskScore.to_list():
                n_High = RiskCount_current_df['Counts'][RiskCount_current_df['RiskScore'] == 12].to_list()[0]
                HighRisk_point_x += DotCoord(n_High, y_lb[count + 1] - count_in*y_margin_in - y_margin, 4 + x_margin)[0]
                HighRisk_point_y += DotCoord(n_High, y_lb[count + 1] - count_in*y_margin_in - y_margin, 4 + x_margin)[1]
                HighRisk_color += ['red' for i in range(n_High)]
                HighRisk_hovertext += RiskProfile_infra_df_gb_current_ClimParam['Study'][RiskProfile_infra_df_gb_current_ClimParam['Score_current'] == 12].to_list()

            if 2 in RiskCount_short_df.RiskScore.to_list():
                n_Low = RiskCount_short_df['Counts'][RiskCount_short_df['RiskScore'] == 2].to_list()[0]
                LowRisk_point_x += DotCoord(n_Low, y_lb[count + 1] - count_in*y_margin_in - y_margin, 6 + x_margin)[0]
                LowRisk_point_y += DotCoord(n_Low, y_lb[count + 1] - count_in*y_margin_in - y_margin, 6 + x_margin)[1]
                LowRisk_color += ['green' for i in range(n_Low)]
                LowRisk_hovertext += RiskProfile_infra_df_gb_short_ClimParam['Study'][RiskProfile_infra_df_gb_short_ClimParam['Score_short'] == 2].to_list()
            if 7 in RiskCount_short_df.RiskScore.to_list():
                n_Med = RiskCount_short_df['Counts'][RiskCount_short_df['RiskScore'] == 7].to_list()[0]
                MedRisk_point_x += DotCoord(n_Med, y_lb[count + 1] - count_in*y_margin_in - y_margin, 6 + 2 + x_margin)[0]
                MedRisk_point_y += DotCoord(n_Med, y_lb[count + 1] - count_in*y_margin_in - y_margin, 6 + 2 + x_margin)[1]
                MedRisk_color += ['yellow' for i in range(n_Med)]
                MedRisk_hovertext += RiskProfile_infra_df_gb_short_ClimParam['Study'][RiskProfile_infra_df_gb_short_ClimParam['Score_short'] == 7].to_list()
            if 12 in RiskCount_short_df.RiskScore.to_list():
                n_High = RiskCount_short_df['Counts'][RiskCount_short_df['RiskScore'] == 12].to_list()[0]
                HighRisk_point_x += DotCoord(n_High, y_lb[count + 1] - count_in*y_margin_in - y_margin, 6 + 4 + x_margin)[0]
                HighRisk_point_y += DotCoord(n_High, y_lb[count + 1] - count_in*y_margin_in - y_margin, 6 + 4 + x_margin)[1]
                HighRisk_color += ['red' for i in range(n_High)]
                HighRisk_hovertext += RiskProfile_infra_df_gb_short_ClimParam['Study'][RiskProfile_infra_df_gb_short_ClimParam['Score_short'] == 12].to_list()

            if 2 in RiskCount_medium_df.RiskScore.to_list():
                n_Low = RiskCount_medium_df['Counts'][RiskCount_medium_df['RiskScore'] == 2].to_list()[0]
                LowRisk_point_x += DotCoord(n_Low, y_lb[count + 1] - count_in*y_margin_in - y_margin, 12 + x_margin)[0]
                LowRisk_point_y += DotCoord(n_Low, y_lb[count + 1] - count_in*y_margin_in - y_margin, 12 + x_margin)[1]
                LowRisk_color += ['green' for i in range(n_Low)]
                LowRisk_hovertext += RiskProfile_infra_df_gb_medium_ClimParam['Study'][RiskProfile_infra_df_gb_medium_ClimParam['Score_medium'] == 2].to_list()
            if 7 in RiskCount_medium_df.RiskScore.to_list():
                n_Med = RiskCount_medium_df['Counts'][RiskCount_medium_df['RiskScore'] == 7].to_list()[0]
                MedRisk_point_x += DotCoord(n_Med, y_lb[count + 1] - count_in*y_margin_in - y_margin, 12 + 2 + x_margin)[0]
                MedRisk_point_y += DotCoord(n_Med, y_lb[count + 1] - count_in*y_margin_in - y_margin, 12 + 2 + x_margin)[1]
                MedRisk_color += ['yellow' for i in range(n_Med)]
                MedRisk_hovertext += RiskProfile_infra_df_gb_medium_ClimParam['Study'][RiskProfile_infra_df_gb_medium_ClimParam['Score_medium'] == 7].to_list()
            if 12 in RiskCount_medium_df.RiskScore.to_list():
                n_High = RiskCount_medium_df['Counts'][RiskCount_medium_df['RiskScore'] == 12].to_list()[0]
                HighRisk_point_x += DotCoord(n_High, y_lb[count + 1] - count_in*y_margin_in - y_margin, 12 + 4 + x_margin)[0]
                HighRisk_point_y += DotCoord(n_High, y_lb[count + 1] - count_in*y_margin_in - y_margin, 12 + 4 + x_margin)[1]
                HighRisk_color += ['red' for i in range(n_High)]
                HighRisk_hovertext += RiskProfile_infra_df_gb_medium_ClimParam['Study'][RiskProfile_infra_df_gb_medium_ClimParam['Score_medium'] == 12].to_list()

            if 2 in RiskCount_long_df.RiskScore.to_list():
                n_Low = RiskCount_long_df['Counts'][RiskCount_long_df['RiskScore'] == 2].to_list()[0]
                LowRisk_point_x += DotCoord(n_Low, y_lb[count + 1] - count_in*y_margin_in - y_margin, 18 + x_margin)[0]
                LowRisk_point_y += DotCoord(n_Low, y_lb[count + 1] - count_in*y_margin_in - y_margin, 18 + x_margin)[1]
                LowRisk_color += ['green' for i in range(n_Low)]
                LowRisk_hovertext += RiskProfile_infra_df_gb_long_ClimParam['Study'][RiskProfile_infra_df_gb_long_ClimParam['Score_long'] == 2].to_list()
            if 7 in RiskCount_long_df.RiskScore.to_list():
                n_Med = RiskCount_long_df['Counts'][RiskCount_long_df['RiskScore'] == 7].to_list()[0]
                MedRisk_point_x += DotCoord(n_Med, y_lb[count + 1] - count_in*y_margin_in - y_margin, 18 + 2 + x_margin)[0]
                MedRisk_point_y += DotCoord(n_Med, y_lb[count + 1] - count_in*y_margin_in - y_margin, 18 + 2 + x_margin)[1]
                MedRisk_color += ['yellow' for i in range(n_Med)]
                MedRisk_hovertext += RiskProfile_infra_df_gb_long_ClimParam['Study'][RiskProfile_infra_df_gb_long_ClimParam['Score_long'] == 7].to_list()
            if 12 in RiskCount_long_df.RiskScore.to_list():
                n_High = RiskCount_long_df['Counts'][RiskCount_long_df['RiskScore'] == 12].to_list()[0]
                HighRisk_point_x += DotCoord(n_High, y_lb[count + 1] - count_in*y_margin_in - y_margin, 18 + 4 + x_margin)[0]
                HighRisk_point_y += DotCoord(n_High, y_lb[count + 1] - count_in*y_margin_in - y_margin, 18 + 4 + x_margin)[1]
                HighRisk_color += ['red' for i in range(n_High)]
                HighRisk_hovertext += RiskProfile_infra_df_gb_long_ClimParam['Study'][RiskProfile_infra_df_gb_long_ClimParam['Score_long'] == 12].to_list()

            count_in += 1
        count += 1

    Risk_point_x = LowRisk_point_x + MedRisk_point_x + HighRisk_point_x
    Risk_point_y = LowRisk_point_y + MedRisk_point_y + HighRisk_point_y
    Risk_color = LowRisk_color + MedRisk_color + HighRisk_color
    Risk_hovertext = LowRisk_hovertext + MedRisk_hovertext + HighRisk_hovertext


    fig = go.Figure(data=[go.Scatter(
        x=Risk_point_x,
        y=Risk_point_y,
        mode='markers',
        marker=dict(color=Risk_color, line_width=2),
        hovertext=Risk_hovertext, hoverinfo='text'
    ),go.Scatter(yaxis='y2')])

    fig.update_yaxes(range=[0, y_lb[-1]], showgrid=False)
    fig.update_xaxes(range=[0, 24], showgrid=False)
    fig.update_traces(marker_size=7)
    fig.add_vrect(x0=0, x1=2, fillcolor="green", opacity=0.25, line_width=0)
    fig.add_vrect(x0=2, x1=4, fillcolor="yellow", opacity=0.25, line_width=0)
    fig.add_vrect(x0=4, x1=6, fillcolor="red", opacity=0.25, line_width=0)
    fig.add_vrect(x0=6, x1=8, fillcolor="green", opacity=0.25, line_width=0)
    fig.add_vrect(x0=8, x1=10, fillcolor="yellow", opacity=0.25, line_width=0)
    fig.add_vrect(x0=10, x1=12, fillcolor="red", opacity=0.25, line_width=0)
    fig.add_vrect(x0=12, x1=14, fillcolor="green", opacity=0.25, line_width=0)
    fig.add_vrect(x0=14, x1=16, fillcolor="yellow", opacity=0.25, line_width=0)
    fig.add_vrect(x0=16, x1=18, fillcolor="red", opacity=0.25, line_width=0)
    fig.add_vrect(x0=18, x1=20, fillcolor="green", opacity=0.25, line_width=0)
    fig.add_vrect(x0=20, x1=22, fillcolor="yellow", opacity=0.25, line_width=0)
    fig.add_vrect(x0=22, x1=24, fillcolor="red", opacity=0.25, line_width=0)
    fig.update_layout(hoverlabel=dict(bgcolor="white", font_size=16))
    fig.add_annotation(x=3, y=y_lb[-1]/2, text='Current', showarrow=False, font_size=50, opacity=0.25,textangle=-90)
    fig.add_vline(x=6, line_width=3, line_color="black")
    fig.add_annotation(x=9, y=y_lb[-1]/2, text='Short<br>Term', showarrow=False, font_size=50, opacity=0.25,textangle=-90)
    fig.add_vline(x=12, line_width=3, line_color="black")
    fig.add_annotation(x=15, y=y_lb[-1]/2, text='Medium<br>Term', showarrow=False, font_size=50, opacity=0.25,textangle=-90)
    fig.add_vline(x=18, line_width=3, line_color="black")
    fig.add_annotation(x=21, y=y_lb[-1]/2, text='Long<br>Term', showarrow=False, font_size=50, opacity=0.25,textangle=-90)
    tickval = [0.5+i for i in range(len(drop_InfraClass_multi_list))]
    tickval2 = []
    ticktext2 = []
    ClimateParamGeneral_tick = ['Temperature', 'Precipitation', 'Wind', 'Sea', 'Composite**', 'Other*']
    for i in range(len(drop_InfraClass_multi_list)):
        tickval2 += [1/12+i,1/12+1/6+i,1/12+2/6+i,1/12+3/6+i,1/12+4/6+i,1/12+5/6+i]
        ticktext2 += ClimateParamGeneral_tick
    fig.update_layout(yaxis=dict(tickmode='array', tickvals=tickval, ticktext=drop_InfraClass_multi_list,tickangle=-90),
                      yaxis2=dict(tickmode='array',range=[0, y_lb[-1]],tickvals=tickval2, ticktext=ticktext2,overlaying="y",side="right"))
    fig.update_layout(xaxis=dict(tickmode='array', tickvals=[1,3,5,7,9,11,13,15,17,19,21,23], ticktext=['Low','Medium','High','Low','Medium','High','Low','Medium','High','Low','Medium','High']))
    fig.update_layout(margin=dict(l=0,r=0,b=25,t=0),paper_bgcolor="#F2F2F2")
    for i in range(len(drop_InfraClass_multi_list)):
        fig.add_hline(y=i+1, line_width=3, line_color="black",opacity=0.4)
        for j in range(len(ClimateParamGeneral)):
            fig.add_hline(y=(i + 1) - j/len(ClimateParamGeneral), line_width=3, line_color="black", opacity=0.2,line_dash="dash")

    return fig




@app.callback([Output('opt_study_sunburstRisk1','options'),
               Output('opt_study_sunburstRisk1','value')],
              [Input('opt_infra_province_study','options')]
)
def Select_Study_SunburstRisk1(opt_infra_province_study):

    opt_study_sunburstRisk1 = opt_infra_province_study

    return opt_study_sunburstRisk1, opt_study_sunburstRisk1[0]['value']


@app.callback([Output('opt_location_sunburstRisk1','options'),
               Output('opt_location_sunburstRisk1','value')],
              [Input('opt_study_sunburstRisk1','value')]
)
def Select_Location_SunburstRisk1(opt_study_sunburstRisk1):
    _RiskProfile_df = RiskProfile_df.copy()

    Location_list = _RiskProfile_df['Location'][_RiskProfile_df['Study'] == opt_study_sunburstRisk1].unique().tolist()
    opt_location_sunburstRisk1 = [dict(label=val, value=val) for val in Location_list]

    return opt_location_sunburstRisk1, opt_location_sunburstRisk1[0]['value']


@app.callback([Output('opt_study_sunburstRisk2','options'),
               Output('opt_study_sunburstRisk2','value')],
              [Input('opt_infra_province_study','options')]
)
def Select_Study_SunburstRisk2(opt_infra_province_study):

    opt_study_sunburstRisk2 = opt_infra_province_study

    return opt_study_sunburstRisk2, opt_study_sunburstRisk2[0]['value']


@app.callback([Output('opt_location_sunburstRisk2','options'),
               Output('opt_location_sunburstRisk2','value')],
              [Input('opt_study_sunburstRisk2','value')]
)
def Select_Location_SunburstRisk2(opt_study_sunburstRisk2):
    _RiskProfile_df = RiskProfile_df.copy()
    Location_list = _RiskProfile_df['Location'][_RiskProfile_df['Study'] == opt_study_sunburstRisk2].unique().tolist()
    opt_location_sunburstRisk2 = [dict(label=val, value=val) for val in Location_list]

    return opt_location_sunburstRisk2, opt_location_sunburstRisk2[0]['value']


@app.callback([Output('Risk_sunburst1','figure'),
               Output('Risk_sunburst2','figure')],
              [Input('opt_study_sunburstRisk1','value'),
               Input('opt_location_sunburstRisk1','value'),
               Input('opt_risklevel_sunburstRisk1','value'),
               Input('opt_timehorizon_sunburstRisk1','value'),
               Input('opt_study_sunburstRisk2','value'),
               Input('opt_location_sunburstRisk2','value'),
               Input('opt_risklevel_sunburstRisk2','value'),
               Input('opt_timehorizon_sunburstRisk2','value'),
               Input('drop_InfraClass_multi','value')]
)
def RiskProf_Plot(opt_study_sunburstRisk1,opt_location_sunburstRisk1,opt_risklevel_sunburstRisk1,opt_timehorizon_sunburstRisk1,
                  opt_study_sunburstRisk2,opt_location_sunburstRisk2,opt_risklevel_sunburstRisk2,opt_timehorizon_sunburstRisk2,
                  drop_InfraClass_multi):

    def RiskScoreValueCalculator(var):
        if var == 'High':
            score = 12
        elif var == 'Med' or var == 'Mod-Low' or var == 'Mod-High':
            score = 7
        elif var == 'Low':
            score = 2
        else:
            score = 0
        return score

    if isinstance(drop_InfraClass_multi, list):
        drop_InfraClass_multi_list = drop_InfraClass_multi
    else:
        drop_InfraClass_multi_list = [drop_InfraClass_multi]

    # Plot 1
    _RiskProfile_df = RiskProfile_df.copy()
    Risk_timehorizon1 = 'Risk '+'('+opt_timehorizon_sunburstRisk1+')'
    _RiskProfile_df['Score1'] = _RiskProfile_df[Risk_timehorizon1].apply(RiskScoreValueCalculator)
    df_sb_col1 = _RiskProfile_df[(_RiskProfile_df['Study'] == opt_study_sunburstRisk1) & (_RiskProfile_df['Location'] == opt_location_sunburstRisk1)]
    df_sb_col1 = df_sb_col1[df_sb_col1['Infrastructure'].isin(drop_InfraClass_multi_list)]
    if opt_risklevel_sunburstRisk1 == 'High':
        path = ['Infrastructure', 'Climate Parameter']
    else:
        path = ['Infrastructure', 'Infrastructure Component 1', 'Climate Parameter']

    sb1 = px.sunburst(df_sb_col1, path=path, color='Score1', color_continuous_scale=[[0,'white'],[0.167,'green'],[0.583,'yellow'],[1,'red']], range_color=(0, 12),custom_data=[Risk_timehorizon1, 'Infrastructure', 'Score1'])
    sb1.update_coloraxes(colorbar=dict(tickmode="array", tickvals=[0,2, 7, 12], ticktext=['N/A','Low', 'Moderate', 'High']))
    sb1.update_layout(coloraxis_colorbar_title='Risk')
    sb1.update_layout(margin={'l': 0, 'r': 0, 'b': 0, 't': 0})
    sb1.update_traces(hovertemplate='<b>Infrastructure Type: %{customdata[1]} <br> Label: %{label}',branchvalues='total', selector=dict(type='sunburst'))
    sb1.update_traces(insidetextorientation='radial', selector=dict(type='sunburst'))

    # Plot 2
    Risk_timehorizon2 = 'Risk '+'('+opt_timehorizon_sunburstRisk2+')'
    _RiskProfile_df['Score2'] = _RiskProfile_df[Risk_timehorizon2].apply(RiskScoreValueCalculator)

    df_sb_col2 = _RiskProfile_df[(_RiskProfile_df['Study'] == opt_study_sunburstRisk2) & (_RiskProfile_df['Location'] == opt_location_sunburstRisk2)]
    df_sb_col2 = df_sb_col2[df_sb_col2['Infrastructure'].isin(drop_InfraClass_multi_list)]
    if opt_risklevel_sunburstRisk2 == 'High':
        path = ['Infrastructure', 'Climate Parameter']
    else:
        path = ['Infrastructure', 'Infrastructure Component 1', 'Climate Parameter']

    sb2 = px.sunburst(df_sb_col2, path=path, color='Score2', color_continuous_scale=[[0,'white'],[0.167,'green'],[0.583,'yellow'],[1,'red']], range_color=(0, 12),custom_data=[Risk_timehorizon2, 'Infrastructure', 'Score2'])
    sb2.update_coloraxes(colorbar=dict(tickmode="array", tickvals=[0,2, 7, 12], ticktext=['N/A','Low', 'Moderate', 'High']))
    sb2.update_layout(coloraxis_colorbar_title='Risk')
    sb2.update_layout(margin={'l': 0, 'r': 0, 'b': 0, 't': 0})
    sb2.update_traces(hovertemplate='<b>Infrastructure Type: %{customdata[1]} <br> Label: %{label}',branchvalues='total', selector=dict(type='sunburst'))
    sb2.update_traces(insidetextorientation='radial', selector=dict(type='sunburst'))

    return sb1, sb2

@app.callback(Output('Recom_statement','children'),
              [Input('opt_infra_province_study','value')]
)
def Recommendation_Statement(opt_infra_province_study):

    if isinstance(opt_infra_province_study, list):
        opt_infra_province_study_list = opt_infra_province_study
    else:
        opt_infra_province_study_list = [opt_infra_province_study]
    Recommendation_df.replace(to_replace="NAN", value='N/A', inplace=True)
    df_st = Recommendation_df[Recommendation_df['Study'].isin(opt_infra_province_study_list)]

    Statement_out = ''
    for i_study in df_st['Study'].unique().tolist():
        Infras = df_st['Infrastructure'][df_st['Study']==i_study].unique().tolist()
        Statement_out += '''#### {} \n'''.format(i_study)
        for i_infras in Infras:
            Statement_out += '''\n** {} :**\n'''.format(i_infras)
            Recoms = df_st['Recommendation'][(df_st['Study']==i_study) & (df_st['Infrastructure']==i_infras)].tolist()
            for i_recom in Recoms:
                Statement_out += '''* {} \n'''.format(i_recom)

    return html.Div([dcc.Markdown(Statement_out)])
