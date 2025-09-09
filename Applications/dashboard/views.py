# Import necessary modules
from django.http import HttpResponse
from django.shortcuts import render
from collections import Counter

import plotly.express as px
import pandas as pd
from django import forms

from Applications.user.models import Player, Guardian
from Applications.payment.models import Payment 

# This function is responsible for creating the logic behind of the dashboard
def dashboard_view(request):
    players = Player.objects.all()
    guardians = Guardian.objects.all()
    payments = Payment.objects.all()

    # Pie chart: porcentaje de jugadores por tipo de documento
    tipo_doc_counts = {}
    total = players.count()
    for p in players:
        type = p.document_type if p.document_type else 'Sin documento'
        tipo_doc_counts[type] = tipo_doc_counts.get(type, 0) + 1

    fig_pie = px.pie(
        names=list(tipo_doc_counts.keys()),
        values=list(tipo_doc_counts.values()),
        title='jugadores por tipo de documento',
        hole=0.4,
        width=500,
        height=450
    )

    fig_pie.update_layout(
        title_text='Jugadores por tipo de documento',
        title_font=dict(size=24, family='Montserrat, sans-serif', color='black'),
        title_x=0.5  # Centra el título
    )
    
    chart_html_pie = fig_pie.to_html(full_html=False)

    # Histogram of ages grouped by medical condition
    from datetime import date
    age_bins = [0, 5, 10, 15, 100]
    age_labels = ['0-5', '6-10', '11-15', 'Mayores a 15']
    today = date.today()
    ages = []
    conditions = []
    for p in players:
        if p.birth_date:
            age = today.year - p.birth_date.year - ((today.month, today.day) < (p.birth_date.month, p.birth_date.day))
            ages.append(age)
            conditions.append('Tiene condicion medica' if p.has_disease else 'No tiene condicion medica')
    df = pd.DataFrame({'age': ages, 'condition': conditions})
    df['grupos de edades'] = pd.cut(df['age'], bins=age_bins, labels=age_labels, right=True)
    fig_hist = px.histogram(
        df,
        x='grupos de edades',
        color='condition',
        barmode='group',
        title='Jugadores por Condición Médica',
        category_orders={'grupos de edades': age_labels},
        width=500,
        height=450
    )
    fig_hist.update_layout(
        title_text='Jugadores por Condición Médica',
        title_font=dict(size=24, family='Montserrat, sans-serif', color='black'),
        title_x=0.5,  # Centra el título
        yaxis_title='Cantidad'
    )
    chart_html_hist = fig_hist.to_html(full_html=False)

    # Bar chart: students training in morning and afternoon
    sessions = [p.training_session if p.training_session else 'Sin jornada' for p in players]
    df_sessions = pd.DataFrame({'Jornada': sessions})
    session_counts = df_sessions['Jornada'].value_counts().reset_index()
    session_counts.columns = ['Jornada', 'Cantidad']
    fig_sessions = px.bar(
        session_counts,
        x='Jornada',
        y='Cantidad',
        title='Cantidad de estudiantes por jornada',
        color='Jornada',
        width=500,
        height=450
    )
    fig_sessions.update_layout(
        title_text='Cantidad de estudiantes por jornada',
        title_font=dict(size=20, family='Montserrat, sans-serif', color='black'),
        title_x=0.5,
        yaxis_title='Cantidad'
    )
    chart_html_sessions = fig_sessions.to_html(full_html=False)

    # Chart: most used EPS
    eps_list = [p.eps if p.eps else 'Sin EPS' for p in players]
    df_eps = pd.DataFrame({'EPS': eps_list})
    eps_counts = df_eps['EPS'].value_counts().reset_index()
    eps_counts.columns = ['EPS', 'Cantidad']
    fig_eps = px.bar(
        eps_counts.head(10),
        x='EPS',
        y='Cantidad',
        title='EPS más usadas',
        color='EPS',
        width=500,
        height=450
    )
    fig_eps.update_layout(
        title_text='EPS más usadas',
        title_font=dict(size=20, family='Montserrat, sans-serif', color='black'),
        title_x=0.5,
        yaxis_title='Cantidad'
    )
    chart_html_eps = fig_eps.to_html(full_html=False)

    # We group all the charts in the context to be rendered in the template
    context = {
        'chart_pie': chart_html_pie,
        'chart_hist': chart_html_hist,
        'chart_sessions': chart_html_sessions,
        'chart_eps': chart_html_eps
    }

    return render(request, 'dashboard.html', context)