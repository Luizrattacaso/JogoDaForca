import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from texto import palavras_com_dicas  # Supondo que palavras_com_dicas seja um dicionário que contenha palavras e dicas
import random

Max_tentativas = 6

class Adivinhe_A_PalavraApp(App):
    def build(self):
        self.iniciar_jogo()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        #palavra
        self.label_palavra = Label(text=self.exibicao, font_size=30)
        layout.add_widget(self.label_palavra)

        #tentativas
        self.label_erros = Label(text=f"Tentativas restantes: {Max_tentativas - self.erros}", font_size=20)
        layout.add_widget(self.label_erros)

        #pontuação
        self.label_pontuacao = Label(text=f"Pontuação: {self.pontuacao}", font_size=20)
        layout.add_widget(self.label_pontuacao)

        #dica
        self.label_dica = Label(text=f"Dica: {self.dica}", font_size=20, color=(0.5, 0.5, 0.5, 1))
        layout.add_widget(self.label_dica)

        # Caixa para a letra
        self.text_input = TextInput(hint_text="Digite uma letra", font_size=30, multiline=False)
        self.text_input.bind(on_text_validate=self.jogar)
        layout.add_widget(self.text_input)

        #botão de reiniciar
        botao_layout = BoxLayout(orientation='horizontal', size_hint=(None, None), size=(400, 50), spacing=10)
        
        #reiniciar jogo
        self.botao_reiniciar = Button(text="Reiniciar Jogo", size_hint=(None, None), size=(200, 50))
        self.botao_reiniciar.bind(on_press=self.reiniciar)
        
        botao_layout.add_widget(self.botao_reiniciar)
        layout.add_widget(botao_layout)

        return layout

    def iniciar_jogo(self):
        """Função para reiniciar as variáveis do jogo."""
        palavra_dica = random.choice(palavras_com_dicas)
        self.palavra = palavra_dica["palavra"]
        self.dica = palavra_dica["dica"]
        self.n = len(self.palavra)
        self.erros = 0
        self.chutes = ""
        self.pontuacao = 0
        self.exibicao = "_ " * self.n  
        self.acerto = False

        if not palavras_com_dicas:
            self.popup_mensagem("Erro: Nenhuma palavra disponível.")
            return

    def jogar(self, instance):
        letra = self.text_input.text.lower()

        if len(letra) > 1:
            if letra == self.palavra:
                self.exibicao = f"Parabéns, você acertou a palavra: {self.palavra}"
                self.label_palavra.text = self.exibicao
                if len(self.chutes) == 0:
                    self.pontuacao += 1450
                elif len(self.chutes) <= 3:
                    self.pontuacao += 1000
                else:
                    self.pontuacao += 800
                self.label_pontuacao.text = f"Pontuação: {self.pontuacao}"
                self.popup_mensagem("Você venceu!")
                self.desabilitar_input()
            else:
                self.erros += 1
                self.label_erros.text = f"Tentativas restantes: {Max_tentativas - self.erros}"
                self.popup_mensagem(f"Errou! A palavra não é {letra}. Continue tentando!")

        if (len(letra) != 1 and letra != self.palavra) or not letra.isalpha():
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
            self.pontuacao += 50
            self.label_pontuacao.text = f"Pontuação: {self.pontuacao}"
            for i in range(self.n):
                if self.palavra[i] in self.chutes:
                    nova += self.palavra[i] + " "
                else:
                    nova += "_ "
            self.exibicao = nova
            self.label_palavra.text = self.exibicao
        else:
            self.erros += 1
            self.pontuacao -= 30
            self.label_pontuacao.text = f"Pontuação: {self.pontuacao}"
            self.label_erros.text = f"Tentativas restantes: {Max_tentativas - self.erros}"

        if "_ " not in self.exibicao:  # Ganha
            self.exibicao = f"Parabéns, você acertou a palavra: {self.palavra}"
            self.label_palavra.text = self.exibicao
            self.popup_mensagem("Você venceu!")
            self.desabilitar_input()

        elif self.erros >= Max_tentativas:  # Perde
            self.exibicao = f"Você perdeu! A palavra era: {self.palavra}"
            self.label_palavra.text = self.exibicao
            self.popup_mensagem("Você perdeu!")
            self.desabilitar_input()

        self.text_input.text = ""  # Limpa o campo de entrada 

    def reiniciar(self, instance):
        """Reinicia o jogo."""
        self.iniciar_jogo()
        self.pontuacao = 0
        self.label_palavra.text = self.exibicao
        self.label_erros.text = f"Tentativas restantes: {Max_tentativas - self.erros}"
        self.label_pontuacao.text = f"Pontuação: {self.pontuacao}"
        self.text_input.text = ""
        self.text_input.disabled = False

    def popup_mensagem(self, mensagem):
        """Exibe uma mensagem em forma de popup."""
        popup = Popup(
            title="Fim de Jogo",
            content=Label(text=mensagem),
            size_hint=(None, None),
            size=(400, 200)
        )
        popup.open()

    def desabilitar_input(self):
        """Desabilita a entrada após o fim do jogo."""
        self.text_input.disabled = True
        self.label_palavra.color = (0, 1, 0, 1)  # Verde para vitória
        if self.erros >= Max_tentativas:
            self.label_palavra.color = (1, 0, 0, 1)  # Vermelho para derrota

if __name__ == '__main__':
    Adivinhe_A_PalavraApp().run()
