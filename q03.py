import hashlib
import random
import time

# 3 - Implemente a construção de blocos de uma blockchain. Simule a evolução de uma blockchain de 10.000 blocos, onde cada bloco possui até 20 transações geradas aleatoriamente. Em seguida, tente fraudar alguma transação do bloco 35, mantendo toda a cadeia íntegra. Ao fim, responda as seguintes perguntas:
# 3.1 - Quanto tempo leva, em média, para a inserir um novo bloco na cadeia?
# 3.2 - Quanto tempo leva, em média, para tornar a blockchain válida após a alteração -indevida- do bloco 35?
# 3.3 - Quanto tempo leva, em média, para tornar a blockchain válida após a alteração -indevida- do N-ésimo bloco?
class Block:

    def __init__(self, data: str, previous_hash: bytes) -> None:
        self.data = data
        self.previous_hash = previous_hash
        self.next_block_challenge = random.getrandbits(160)
        self.challenge_result = 0
        self.hash = 0

    def __str__(self) -> str:
        return f"{self.data}-{self.previous_hash}-{self.next_block_challenge}-{self.challenge_result}"

    def is_valid(self):
        return hashlib.sha1(str(self).encode()) == self.hash

    def update_hash(self):
        self.hash = hashlib.sha1(str(self).encode())

class BlockChain:

    def __init__(self, data) -> None:
        self.chain = [Block(data, 0)]

    def get_block(self, i=0):
        return self.chain[i]

    def add_new_block(self, data: str):
        last_block = self.chain[-1]

        new_block = Block(data, last_block.hash)
        new_block.update_hash()
        new_block.challenge_result = solve_challenge(
            new_block.hash, last_block.next_block_challenge)
        new_block.update_hash()

        self.chain.append(new_block)

def method_extra_added_by_hacker(block_number, block_chain, new_data):
    block = block_chain.get_block(block_number)
    block.data = new_data
    block.update_hash()
    block.next_block_challenge = random.getrandbits(160)

    time_challenge = 0
    time_hash = 0
    previous_block = block
    for num in range(block_number + 1, len(block_chain.chain)):
        blck = block_chain.get_block(num)
        blck.previous_hash = previous_block.hash
        # Não acho que vai precisar atualizar o next_block_challenge,
        # pois só iria dar trabalho ao invasor, uma vez que pouco importa essa informação, no final
        # pois ela importa para adicionar o bloco, e os blocos já estão adicionados.
        # Mas como foi passado na aula:
        blck.next_block_challenge = random.getrandbits(160)

        begin_challenge = time.time()
        blck.challenge_result = solve_challenge(
            blck.hash, blck.next_block_challenge)
        time_challenge = time.time() - begin_challenge

        # Podia colocar dentro de um if para calcular só uma vez,
        # mas devido ao tempo deixei assim, e nem gasta muito tempo essa operação.
        begin_hash = time.time()
        blck.update_hash()
        time_hash = time.time() - begin_hash

        previous_block = blck

        # Não precisa atualizar a lista pois não tem ponteiros apontando nela!
    return (time_hash, time_challenge)

def solve_challenge(block_hash, challenge):
    # encontrar um x tal que hash(x + block_hash) < challenge

    x = 0
    block_hash2 = int(block_hash.hexdigest(), 16)

    while True:
        # print("x", x, end="\n")
        # print("hash\t\t", block_hash2)
        # print("challenge\t", challenge)
        new_hash = (x + block_hash2)
        new_hash = hashlib.sha1(new_hash.to_bytes(160, 'little'))
        new_hash2 = int(new_hash.hexdigest(), 16)
        # print("new hash\t", new_hash2)
        if (new_hash2 < challenge):
            # print("achou", x)
            return x
        x += 1


blockchain = BlockChain("genesis")

beginn = time.time()
for idx in range(1, 999):  # vai entender depois esse 999
    blockchain.add_new_block("transacao " + str(idx))

print("Blockchain criada com", len(blockchain.chain), "posições")

print("")
print("1) Tempo para adicionar o 1000º bloco (desafio + calculo do hash + processamento extra):")
begin = time.time()

blockchain.add_new_block("babau")

end = time.time() - begin

print(end * 1000, "milisegundos")

# 3.2 - Quanto tempo leva, em média, para tornar a blockchain válida após a alteração
# -indevida- do bloco 35?

begin = time.time()

time_hash, time_challenge = method_extra_added_by_hacker(  # vai entender depois esses times
    35, blockchain, "iuribidubidu")

end = time.time() - begin

print("")
print("2) Tempo para tornar a blockchain válida após a alteração indevida do bloco 35")
print(end * 1000, "milisegundos")

# 3.3 - Quanto tempo leva, em média, para tornar a blockchain válida após a alteração
# -indevida- do N-ésimo bloco?

print("")
print("3) Tempo para tornar a blockchain válida após a alteração indevida do n-ésimo bloco")
print("Tecnicamente bastaria fazer")
print("Tempo de recalcular hash (em média) + Tempo para desafio (em média) * 1000-N (tamanho da lista - o que falta)")
print("\nNo caso anterior, o tempo de recalcular hash foi", time_hash, "segundos")
print("O tempo de desafio foi", time_challenge, "segundos")
time_3 = (time_hash + time_challenge) * 965 * 1000
print("1000-35 é 965, então, tecnicamente, ficaria",
      time_3, "milisegundos")
time_4 = end * 1000 - time_3
print("Mas teve um tempo de processamento extra de",
      (time_4), "milisegundos...")
print("Uma média de",
      (time_4 / 965), "milisegundos por block...")
print("Então na fórmula acrescentaria o tempo extra de processamento:\n")

print("Resposta: Tempo de recalcular hash (em média) + Tempo para desafio (em média) + Tempo de processamento extra * 1000-N (tamanho da lista - o que falta)")

endd = time.time() - beginn
print(endd)
