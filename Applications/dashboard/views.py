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
        title='Porcentaje de jugadores por tipo de documento',
        hole=0.4
    )

    fig_pie.update_layout(
    title_text='Porcentaje de jugadores por tipo de documento',
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
        title='Edades de Jugadores por Condición Médica',
        category_orders={'grupos de edades': age_labels}
    )
    fig_hist.update_layout(
        title_text='Edades de Jugadores por Condición Médica',
        title_font=dict(size=24, family='Montserrat, sans-serif', color='black'),
        title_x=0.5,  # Centra el título
        yaxis_title='Cantidad'
    )
    chart_html_hist = fig_hist.to_html(full_html=False)

    # We group all the charts in the context to be rendered in the template
    context = {
        'chart_pie': chart_html_pie,
        'chart_hist': chart_html_hist
    }

    return render(request, 'dashboard.html', context)