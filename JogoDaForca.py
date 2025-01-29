import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout


from texto import palavras_com_dicas
import random

class ForcaApp(App):
    def build(self):
        self.iniciar_jogo()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.label_palavra = Label(text=self.exibicao, font_size=30)
        layout.add_widget(self.label_palavra)

        #erros
        self.label_erros = Label(text=f"Tentativas restantes: {6 - self.erros}", font_size=20)
        layout.add_widget(self.label_erros)

        #letra
        self.text_input = TextInput(hint_text="Digite uma letra", font_size=30, multiline=False)
        self.text_input.bind(on_text_validate=self.jogar)  # Vincula o evento de validação
        layout.add_widget(self.text_input)

        #botões
        botao_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(400, 50), spacing=10)
        botao_layout.add_widget(self.botao_dica)
        botao_layout.add_widget(self.botao_reiniciar)

        layout.add_widget(botao_layout)

        return layout

    def iniciar_jogo(self):
        ("""Função para reiniciar as variáveis do jogo.""")
        palavra_dica = random.choice(palavras_com_dicas)
        self.palavra = palavra_dica["palavra"]
        self.dica = palavra_dica["dica"]
        self.n = len(self.palavra)
        self.erros = 0
        self.chutes = ""
        self.exibicao = "_ " * self.n  #exibição
        self.acerto = False

        #botões
        self.botao_dica = Button(text="Mostrar Dica", size_hint=(None, None), size=(200, 50))
        self.botao_dica.bind(on_press=self.mostrar_dica)

        self.botao_reiniciar = Button(text="Reiniciar Jogo", size_hint=(None, None), size=(200, 50))
        self.botao_reiniciar.bind(on_press=self.reiniciar)

    def jogar(self, instance):
        letra = self.text_input.text.lower()

        # Verificando se a entrada é uma letra válida
        if len(letra) != 1 or not letra.isalpha():
            self.popup_mensagem("Por favor, digite uma letra válida.")
            self.text_input.text = "" 
            return

        if letra in self.chutes:
            self.popup_mensagem("Você já tentou essa letra!")
            self.text_input.text = ""  
            return

        self.chutes += letra

        if letra in self.palavra:
            nova = ""
            for i in range(self.n):
                if self.palavra[i] in self.chutes:
                    nova += self.palavra[i] + " "
                else:
                    nova += "_ "
            self.exibicao = nova
            self.label_palavra.text = self.exibicao
        else:
            self.erros += 1
            self.label_erros.text = f"Tentativas restantes: {6 - self.erros}"

        if "_ " not in self.exibicao:  #ganhou
            self.exibicao = f"Parabéns, você acertou a palavra: {self.palavra}"
            self.label_palavra.text = self.exibicao
            self.popup_mensagem("Você venceu!")
            self.desabilitar_input()

        elif self.erros >= 6: #perdeu
            self.exibicao = (f"Você perdeu! A palavra era: {self.palavra}")
            self.label_palavra.text = self.exibicao
            self.popup_mensagem("Você perdeu!")
            self.desabilitar_input()

        self.text_input.text = ""  # Limpa o campo de entrada 

    def reiniciar(self, instance):
        ("""Reinicia o jogo.""")
        self.iniciar_jogo()
        self.label_palavra.text = self.exibicao
        self.label_erros.text = (f"Tentativas restantes: {6 - self.erros}")
        self.text_input.text = ""
        self.text_input.disabled = False

    def mostrar_dica(self, instance):
        ("""Mostra a dica da palavra escolhida.""")
        self.popup_mensagem(f"Dica: {self.dica}")

    def popup_mensagem(self, mensagem):
        ("""Exibe uma mensagem em forma de popup.""")
        popup = Popup(
            title="Fim de Jogo",
            content=Label(text=mensagem),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()

    def desabilitar_input(self):
        ("""Desabilita a entrada após o fim do jogo.""")
        self.text_input.disabled = True

if __name__ == '__main__':
    ForcaApp().run()
