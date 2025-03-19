from dash import Input, Output, html
import plotly.express as px
from babel.numbers import format_decimal, format_percent

from src.config import TEMPLATE
from src.tabs.tab_des_economico import tab_economia
from src.tabs.tab_trabalho_renda import tab_trabalho_renda
from src.tabs.tab_des_urbano import tab_desenvolvimento_urbano
from src.tabs.tab_home import tab_home


def init_callbacks(app, all_data):

    @app.callback(Output("tabs-content", "children"), Input("tabs", "value"))
    def render_content(tab):
        if tab == "economia":
            return tab_economia

        elif tab == "trabalho":
            return tab_trabalho_renda

        elif tab == "urbano":
            return tab_desenvolvimento_urbano
        
        return tab_home


    # CALLBACKS DE FILTRO - GRÁFICOS
    @app.callback(
        Output("fig-rais-anual", "figure"), Input("filtro-cnae-rais-saldo", "value")
    )
    def atualizar_grafico_rais_anual(filtro_cnae):
        if filtro_cnae == "Todos":
            df_filtrado = all_data["rais_anual"]
        else:
            df_filtrado = all_data["rais_anual"][
                all_data["rais_anual"]["descricao_secao_cnae"] == filtro_cnae
            ]

        rais_anual_grp = df_filtrado.groupby("ano", as_index=False).agg(
            {"quantidade_vinculos_ativos": "sum"}
        )

        fig = px.area(
            rais_anual_grp,
            x="ano",
            y="quantidade_vinculos_ativos",
            labels={
                "ano": "Ano",
                "quantidade_vinculos_ativos": "Quantidade de vínculos empregatícios ativos",
            },
            markers="o",
            template="plotly_white",
        )
        fig.add_annotation(
            text="Fonte: RAIS Estabelecimentos",
            xref="paper",
            yref="paper",
            x=0,
            y=-0.2,
            showarrow=False,
            font=dict(size=12),
        )
        fig.update_xaxes(tickmode="linear", dtick="M1", tickangle=45)
        return fig


    @app.callback(
        [
            Output("card-estoque-atual-value", "children"),
            Output("card-variacao-estoque-value", "children"),
            Output("card-variacao-arrow", "children"),
            Output("card-variacao-arrow", "style"),
        ],
        Input("filtro-cnae-rais-saldo", "value")
    )
    def atualizar_cards_estoque(filtro_cnae):
        if filtro_cnae == "Todos":
            df_filtrado = all_data["rais_anual"]
        else:
            df_filtrado = all_data["rais_anual"][
                all_data["rais_anual"]["descricao_secao_cnae"] == filtro_cnae
            ]

        # Existing calculations
        estoque_atual = (
            df_filtrado.loc[df_filtrado["ano"] == df_filtrado["ano"].max()]
            .agg({"quantidade_vinculos_ativos": "sum"})
            .values[0]
        )
        estoque_atual_formatted = format_decimal(estoque_atual, format='#,##0', locale='pt_BR')

        estoque_anterior = (
            df_filtrado.loc[df_filtrado["ano"] == df_filtrado["ano"].max() - 1]
            .agg({"quantidade_vinculos_ativos": "sum"})
            .values[0]
        )
        variacao_estoque = ((estoque_atual - estoque_anterior) / estoque_anterior)
        variacao_estoque_formatted = format_percent(variacao_estoque, format='#,##0.0%', locale='pt_BR')
        
        # Define arrow properties based on variation
        arrow_symbol = "▲" if variacao_estoque >= 0 else "▼"
        arrow_style = {
            "color": "#28a745" if variacao_estoque >= 0 else "#dc3545",
            "fontSize": "24px",
            "marginLeft": "8px"
        }
        
        return estoque_atual_formatted, variacao_estoque_formatted, arrow_symbol, arrow_style
        
    
    @app.callback(
        Output("fig-saldo-anual", "figure"), Input("filtro-cnae-caged-saldo", "value")
    )
    def atualizar_grafico_caged(filtro_cnae):
        if filtro_cnae == "Todos":
            df_filtrado = all_data["caged_saldo_anual"]
        else:
            df_filtrado = all_data["caged_saldo_anual"][
                all_data["caged_saldo_anual"]["cnae_2_descricao_secao"] == filtro_cnae
            ]

        caged_ano = df_filtrado.groupby("ano", as_index=False).agg(
            {"saldo_movimentacao": "sum"}
        )

        fig = px.bar(
            caged_ano,
            x="ano",
            y="saldo_movimentacao",
            template=TEMPLATE,
            labels={
                "ano": "Ano",
                "saldo_movimentacao": "Saldo das movimentações",
            },
        )
        fig.add_annotation(
            text="Fonte: CAGED e NOVO CAGED",
            xref="paper",
            yref="paper",
            x=0,
            y=-0.2,
            showarrow=False,
            font=dict(size=12),
        )
        fig.update_xaxes(tickmode="linear", dtick="M1", tickangle=45)
        return fig


    @app.callback(
        [
            Output("card-saldo-atual-value", "children"),
            Output("card-variacao-saldo-value", "children"),
            Output("card-variacao-saldo-arrow", "children"),
            Output("card-variacao-saldo-arrow", "style"),
        ],
        Input("filtro-cnae-caged-saldo", "value")
    )
    def atualizar_cards_estoque(filtro_cnae):
        if filtro_cnae == "Todos":
            df_filtrado = all_data['caged_saldo_anual']
        else:
            df_filtrado = all_data['caged_saldo_anual'][
                all_data['caged_saldo_anual']["cnae_2_descricao_secao"] == filtro_cnae
            ]
        saldo_ano_max = (
            df_filtrado.loc[df_filtrado["ano"] == df_filtrado["ano"].max()]
            .agg({"saldo_movimentacao": "sum"})
            .values[0]
        )
        saldo_ano_max_formatted = format_decimal(saldo_ano_max, format='#,##0', locale='pt_BR')

        saldo_ano_max_lag1 = (
            df_filtrado.loc[df_filtrado["ano"] == df_filtrado["ano"].max() - 1]
            .agg({"saldo_movimentacao": "sum"})
            .values[0]
        )
        variacao_mov = ((saldo_ano_max - saldo_ano_max_lag1) / saldo_ano_max_lag1)
        variacao_mov_formatted = format_percent(variacao_mov, format='#,##0.0%', locale='pt_BR')
        
        # Define arrow properties based on variation
        arrow_symbol = "▲" if variacao_mov >= 0 else "▼"
        arrow_style = {
            "color": "#28a745" if variacao_mov >= 0 else "#dc3545",
            "fontSize": "24px",
            "marginLeft": "8px"
        }
        
        return saldo_ano_max_formatted, variacao_mov_formatted, arrow_symbol, arrow_style

    @app.callback(
        Output("fig-caged-saldo-secao", "figure"), Input("filtro-ano-caged-secao", "value")
    )
    def atualizar_grafico_caged_saldo_secao(filtro_ano):
        if filtro_ano == "Todos":
            df_filtrado = all_data["caged_saldo_secao"]
        else:
            df_filtrado = all_data["caged_saldo_secao"][
                all_data["caged_saldo_secao"]["ano"] == filtro_ano
            ]

        caged_saldo_secao_grp = (
            df_filtrado.groupby("cnae_2_descricao_secao", as_index=False)
            .agg({"saldo_movimentacao": "sum"})
            .sort_values("saldo_movimentacao")
        )

        fig = px.bar(
            caged_saldo_secao_grp,
            x="saldo_movimentacao",
            y="cnae_2_descricao_secao",
            orientation="h",
            labels={
                "saldo_movimentacao": "Saldo das movimentações",
                "cnae_2_descricao_secao": "Seção da CNAE",
            },
            template=TEMPLATE,
        )
        fig.add_annotation(
            text="Fonte: CAGED e NOVO CAGED",
            xref="paper",
            yref="paper",
            x=0.0,
            y=-0.2,
            showarrow=False,
            font=dict(size=12),
            xanchor="center",
        )
        return fig


    @app.callback(
        Output("fig-caged-saldo-idade", "figure"), Input("filtro-ano-caged-idade", "value")
    )
    def atualizar_grafico_caged_saldo_idade(filtro_ano):
        if filtro_ano == "Todos":
            df_filtrado = all_data["caged_saldo_idade"]
        else:
            df_filtrado = all_data["caged_saldo_idade"][
                all_data["caged_saldo_idade"]["ano"] == filtro_ano
            ]

        caged_saldo_idade_grp = (
            df_filtrado.groupby("idade", as_index=False)
            .agg({"saldo_movimentacao": "sum"})
            .sort_values("saldo_movimentacao")
        )

        fig = px.bar(
            caged_saldo_idade_grp,
            x="saldo_movimentacao",
            y="idade",
            labels={
                "idade": "Idade",
                "saldo_movimentacao": "Saldo das movimentações",
            },
            orientation="h",
            template=TEMPLATE,
        )
        fig.add_annotation(
            text="Fonte: CAGED e NOVO CAGED",
            xref="paper",
            yref="paper",
            x=0.05,
            y=-0.2,
            showarrow=False,
            font=dict(size=12),
            xanchor="center",
        )
        return fig


    @app.callback(
        Output("fig-caged-salario-medio", "figure"),
        [
            Input("filtro-ano-caged-salario-medio", "value"),
            Input("salario-stat-type", "value")
        ]
    )
    def atualizar_grafico_caged_media_salario(filtro_cnae, stat_type):
        # Filtrar por CNAE, se aplicável
        df_filtrado = (
            all_data["caged_media_salario"]
            if filtro_cnae == "Todos"
            else all_data["caged_media_salario"][
                all_data["caged_media_salario"]["cnae_2_descricao_secao"] == filtro_cnae
            ]
        )

        # Choose aggregation function based on radio button selection
        agg_func = 'mean' if stat_type == 'mean' else 'median'
        stat_label = "Média" if stat_type == "mean" else "Mediana"

        # Agrupar corretamente
        caged_media_salario_grp = (
            df_filtrado.groupby(["ano", "variable"], as_index=False)
            .agg({"salario_medio": agg_func})
            .sort_values("ano")
        )

        # Criar gráfico de linha
        fig = px.line(
            caged_media_salario_grp,
            y="salario_medio",
            x="ano",
            labels={
                "ano": "Ano",
                "salario_medio": f"{stat_label} Salarial",
                "variable": "Tipo de movimentação",
            },
            color="variable",
            markers=True,
            template=TEMPLATE,
        )

        # Adicionar anotação da fonte
        fig.add_annotation(
            text="Fonte: CAGED e NOVO CAGED",
            xref="paper",
            yref="paper",
            x=0.0,
            y=-0.2,
            showarrow=False,
            font=dict(size=12),
            xanchor="left",
        )

        return fig


    @app.callback(
        Output("fig-caged-media-idade", "figure"),
        [
            Input("filtro-ano-caged-media-idade", "value"),
            Input("media-idade-stat-type", "value")
        ]
    )
    def atualizar_grafico_caged_media_idade(filtro_cnae, stat_type):
        # Filtrar por CNAE, se aplicável
        df_filtrado = (
            all_data["caged_media_idade"]
            if filtro_cnae == "Todos"
            else all_data["caged_media_idade"][
                all_data["caged_media_idade"]["cnae_2_descricao_secao"] == filtro_cnae
            ]
        )

        # Choose aggregation function based on radio button selection
        agg_func = 'mean' if stat_type == 'mean' else 'median'
        stat_label = "Média" if stat_type == "mean" else "Mediana"

        # Agrupar corretamente
        caged_media_idade_grp = (
            df_filtrado.groupby(["ano", "variable"], as_index=False)
            .agg({"media_idade": agg_func})  # Fixed the aggregation syntax
            .sort_values("ano")
        )

        # Criar gráfico de linha
        fig = px.line(
            caged_media_idade_grp,
            y="media_idade",
            x="ano",
            labels={
                "ano": "Ano",
                "media_idade": f"{stat_label} de Idade",
                "variable": "Tipo de movimentação",
            },
            color="variable",
            markers=True,
            template=TEMPLATE,
        )

        # Adicionar anotação da fonte
        fig.add_annotation(
            text="Fonte: CAGED e NOVO CAGED",
            xref="paper",
            yref="paper",
            x=0.0,
            y=-0.2,
            showarrow=False,
            font=dict(size=12),
            xanchor="left",
        )

        return fig