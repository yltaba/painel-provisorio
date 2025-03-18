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
            Output("card-variacao-estoque-value", "children")
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

        # Calcular estoque atual
        estoque_atual = (
            df_filtrado.loc[df_filtrado["ano"] == df_filtrado["ano"].max()]
            .agg({"quantidade_vinculos_ativos": "sum"})
            .values[0]
        )
        
        # Format estoque_atual
        estoque_atual_formatted = format_decimal(estoque_atual, format='#,##0', locale='pt_BR')

        # Calcular variação
        estoque_anterior = (
            df_filtrado.loc[df_filtrado["ano"] == df_filtrado["ano"].max() - 1]
            .agg({"quantidade_vinculos_ativos": "sum"})
            .values[0]
        )
        variacao_estoque = ((estoque_atual - estoque_anterior) / estoque_anterior)
        variacao_estoque_formatted = format_percent(variacao_estoque, format='#,##0.0%', locale='pt_BR')
        
        # Return only the values (they will inherit the card-value class from their containers)
        return estoque_atual_formatted, variacao_estoque_formatted

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
        Input("filtro-ano-caged-salario-medio", "value"),
    )
    def atualizar_grafico_caged_media_salario(filtro_cnae):
        # Filtrar por CNAE, se aplicável
        df_filtrado = (
            all_data["caged_media_salario"]
            if filtro_cnae == "Todos"
            else all_data["caged_media_salario"][
                all_data["caged_media_salario"]["cnae_2_descricao_secao"] == filtro_cnae
            ]
        )

        # Agrupar corretamente
        caged_media_salario_grp = (
            df_filtrado.groupby(["ano", "variable"], as_index=False)
            .agg(salario_medio=("salario_medio", "mean"))  # Evita dicionário dentro do agg
            .sort_values("ano")  # Garante ordenação correta para o gráfico
        )

        # Criar gráfico de linha
        fig = px.line(
            caged_media_salario_grp,
            y="salario_medio",
            x="ano",
            labels={
                "ano": "Ano",
                "salario_medio": "Média Salarial",
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
        Input("filtro-ano-caged-media-idade", "value"),
    )
    def atualizar_grafico_caged_media_idade(filtro_cnae):
        # Filtrar por CNAE, se aplicável
        df_filtrado = (
            all_data["caged_media_idade"]
            if filtro_cnae == "Todos"
            else all_data["caged_media_idade"][
                all_data["caged_media_idade"]["cnae_2_descricao_secao"] == filtro_cnae
            ]
        )

        # Agrupar corretamente
        caged_media_idade_grp = (
            df_filtrado.groupby(["ano", "variable"], as_index=False)
            .agg(media_idade=("media_idade", "mean"))  # Evita dicionário dentro do agg
            .sort_values("ano")  # Garante ordenação correta para o gráfico
        )

        # Criar gráfico de linha
        fig = px.line(
            caged_media_idade_grp,
            y="media_idade",
            x="ano",
            labels={
                "ano": "Ano",
                "media_idade": "Média de Idade",
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