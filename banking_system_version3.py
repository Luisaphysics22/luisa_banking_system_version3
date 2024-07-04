from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nasc = data_nascimento
        self.cpf = cpf

class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo
        saldo_insuficiente = saldo < valor

        if saldo_insuficiente:
            print("Operação não realizada, pois não há saldo suficiente.\n")

        elif valor > 0:
            self._saldo -= valor
            print(f"Saque de R$ {valor:.2f} realizado com sucesso, por favor retire o seu dinheiro!\n")
            return True

        else:
            print(f"Operação não realizada! O {valor} informado é inválido. Por favor, tente novamente.")
        
        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"Depósito realizado de R$ {valor:.2f} com sucesso!\n")
            
        else:
            print(f"Operação não realizada! O {valor} informado é inválido. Por favor, tente novamente.\n")
            return False
        
        return True
        

class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite_valor =500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite_valor
        self._limite_saques = limite_saques      
    
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao ["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite_valor
        excedeu_saques = numero_saques >= self.limite_saques  

        if excedeu_limite:
            print(f"Operação não realizada, pois o  valor de R$ {valor:.2f} ultrapassa o limite diário.\n")
            
        elif excedeu_saques:
            print("Operação não realizada, pois excedeu o número de saques diários. Por favor, tente novamente amanhã.\n")

        else:
            return super().sacar(valor)

        return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

class Historico():
    def __init__(self):
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )
    
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

class Saque(Transacao):
    def __init__(self,valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor
    
    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)
    
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self) 
