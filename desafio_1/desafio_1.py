import flet as ft
from stellar_sdk import Keypair
import logging
from mnemonic import Mnemonic

def main(page: ft.Page):
    # Configurações da página
    page.title = "Stellar Wallet Generator"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = "#FFFFFF"
    page.window_width = 1000
    page.window_height = 800
    page.vertical_alignment = ft.MainAxisAlignment.CENTER  # Centralização vertical
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER  # Centralização horizontal
    
    # Configurar logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Header
    header = ft.Container(
        content=ft.Column([
            ft.Text(
                "Gerador de Carteira Stellar",
                size=32,
                weight=ft.FontWeight.BOLD,
                color="#3E1BDB",
                text_align=ft.TextAlign.CENTER,  # Texto centralizado
            ),
            ft.Text(
                "Crie suas credenciais Stellar de forma segura",
                size=16,
                color="#666666",
                text_align=ft.TextAlign.CENTER,  # Texto centralizado
            )
        ], 
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Alinhamento horizontal central
        spacing=10),
        padding=ft.padding.all(30),
        bgcolor="#F7F7F7",
        width=800,  # Reduzido para melhor centralização
        alignment=ft.alignment.center  # Container centralizado
    )
    
    # Área de resultados
    result_container = ft.Container(
        content=ft.Column([
            ft.Text(
                "Suas Credenciais", 
                size=20, 
                weight=ft.FontWeight.BOLD, 
                color="#3E1BDB",
                text_align=ft.TextAlign.CENTER,  # Texto centralizado
            ),
            ft.Container(
                content=ft.Column([
                    ft.TextField(
                        label="Chave Privada (SECRET)",
                        multiline=True,
                        read_only=True,
                        border_color="#3E1BDB",
                        text_size=14,
                        min_lines=2,
                        max_lines=2,
                        width=600,  # Largura fixa para melhor apresentação
                    ),
                    ft.TextField(
                        label="Chave Pública (PUBLIC KEY)",
                        multiline=True,
                        read_only=True,
                        border_color="#3E1BDB",
                        text_size=14,
                        min_lines=2,
                        max_lines=2,
                        width=600,  # Largura fixa para melhor apresentação
                    ),
                    ft.TextField(
                        label="Frase Mnemônica",
                        multiline=True,
                        read_only=True,
                        border_color="#3E1BDB",
                        text_size=14,
                        min_lines=2,
                        max_lines=2,
                        width=600,  # Largura fixa para melhor apresentação
                    )
                ], 
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centralização horizontal
                ),
                padding=20,
                bgcolor="#F7F7F7",
                border_radius=10,
            )
        ], 
        spacing=20,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # Centralização horizontal
        ),
        visible=False,
        alignment=ft.alignment.center  # Container centralizado
    )
    
    def gerar_credenciais(e):
        try:
            # Gerar keypair Stellar
            keypair = Keypair.random()
            secret = keypair.secret
            public_key = keypair.public_key
            
            # Gerar frase mnemônica (12 palavras em inglês)
            mnemo = Mnemonic("english")
            mnemonic = mnemo.generate(strength=128)  # 12 palavras
            
            # Atualizar campos
            result_container.content.controls[1].content.controls[0].value = secret
            result_container.content.controls[1].content.controls[1].value = public_key
            result_container.content.controls[1].content.controls[2].value = mnemonic
            
            # Mostrar container
            result_container.visible = True
            
            # Mostrar aviso de segurança
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(
                        "⚠️ IMPORTANTE: Guarde sua chave privada e frase mnemônica em um local seguro!",
                        color="#FFFFFF"
                    ),
                    bgcolor="#FF4B4B"
                )
            )
            
            logging.info("Credenciais geradas com sucesso!")
            page.update()
            
        except Exception as e:
            logging.error(f"Erro ao gerar credenciais: {str(e)}")
            page.dialog = ft.AlertDialog(
                title=ft.Text("Erro"),
                content=ft.Text(f"Ocorreu um erro ao gerar as credenciais: {str(e)}")
            )
            page.dialog.open = True
            page.update()
    
    # Botão de geração
    generate_button = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.icons.WALLET_ROUNDED),
                ft.Text("Gerar Nova Carteira", size=16)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        style=ft.ButtonStyle(
            color="#FFFFFF",
            bgcolor="#3E1BDB",
            padding=20,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        on_click=gerar_credenciais,
        width=250,
        height=50,
    )
    
    # Layout principal com espaçamento vertical
    page.add(
        ft.Container(
            content=ft.Column(
                [
                    header,
                    ft.Container(height=20),  # Espaçamento
                    generate_button,
                    ft.Container(height=20),  # Espaçamento
                    result_container
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            alignment=ft.alignment.center,  # Container principal centralizado
            padding=ft.padding.symmetric(vertical=40)  # Padding vertical
        )
    )

if __name__ == '__main__':
    ft.app(target=main)
