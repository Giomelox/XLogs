import flet as ft

neon_color_azul = "#00eaff"
neon_color_branco = "#ffffff"
neon_color_preto = "#000000"
neon_color_vermelho = "#ff0000"
neon_color_verde = "#00ff00"




estilo_botao_neon_azul = ft.ButtonStyle(
    bgcolor = ft.Colors.with_opacity(0.15, neon_color_azul),
    color = neon_color_azul,
    overlay_color = ft.Colors.with_opacity(0.2, neon_color_azul),
    shadow_color = ft.Colors.with_opacity(0.8, neon_color_azul),
    elevation = 4,
    surface_tint_color = ft.Colors.TRANSPARENT,
    padding = 15,
    shape = ft.RoundedRectangleBorder(radius = 12),
    side = ft.BorderSide(width = 2, color = neon_color_azul),
)
###########################################################################
estilo_botao_neon_branco = ft.ButtonStyle(
    bgcolor = ft.Colors.with_opacity(0.15, neon_color_branco),
    color = neon_color_branco,
    overlay_color = ft.Colors.with_opacity(0.2, neon_color_branco),
    shadow_color = ft.Colors.with_opacity(0.8, neon_color_branco),
    elevation = 4,
    surface_tint_color = ft.Colors.TRANSPARENT,
    padding = 15,
    shape = ft.RoundedRectangleBorder(radius = 20),
    side = ft.BorderSide(width = 2, color = neon_color_branco),
)
###########################################################################
estilo_botao_neon_branco_superiores = ft.ButtonStyle(
    text_style = ft.TextStyle(size = 18),
    bgcolor = ft.Colors.with_opacity(0.15, neon_color_branco),
    color = neon_color_branco,
    overlay_color = ft.Colors.with_opacity(0.2, neon_color_branco),
    shadow_color = ft.Colors.with_opacity(0.8, neon_color_branco),
    elevation = 4,
    surface_tint_color = ft.Colors.TRANSPARENT,
    padding = 15,
    shape = ft.RoundedRectangleBorder(radius = 20),
    side = ft.BorderSide(width = 2, color = neon_color_branco),
)
###########################################################################
estilo_botao_neon_branco_login = ft.ButtonStyle(
    text_style = ft.TextStyle(size = 18),
    bgcolor = ft.Colors.with_opacity(0.15, neon_color_branco),
    color = neon_color_branco,
    overlay_color = ft.Colors.with_opacity(0.2, neon_color_branco),
    shadow_color = ft.Colors.with_opacity(0.8, neon_color_branco),
    elevation = 4,
    surface_tint_color = ft.Colors.TRANSPARENT,
    padding = 15,
    shape = ft.RoundedRectangleBorder(radius = 20),
    side = ft.BorderSide(width = 2, color = neon_color_branco),
)
###########################################################################
estilo_botao_neon_branco_cancelar = ft.ButtonStyle(
    text_style = ft.TextStyle(size = 18),
    bgcolor = ft.Colors.with_opacity(0.15, neon_color_vermelho),
    color = neon_color_vermelho,
    overlay_color = ft.Colors.with_opacity(0.2, neon_color_vermelho),
    shadow_color = ft.Colors.with_opacity(0.8, neon_color_vermelho),
    elevation = 4,
    surface_tint_color = ft.Colors.TRANSPARENT,
    padding = 15,
    shape = ft.RoundedRectangleBorder(radius = 20),
    side = ft.BorderSide(width = 2, color = neon_color_vermelho),
)
###########################################################################
estilo_botao_neon_branco_salvar = ft.ButtonStyle(
    text_style = ft.TextStyle(size = 18),
    bgcolor = ft.Colors.with_opacity(0.15, neon_color_verde),
    color = neon_color_verde,
    overlay_color = ft.Colors.with_opacity(0.2, neon_color_verde),
    shadow_color = ft.Colors.with_opacity(0.8, neon_color_verde),
    elevation = 4,
    surface_tint_color = ft.Colors.TRANSPARENT,
    padding = 15,
    shape = ft.RoundedRectangleBorder(radius = 20),
    side = ft.BorderSide(width = 2, color = neon_color_verde),
)