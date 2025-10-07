# Import necessary modules
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from collections import Counter

import plotly.express as px
import pandas as pd
from django import forms

from Applications.user.models import Player, Guardian
from Applications.payment.models import Payment 
from Applications.core.utils import user_can_access_dashboard
from datetime import datetime, timedelta

# This function is responsible for creating the logic behind of the dashboard
@login_required
def dashboard_view(request):
    """
    Vista del dashboard con datos y gráficos.
    Solo los usuarios Admin pueden acceder.
    """
    # Verificar si el usuario puede acceder al dashboard
    if not user_can_access_dashboard(request.user):
        messages.error(request, 'No tienes permisos para acceder al dashboard. Solo los administradores pueden verlo.')
        return redirect('homePage')
    players = Player.objects.all()
    guardians = Guardian.objects.all()
    payments = Payment.objects.all()

    # Player Charts
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
    
    chart_html_pie = fig_pie.to_html(full_html=False, include_plotlyjs='cdn')

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
    chart_html_hist = fig_hist.to_html(full_html=False, include_plotlyjs=False)

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
    chart_html_sessions = fig_sessions.to_html(full_html=False, include_plotlyjs=False)

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
    chart_html_eps = fig_eps.to_html(full_html=False, include_plotlyjs=False)

    # Guardian Charts
    # Guardian pie chart: IVA responsibility
    iva_types = [g.regime_type if g.regime_type else 'Sin dato' for g in guardians]
    iva_counts = pd.Series(iva_types).value_counts().reset_index()
    iva_counts.columns = ['Responsabilidad IVA', 'Cantidad']
    fig_guardian_iva = px.pie(
        iva_counts,
        names='Responsabilidad IVA',
        values='Cantidad',
        title='Acudientes responsables de IVA',
        hole=0.4,
        width=500,
        height=450
    )
    fig_guardian_iva.update_layout(
        title_text='Acudientes responsables de IVA',
        title_font=dict(size=24, family='Montserrat, sans-serif', color='black'),
        title_x=0.5
    )
    chart_html_guardian_iva = fig_guardian_iva.to_html(full_html=False, include_plotlyjs=False)

    # Guardian bar chart: most common cities
    guardian_cities = [g.city if g.city else 'Sin ciudad' for g in guardians]
    df_guardian_cities = pd.DataFrame({'Ciudad': guardian_cities})
    city_counts = df_guardian_cities['Ciudad'].value_counts().reset_index()
    city_counts.columns = ['Ciudad', 'Cantidad']
    fig_guardian_cities = px.bar(
        city_counts.head(10),
        x='Ciudad',
        y='Cantidad',
        title='Ciudades más frecuentes de acudientes',
        color='Ciudad',
        width=500,
        height=450
    )
    fig_guardian_cities.update_layout(
        title_text='Ciudades más frecuentes de acudientes',
        title_font=dict(size=20, family='Montserrat, sans-serif', color='black'),
        title_x=0.5,
        yaxis_title='Cantidad'
    )
    chart_html_guardian_cities = fig_guardian_cities.to_html(full_html=False, include_plotlyjs=False)

    # Payments Charts
    payments_df = pd.DataFrame(list(payments.values()))

    # 1. Ingresos mensuales del último año
    if not payments_df.empty:
        payments_df['date'] = pd.to_datetime(payments_df['date'])
        payments_df['amount'] = payments_df['amount'].astype(float)
        today = datetime.today()
        one_year_ago = today - timedelta(days=365)
        last_year_df = payments_df[(payments_df['date'] >= one_year_ago) & (payments_df['date'] <= today)]
        monthly_income = last_year_df.groupby(last_year_df['date'].dt.to_period('M')).agg({'amount': 'sum'}).reset_index()
        monthly_income['month'] = monthly_income['date'].astype(str)
        fig_payments_time = px.bar(
            monthly_income,
            x='month',
            y='amount',
            title='Ingresos mensuales a CEFUSA (último año)',
            color='month',
            width=500,
            height=450
        )
        fig_payments_time.update_layout(
            title_text='Ingresos mensuales a CEFUSA (último año)',
            title_font=dict(size=20, family='Montserrat, sans-serif', color='black'),
            title_x=0.5,
            yaxis_title='Valor'
        )
        chart_payments_time = fig_payments_time.to_html(full_html=False, include_plotlyjs='cdn')

        # 2. Cantidad de pagos a agrupados por sucursal
        cuentas_df = payments_df[payments_df['account'].isin(['5031', '5032'])]
        cuentas_group = cuentas_df.groupby(['account', 'branch']).size().reset_index(name='Cantidad')
        fig_cuentas_sucursal = px.bar(
            cuentas_group,
            x='branch',
            y='Cantidad',
            color='account',
            barmode='group',
            title='Pagos hechos por sucursal',
            width=500,
            height=450
        )
        fig_cuentas_sucursal.update_layout(
            title_text='Pagos hechos por sucursal',
            title_font=dict(size=20, family='Montserrat, sans-serif', color='black'),
            title_x=0.5,
            yaxis_title='Cantidad'
        )
        chart_cuentas_sucursal = fig_cuentas_sucursal.to_html(full_html=False, include_plotlyjs=False)

        # 3. Grafico de barras descripciones de pagos
        desc_group = payments_df['description'].value_counts().reset_index()
        desc_group.columns = ['Descripción', 'Cantidad']
        fig_desc = px.bar(
            desc_group.head(10),
            x='Descripción',
            y='Cantidad',
            color='Descripción',
            title='Cantidad de pagos por descripción',
            width=500,
            height=450
        )
        fig_desc.update_layout(
            title_text='Cantidad de pagos por descripción',
            title_font=dict(size=20, family='Montserrat, sans-serif', color='black'),
            title_x=0.5,
            yaxis_title='Cantidad'
        )
        chart_motivo = fig_desc.to_html(full_html=False, include_plotlyjs=False)

        # 4. Pagos por responsable y valor total en el mes
        if 'fk_responsible_id' in payments_df.columns:
            # Agrupar por responsable y mes, sumar valor
            payments_df['month'] = payments_df['date'].dt.to_period('M').astype(str)
            guardian_payments = payments_df.groupby(['fk_responsible_id', 'month']).agg({'amount': 'sum'}).reset_index()
            # Obtener nombres de responsables
            guardian_map = {g.id: f"{g.first_name} {g.last_name}" for g in guardians}
            guardian_payments['Responsable'] = guardian_payments['fk_responsible_id'].map(guardian_map)
            fig_ranking = px.bar(
                guardian_payments.sort_values('amount', ascending=False).head(10),
                x='Responsable',
                y='amount',
                color='month',
                title='Pagos realizados por responsables (valor total mensual)',
                width=500,
                height=450
            )
            fig_ranking.update_layout(
                title_text='Pagos realizados por responsables (valor total mensual)',
                title_font=dict(size=20, family='Montserrat, sans-serif', color='black'),
                title_x=0.5,
                yaxis_title='Valor total'
            )
            chart_ranking_acudientes = fig_ranking.to_html(full_html=False, include_plotlyjs=False)
        else:
            chart_ranking_acudientes = "<div>No hay datos de responsables disponibles.</div>"
    else:
        chart_payments_time = chart_cuentas_sucursal = chart_motivo = chart_ranking_acudientes = "<div>No hay datos de pagos disponibles.</div>"

    # We group all the charts in the context to be rendered in the template
    context = {
        'chart_pie': chart_html_pie,
        'chart_hist': chart_html_hist,
        'chart_sessions': chart_html_sessions,
        'chart_eps': chart_html_eps,
        'chart_guardian_iva': chart_html_guardian_iva,
        'chart_guardian_cities': chart_html_guardian_cities,
        'chart_payments_time': chart_payments_time,
        'chart_cuentas_sucursal': chart_cuentas_sucursal,
        'chart_motivo': chart_motivo,
        'chart_ranking_acudientes': chart_ranking_acudientes
    }

    return render(request, 'dashboard.html', context)