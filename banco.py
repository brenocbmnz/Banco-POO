from datetime import datetime

# Classe PessoaFisica
class PessoaFisica:
    def __init__(self, cpf, nome, data_nascimento):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = datetime.strptime(data_nascimento, '%d/%m/%Y')

# Classe Cliente
class Cliente(PessoaFisica):
    def __init__(self, cpf, nome, data_nascimento, endereco):
        super().__init__(cpf, nome, data_nascimento)
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def realizar_transacao(self, conta, transacao):
        conta.historico.adicionar_transacao(transacao)
        transacao.registrar(conta)

# Classe Conta
class Conta:
    def __init__(self, cliente, numero, agencia="0001"):
        self.saldo = 0.0
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.historico = Historico()

    def obter_saldo(self):
        return self.saldo

    def sacar(self, valor):
        if valor > self.saldo:
            print("Saldo insuficiente.")
            return False
        self.saldo -= valor
        return True

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            return True
        return False

# Classe ContaCorrente (herança de Conta)
class ContaCorrente(Conta):
    def __init__(self, cliente, numero, limite=500.0, limite_saques=3):
        super().__init__(cliente, numero)
        self.limite = limite
        self.limite_saques = limite_saques
        self.numero_saques = 0

    def sacar(self, valor):
        if self.numero_saques >= self.limite_saques:
            print("Limite de saques excedido.")
            return False
        if valor > self.limite:
            print("Valor excede o limite de saque.")
            return False
        if super().sacar(valor):
            self.numero_saques += 1
            return True
        return False

# Classe Historico
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao):
        self.transacoes.append(transacao)

# Interface Transacao
class Transacao:
    def registrar(self, conta):
        raise NotImplementedError

# Classe Deposito
class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            print(f"Depósito de R$ {self.valor:.2f} realizado com sucesso!")
        else:
            print("Erro ao realizar o depósito.")

# Classe Saque
class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            print(f"Saque de R$ {self.valor:.2f} realizado com sucesso!")
        else:
            print("Erro ao realizar o saque.")

# Função para cadastrar um novo cliente
def cadastrar_cliente(clientes):
    nome = input("Informe o nome completo: ")
    cpf = input("Informe o CPF (somente números): ")
    data_nascimento = input("Informe a data de nascimento (dd/mm/aaaa): ")
    endereco = input("Informe o endereço (logradouro, número - bairro - cidade/estado): ")

    cliente = Cliente(cpf, nome, data_nascimento, endereco)
    clientes.append(cliente)
    print("Cliente cadastrado com sucesso!")

# Função para cadastrar uma nova conta
def cadastrar_conta(clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente_encontrado = None

    for cliente in clientes:
        if cliente.cpf == cpf:
            cliente_encontrado = cliente
            break

    if cliente_encontrado:
        numero_conta = len(contas) + 1
        conta = ContaCorrente(cliente_encontrado, numero_conta)
        cliente_encontrado.adicionar_conta(conta)
        contas.append(conta)
        print(f"Conta {numero_conta} cadastrada com sucesso!")
    else:
        print("Cliente não encontrado. Verifique o CPF.")

# Função para realizar um depósito
def realizar_deposito(contas):
    numero_conta = int(input("Informe o número da conta: "))
    valor = float(input("Informe o valor do depósito: "))

    conta_encontrada = None
    for conta in contas:
        if conta.numero == numero_conta:
            conta_encontrada = conta
            break

    if conta_encontrada:
        deposito = Deposito(valor)
        conta_encontrada.cliente.realizar_transacao(conta_encontrada, deposito)
    else:
        print("Conta não encontrada.")

# Função para realizar um saque
def realizar_saque(contas):
    numero_conta = int(input("Informe o número da conta: "))
    valor = float(input("Informe o valor do saque: "))

    conta_encontrada = None
    for conta in contas:
        if conta.numero == numero_conta:
            conta_encontrada = conta
            break

    if conta_encontrada:
        saque = Saque(valor)
        conta_encontrada.cliente.realizar_transacao(conta_encontrada, saque)
    else:
        print("Conta não encontrada.")

# Função para exibir o extrato
def exibir_extrato(contas):
    numero_conta = int(input("Informe o número da conta: "))

    conta_encontrada = None
    for conta in contas:
        if conta.numero == numero_conta:
            conta_encontrada = conta
            break

    if conta_encontrada:
        print("\n================ EXTRATO ================")
        for transacao in conta_encontrada.historico.transacoes:
            print(type(transacao).__name__, f": R$ {transacao.valor:.2f}")
        print(f"Saldo: R$ {conta_encontrada.obter_saldo():.2f}")
        print("==========================================")
    else:
        print("Conta não encontrada.")

# Programa principal
def main():
    clientes = []
    contas = []

    menu = """
    [d] Depositar
    [s] Sacar
    [e] Extrato
    [c] Cadastrar Cliente
    [n] Cadastrar Conta
    [q] Sair

    => """

    while True:
        opcao = input(menu)

        if opcao == "d":
            realizar_deposito(contas)

        elif opcao == "s":
            realizar_saque(contas)

        elif opcao == "e":
            exibir_extrato(contas)

        elif opcao == "c":
            cadastrar_cliente(clientes)

        elif opcao == "n":
            cadastrar_conta(clientes, contas)

        elif opcao == "q":
            break

        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
